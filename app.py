import hashlib
import io
import json
import mimetypes
import os
import re
import secrets
import subprocess
import tempfile
import time
import uuid
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    session,
    url_for,
)
from flask_compress import Compress
from PIL import Image, ImageOps
from werkzeug.security import check_password_hash, generate_password_hash

import metrics
from ai_scan import ScanError, analyze_screenshot, is_configured
from changelog import CHANGELOG
from translations import TR
from db import DATA_DIR, DB_PATH, get_db, init_db
from douban import DoubanFetchError, fetch_douban_info
from novel_export import build_novel_docx, build_novel_pdf
from trading import (
    build_cumulative_series,
    build_month_calendar,
    build_month_summary,
    build_pnl_chart,
    compute_daily_pnl,
    parse_schwab_csv,
    summarize_daily_pnl,
    summarize_trades,
)
import bank
from share_card import (
    build_changelog_share_card,
    build_chapter_share_card,
    build_day_share_card,
    build_expense_bar_share_card,
    build_novel_share_card,
    build_route_outline_card,
    build_route_share_card,
    build_share_card,
    build_showcase_card,
    build_trading_share_card,
)

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 300 * 1024 * 1024  # 300MB (raw video uploads get compressed down after)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 60 * 60 * 24 * 30  # 30 days for static files
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.permanent_session_lifetime = timedelta(days=30)
Compress(app)

init_db()  # runs on import too, so it also works under gunicorn (not just `python app.py`)

STATUSES = ["想看", "进行中", "已完成", "放弃"]
HEATMAP_WEEKS = 53
WEEKDAY_CN = ["一", "二", "三", "四", "五", "六", "日"]

MOMENT_TYPES = {
    "stock": {"label": "股票", "icon": "📈"},
    "exercise": {"label": "运动", "icon": "🏃"},
    "photo": {"label": "照片", "icon": "📷"},
    "thought": {"label": "想法", "icon": "💭"},
}

# Not user-creatable (kept out of MOMENT_TYPES so it never shows up in the
# "add moment" form or the AI screenshot classifier) — just a feed badge for
# changelog entries.
CHANGELOG_TYPE = {"label": "网站更新", "icon": "🛠️"}

# i18n for the changelog page only (per user request — rest of the site stays Chinese-only).
CHANGELOG_STRINGS = {
    "zh": {
        "page_title": "更新日志",
        "heading": "更新日志",
        "hint": "记录这个网站从零搭建到现在的开发过程（截图是重新生成的当前效果，不是每次改动当时的原图）。",
        "heatmap_summary": "过去一年 {days} 天有更新，共 {updates} 次迭代，累计约 {lines} 行代码",
        "lines_hint": "代码量：本次会话开始前的历史记录（标了「估算」）是回顾整理出来的大致数字；从这次开始的每一条都是改动时精确统计的。",
        "share_recent": "📤 最近 10 条更新分享图",
        "share_today": "📤 今天的更新分享图",
        "day_total": "共 {count} 次更新 · 当日约 {lines} 行代码",
        "today_tag": "今天",
        "date_label": "选择日期",
        "date_today_suffix": " · 今天",
        "search_placeholder": "搜索更新日志…",
        "search_results_label": "「{q}」共 {count} 条结果",
        "search_no_results": "没有匹配「{q}」的更新记录",
        "search_clear": "清除搜索",
        "lines_badge": "+{lines} 行",
        "estimated_suffix": "（估算）",
        "empty": "这段时间还没有更新记录",
        "count_label": "共 {count} 条更新",
        "recent_heading": "最近 10 条更新",
        "today_heading": "{month}月{day}日的更新",
        "watermark": "知行合一AI实验室 开发日志",
        "lang_label": "EN",
        "lang_code": "en",
        "months": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        "metrics_heading": "站点实时概况",
        "metrics_qps": "QPS（近1分钟）",
        "metrics_avg": "平均响应",
        "metrics_p95": "P95",
        "metrics_uptime": "运行时长",
        "metrics_hint": "只统计打到源站的请求，命中 CDN 边缘缓存的静态资源不计入；数据存在内存里，服务重启会清零。",
    },
    "en": {
        "page_title": "Changelog",
        "heading": "Changelog",
        "hint": (
            "A record of this site's development from scratch to now (screenshots are "
            "freshly regenerated to reflect the current UI, not the original at the time "
            "of each change)."
        ),
        "heatmap_summary": "{days} active days in the past year, {updates} updates, ~{lines} lines of code changed",
        "lines_hint": (
            'Code volume: entries from before this session (marked "estimated") are rough '
            "figures reconstructed in hindsight; every entry from this one onward is "
            "measured precisely at the time of the change."
        ),
        "share_recent": "📤 Share: last 10 updates",
        "share_today": "📤 Share: today's updates",
        "day_total": "{count} updates · ~{lines} lines that day",
        "today_tag": "Today",
        "date_label": "Pick a date",
        "date_today_suffix": " · Today",
        "search_placeholder": "Search the changelog…",
        "search_results_label": "{count} results for “{q}”",
        "search_no_results": "No updates match “{q}”",
        "search_clear": "Clear search",
        "lines_badge": "+{lines} lines",
        "estimated_suffix": " (estimated)",
        "empty": "No updates in this range yet",
        "count_label": "{count} updates",
        "recent_heading": "Last 10 Updates",
        "today_heading": "Updates on {month}/{day}",
        "watermark": "Unity of Knowledge and Action AI Lab — Dev Log",
        "lang_label": "中文",
        "lang_code": "zh",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "metrics_heading": "Live Site Stats",
        "metrics_qps": "QPS (last 1 min)",
        "metrics_avg": "Avg latency",
        "metrics_p95": "P95",
        "metrics_uptime": "Uptime",
        "metrics_hint": (
            "Only counts requests that reach the origin server; static assets served from the "
            "CDN edge cache aren't included. Kept in memory only — resets on each restart."
        ),
    },
}


def localize_entry(e, lang):
    if lang == "en":
        return {**e, "title": e.get("title_en") or e["title"], "summary": e.get("summary_en") or e["summary"]}
    return e

UPLOAD_DIR = DATA_DIR / "uploads"
ALLOWED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Novel character art + videos are public (viewable without login), unlike the
# rest of /data/uploads — kept in a separate directory with its own public
# serving route so login-gated photo uploads never become accidentally public.
NOVEL_MEDIA_DIR = DATA_DIR / "novel_media"
ALLOWED_VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".avi", ".mkv"}
MAX_VIDEO_SECONDS = 5 * 60


def get_current_user():
    if not hasattr(g, "user"):
        user_id = session.get("user_id")
        g.user = None
        if user_id:
            conn = get_db()
            g.user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            conn.close()
    return g.user


@app.context_processor
def inject_auth_state():
    return {"current_user": get_current_user()}


@app.before_request
def set_language():
    # Site-wide language preference, remembered across visits via the session
    # cookie. ?lang=en|zh on any page both applies immediately and sticks for
    # later navigation; without it, falls back to whatever was last chosen (or
    # zh for a first-time visitor). Separate from CHANGELOG_STRINGS's own
    # per-page ?lang= handling, which stays query-param-only on purpose (share
    # images are fixed artifacts, not something a "current preference" should
    # silently affect).
    requested = request.args.get("lang")
    if requested in ("zh", "en"):
        session["lang"] = requested
        session.permanent = True
    g.lang = session.get("lang", "zh")


def tr(text, **kwargs):
    """Look up `text` in the site-wide UI dictionary (translations.py) when the
    visitor's language is English; otherwise (or if untranslated) return it
    unchanged. Keyed by the original Chinese string itself, not an invented
    key name — see translations.py for why. Pass kwargs for strings with
    {placeholder} spots (e.g. counts) — applied to whichever string (Chinese
    or English) ends up selected, so both sides use the same {name} syntax."""
    if g.get("lang", "zh") == "en":
        text = TR.get(text, text)
    return text.format(**kwargs) if kwargs else text


app.jinja_env.globals["tr"] = tr


def fmt_money(v):
    if v is None:
        return "-"
    sign = "-" if v < 0 else "+" if v > 0 else ""
    return f"{sign}${abs(v):,.2f}"


app.jinja_env.filters["money"] = fmt_money


@app.context_processor
def inject_lang():
    lang = g.get("lang", "zh")
    # Preserve whatever query params the current page already has (date
    # filters, search terms, pagination…) and just flip `lang`, so the one
    # nav-level toggle works correctly everywhere instead of dropping state.
    args = request.args.to_dict(flat=True)
    args["lang"] = "zh" if lang == "en" else "en"
    try:
        toggle_url = url_for(request.endpoint, **(request.view_args or {}), **args)
    except Exception:
        toggle_url = request.path + "?lang=" + args["lang"]
    return {"current_lang": lang, "lang_toggle_url": toggle_url}


@app.context_processor
def inject_asset_version():
    css_path = Path(__file__).parent / "static" / "style.css"
    try:
        version = int(css_path.stat().st_mtime)
    except OSError:
        version = 0
    return {"asset_version": version}


PUBLIC_ENDPOINTS = {
    "login", "register", "reset_password", "static", "changelog", "changelog_more",
    "changelog_share_image", "index", "serve_novel_media", "novels_list", "novel_detail",
    "novel_chapter_read", "novel_share_image", "cover_proxy", "route_detail", "route_share_image",
}

# Polling endpoint for the metrics page itself — excluded so it doesn't skew its own stats.
METRICS_EXCLUDED_ENDPOINTS = {"admin_metrics_data"}


@app.before_request
def start_timer():
    g.request_start = time.time()


@app.after_request
def record_metrics(response):
    start = getattr(g, "request_start", None)
    if start is not None and request.endpoint not in METRICS_EXCLUDED_ENDPOINTS:
        duration_ms = (time.time() - start) * 1000
        metrics.record(request.endpoint, response.status_code, duration_ms)
    return response


@app.after_request
def make_inline_media_cacheable(response):
    # send_file adds Content-Disposition and Accept-Ranges to image/video responses,
    # and Railway's edge CDN then refuses to cache them (x-cache: DYNAMIC) — so every
    # cover/photo round-tripped all the way to the Singapore origin instead of being
    # served from a nearby edge node. Strip those headers for *inline* media so the
    # edge caches them. Attachment downloads (share-card PNGs) keep their disposition,
    # and videos keep Accept-Ranges so seeking still works.
    cd = response.headers.get("Content-Disposition", "")
    top_type = (response.mimetype or "").split("/")[0]
    if cd.startswith("inline") and top_type in ("image", "video"):
        del response.headers["Content-Disposition"]
        if top_type == "image":
            response.headers.pop("Accept-Ranges", None)
    return response


@app.before_request
def require_login():
    get_current_user()  # populate g.user for every request before any view function runs
    if request.endpoint in PUBLIC_ENDPOINTS or request.endpoint is None:
        return None
    if not session.get("user_id"):
        return redirect(url_for("login", next=request.path))
    return None


def registration_open():
    conn = get_db()
    row = conn.execute("SELECT allow_registration FROM app_settings WHERE id = 1").fetchone()
    conn.close()
    return bool(row and row["allow_registration"])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password_hash"], password):
            lang = session.get("lang")
            session.clear()
            session["user_id"] = user["id"]
            if lang:
                session["lang"] = lang
            session.permanent = True
            return redirect(safe_next(request.form.get("next"), url_for("index")))
        return render_template(
            "login.html", error="用户名或密码不对，再试一次",
            next=request.form.get("next", ""), registration_open=registration_open(),
        )
    return render_template(
        "login.html", error=None, next=request.args.get("next", ""), registration_open=registration_open()
    )


@app.route("/logout", methods=["POST"])
def logout():
    lang = session.get("lang")
    session.clear()
    if lang:
        session["lang"] = lang
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if not registration_open():
        return "未找到该页面", 404

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        error = None
        if not username or not password:
            error = "用户名和密码都要填"
        elif len(password) < 6:
            error = "密码至少要 6 位"
        else:
            conn = get_db()
            existing = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
            if existing:
                conn.close()
                error = "这个用户名已经有人用了"
            else:
                conn.execute(
                    "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 0)",
                    (username, generate_password_hash(password, method="pbkdf2:sha256")),
                )
                conn.commit()
                user_id = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()["id"]
                conn.close()
                lang = session.get("lang")
                session.clear()
                session["user_id"] = user_id
                if lang:
                    session["lang"] = lang
                session.permanent = True
                return redirect(url_for("index"))
        return render_template("register.html", error=error)

    return render_template("register.html", error=None)


def is_admin():
    return bool(g.user and g.user["is_admin"])


@app.route("/admin/users")
def admin_users():
    if not is_admin():
        return "未找到该页面", 404
    conn = get_db()
    users = conn.execute("SELECT id, username, is_admin, created_at FROM users ORDER BY id ASC").fetchall()
    settings = conn.execute("SELECT allow_registration FROM app_settings WHERE id = 1").fetchone()
    conn.close()
    return render_template(
        "admin_users.html",
        users=users,
        allow_registration=bool(settings["allow_registration"]) if settings else False,
        error=request.args.get("error"),
        info=request.args.get("info"),
        reset_link=request.args.get("reset_link"),
        reset_username=request.args.get("reset_username"),
    )


@app.route("/admin/users/new", methods=["POST"])
def admin_users_new():
    if not is_admin():
        return "未找到该页面", 404
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    new_is_admin = 1 if request.form.get("is_admin") else 0

    if not username or not password:
        return redirect(url_for("admin_users", error="用户名和密码都要填"))

    conn = get_db()
    existing = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
    if existing:
        conn.close()
        return redirect(url_for("admin_users", error="这个用户名已经有人用了"))

    conn.execute(
        "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
        (username, generate_password_hash(password, method="pbkdf2:sha256"), new_is_admin),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("admin_users"))


@app.route("/admin/users/toggle-registration", methods=["POST"])
def admin_toggle_registration():
    if not is_admin():
        return "未找到该页面", 404
    conn = get_db()
    row = conn.execute("SELECT allow_registration FROM app_settings WHERE id = 1").fetchone()
    new_value = 0 if (row and row["allow_registration"]) else 1
    conn.execute(
        "INSERT INTO app_settings (id, allow_registration) VALUES (1, ?) "
        "ON CONFLICT(id) DO UPDATE SET allow_registration = ?",
        (new_value, new_value),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("admin_users"))


@app.route("/admin/users/<int:user_id>/reset-password", methods=["POST"])
def admin_reset_password(user_id):
    if not is_admin():
        return "未找到该页面", 404
    new_password = request.form.get("password", "")
    if len(new_password) < 6:
        return redirect(url_for("admin_users", error="密码至少要 6 位"))

    conn = get_db()
    user = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        conn.close()
        return redirect(url_for("admin_users", error="账号不存在"))

    conn.execute(
        "UPDATE users SET password_hash = ? WHERE id = ?",
        (generate_password_hash(new_password, method="pbkdf2:sha256"), user_id),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("admin_users", info=tr("{u} 的密码已经重置", u=user["username"])))


@app.route("/admin/users/<int:user_id>/reset-link", methods=["POST"])
def admin_generate_reset_link(user_id):
    if not is_admin():
        return "未找到该页面", 404

    conn = get_db()
    user = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        conn.close()
        return redirect(url_for("admin_users", error="账号不存在"))

    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO password_resets (user_id, token, expires_at) VALUES (?, ?, ?)",
        (user_id, token, expires_at),
    )
    conn.commit()
    conn.close()
    link = url_for("reset_password", token=token, _external=True)
    return redirect(url_for("admin_users", reset_link=link, reset_username=user["username"]))


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    conn = get_db()
    reset = conn.execute(
        "SELECT * FROM password_resets WHERE token = ? AND used = 0 "
        "AND expires_at >= datetime('now', 'localtime')",
        (token,),
    ).fetchone()

    if not reset:
        conn.close()
        return render_template("reset_password.html", valid=False, error=None, done=False)

    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if len(password) < 6:
            error = "密码至少要 6 位"
        else:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (generate_password_hash(password, method="pbkdf2:sha256"), reset["user_id"]),
            )
            conn.execute("UPDATE password_resets SET used = 1 WHERE id = ?", (reset["id"],))
            conn.commit()
            conn.close()
            return render_template("reset_password.html", valid=True, error=None, done=True)

    conn.close()
    return render_template("reset_password.html", valid=True, error=error, done=False)


COVER_CACHE_DIR = DATA_DIR / "cover_cache"


@app.route("/admin/backup.zip")
def admin_backup():
    # A raw, byte-for-byte copy of the real data: the sqlite file plus every
    # uploaded/generated file (moment photos, novel covers/character art/
    # videos, cover cache). Deliberately not scoped to one account or curated
    # into a JSON shape: this is the "grab a real snapshot right now" button,
    # not the polished per-account export/import from the plan above.
    #
    # Explicitly allow-listed rather than DATA_DIR.rglob("*") — in local dev
    # DATA_DIR falls back to the whole project directory (source code, venv,
    # .git and all), and only in production does Dockerfile pin it to a clean
    # /data volume. Listing the known data paths keeps this correct either way.
    if not is_admin():
        return "未找到该页面", 404

    data_paths = [DB_PATH, UPLOAD_DIR, NOVEL_MEDIA_DIR, COVER_CACHE_DIR]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for base in data_paths:
            if base.is_file():
                zf.write(base, base.relative_to(DATA_DIR))
            elif base.is_dir():
                for path in base.rglob("*"):
                    if path.is_file():
                        zf.write(path, path.relative_to(DATA_DIR))
    buf.seek(0)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return send_file(
        buf,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"knowing-doing-backup-{stamp}.zip",
    )


@app.route("/data/<path:filename>")
def serve_data(filename):
    return send_from_directory(DATA_DIR, filename)


@app.route("/novel-media/<path:filename>")
def serve_novel_media(filename):
    return send_from_directory(NOVEL_MEDIA_DIR, filename)


@app.route("/cover-proxy")
def cover_proxy():
    url = request.args.get("url", "")
    if not url or "doubanio.com" not in url:
        return "", 404

    cache_key = hashlib.sha256(url.encode()).hexdigest()
    COVER_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = next(COVER_CACHE_DIR.glob(f"{cache_key}.*"), None)
    if cached:
        return send_file(cached, mimetype=mimetypes.guess_type(cached.name)[0] or "image/jpeg", max_age=86400)

    try:
        resp = requests.get(
            url,
            timeout=6,
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.douban.com/"},
        )
        resp.raise_for_status()
    except requests.RequestException:
        return "", 502

    content_type = resp.headers.get("Content-Type", "image/jpeg")
    ext = mimetypes.guess_extension(content_type) or ".jpg"
    cache_path = COVER_CACHE_DIR / f"{cache_key}{ext}"
    cache_path.write_bytes(resp.content)

    return send_file(cache_path, mimetype=content_type, max_age=86400)


def cover_src(url):
    if url and "doubanio.com" in url:
        return url_for("cover_proxy", url=url)
    return url


app.jinja_env.globals["cover_src"] = cover_src


@app.route("/admin/migrate", methods=["POST"])
def admin_migrate():
    # One-time data-migration helper. Only active when ENABLE_MIGRATION is set
    # on the deployment, and (like every other route) still requires being
    # logged in whenever APP_PASSWORD is configured. Meant to be turned off
    # again (unset ENABLE_MIGRATION) right after use.
    if not os.environ.get("ENABLE_MIGRATION"):
        return "migration disabled", 404

    result = {}
    db_file = request.files.get("db_file")
    if db_file:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        db_file.save(DATA_DIR / "tracker.db")
        result["db"] = "restored"

    uploads_zip = request.files.get("uploads_zip")
    if uploads_zip:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(uploads_zip) as zf:
            zf.extractall(UPLOAD_DIR)
        result["uploads"] = "restored"

    return jsonify(result)


@app.route("/admin/metrics")
def admin_metrics_page():
    return render_template("admin_metrics.html")


@app.route("/admin/metrics/data")
def admin_metrics_data():
    return jsonify({"last_60s": metrics.get_stats(60), "last_5m": metrics.get_stats(300)})


UPLOAD_MAX_DIMENSION = 1600
UPLOAD_JPEG_QUALITY = 85


def save_image_to(file_storage, target_dir):
    """Resize/re-encode an uploaded image into target_dir; returns the bare filename or ''."""
    if not file_storage or not file_storage.filename:
        return ""
    ext = Path(file_storage.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXT:
        return ""
    target_dir.mkdir(parents=True, exist_ok=True)

    if ext == ".gif":
        filename = f"{uuid.uuid4().hex}{ext}"
        file_storage.save(target_dir / filename)
        return filename

    try:
        img = Image.open(file_storage.stream)
        img = ImageOps.exif_transpose(img)
        img.thumbnail((UPLOAD_MAX_DIMENSION, UPLOAD_MAX_DIMENSION), Image.LANCZOS)

        has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
        if has_alpha:
            filename = f"{uuid.uuid4().hex}.png"
            img.save(target_dir / filename, format="PNG", optimize=True)
        else:
            filename = f"{uuid.uuid4().hex}.jpg"
            img.convert("RGB").save(
                target_dir / filename, format="JPEG", quality=UPLOAD_JPEG_QUALITY, optimize=True
            )
        return filename
    except Exception:
        filename = f"{uuid.uuid4().hex}{ext}"
        file_storage.save(target_dir / filename)
        return filename


def save_upload(file_storage):
    filename = save_image_to(file_storage, UPLOAD_DIR)
    return f"uploads/{filename}" if filename else ""


def save_novel_image(file_storage):
    return save_image_to(file_storage, NOVEL_MEDIA_DIR)


def probe_video_duration(path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, timeout=30,
        )
        return float(result.stdout.strip())
    except (subprocess.SubprocessError, ValueError, OSError):
        return None


def compress_video(src_path, dest_path):
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(src_path),
                "-vf", "scale='min(1280,iw)':-2",
                "-vcodec", "libx264", "-preset", "veryfast", "-crf", "27",
                "-acodec", "aac", "-b:a", "128k",
                "-movflags", "+faststart",
                str(dest_path),
            ],
            capture_output=True, timeout=280,
        )
    except (subprocess.SubprocessError, OSError):
        pass
    return dest_path.exists()


def make_video_thumbnail(video_path, thumb_path):
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(video_path), "-ss", "00:00:01", "-vframes", "1",
                "-vf", "scale=480:-2", str(thumb_path),
            ],
            capture_output=True, timeout=30,
        )
    except (subprocess.SubprocessError, OSError):
        pass
    return thumb_path.exists()


def parse_video_embed(url):
    if not url:
        return None
    m = re.search(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/))([\w-]{11})", url)
    if m:
        return {"provider": "youtube", "embed_url": f"https://www.youtube-nocookie.com/embed/{m.group(1)}"}
    m = re.search(r"bilibili\.com/video/(BV\w+)", url)
    if m:
        return {"provider": "bilibili", "embed_url": f"https://player.bilibili.com/player.html?bvid={m.group(1)}&autoplay=0"}
    return None


app.jinja_env.globals["parse_video_embed"] = parse_video_embed


def to_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def to_float(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def group_chapters_by_volume(chapters):
    """Buckets chapters (already ordered by chapter_no) into runs that share the
    same volume_id, so consecutive same-volume chapters render under one
    heading. Chapters with no volume_id form their own (headerless) groups."""
    groups = []
    for c in chapters:
        vid = c["volume_id"]
        if not groups or groups[-1]["volume_id"] != vid:
            groups.append({
                "volume_id": vid,
                "volume_no": c["volume_no"] if vid else None,
                "volume_title": c["volume_title"] if vid else None,
                "chapters": [],
            })
        groups[-1]["chapters"].append(c)
    return groups


def to_int_list(values):
    result = []
    for v in values:
        n = to_int(v)
        if n is not None:
            result.append(n)
    return result


def heat_level(minutes, has_entries):
    if not has_entries:
        return 0
    if not minutes:
        return 1
    if minutes < 30:
        return 1
    if minutes < 60:
        return 2
    if minutes < 120:
        return 3
    return 4


def build_heatmap(conn, user_id, weeks=HEATMAP_WEEKS):
    today = date.today()
    dow_sunday_first = (today.weekday() + 1) % 7  # Monday=1 ... Sunday=0
    grid_end = today + timedelta(days=6 - dow_sunday_first)  # this week's Saturday
    grid_start = grid_end - timedelta(days=weeks * 7 - 1)  # a Sunday

    rows = conn.execute(
        "SELECT log_date, SUM(minutes_spent) AS minutes FROM ("
        "  SELECT log_date, minutes_spent FROM logs WHERE log_date >= ? AND log_date <= ? AND user_id = ?"
        "  UNION ALL"
        "  SELECT log_date, minutes_spent FROM moments WHERE log_date >= ? AND log_date <= ? AND user_id = ?"
        ") GROUP BY log_date",
        (
            grid_start.isoformat(),
            today.isoformat(),
            user_id,
            grid_start.isoformat(),
            today.isoformat(),
            user_id,
        ),
    ).fetchall()
    minutes_by_date = {r["log_date"]: r["minutes"] for r in rows}

    weeks_data = []
    cursor = grid_start
    last_month = None
    for _ in range(weeks):
        days = []
        for d in range(7):
            day = cursor + timedelta(days=d)
            iso = day.isoformat()
            future = day > today
            has_entries = iso in minutes_by_date
            minutes = None if future else minutes_by_date.get(iso, 0)
            days.append(
                {
                    "date": iso,
                    "minutes": minutes,
                    "level": -1 if future else heat_level(minutes, has_entries),
                }
            )
        month_num = cursor.month
        month_label = ""
        if month_num != last_month:
            month_label = f"{month_num}月"
            last_month = month_num
        weeks_data.append({"month_label": month_label, "days": days})
        cursor += timedelta(days=7)

    total_days = len(minutes_by_date)
    total_minutes = sum(minutes_by_date.values())
    return {"weeks": weeks_data, "total_days": total_days, "total_minutes": total_minutes}


def code_heat_level(lines, has_entries):
    if not has_entries:
        return 0
    if not lines:
        return 1
    if lines < 100:
        return 1
    if lines < 300:
        return 2
    if lines < 600:
        return 3
    return 4


def build_changelog_heatmap(weeks=HEATMAP_WEEKS, lang="zh"):
    today = date.today()
    dow_sunday_first = (today.weekday() + 1) % 7
    grid_end = today + timedelta(days=6 - dow_sunday_first)
    grid_start = grid_end - timedelta(days=weeks * 7 - 1)

    lines_by_date = {}
    count_by_date = {}
    for c in CHANGELOG:
        d = c["date"]
        if grid_start.isoformat() <= d <= today.isoformat():
            lines_by_date[d] = lines_by_date.get(d, 0) + (c.get("lines_changed") or 0)
            count_by_date[d] = count_by_date.get(d, 0) + 1

    weeks_data = []
    cursor = grid_start
    last_month = None
    for _ in range(weeks):
        days = []
        for d in range(7):
            day = cursor + timedelta(days=d)
            iso = day.isoformat()
            future = day > today
            has_entries = iso in lines_by_date
            lines = None if future else lines_by_date.get(iso, 0)
            days.append(
                {
                    "date": iso,
                    "lines": lines,
                    "count": count_by_date.get(iso, 0),
                    "level": -1 if future else code_heat_level(lines, has_entries),
                }
            )
        month_num = cursor.month
        month_label = ""
        if month_num != last_month:
            month_label = CHANGELOG_STRINGS[lang]["months"][month_num - 1]
            last_month = month_num
        weeks_data.append({"month_label": month_label, "days": days})
        cursor += timedelta(days=7)

    return {
        "weeks": weeks_data,
        "total_days": len(lines_by_date),
        "total_lines": sum(lines_by_date.values()),
        "total_updates": len(CHANGELOG),
    }


def group_changelog_by_day(entries, lang="zh", offset=0, limit=None):
    by_date = {}
    for e in entries:
        by_date.setdefault(e["date"], []).append(e)
    all_dates = sorted(by_date.keys(), reverse=True)
    selected_dates = all_dates[offset : offset + limit] if limit is not None else all_dates[offset:]
    has_more = limit is not None and len(all_dates) > offset + limit

    days = []
    for d in selected_dates:
        day_entries = [localize_entry(e, lang) for e in reversed(by_date[d])]
        days.append(
            {
                "date": d,
                "entries": day_entries,
                "count": len(day_entries),
                "total_lines": sum(e.get("lines_changed") or 0 for e in day_entries),
            }
        )
    return days, has_more


def safe_next(next_url, fallback):
    if next_url and next_url.startswith("/") and not next_url.startswith("//"):
        return next_url
    return fallback


FEED_PAGE_SIZE = 20
LOG_PAGE_SIZE = 20
CHANGELOG_PAGE_DAYS = 5
SEARCH_PAGE_SIZE = 20


def build_feed(conn, user_id, type_filter, status_filter, offset=0, limit=FEED_PAGE_SIZE):
    show_items = type_filter == "" or type_filter in ("book", "show")
    show_moments = type_filter == "" or type_filter in MOMENT_TYPES
    show_changelog = type_filter == "" or type_filter == "update"

    entries = []

    if show_items:
        log_query = (
            "SELECT logs.id AS log_id, logs.log_date AS date, logs.minutes_spent, "
            "logs.progress_at, logs.comment, "
            "items.id AS item_id, items.title, items.creator, items.cover_url, "
            "items.type AS item_type, items.status, items.total_units, items.unit_label "
            "FROM logs JOIN items ON logs.item_id = items.id WHERE items.user_id = ?"
        )
        params = [user_id]
        if type_filter in ("book", "show"):
            log_query += " AND items.type = ?"
            params.append(type_filter)
        if status_filter in STATUSES:
            log_query += " AND items.status = ?"
            params.append(status_filter)
        for row in conn.execute(log_query, params).fetchall():
            entry = dict(row)
            entry["kind"] = "log"
            entries.append(entry)

        untouched_query = (
            "SELECT items.* FROM items "
            "WHERE items.user_id = ? AND NOT EXISTS (SELECT 1 FROM logs WHERE logs.item_id = items.id)"
        )
        params2 = [user_id]
        if type_filter in ("book", "show"):
            untouched_query += " AND items.type = ?"
            params2.append(type_filter)
        if status_filter in STATUSES:
            untouched_query += " AND items.status = ?"
            params2.append(status_filter)
        for row in conn.execute(untouched_query, params2).fetchall():
            entry = dict(row)
            entry["kind"] = "item_new"
            entry["date"] = entry["created_at"][:10]
            entries.append(entry)

    if show_moments:
        moment_query = "SELECT * FROM moments WHERE user_id = ?"
        params3 = [user_id]
        if type_filter in MOMENT_TYPES:
            moment_query += " AND type = ?"
            params3.append(type_filter)
        for row in conn.execute(moment_query, params3).fetchall():
            entry = dict(row)
            entry["kind"] = "moment"
            entry["date"] = entry["log_date"]
            entries.append(entry)

    if show_changelog:
        lang = g.get("lang", "zh")
        for i, c in enumerate(CHANGELOG):
            c = localize_entry(c, lang)
            entries.append(
                {
                    "kind": "changelog",
                    "date": c["date"],
                    "title": c["title"],
                    "summary": c["summary"],
                    "image": c.get("image"),
                    "_seq": i,
                }
            )

    entries.sort(
        key=lambda e: (
            e["date"],
            0 if e["kind"] == "changelog" else 1,  # non-changelog entries first within a day
            e.get("log_id") or e.get("id") or e.get("_seq") or 0,
        ),
        reverse=True,
    )
    page = entries[offset : offset + limit]
    has_more = len(entries) > offset + limit
    return page, has_more


@app.route("/changelog")
def changelog():
    lang = g.lang
    t = CHANGELOG_STRINGS[lang]
    # Show one day at a time, chosen via the date picker; default to today, or the
    # most recent update day when today has no entries yet. A search query takes
    # over and shows matches across all days instead.
    all_dates = sorted({c["date"] for c in CHANGELOG}, reverse=True)
    today_str = date.today().isoformat()
    default_date = today_str if today_str in all_dates else (all_dates[0] if all_dates else today_str)
    selected_date = request.args.get("date") or default_date
    if all_dates and selected_date not in all_dates:
        selected_date = default_date

    q = request.args.get("q", "").strip()
    if q:
        needle = q.lower()
        matches = [
            c for c in CHANGELOG
            if needle in c["title"].lower()
            or needle in c.get("title_en", "").lower()
            or needle in c["summary"].lower()
            or needle in c.get("summary_en", "").lower()
        ]
        days, _ = group_changelog_by_day(matches, lang=lang)
        search_count = len(matches)
    else:
        day_entries = [c for c in CHANGELOG if c["date"] == selected_date]
        days, _ = group_changelog_by_day(day_entries, lang=lang)
        search_count = 0

    metrics_summary = metrics.get_stats(60)
    return render_template(
        "changelog.html",
        days=days,
        days_has_more=False,
        heatmap=build_changelog_heatmap(lang=lang),
        today=today_str,
        lang=lang,
        t=t,
        all_dates=all_dates,
        selected_date=selected_date,
        q=q,
        search_count=search_count,
        metrics_summary=metrics_summary,
        uptime_human=metrics.format_uptime(metrics_summary["uptime_seconds"]),
        share_ver=int(time.time()),
    )


@app.route("/changelog/more")
def changelog_more():
    lang = g.lang
    offset = to_int(request.args.get("offset"), 0) or 0

    days, has_more = group_changelog_by_day(CHANGELOG, lang=lang, offset=offset, limit=CHANGELOG_PAGE_DAYS)
    html = render_template("_changelog_days.html", days=days, t=CHANGELOG_STRINGS[lang], today=date.today().isoformat())
    return jsonify({"html": html, "has_more": has_more, "count": len(days)})


@app.route("/changelog/share.png")
def changelog_share_image():
    lang = request.args.get("lang", "zh")
    if lang not in CHANGELOG_STRINGS:
        lang = "zh"
    t = CHANGELOG_STRINGS[lang]

    range_ = request.args.get("range", "recent")
    ordered = sorted(enumerate(CHANGELOG), key=lambda pair: (pair[1]["date"], pair[0]), reverse=True)
    ordered = [localize_entry(c, lang) for _, c in ordered]

    if range_ == "today":
        today = date.today()
        today_str = today.isoformat()
        entries = [c for c in ordered if c["date"] == today_str]
        heading = t["today_heading"].format(month=today.month, day=today.day)
    else:
        range_ = "recent"
        entries = ordered[:10]
        heading = t["recent_heading"]

    buf = build_changelog_share_card(entries, heading, heatmap=build_changelog_heatmap(lang=lang), t=t)

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"changelog-{range_}-{lang}.png" if download else None,
        max_age=0,
    )


@app.route("/")
def index():
    if not session.get("user_id"):
        return public_landing()

    type_filter = request.args.get("type", "")
    status_filter = request.args.get("status", "")

    conn = get_db()
    feed, has_more = build_feed(conn, g.user["id"], type_filter, status_filter)
    heatmap = build_heatmap(conn, g.user["id"])
    conn.close()

    return render_template(
        "index.html",
        feed=feed,
        has_more=has_more,
        statuses=STATUSES,
        type_filter=type_filter,
        status_filter=status_filter,
        heatmap=heatmap,
        moment_types=MOMENT_TYPES,
        changelog_type=CHANGELOG_TYPE,
        today=date.today().isoformat(),
    )


def public_landing():
    lang = g.lang
    t = CHANGELOG_STRINGS[lang]

    # Public homepage shows only today's changelog entries. On days with no update
    # yet, fall back to the single most recent day so the page never looks empty.
    today_str = date.today().isoformat()
    today_entries = [c for c in CHANGELOG if c["date"] == today_str]
    if today_entries:
        days, _ = group_changelog_by_day(today_entries, lang=lang)
    else:
        days, _ = group_changelog_by_day(CHANGELOG, lang=lang, limit=1)

    return render_template(
        "public_home.html",
        days=days,
        days_has_more=False,
        heatmap=build_changelog_heatmap(lang=lang),
        today=today_str,
        lang=lang,
        t=t,
        features=SHOWCASE_FEATURES,
    )


@app.route("/feed/more")
def feed_more():
    type_filter = request.args.get("type", "")
    status_filter = request.args.get("status", "")
    offset = to_int(request.args.get("offset"), 0) or 0

    conn = get_db()
    feed, has_more = build_feed(conn, g.user["id"], type_filter, status_filter, offset=offset)
    conn.close()

    html = render_template(
        "_feed_items.html",
        feed=feed,
        moment_types=MOMENT_TYPES,
        changelog_type=CHANGELOG_TYPE,
    )
    return jsonify({"html": html, "has_more": has_more, "count": len(feed)})


def run_search(conn, user_id, q):
    like = f"%{q}%"
    results = []

    for row in conn.execute(
        "SELECT * FROM items WHERE user_id = ? AND (title LIKE ? OR creator LIKE ? OR review LIKE ?) "
        "ORDER BY created_at DESC",
        (user_id, like, like, like),
    ).fetchall():
        entry = dict(row)
        entry["kind"] = "item_match"
        entry["date"] = entry["created_at"][:10]
        results.append(entry)

    for row in conn.execute(
        "SELECT logs.*, items.title AS item_title, items.type AS item_type, "
        "items.cover_url AS item_cover_url, items.unit_label AS item_unit_label "
        "FROM logs JOIN items ON logs.item_id = items.id "
        "WHERE logs.user_id = ? AND logs.comment LIKE ? ORDER BY logs.log_date DESC",
        (user_id, like),
    ).fetchall():
        entry = dict(row)
        entry["kind"] = "log"
        entry["date"] = entry["log_date"]
        results.append(entry)

    for row in conn.execute(
        "SELECT * FROM moments WHERE user_id = ? AND (title LIKE ? OR content LIKE ?) ORDER BY log_date DESC",
        (user_id, like, like),
    ).fetchall():
        entry = dict(row)
        entry["kind"] = "moment"
        entry["date"] = entry["log_date"]
        results.append(entry)

    results.sort(key=lambda e: (e["date"], e.get("log_id") or e.get("id") or 0), reverse=True)
    return results


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    feed, has_more = [], False
    if q:
        conn = get_db()
        all_results = run_search(conn, g.user["id"], q)
        conn.close()
        feed = all_results[:SEARCH_PAGE_SIZE]
        has_more = len(all_results) > SEARCH_PAGE_SIZE

    return render_template(
        "search.html",
        query=q,
        feed=feed,
        has_more=has_more,
        moment_types=MOMENT_TYPES,
        changelog_type=CHANGELOG_TYPE,
    )


@app.route("/search/more")
def search_more():
    q = request.args.get("q", "").strip()
    offset = to_int(request.args.get("offset"), 0) or 0
    if not q:
        return jsonify({"html": "", "has_more": False, "count": 0})

    conn = get_db()
    all_results = run_search(conn, g.user["id"], q)
    conn.close()

    page = all_results[offset : offset + SEARCH_PAGE_SIZE]
    has_more = len(all_results) > offset + SEARCH_PAGE_SIZE
    html = render_template(
        "_feed_items.html", feed=page, moment_types=MOMENT_TYPES, changelog_type=CHANGELOG_TYPE
    )
    return jsonify({"html": html, "has_more": has_more, "count": len(page)})


@app.route("/add")
def add_new():
    default_type = request.args.get("type", "book")
    return render_template(
        "add_form.html", default_type=default_type, statuses=STATUSES, moment_types=MOMENT_TYPES,
        default_date=date.today().isoformat(),
    )


@app.route("/item/new", methods=["GET", "POST"])
def item_new():
    if request.method == "POST":
        conn = get_db()
        conn.execute(
            "INSERT INTO items (type, title, creator, cover_url, total_units, unit_label, status, rating, "
            "review, douban_url, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                request.form["type"],
                request.form["title"].strip(),
                request.form.get("creator", "").strip(),
                request.form.get("cover_url", "").strip(),
                to_int(request.form.get("total_units")),
                request.form.get("unit_label") or ("页" if request.form["type"] == "book" else "集"),
                request.form.get("status", "想看"),
                to_int(request.form.get("rating")),
                request.form.get("review", "").strip(),
                request.form.get("douban_url", "").strip(),
                g.user["id"],
            ),
        )
        conn.commit()
        item_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        conn.close()
        return redirect(url_for("item_detail", item_id=item_id))

    default_type = request.args.get("type", "book")
    return render_template("item_form.html", item=None, default_type=default_type, statuses=STATUSES)


@app.route("/item/<int:item_id>")
def item_detail(item_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM items WHERE id = ? AND user_id = ?", (item_id, g.user["id"])).fetchone()
    if item is None:
        conn.close()
        return "未找到该条目", 404

    logs = conn.execute(
        "SELECT * FROM logs WHERE item_id = ? ORDER BY log_date DESC, id DESC LIMIT ?",
        (item_id, LOG_PAGE_SIZE + 1),
    ).fetchall()
    logs_has_more = len(logs) > LOG_PAGE_SIZE
    logs = logs[:LOG_PAGE_SIZE]

    totals = conn.execute(
        "SELECT MAX(progress_at) AS current, COALESCE(SUM(minutes_spent), 0) AS total_minutes, COUNT(*) AS log_count "
        "FROM logs WHERE item_id = ?",
        (item_id,),
    ).fetchone()
    conn.close()

    current = totals["current"] or 0
    total_units = item["total_units"] or 0
    pct = min(100, round(current / total_units * 100)) if total_units else 0

    return render_template(
        "item_detail.html",
        item=item,
        logs=logs,
        logs_has_more=logs_has_more,
        current_progress=current,
        total_minutes=totals["total_minutes"],
        log_count=totals["log_count"],
        pct=pct,
        today=date.today().isoformat(),
        statuses=STATUSES,
    )


@app.route("/item/<int:item_id>/logs/more")
def item_logs_more(item_id):
    offset = to_int(request.args.get("offset"), 0) or 0
    conn = get_db()
    item = conn.execute("SELECT * FROM items WHERE id = ? AND user_id = ?", (item_id, g.user["id"])).fetchone()
    if item is None:
        conn.close()
        return jsonify({"html": "", "has_more": False, "count": 0})

    logs = conn.execute(
        "SELECT * FROM logs WHERE item_id = ? ORDER BY log_date DESC, id DESC LIMIT ? OFFSET ?",
        (item_id, LOG_PAGE_SIZE + 1, offset),
    ).fetchall()
    conn.close()

    has_more = len(logs) > LOG_PAGE_SIZE
    logs = logs[:LOG_PAGE_SIZE]

    html = render_template("_log_items.html", logs=logs, item=item)
    return jsonify({"html": html, "has_more": has_more, "count": len(logs)})


@app.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
def item_edit(item_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM items WHERE id = ? AND user_id = ?", (item_id, g.user["id"])).fetchone()
    if item is None:
        conn.close()
        return "未找到该条目", 404

    if request.method == "POST":
        conn.execute(
            "UPDATE items SET type=?, title=?, creator=?, cover_url=?, total_units=?, unit_label=?, "
            "status=?, rating=?, review=?, douban_url=? WHERE id=? AND user_id=?",
            (
                request.form["type"],
                request.form["title"].strip(),
                request.form.get("creator", "").strip(),
                request.form.get("cover_url", "").strip(),
                to_int(request.form.get("total_units")),
                request.form.get("unit_label") or "页",
                request.form.get("status", "想看"),
                to_int(request.form.get("rating")),
                request.form.get("review", "").strip(),
                request.form.get("douban_url", "").strip(),
                item_id,
                g.user["id"],
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("item_detail", item_id=item_id))

    conn.close()
    return render_template("item_form.html", item=item, default_type=item["type"], statuses=STATUSES)


@app.route("/item/<int:item_id>/status", methods=["POST"])
def item_status(item_id):
    status = request.form.get("status")
    if status in STATUSES:
        conn = get_db()
        conn.execute("UPDATE items SET status=? WHERE id=? AND user_id=?", (status, item_id, g.user["id"]))
        conn.commit()
        conn.close()
    return redirect(safe_next(request.form.get("next"), url_for("index")))


@app.route("/item/<int:item_id>/delete", methods=["POST"])
def item_delete(item_id):
    conn = get_db()
    conn.execute("DELETE FROM items WHERE id = ? AND user_id = ?", (item_id, g.user["id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/item/<int:item_id>/log", methods=["POST"])
def log_add(item_id):
    conn = get_db()
    item = conn.execute("SELECT id FROM items WHERE id = ? AND user_id = ?", (item_id, g.user["id"])).fetchone()
    if item is None:
        conn.close()
        return "未找到该条目", 404
    conn.execute(
        "INSERT INTO logs (item_id, log_date, minutes_spent, progress_at, comment, user_id) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            item_id,
            request.form.get("log_date") or date.today().isoformat(),
            to_int(request.form.get("minutes_spent"), 0),
            to_float(request.form.get("progress_at")),
            request.form.get("comment", "").strip(),
            g.user["id"],
        ),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("item_detail", item_id=item_id))


@app.route("/douban/fetch")
def douban_fetch():
    url = request.args.get("url", "")
    try:
        info = fetch_douban_info(url)
    except DoubanFetchError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "抓取失败，可能是网络问题或豆瓣页面结构变化，请手动填写"}), 502
    return jsonify(info)


@app.route("/item/<int:item_id>/share.png")
def item_share_image(item_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM items WHERE id = ? AND user_id = ?", (item_id, g.user["id"])).fetchone()
    if item is None:
        conn.close()
        return "未找到该条目", 404

    totals = conn.execute(
        "SELECT MAX(progress_at) AS current, COALESCE(SUM(minutes_spent), 0) AS total_minutes "
        "FROM logs WHERE item_id = ?",
        (item_id,),
    ).fetchone()
    latest_log = conn.execute(
        "SELECT comment FROM logs WHERE item_id = ? AND comment != '' ORDER BY log_date DESC, id DESC LIMIT 1",
        (item_id,),
    ).fetchone()
    conn.close()

    comment_text = (latest_log["comment"] if latest_log else "") or item["review"] or ""

    buf = build_share_card(
        dict(item),
        current_progress=totals["current"] or 0,
        total_minutes=totals["total_minutes"],
        comment_text=comment_text,
    )

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"{item['title']}-分享卡片.png" if download else None,
        max_age=0,
    )


@app.route("/day/<date_str>")
def day_view(date_str):
    try:
        day = date.fromisoformat(date_str)
    except ValueError:
        return "日期格式不正确", 404

    conn = get_db()
    logs = conn.execute(
        "SELECT logs.*, items.title AS item_title, items.type AS item_type, "
        "items.cover_url AS item_cover_url, items.unit_label AS item_unit_label "
        "FROM logs JOIN items ON logs.item_id = items.id "
        "WHERE logs.log_date = ? AND logs.user_id = ? ORDER BY logs.id",
        (date_str, g.user["id"]),
    ).fetchall()
    moments = conn.execute(
        "SELECT * FROM moments WHERE log_date = ? AND user_id = ? ORDER BY id", (date_str, g.user["id"])
    ).fetchall()
    # Items added this day with no log entry yet (no progress/comment recorded)
    # were invisible here even though they already show on the homepage feed as
    # "item_new" — same gap build_feed() already handles, applied to a single day.
    new_items = conn.execute(
        "SELECT * FROM items WHERE substr(created_at, 1, 10) = ? AND user_id = ? "
        "AND NOT EXISTS (SELECT 1 FROM logs WHERE logs.item_id = items.id) "
        "ORDER BY id",
        (date_str, g.user["id"]),
    ).fetchall()
    conn.close()

    day_changelog = [localize_entry(c, g.lang) for c in CHANGELOG if c["date"] == date_str]

    total_minutes = sum(row["minutes_spent"] or 0 for row in logs) + sum(
        row["minutes_spent"] or 0 for row in moments
    )

    return render_template(
        "day.html",
        day=day,
        date_str=date_str,
        logs=logs,
        moments=moments,
        new_items=new_items,
        day_changelog=day_changelog,
        changelog_type=CHANGELOG_TYPE,
        moment_types=MOMENT_TYPES,
        total_minutes=total_minutes,
        activity_count=len(logs) + len(moments) + len(day_changelog) + len(new_items),
        date_heading=(
            f"{day.strftime('%B')} {day.day}, {day.strftime('%A')}"
            if g.lang == "en"
            else f"{day.month}月{day.day}日 星期{WEEKDAY_CN[day.weekday()]}"
        ),
        prev_date=(day - timedelta(days=1)).isoformat(),
        next_date=(day + timedelta(days=1)).isoformat(),
        is_today=(day == date.today()),
    )


@app.route("/day/<date_str>/share.png")
def day_share_image(date_str):
    try:
        day = date.fromisoformat(date_str)
    except ValueError:
        return "日期格式不正确", 404

    conn = get_db()
    logs = conn.execute(
        "SELECT logs.*, items.title AS item_title, items.type AS item_type, "
        "items.cover_url AS item_cover_url, items.unit_label AS item_unit_label "
        "FROM logs JOIN items ON logs.item_id = items.id "
        "WHERE logs.log_date = ? AND logs.user_id = ? ORDER BY logs.id",
        (date_str, g.user["id"]),
    ).fetchall()
    moments = conn.execute(
        "SELECT * FROM moments WHERE log_date = ? AND user_id = ? ORDER BY id", (date_str, g.user["id"])
    ).fetchall()
    new_items = conn.execute(
        "SELECT * FROM items WHERE substr(created_at, 1, 10) = ? AND user_id = ? "
        "AND NOT EXISTS (SELECT 1 FROM logs WHERE logs.item_id = items.id) "
        "ORDER BY id",
        (date_str, g.user["id"]),
    ).fetchall()
    conn.close()

    # Reuse the log card layout for items added today with no log yet (same gap
    # as day_view) by shaping them like a zero-effort log entry.
    log_rows = [dict(row) for row in logs] + [
        {
            "item_title": item["title"],
            "item_type": item["type"],
            "item_cover_url": item["cover_url"],
            "item_unit_label": item["unit_label"],
            "minutes_spent": 0,
            "progress_at": None,
            "comment": f"新添加 · {item['status']}",
        }
        for item in new_items
    ]

    buf = build_day_share_card(
        day,
        log_rows,
        [dict(row) for row in moments],
        MOMENT_TYPES,
    )

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"{date_str}-每日分享.png" if download else None,
        max_age=0,
    )


@app.route("/moment/new", methods=["GET", "POST"])
def moment_new():
    if request.method == "POST":
        moment_type = request.form.get("type", "thought")
        if moment_type not in MOMENT_TYPES:
            moment_type = "thought"
        log_date = request.form.get("log_date") or date.today().isoformat()
        image_path = save_upload(request.files.get("image"))

        conn = get_db()
        conn.execute(
            "INSERT INTO moments (type, log_date, title, content, image_path, minutes_spent, user_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                moment_type,
                log_date,
                request.form.get("title", "").strip(),
                request.form.get("content", "").strip(),
                image_path,
                to_int(request.form.get("minutes_spent"), 0),
                g.user["id"],
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("day_view", date_str=log_date))

    default_date = request.args.get("date") or date.today().isoformat()
    default_type = request.args.get("type", "thought")
    if default_type not in MOMENT_TYPES:
        default_type = "thought"
    return render_template(
        "moment_form.html",
        moment_types=MOMENT_TYPES,
        default_date=default_date,
        default_type=default_type,
    )


@app.route("/moment/<int:moment_id>/delete", methods=["POST"])
def moment_delete(moment_id):
    conn = get_db()
    row = conn.execute(
        "SELECT log_date FROM moments WHERE id = ? AND user_id = ?", (moment_id, g.user["id"])
    ).fetchone()
    log_date = row["log_date"] if row else None
    conn.execute("DELETE FROM moments WHERE id = ? AND user_id = ?", (moment_id, g.user["id"]))
    conn.commit()
    conn.close()
    if log_date:
        return redirect(url_for("day_view", date_str=log_date))
    return redirect(url_for("index"))


@app.route("/moment/scan", methods=["GET", "POST"])
def moment_scan():
    configured = is_configured()

    if request.method == "GET":
        return render_template("moment_scan.html", configured=configured, error=None)

    if not configured:
        return render_template(
            "moment_scan.html",
            configured=False,
            error="还没有配置 ANTHROPIC_API_KEY，请先在 .env 文件里填好再重试。",
        )

    files = [f for f in request.files.getlist("images") if f and f.filename]
    if not files:
        return render_template(
            "moment_scan.html", configured=True, error="请至少选择一张截图。"
        )

    entries = []
    errors = []
    for f in files:
        image_path = save_upload(f)
        if not image_path:
            errors.append(f"{f.filename}：格式不支持，已跳过")
            continue
        try:
            result = analyze_screenshot(image_path)
        except ScanError as exc:
            result = {"type": "thought", "title": "", "content": "", "log_date": ""}
            errors.append(f"{f.filename}：识别失败（{exc}），请手动填写")
        entries.append({"image_path": image_path, **result})

    return render_template(
        "moment_scan_review.html",
        entries=entries,
        errors=errors,
        moment_types=MOMENT_TYPES,
        today=date.today().isoformat(),
    )


@app.route("/moment/scan/save", methods=["POST"])
def moment_scan_save():
    count = to_int(request.form.get("count"), 0) or 0
    conn = get_db()
    saved = 0
    last_date = date.today().isoformat()
    for i in range(count):
        if not request.form.get(f"keep_{i}"):
            continue
        moment_type = request.form.get(f"type_{i}", "thought")
        if moment_type not in MOMENT_TYPES:
            moment_type = "thought"
        log_date = request.form.get(f"log_date_{i}") or date.today().isoformat()
        conn.execute(
            "INSERT INTO moments (type, log_date, title, content, image_path, minutes_spent, user_id) "
            "VALUES (?, ?, ?, ?, ?, 0, ?)",
            (
                moment_type,
                log_date,
                request.form.get(f"title_{i}", "").strip(),
                request.form.get(f"content_{i}", "").strip(),
                request.form.get(f"image_path_{i}", ""),
                g.user["id"],
            ),
        )
        saved += 1
        last_date = log_date
    conn.commit()
    conn.close()

    if saved == 0:
        return redirect(url_for("moment_scan"))
    return redirect(url_for("day_view", date_str=last_date))


@app.route("/log/<int:log_id>/delete", methods=["POST"])
def log_delete(log_id):
    conn = get_db()
    row = conn.execute(
        "SELECT item_id FROM logs WHERE id = ? AND user_id = ?", (log_id, g.user["id"])
    ).fetchone()
    item_id = row["item_id"] if row else None
    conn.execute("DELETE FROM logs WHERE id = ? AND user_id = ?", (log_id, g.user["id"]))
    conn.commit()
    conn.close()
    if item_id:
        return redirect(url_for("item_detail", item_id=item_id))
    return redirect(url_for("index"))


@app.route("/trading")
def trading():
    today = date.today()
    year = to_int(request.args.get("year"), today.year) or today.year
    month = to_int(request.args.get("month"), today.month) or today.month
    if month < 1 or month > 12:
        month = today.month

    conn = get_db()
    trades_rows = conn.execute(
        "SELECT * FROM trades WHERE user_id = ? ORDER BY trade_date, id", (g.user["id"],)
    ).fetchall()
    conn.close()
    trades_list = [dict(r) for r in trades_rows]

    daily_pnl, match_meta = compute_daily_pnl(trades_list)
    stats = summarize_daily_pnl(daily_pnl)
    stats["gross_total"] = stats["total"] + match_meta["total_fees"]
    trade_stats = summarize_trades(match_meta["closes"])
    weeks = build_month_calendar(year, month, daily_pnl)
    month_summary = build_month_summary(daily_pnl)
    series = build_cumulative_series(daily_pnl)
    chart = build_pnl_chart(series)

    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)

    month_heading = (
        date(year, month, 1).strftime("%B %Y") + " P&L Calendar"
        if g.lang == "en"
        else f"{year} 年 {month} 月盈亏日历"
    )
    for m in month_summary:
        m["label"] = (
            date(m["year"], m["month"], 1).strftime("%b %Y")
            if g.lang == "en"
            else f"{m['year']} 年 {m['month']} 月"
        )

    return render_template(
        "trading.html",
        has_trades=bool(trades_list),
        cur_year=year,
        cur_month=month,
        month_heading=month_heading,
        weeks=weeks,
        month_summary=month_summary,
        chart=chart,
        stats=stats,
        trade_stats=trade_stats,
        match_meta=match_meta,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        today=today.isoformat(),
        error=request.args.get("error"),
        info=request.args.get("info"),
    )


@app.route("/trading/upload", methods=["POST"])
def trading_upload():
    file = request.files.get("csv_file")
    if not file or not file.filename:
        return redirect(url_for("trading", error="请选择一个 CSV 文件"))

    try:
        rows, warnings = parse_schwab_csv(file.read())
    except Exception:
        return redirect(url_for("trading", error="文件解析失败，确认是券商导出的交易记录 CSV"))

    conn = get_db()
    inserted = 0
    for row in rows:
        cur = conn.execute(
            "INSERT OR IGNORE INTO trades "
            "(user_id, trade_date, action, symbol, description, quantity, price, fees, amount, dedup_key) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                g.user["id"], row["trade_date"], row["action"], row["symbol"], row["description"],
                row["quantity"], row["price"], row["fees"], row["amount"], row["dedup_key"],
            ),
        )
        if cur.rowcount:
            inserted += 1
    conn.commit()
    conn.close()

    skipped = len(rows) - inserted
    info = tr("导入完成：新增 {n} 条，跳过 {s} 条重复。", n=inserted, s=skipped)
    if warnings:
        info += " " + " ".join(warnings)
    return redirect(url_for("trading", info=info))


@app.route("/trading/clear", methods=["POST"])
def trading_clear():
    conn = get_db()
    conn.execute("DELETE FROM trades WHERE user_id = ?", (g.user["id"],))
    conn.commit()
    conn.close()
    return redirect(url_for("trading", info=tr("已清空所有导入的交易记录。")))


@app.route("/trading/share.png")
def trading_share_image():
    conn = get_db()
    trades_rows = conn.execute(
        "SELECT * FROM trades WHERE user_id = ? ORDER BY trade_date, id", (g.user["id"],)
    ).fetchall()
    conn.close()
    trades_list = [dict(r) for r in trades_rows]

    daily_pnl, match_meta = compute_daily_pnl(trades_list)
    stats = summarize_daily_pnl(daily_pnl)
    trade_stats = summarize_trades(match_meta["closes"])
    series = build_cumulative_series(daily_pnl)

    # Opt-in only -- the page has a checkbox for this, unchecked by default,
    # since position size (even without cost/quantity shown) is information
    # someone might not want to include on every share.
    include_positions = request.args.get("positions") == "1"
    open_positions = match_meta["open_position_list"] if include_positions else None

    buf = build_trading_share_card(series, stats, trade_stats, open_positions)

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"trading-pnl-{date.today().isoformat()}.png" if download else None,
        max_age=0,
    )


@app.route("/expenses")
def expenses():
    today = date.today()

    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM bank_transactions WHERE user_id = ? ORDER BY tx_date, tx_time, id", (g.user["id"],)
    ).fetchall()
    conn.close()
    tx_list = [dict(r) for r in rows]

    stats = bank.summarize(tx_list)
    daily_spending = bank.build_daily_spending(tx_list)

    years = bank.list_years(daily_spending)
    if not years:
        years = [today.year]
    summary_year = to_int(request.args.get("year"), today.year) or today.year
    if summary_year not in years:
        summary_year = years[0]

    cur_month = to_int(request.args.get("month"), today.month) or today.month
    if cur_month < 1 or cur_month > 12:
        cur_month = today.month

    year_calendar = bank.build_year_calendar(summary_year, daily_spending)
    year_spend_total = bank.year_total(summary_year, daily_spending)
    for m in year_calendar:
        m["label"] = date(2000, m["month"], 1).strftime("%b") if g.lang == "en" else f"{m['month']} 月"
    year_bar_chart = bank.build_year_bar_chart(year_calendar)
    year_txs = [t for t in tx_list if t["tx_date"][:4] == str(summary_year)]
    year_stats = bank.summarize(year_txs)
    year_top_merchants = bank.top_counterparties(year_txs)

    # All 12 months' day-calendars for the selected year are rendered into the
    # page at once (cheap -- just a few hundred small cells) and toggled with
    # JS when a month is clicked in the grid above, instead of round-tripping
    # to the server for every month switch.
    month_calendars = []
    for m in range(1, 13):
        month_prefix = f"{summary_year}-{m:02d}"
        month_calendars.append({
            "month": m,
            "weeks": bank.build_month_calendar(summary_year, m, daily_spending),
            "heading": (
                date(summary_year, m, 1).strftime("%B %Y") + " Spending Calendar"
                if g.lang == "en"
                else f"{summary_year} 年 {m} 月消费日历"
            ),
            "top_merchants": bank.top_counterparties(
                [t for t in year_txs if t["tx_date"][:7] == month_prefix]
            ),
        })

    return render_template(
        "expenses.html",
        has_transactions=bool(tx_list),
        cur_month=cur_month,
        month_calendars=month_calendars,
        years=years,
        summary_year=summary_year,
        year_calendar=year_calendar,
        year_bar_chart=year_bar_chart,
        year_spend_total=year_spend_total,
        year_stats=year_stats,
        year_top_merchants=year_top_merchants,
        stats=stats,
        error=request.args.get("error"),
        info=request.args.get("info"),
    )


@app.route("/expenses/upload", methods=["POST"])
def expenses_upload():
    file = request.files.get("pdf_file")
    password = request.form.get("password", "")
    if not file or not file.filename:
        return redirect(url_for("expenses", error="请选择一个 PDF 文件"))

    try:
        rows, warnings = bank.parse_icbc_pdf(file.read(), password)
    except ValueError:
        return redirect(url_for("expenses", error="打不开这个文件，确认密码是否正确、文件是否为工商银行历史明细 PDF"))
    except Exception:
        return redirect(url_for("expenses", error="文件解析失败，确认是工商银行导出的历史明细 PDF"))

    conn = get_db()
    inserted = 0
    for row in rows:
        cur = conn.execute(
            "INSERT OR IGNORE INTO bank_transactions "
            "(user_id, tx_date, tx_time, category, amount, balance, counterparty_name, "
            "counterparty_account, channel, dedup_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                g.user["id"], row["tx_date"], row["tx_time"], row["category"], row["amount"],
                row["balance"], row["counterparty_name"], row["counterparty_account"],
                row["channel"], row["dedup_key"],
            ),
        )
        if cur.rowcount:
            inserted += 1
    conn.commit()
    conn.close()

    skipped = len(rows) - inserted
    info = tr("导入完成：新增 {n} 条，跳过 {s} 条重复。", n=inserted, s=skipped)
    if warnings:
        info += " " + " ".join(warnings)
    return redirect(url_for("expenses", info=info))


@app.route("/expenses/clear", methods=["POST"])
def expenses_clear():
    conn = get_db()
    conn.execute("DELETE FROM bank_transactions WHERE user_id = ?", (g.user["id"],))
    conn.commit()
    conn.close()
    return redirect(url_for("expenses", info=tr("已清空所有导入的流水记录。")))


@app.route("/expenses/share.png")
def expenses_share_image():
    today = date.today()
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM bank_transactions WHERE user_id = ? ORDER BY tx_date, tx_time, id", (g.user["id"],)
    ).fetchall()
    conn.close()
    tx_list = [dict(r) for r in rows]
    daily_spending = bank.build_daily_spending(tx_list)

    years = bank.list_years(daily_spending)
    if not years:
        years = [today.year]
    year = to_int(request.args.get("year"), today.year) or today.year
    if year not in years:
        year = years[0]

    year_calendar = bank.build_year_calendar(year, daily_spending)
    for m in year_calendar:
        m["label"] = date(2000, m["month"], 1).strftime("%b") if g.lang == "en" else f"{m['month']} 月"
    year_bar_chart = bank.build_year_bar_chart(year_calendar)

    buf = build_expense_bar_share_card(year, year_bar_chart)

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"expenses-{year}-{today.isoformat()}.png" if download else None,
        max_age=0,
    )


# Marketing copy for the /showcase page -- kept as one shared list so the
# HTML page and the Pillow-rendered share card can't drift out of sync with
# each other. Bilingual pairs bundled directly here (title/title_en,
# desc/desc_en) rather than routed through tr()/translations.py, matching
# how changelog.py already handles this kind of hand-written prose. Emoji is
# used only in the HTML template; build_showcase_card deliberately leaves it
# out of the drawn image (see its docstring).
SHOWCASE_FEATURES = [
    {
        "endpoint": "trading", "emoji": "📈",
        "title": "交易盈亏", "title_en": "Trading P&L",
        "desc": "导入券商交易记录，自动生成每日盈亏日历、累计盈亏走势图，交易费用也单独算清楚。",
        "desc_en": "Import broker exports and get an auto-generated daily P&L calendar, a cumulative "
                   "equity curve, and fees broken out separately.",
    },
    {
        "endpoint": "expenses", "emoji": "💰",
        "title": "消费追踪", "title_en": "Expense Tracking",
        "desc": "上传银行流水 PDF 就能识别，生成消费日历、收支分类、消费商户排行，一张图看懂钱花哪了。",
        "desc_en": "Upload a bank statement PDF and it's parsed automatically into a spending calendar, "
                   "income/expense breakdown, and a top-merchants ranking.",
    },
    {
        "endpoint": "novels_list", "emoji": "📖",
        "title": "小说创作", "title_en": "Novel Writing",
        "desc": "在线写小说、发章节、加角色和视频，边写边发，读者可以直接在网页上追更。",
        "desc_en": "Write and publish novels chapter by chapter, with characters and video, right from "
                   "the browser -- readers follow along on the same site.",
    },
    {
        "endpoint": "moment_new", "emoji": "📝",
        "title": "分享动态", "title_en": "Life Moments",
        "desc": "记录看书追剧、运动健身、生活点滴，还能把手机截图丢给 AI 自动识别导入。",
        "desc_en": "Log day-to-day life -- books, shows, workouts, thoughts -- or just hand a screenshot "
                   "to AI and let it fill the entry in for you.",
    },
]


@app.route("/showcase")
def showcase():
    return render_template("showcase.html", features=SHOWCASE_FEATURES)


@app.route("/showcase/share.png")
def showcase_share_image():
    en = g.lang == "en"
    pairs = [
        (f["title_en"] if en else f["title"], f["desc_en"] if en else f["desc"])
        for f in SHOWCASE_FEATURES
    ]
    buf = build_showcase_card(pairs)
    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"showcase-{date.today().isoformat()}.png" if download else None,
        max_age=0,
    )


# Just a label for organizing the list / centering the draw-map's initial
# view -- not a hard technical restriction, OSM tiles cover the world.
ROUTE_COUNTRIES = ["中国", "日本", "美国", "其他"]


ROUTE_MAX_POINTS = 2000  # generous for hand-clicked points; just a backstop
# against a client-side glitch (e.g. a double-firing click handler) flooding
# storage or, worse, generating a share-image request that hammers OSM's
# tile servers for thousands of tiles at once.


def _parse_route_points(raw):
    """raw: the JSON string posted from the draw-route form (a list of
    {"lat":, "lng":, "label":} objects, see db.py's custom_routes.points
    comment -- "label" is optional, populated when a point came from typing
    a place name in and geocoding it rather than clicking the map). Drops
    anything malformed instead of failing the whole save -- a few bad
    points from some client-side glitch shouldn't lose an otherwise-valid
    route. Returns [] if raw doesn't even parse as JSON."""
    try:
        points = json.loads(raw or "[]")
    except (TypeError, ValueError):
        return []
    clean = []
    for p in points if isinstance(points, list) else []:
        if len(clean) >= ROUTE_MAX_POINTS:
            break
        try:
            lat, lng = float(p["lat"]), float(p["lng"])
        except (KeyError, TypeError, ValueError):
            continue
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            point = {"lat": lat, "lng": lng}
            label = p.get("label") if isinstance(p, dict) else None
            if isinstance(label, str) and label.strip():
                point["label"] = label.strip()[:60]
            clean.append(point)
    return clean


def _route_is_locked_for_viewer(route):
    if not route["is_locked"]:
        return False
    return not g.user or (g.user["id"] != route["user_id"] and not g.user["is_admin"])


@app.route("/routes")
def routes_list():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM custom_routes WHERE user_id = ? ORDER BY created_at DESC", (g.user["id"],)
    ).fetchall()
    conn.close()
    routes = []
    for r in rows:
        d = dict(r)
        d["points"] = json.loads(d["points"])
        routes.append(d)
    return render_template("routes_list.html", routes=routes, info=request.args.get("info"))


@app.route("/routes/new", methods=["GET", "POST"])
def routes_new():
    if request.method == "POST":
        title = request.form.get("title", "").strip() or tr("未命名路线")
        country = request.form.get("country", "").strip()
        points = _parse_route_points(request.form.get("points"))
        if len(points) < 2:
            return redirect(url_for("routes_new", error=tr("路线至少需要两个点，在地图上多点几下")))

        conn = get_db()
        cur = conn.execute(
            "INSERT INTO custom_routes (user_id, title, country, points) VALUES (?, ?, ?, ?)",
            (g.user["id"], title, country, json.dumps(points)),
        )
        route_id = cur.lastrowid
        conn.commit()
        conn.close()
        return redirect(url_for("route_detail", route_id=route_id))

    return render_template("routes_new.html", countries=ROUTE_COUNTRIES, error=request.args.get("error"))


@app.route("/routes/<int:route_id>/edit", methods=["GET", "POST"])
def route_edit(route_id):
    conn = get_db()
    route = conn.execute("SELECT * FROM custom_routes WHERE id = ?", (route_id,)).fetchone()
    if route is None or route["user_id"] != g.user["id"]:
        conn.close()
        return "未找到该路线", 404

    if request.method == "POST":
        title = request.form.get("title", "").strip() or tr("未命名路线")
        country = request.form.get("country", "").strip()
        points = _parse_route_points(request.form.get("points"))
        if len(points) < 2:
            conn.close()
            return redirect(url_for("route_edit", route_id=route_id, error=tr("路线至少需要两个点，在地图上多点几下")))

        conn.execute(
            "UPDATE custom_routes SET title = ?, country = ?, points = ?, updated_at = datetime('now','localtime') "
            "WHERE id = ?",
            (title, country, json.dumps(points), route_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("route_detail", route_id=route_id))

    conn.close()
    route_dict = dict(route)
    route_dict["points"] = json.loads(route_dict["points"])
    return render_template(
        "routes_new.html", countries=ROUTE_COUNTRIES, error=request.args.get("error"), route=route_dict
    )


@app.route("/routes/<int:route_id>")
def route_detail(route_id):
    conn = get_db()
    route = conn.execute("SELECT * FROM custom_routes WHERE id = ?", (route_id,)).fetchone()
    conn.close()
    if route is None:
        return "未找到该路线", 404

    if _route_is_locked_for_viewer(route):
        return "这条路线还没有公开分享，只有创建者能看", 403

    is_owner = bool(g.user) and g.user["id"] == route["user_id"]
    points = json.loads(route["points"])
    return render_template("route_detail.html", route=route, points=points, is_owner=is_owner)


@app.route("/routes/<int:route_id>/share", methods=["POST"])
def route_share_toggle(route_id):
    conn = get_db()
    route = conn.execute("SELECT * FROM custom_routes WHERE id = ?", (route_id,)).fetchone()
    if route is None or route["user_id"] != g.user["id"]:
        conn.close()
        return "未找到该路线", 404
    new_locked = 0 if route["is_locked"] else 1
    conn.execute(
        "UPDATE custom_routes SET is_locked = ?, updated_at = datetime('now','localtime') WHERE id = ?",
        (new_locked, route_id),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("route_detail", route_id=route_id))


@app.route("/routes/<int:route_id>/delete", methods=["POST"])
def route_delete(route_id):
    conn = get_db()
    route = conn.execute("SELECT * FROM custom_routes WHERE id = ?", (route_id,)).fetchone()
    if route is None or route["user_id"] != g.user["id"]:
        conn.close()
        return "未找到该路线", 404
    conn.execute("DELETE FROM custom_routes WHERE id = ?", (route_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("routes_list", info=tr("已删除该路线")))


@app.route("/routes/<int:route_id>/share.png")
def route_share_image(route_id):
    conn = get_db()
    route = conn.execute("SELECT * FROM custom_routes WHERE id = ?", (route_id,)).fetchone()
    conn.close()
    if route is None:
        return "未找到该路线", 404
    if _route_is_locked_for_viewer(route):
        return "这条路线还没有公开分享，只有创建者能看", 403

    points = json.loads(route["points"])
    style = request.args.get("style")
    if style not in ("standard", "terrain", "outline"):
        style = "standard"
    if style == "outline":
        buf = build_route_outline_card(route["title"], points)
    else:
        buf = build_route_share_card(route["title"], points, style=style)

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"route-{route_id}-{date.today().isoformat()}.png" if download else None,
        max_age=0,
    )


NOVEL_STATUSES = ["连载中", "已完结", "暂停"]


@app.route("/novels")
def novels_list():
    conn = get_db()
    novels = conn.execute("SELECT * FROM novels ORDER BY updated_at DESC").fetchall()
    word_counts = dict(conn.execute(
        "SELECT novel_id, SUM(LENGTH(content)) AS total FROM novel_chapters GROUP BY novel_id"
    ).fetchall())
    conn.close()
    return render_template("novels_list.html", novels=novels, word_counts=word_counts)


@app.route("/novel/<int:novel_id>")
def novel_detail(novel_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
    if novel is None:
        conn.close()
        return "未找到该小说", 404
    chapters = conn.execute(
        "SELECT c.id, c.chapter_no, c.title, c.is_locked, LENGTH(c.content) AS word_count, c.updated_at, "
        "c.volume_id, v.volume_no, v.title AS volume_title "
        "FROM novel_chapters c LEFT JOIN novel_volumes v ON v.id = c.volume_id "
        "WHERE c.novel_id = ? ORDER BY c.chapter_no ASC",
        (novel_id,),
    ).fetchall()
    total_words = sum(c["word_count"] or 0 for c in chapters)
    volumes = conn.execute(
        "SELECT * FROM novel_volumes WHERE novel_id = ? ORDER BY volume_no ASC", (novel_id,)
    ).fetchall()
    chapter_groups = group_chapters_by_volume(chapters)
    characters = conn.execute(
        "SELECT * FROM novel_characters WHERE novel_id = ? ORDER BY sort_order ASC, id ASC", (novel_id,)
    ).fetchall()
    videos = conn.execute(
        "SELECT * FROM novel_videos WHERE novel_id = ? ORDER BY created_at DESC", (novel_id,)
    ).fetchall()
    references = conn.execute(
        "SELECT i.* FROM items i JOIN novel_references nr ON nr.item_id = i.id "
        "WHERE nr.novel_id = ? ORDER BY i.title ASC",
        (novel_id,),
    ).fetchall()
    conn.close()
    # cache-busting timestamp so a stale CDN-cached response for this URL never gets
    # stuck being served long-term (max_age=0 on the route itself only prevents new
    # long-lived caching going forward, not an already-cached copy of the bare URL).
    share_ts = int(time.time())
    share_url = url_for("novel_share_image", novel_id=novel_id, download=1, v=share_ts)
    preview_url = url_for("novel_share_image", novel_id=novel_id, v=share_ts)
    return render_template(
        "novel_detail.html", novel=novel, chapters=chapters, chapter_groups=chapter_groups,
        volumes=volumes, characters=characters, videos=videos,
        references=references, share_url=share_url, preview_url=preview_url, total_words=total_words,
    )


@app.route("/novel/<int:novel_id>/share.png")
def novel_share_image(novel_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
    if novel is None:
        conn.close()
        return "未找到该小说", 404
    chapters = conn.execute(
        "SELECT c.id, c.chapter_no, c.title, LENGTH(c.content) AS word_count, "
        "c.volume_id, v.volume_no, v.title AS volume_title "
        "FROM novel_chapters c LEFT JOIN novel_volumes v ON v.id = c.volume_id "
        "WHERE c.novel_id = ? ORDER BY c.chapter_no ASC",
        (novel_id,),
    ).fetchall()
    total_words = sum(c["word_count"] or 0 for c in chapters)
    references = conn.execute(
        "SELECT i.* FROM items i JOIN novel_references nr ON nr.item_id = i.id "
        "WHERE nr.novel_id = ? AND nr.in_share = 1 ORDER BY i.title ASC LIMIT 10",
        (novel_id,),
    ).fetchall()
    conn.close()

    buf = build_novel_share_card(dict(novel), chapters, references, total_words)

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"{novel['title']}-分享卡片.png" if download else None,
        max_age=0,
    )


def _get_owned_novel(conn, novel_id):
    """The novel-authoring equivalent of the item ownership checks from step 2 —
    returns the novel row only if it belongs to the logged-in user, else None
    (same 404 either way, so a wrong-owner guess doesn't reveal the novel exists)."""
    return conn.execute(
        "SELECT * FROM novels WHERE id = ? AND user_id = ?", (novel_id, g.user["id"])
    ).fetchone()


def _load_novel_and_chapters(novel_id, conn):
    novel = _get_owned_novel(conn, novel_id)
    if novel is None:
        return None, None
    chapters = conn.execute(
        "SELECT c.*, v.volume_no, v.title AS volume_title "
        "FROM novel_chapters c LEFT JOIN novel_volumes v ON v.id = c.volume_id "
        "WHERE c.novel_id = ? ORDER BY c.chapter_no ASC",
        (novel_id,),
    ).fetchall()
    return novel, chapters


# Not in PUBLIC_ENDPOINTS, so require_login() gates these behind a password login.
@app.route("/novel/<int:novel_id>/export.docx")
def novel_export_docx(novel_id):
    conn = get_db()
    novel, chapters = _load_novel_and_chapters(novel_id, conn)
    conn.close()
    if novel is None:
        return "未找到该小说", 404

    buf = build_novel_docx(dict(novel), [dict(c) for c in chapters])
    return send_file(
        buf,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        as_attachment=True,
        download_name=f"{novel['title']}.docx",
    )


@app.route("/novel/<int:novel_id>/export.pdf")
def novel_export_pdf(novel_id):
    conn = get_db()
    novel, chapters = _load_novel_and_chapters(novel_id, conn)
    conn.close()
    if novel is None:
        return "未找到该小说", 404

    buf = build_novel_pdf(dict(novel), [dict(c) for c in chapters])
    return send_file(
        buf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"{novel['title']}.pdf",
    )


def build_chapter_blocks(content, characters, routes=None):
    """Split chapter text into paragraphs and slot each character's standee (or,
    for a travelogue reusing the novel feature, each attached route's outline
    map) in right after the paragraph where its name/title is first mentioned,
    so it reveals as the reader actually gets there rather than all at once at
    the top of the page. Same matching rule for both: a plain substring check
    against the paragraph text, no special markup to type -- just mention the
    route by its title somewhere in the prose."""
    routes = routes or []
    paragraphs = [p for p in content.split("\n") if p.strip()]
    introduced_chars = set()
    introduced_routes = set()
    blocks = []
    for p in paragraphs:
        blocks.append({"type": "text", "text": p})
        for ch in characters:
            if ch["id"] in introduced_chars or not ch["name"] or ch["name"] not in p:
                continue
            introduced_chars.add(ch["id"])
            blocks.append({"type": "character", "character": ch})
        for rt in routes:
            if rt["id"] in introduced_routes or not rt["title"] or rt["title"] not in p:
                continue
            introduced_routes.add(rt["id"])
            blocks.append({"type": "route", "route": rt})
    unmatched_characters = [ch for ch in characters if ch["id"] not in introduced_chars]
    unmatched_routes = [rt for rt in routes if rt["id"] not in introduced_routes]
    return blocks, unmatched_characters, unmatched_routes


CHAPTER_LOCK_PREVIEW_PARAGRAPHS = 3


@app.route("/novel/<int:novel_id>/chapter/<int:chapter_id>")
def novel_chapter_read(novel_id, chapter_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
    chapter = conn.execute(
        "SELECT * FROM novel_chapters WHERE id = ? AND novel_id = ?", (chapter_id, novel_id)
    ).fetchone()
    if novel is None or chapter is None:
        conn.close()
        return "未找到该章节", 404

    # Locked content used to mean "any logged-in session" — now that novels have
    # real per-account owners, it means "the author, or an admin"; unlocked
    # content is unaffected and stays public exactly as before.
    locked = bool(novel["is_locked"] or chapter["is_locked"]) and (
        not g.user or (g.user["id"] != novel["user_id"] and not g.user["is_admin"])
    )

    chapters = conn.execute(
        "SELECT id, chapter_no, title, is_locked FROM novel_chapters WHERE novel_id = ? ORDER BY chapter_no ASC",
        (novel_id,),
    ).fetchall()
    if locked:
        # Don't reveal characters/videos/routes tied to content the viewer can't actually read.
        characters, videos, routes = [], [], []
    else:
        characters = conn.execute(
            "SELECT nc.* FROM novel_characters nc "
            "JOIN novel_chapter_characters ncc ON ncc.character_id = nc.id "
            "WHERE ncc.chapter_id = ? ORDER BY nc.sort_order ASC, nc.id ASC",
            (chapter_id,),
        ).fetchall()
        videos = conn.execute(
            "SELECT nv.* FROM novel_videos nv "
            "JOIN novel_chapter_videos ncv ON ncv.video_id = nv.id "
            "WHERE ncv.chapter_id = ? ORDER BY nv.created_at DESC",
            (chapter_id,),
        ).fetchall()
        route_rows = conn.execute(
            "SELECT cr.* FROM custom_routes cr "
            "JOIN novel_chapter_routes ncr ON ncr.route_id = cr.id "
            "WHERE ncr.chapter_id = ? ORDER BY cr.created_at DESC",
            (chapter_id,),
        ).fetchall()
        # A route attached to this chapter can still be privately locked on
        # its own -- that's a separate setting from the chapter's, so it only
        # shows here to its own owner (or an admin) until they share it too.
        routes = [r for r in route_rows if not _route_is_locked_for_viewer(r)]
    conn.close()

    ids = [c["id"] for c in chapters]
    idx = ids.index(chapter_id)
    prev_chapter = chapters[idx - 1] if idx > 0 else None
    next_chapter = chapters[idx + 1] if idx < len(chapters) - 1 else None

    if locked:
        paragraphs = [
            p for p in chapter["content"].replace("\r\n", "\n").replace("\r", "\n").split("\n") if p.strip()
        ]
        preview_text = "\n".join(paragraphs[:CHAPTER_LOCK_PREVIEW_PARAGRAPHS])
        blocks, unmatched_characters, unmatched_routes = build_chapter_blocks(preview_text, [])
    else:
        blocks, unmatched_characters, unmatched_routes = build_chapter_blocks(chapter["content"], characters, routes)

    # Same cache-busting versioning as the novel share link — see the comment there.
    share_ts = int(time.time())
    share_url = url_for("novel_chapter_share_image", novel_id=novel_id, chapter_id=chapter_id, download=1, v=share_ts)
    preview_url = url_for("novel_chapter_share_image", novel_id=novel_id, chapter_id=chapter_id, v=share_ts)

    return render_template(
        "novel_chapter.html", novel=novel, chapter=chapter, chapters=chapters,
        blocks=blocks, unmatched_characters=unmatched_characters, videos=videos,
        unmatched_routes=unmatched_routes,
        prev_chapter=prev_chapter, next_chapter=next_chapter,
        share_url=share_url, preview_url=preview_url, locked=locked,
    )


@app.route("/novel/<int:novel_id>/chapter/<int:chapter_id>/share.png")
def novel_chapter_share_image(novel_id, chapter_id):
    conn = get_db()
    novel = _get_owned_novel(conn, novel_id)
    chapter = conn.execute(
        "SELECT * FROM novel_chapters WHERE id = ? AND novel_id = ?", (chapter_id, novel_id)
    ).fetchone()
    route_rows = [] if chapter is None else conn.execute(
        "SELECT cr.* FROM custom_routes cr "
        "JOIN novel_chapter_routes ncr ON ncr.route_id = cr.id "
        "WHERE ncr.chapter_id = ? ORDER BY cr.created_at DESC",
        (chapter_id,),
    ).fetchall()
    conn.close()
    if novel is None or chapter is None:
        return "未找到该章节", 404

    # This endpoint only ever runs for the novel's own owner (_get_owned_novel
    # above already enforces that), so unlike the read page there's no need to
    # filter attached routes by their own lock -- the owner can always see
    # their own routes regardless of that route's separate sharing setting.
    routes = [dict(r, points=json.loads(r["points"])) for r in route_rows]
    blocks, _, unmatched_routes = build_chapter_blocks(chapter["content"], [], routes)
    buf = build_chapter_share_card(dict(novel), dict(chapter), blocks=blocks, unmatched_routes=unmatched_routes)

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"{novel['title']}-第{chapter['chapter_no']}章-分享图.png" if download else None,
        max_age=0,
    )


@app.route("/novel/new", methods=["GET", "POST"])
def novel_new():
    if request.method == "POST":
        cover_path = save_novel_image(request.files.get("cover_file"))
        conn = get_db()
        conn.execute(
            "INSERT INTO novels (title, summary, status, cover_image, is_locked, user_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                request.form["title"].strip(),
                request.form.get("summary", "").strip(),
                request.form.get("status", "连载中"),
                cover_path,
                1 if request.form.get("is_locked") else 0,
                g.user["id"],
            ),
        )
        conn.commit()
        novel_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id))

    return render_template("novel_form.html", novel=None, statuses=NOVEL_STATUSES)


@app.route("/novel/<int:novel_id>/edit", methods=["GET", "POST"])
def novel_edit(novel_id):
    conn = get_db()
    novel = _get_owned_novel(conn, novel_id)
    if novel is None:
        conn.close()
        return "未找到该小说", 404

    if request.method == "POST":
        cover_path = save_novel_image(request.files.get("cover_file")) or novel["cover_image"]
        conn.execute(
            "UPDATE novels SET title=?, summary=?, status=?, cover_image=?, is_locked=?, "
            "updated_at=datetime('now','localtime') WHERE id=?",
            (
                request.form["title"].strip(),
                request.form.get("summary", "").strip(),
                request.form.get("status", "连载中"),
                cover_path,
                1 if request.form.get("is_locked") else 0,
                novel_id,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id))

    chapters = conn.execute(
        "SELECT c.id, c.chapter_no, c.title, c.is_locked, LENGTH(c.content) AS word_count, c.updated_at, "
        "c.volume_id, v.volume_no, v.title AS volume_title "
        "FROM novel_chapters c LEFT JOIN novel_volumes v ON v.id = c.volume_id "
        "WHERE c.novel_id = ? ORDER BY c.chapter_no ASC",
        (novel_id,),
    ).fetchall()
    total_words = sum(c["word_count"] or 0 for c in chapters)
    volumes = conn.execute(
        "SELECT * FROM novel_volumes WHERE novel_id = ? ORDER BY volume_no ASC", (novel_id,)
    ).fetchall()
    chapter_groups = group_chapters_by_volume(chapters)
    characters = conn.execute(
        "SELECT * FROM novel_characters WHERE novel_id = ? ORDER BY sort_order ASC, id ASC", (novel_id,)
    ).fetchall()
    videos = conn.execute(
        "SELECT * FROM novel_videos WHERE novel_id = ? ORDER BY created_at DESC", (novel_id,)
    ).fetchall()
    references = conn.execute(
        "SELECT i.*, nr.in_share FROM items i JOIN novel_references nr ON nr.item_id = i.id "
        "WHERE nr.novel_id = ? ORDER BY i.title ASC",
        (novel_id,),
    ).fetchall()
    conn.close()
    return render_template(
        "novel_form.html", novel=novel, statuses=NOVEL_STATUSES,
        chapters=chapters, chapter_groups=chapter_groups, volumes=volumes,
        characters=characters, videos=videos, references=references,
        total_words=total_words, error=request.args.get("error"),
    )


@app.route("/novel/<int:novel_id>/delete", methods=["POST"])
def novel_delete(novel_id):
    conn = get_db()
    conn.execute("DELETE FROM novels WHERE id = ? AND user_id = ?", (novel_id, g.user["id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("novels_list"))


def set_chapter_links(conn, chapter_id, character_ids, video_ids, route_ids=()):
    conn.execute("DELETE FROM novel_chapter_characters WHERE chapter_id = ?", (chapter_id,))
    conn.executemany(
        "INSERT INTO novel_chapter_characters (chapter_id, character_id) VALUES (?, ?)",
        [(chapter_id, cid) for cid in character_ids],
    )
    conn.execute("DELETE FROM novel_chapter_videos WHERE chapter_id = ?", (chapter_id,))
    conn.executemany(
        "INSERT INTO novel_chapter_videos (chapter_id, video_id) VALUES (?, ?)",
        [(chapter_id, vid) for vid in video_ids],
    )
    conn.execute("DELETE FROM novel_chapter_routes WHERE chapter_id = ?", (chapter_id,))
    conn.executemany(
        "INSERT INTO novel_chapter_routes (chapter_id, route_id) VALUES (?, ?)",
        [(chapter_id, rid) for rid in route_ids],
    )


@app.route("/novel/<int:novel_id>/chapter/new", methods=["GET", "POST"])
def novel_chapter_new(novel_id):
    conn = get_db()
    novel = _get_owned_novel(conn, novel_id)
    if novel is None:
        conn.close()
        return "未找到该小说", 404

    if request.method == "POST":
        next_no = conn.execute(
            "SELECT COALESCE(MAX(chapter_no), 0) + 1 AS n FROM novel_chapters WHERE novel_id = ?", (novel_id,)
        ).fetchone()["n"]
        conn.execute(
            "INSERT INTO novel_chapters (novel_id, chapter_no, title, content, is_locked, volume_id, user_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                novel_id, next_no, request.form["title"].strip(), request.form.get("content", ""),
                1 if request.form.get("is_locked") else 0, to_int(request.form.get("volume_id")),
                g.user["id"],
            ),
        )
        chapter_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        set_chapter_links(
            conn, chapter_id,
            to_int_list(request.form.getlist("character_ids")),
            to_int_list(request.form.getlist("video_ids")),
            to_int_list(request.form.getlist("route_ids")),
        )
        conn.execute("UPDATE novels SET updated_at=datetime('now','localtime') WHERE id=?", (novel_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id))

    volumes = conn.execute(
        "SELECT * FROM novel_volumes WHERE novel_id = ? ORDER BY volume_no ASC", (novel_id,)
    ).fetchall()
    conn.close()
    return render_template(
        "novel_chapter_form.html", novel=novel, chapter=None, volumes=volumes,
        preselected_characters=[], preselected_videos=[], preselected_routes=[],
    )


@app.route("/novel/<int:novel_id>/chapter/<int:chapter_id>/edit", methods=["GET", "POST"])
def novel_chapter_edit(novel_id, chapter_id):
    conn = get_db()
    novel = _get_owned_novel(conn, novel_id)
    chapter = conn.execute(
        "SELECT * FROM novel_chapters WHERE id = ? AND novel_id = ?", (chapter_id, novel_id)
    ).fetchone()
    if novel is None or chapter is None:
        conn.close()
        return "未找到该章节", 404

    if request.method == "POST":
        conn.execute(
            "UPDATE novel_chapters SET title=?, content=?, is_locked=?, volume_id=?, "
            "updated_at=datetime('now','localtime') WHERE id=?",
            (
                request.form["title"].strip(), request.form.get("content", ""),
                1 if request.form.get("is_locked") else 0, to_int(request.form.get("volume_id")), chapter_id,
            ),
        )
        set_chapter_links(
            conn, chapter_id,
            to_int_list(request.form.getlist("character_ids")),
            to_int_list(request.form.getlist("video_ids")),
            to_int_list(request.form.getlist("route_ids")),
        )
        conn.execute("UPDATE novels SET updated_at=datetime('now','localtime') WHERE id=?", (novel_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id))

    preselected_characters = conn.execute(
        "SELECT nc.id, nc.name, nc.image_path FROM novel_characters nc "
        "JOIN novel_chapter_characters ncc ON ncc.character_id = nc.id "
        "WHERE ncc.chapter_id = ? ORDER BY nc.sort_order ASC, nc.id ASC",
        (chapter_id,),
    ).fetchall()
    preselected_videos = conn.execute(
        "SELECT nv.id, nv.title, nv.thumbnail_path, nv.source_type FROM novel_videos nv "
        "JOIN novel_chapter_videos ncv ON ncv.video_id = nv.id "
        "WHERE ncv.chapter_id = ? ORDER BY nv.created_at DESC",
        (chapter_id,),
    ).fetchall()
    preselected_routes = conn.execute(
        "SELECT cr.id, cr.title, cr.country FROM custom_routes cr "
        "JOIN novel_chapter_routes ncr ON ncr.route_id = cr.id "
        "WHERE ncr.chapter_id = ? ORDER BY cr.created_at DESC",
        (chapter_id,),
    ).fetchall()
    volumes = conn.execute(
        "SELECT * FROM novel_volumes WHERE novel_id = ? ORDER BY volume_no ASC", (novel_id,)
    ).fetchall()
    conn.close()
    return render_template(
        "novel_chapter_form.html", novel=novel, chapter=chapter, volumes=volumes,
        preselected_characters=preselected_characters, preselected_videos=preselected_videos,
        preselected_routes=preselected_routes,
    )


@app.route("/novel/<int:novel_id>/characters/search")
def novel_character_search(novel_id):
    # Per-novel list is small, so an empty query returns everyone (typing filters) —
    # this way untitled/hard-to-spell entries are still reachable by just focusing.
    q = request.args.get("q", "").strip()
    conn = get_db()
    if _get_owned_novel(conn, novel_id) is None:
        conn.close()
        return jsonify([])
    if q:
        rows = conn.execute(
            "SELECT id, name, image_path FROM novel_characters WHERE novel_id = ? AND name LIKE ? "
            "ORDER BY sort_order ASC, id ASC LIMIT 20",
            (novel_id, f"%{q}%"),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, image_path FROM novel_characters WHERE novel_id = ? "
            "ORDER BY sort_order ASC, id ASC LIMIT 20",
            (novel_id,),
        ).fetchall()
    conn.close()
    return jsonify([
        {
            "id": r["id"],
            "label": r["name"],
            "image_url": url_for("serve_novel_media", filename=r["image_path"]) if r["image_path"] else "",
        }
        for r in rows
    ])


@app.route("/novel/<int:novel_id>/videos/search")
def novel_video_search(novel_id):
    q = request.args.get("q", "").strip()
    conn = get_db()
    if _get_owned_novel(conn, novel_id) is None:
        conn.close()
        return jsonify([])
    if q:
        rows = conn.execute(
            "SELECT id, title, thumbnail_path, source_type FROM novel_videos "
            "WHERE novel_id = ? AND title LIKE ? ORDER BY created_at DESC LIMIT 20",
            (novel_id, f"%{q}%"),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, title, thumbnail_path, source_type FROM novel_videos "
            "WHERE novel_id = ? ORDER BY created_at DESC LIMIT 20",
            (novel_id,),
        ).fetchall()
    conn.close()
    return jsonify([
        {
            "id": r["id"],
            "label": r["title"] or f"视频 #{r['id']}",
            "image_url": (
                url_for("serve_novel_media", filename=r["thumbnail_path"])
                if r["source_type"] == "upload" and r["thumbnail_path"] else ""
            ),
        }
        for r in rows
    ])


@app.route("/routes/search")
def routes_search():
    """Same shape as novel_video_search/novel_character_search, but routes
    belong to a user, not a novel -- scoped by the logged-in user instead of
    a novel_id, so this works for any chapter in any of their novels."""
    if not g.user:
        return jsonify([])
    q = request.args.get("q", "").strip()
    conn = get_db()
    if q:
        rows = conn.execute(
            "SELECT id, title, country FROM custom_routes "
            "WHERE user_id = ? AND title LIKE ? ORDER BY created_at DESC LIMIT 20",
            (g.user["id"], f"%{q}%"),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, title, country FROM custom_routes "
            "WHERE user_id = ? ORDER BY created_at DESC LIMIT 20",
            (g.user["id"],),
        ).fetchall()
    conn.close()
    return jsonify([
        {
            "id": r["id"],
            "label": r["title"] or f"路线 #{r['id']}",
            "image_url": "",
        }
        for r in rows
    ])


@app.route("/novel/<int:novel_id>/chapter/<int:chapter_id>/delete", methods=["POST"])
def novel_chapter_delete(novel_id, chapter_id):
    conn = get_db()
    if _get_owned_novel(conn, novel_id) is None:
        conn.close()
        return "未找到该小说", 404
    conn.execute("DELETE FROM novel_chapters WHERE id = ? AND novel_id = ?", (chapter_id, novel_id))
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/volume/new", methods=["POST"])
def novel_volume_new(novel_id):
    title = request.form.get("title", "").strip()
    conn = get_db()
    if title and _get_owned_novel(conn, novel_id) is not None:
        next_no = conn.execute(
            "SELECT COALESCE(MAX(volume_no), 0) + 1 AS n FROM novel_volumes WHERE novel_id = ?", (novel_id,)
        ).fetchone()["n"]
        conn.execute(
            "INSERT INTO novel_volumes (novel_id, volume_no, title, user_id) VALUES (?, ?, ?, ?)",
            (novel_id, next_no, title, g.user["id"]),
        )
        conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/volume/<int:volume_id>/delete", methods=["POST"])
def novel_volume_delete(novel_id, volume_id):
    conn = get_db()
    if _get_owned_novel(conn, novel_id) is None:
        conn.close()
        return "未找到该小说", 404
    # ON DELETE SET NULL unassigns any chapters in this volume rather than
    # deleting them — a volume is just an organizational label on chapters,
    # not a container that owns them.
    conn.execute("DELETE FROM novel_volumes WHERE id = ? AND novel_id = ?", (volume_id, novel_id))
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/chapters/bulk-lock", methods=["POST"])
def novel_chapters_bulk_lock(novel_id):
    chapter_ids = to_int_list(request.form.getlist("chapter_ids"))
    lock = 1 if request.form.get("action") == "lock" else 0
    conn = get_db()
    if chapter_ids and _get_owned_novel(conn, novel_id) is not None:
        conn.executemany(
            "UPDATE novel_chapters SET is_locked = ?, updated_at=datetime('now','localtime') "
            "WHERE id = ? AND novel_id = ?",
            [(lock, cid, novel_id) for cid in chapter_ids],
        )
        conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/chapters/bulk-volume", methods=["POST"])
def novel_chapters_bulk_volume(novel_id):
    chapter_ids = to_int_list(request.form.getlist("chapter_ids"))
    volume_id = to_int(request.form.get("volume_id"))
    conn = get_db()
    if chapter_ids and _get_owned_novel(conn, novel_id) is not None:
        if volume_id is not None:
            # Guard against a volume_id from a different novel ever landing on a
            # chapter here — the grouped-list query trusts volume_id -> novel_id
            # implicitly via the join, so a mismatch would show a chapter under
            # another novel's volume heading.
            owns_volume = conn.execute(
                "SELECT 1 FROM novel_volumes WHERE id = ? AND novel_id = ?", (volume_id, novel_id)
            ).fetchone()
            if not owns_volume:
                volume_id = None
        conn.executemany(
            "UPDATE novel_chapters SET volume_id = ?, updated_at=datetime('now','localtime') "
            "WHERE id = ? AND novel_id = ?",
            [(volume_id, cid, novel_id) for cid in chapter_ids],
        )
        conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/character/new", methods=["POST"])
def novel_character_new(novel_id):
    conn = get_db()
    novel = _get_owned_novel(conn, novel_id)
    if novel is None:
        conn.close()
        return "未找到该小说", 404

    image_path = save_novel_image(request.files.get("image_file"))
    conn.execute(
        "INSERT INTO novel_characters (novel_id, name, description, image_path, user_id) VALUES (?, ?, ?, ?, ?)",
        (
            novel_id, request.form.get("name", "").strip(), request.form.get("description", "").strip(),
            image_path, g.user["id"],
        ),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/character/<int:character_id>/edit", methods=["GET", "POST"])
def novel_character_edit(novel_id, character_id):
    conn = get_db()
    novel = _get_owned_novel(conn, novel_id)
    character = conn.execute(
        "SELECT * FROM novel_characters WHERE id = ? AND novel_id = ?", (character_id, novel_id)
    ).fetchone()
    if novel is None or character is None:
        conn.close()
        return "未找到该角色", 404

    if request.method == "POST":
        image_path = save_novel_image(request.files.get("image_file")) or character["image_path"]
        conn.execute(
            "UPDATE novel_characters SET name=?, description=?, image_path=? WHERE id=?",
            (
                request.form.get("name", "").strip(),
                request.form.get("description", "").strip(),
                image_path,
                character_id,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id))

    conn.close()
    return render_template("novel_character_form.html", novel=novel, character=character)


@app.route("/novel/<int:novel_id>/character/<int:character_id>/delete", methods=["POST"])
def novel_character_delete(novel_id, character_id):
    conn = get_db()
    if _get_owned_novel(conn, novel_id) is None:
        conn.close()
        return "未找到该小说", 404
    conn.execute("DELETE FROM novel_characters WHERE id = ? AND novel_id = ?", (character_id, novel_id))
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/video/new", methods=["POST"])
def novel_video_new(novel_id):
    conn = get_db()
    novel = _get_owned_novel(conn, novel_id)
    if novel is None:
        conn.close()
        return "未找到该小说", 404

    title = request.form.get("title", "").strip()
    source_type = request.form.get("source_type", "upload")

    if source_type == "link":
        video_url = request.form.get("video_url", "").strip()
        conn.close()
        if not video_url:
            return redirect(url_for("novel_edit", novel_id=novel_id, error="请填写视频链接"))
        conn = get_db()
        conn.execute(
            "INSERT INTO novel_videos (novel_id, title, source_type, video_url, user_id) "
            "VALUES (?, ?, 'link', ?, ?)",
            (novel_id, title, video_url, g.user["id"]),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id))

    conn.close()
    file_storage = request.files.get("video_file")
    if not file_storage or not file_storage.filename:
        return redirect(url_for("novel_edit", novel_id=novel_id, error="请选择要上传的视频文件"))

    ext = Path(file_storage.filename).suffix.lower()
    if ext not in ALLOWED_VIDEO_EXT:
        return redirect(url_for("novel_edit", novel_id=novel_id, error="不支持的视频格式"))

    NOVEL_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(suffix=ext, dir=NOVEL_MEDIA_DIR)
    os.close(fd)
    tmp_path = Path(tmp_name)
    file_storage.save(tmp_path)

    duration = probe_video_duration(tmp_path)
    if duration is None:
        tmp_path.unlink(missing_ok=True)
        return redirect(url_for("novel_edit", novel_id=novel_id, error="无法解析视频文件"))
    if duration > MAX_VIDEO_SECONDS:
        tmp_path.unlink(missing_ok=True)
        return redirect(url_for("novel_edit", novel_id=novel_id, error="视频超过 5 分钟限制"))

    uid = uuid.uuid4().hex
    out_path = NOVEL_MEDIA_DIR / f"{uid}.mp4"
    thumb_path = NOVEL_MEDIA_DIR / f"{uid}.jpg"
    ok = compress_video(tmp_path, out_path)
    tmp_path.unlink(missing_ok=True)
    if not ok:
        return redirect(url_for("novel_edit", novel_id=novel_id, error="视频处理失败"))
    has_thumb = make_video_thumbnail(out_path, thumb_path)

    conn = get_db()
    conn.execute(
        "INSERT INTO novel_videos (novel_id, title, source_type, video_path, thumbnail_path, "
        "duration_seconds, user_id) VALUES (?, ?, 'upload', ?, ?, ?, ?)",
        (novel_id, title, out_path.name, thumb_path.name if has_thumb else "", int(duration), g.user["id"]),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/video/<int:video_id>/delete", methods=["POST"])
def novel_video_delete(novel_id, video_id):
    conn = get_db()
    if _get_owned_novel(conn, novel_id) is None:
        conn.close()
        return "未找到该小说", 404
    conn.execute("DELETE FROM novel_videos WHERE id = ? AND novel_id = ?", (video_id, novel_id))
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/reference/search")
def novel_reference_search(novel_id):
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    like = f"%{q}%"
    conn = get_db()
    if _get_owned_novel(conn, novel_id) is None:
        conn.close()
        return jsonify([])
    rows = conn.execute(
        "SELECT id, title, creator, cover_url FROM items "
        "WHERE type = 'book' AND user_id = ? AND (title LIKE ? OR creator LIKE ?) "
        "AND id NOT IN (SELECT item_id FROM novel_references WHERE novel_id = ?) "
        "ORDER BY title ASC LIMIT 10",
        (g.user["id"], like, like, novel_id),
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/novel/<int:novel_id>/reference/new", methods=["POST"])
def novel_reference_new(novel_id):
    conn = get_db()
    novel = _get_owned_novel(conn, novel_id)
    if novel is None:
        conn.close()
        return "未找到该小说", 404

    # Additive: search-and-add drops one book in at a time; the per-book remove
    # button handles taking one back out (no full-list re-sync anymore).
    item_ids = to_int_list(request.form.getlist("item_ids"))
    conn.executemany(
        "INSERT OR IGNORE INTO novel_references (novel_id, item_id) VALUES (?, ?)",
        [(novel_id, item_id) for item_id in item_ids],
    )
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/reference/<int:item_id>/delete", methods=["POST"])
def novel_reference_delete(novel_id, item_id):
    conn = get_db()
    if _get_owned_novel(conn, novel_id) is None:
        conn.close()
        return "未找到该小说", 404
    conn.execute("DELETE FROM novel_references WHERE item_id = ? AND novel_id = ?", (item_id, novel_id))
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/reference/<int:item_id>/toggle-share", methods=["POST"])
def novel_reference_toggle_share(novel_id, item_id):
    conn = get_db()
    if _get_owned_novel(conn, novel_id) is None:
        conn.close()
        return "未找到该小说", 404
    row = conn.execute(
        "SELECT in_share FROM novel_references WHERE novel_id = ? AND item_id = ?", (novel_id, item_id)
    ).fetchone()
    if row is not None:
        conn.execute(
            "UPDATE novel_references SET in_share = ? WHERE novel_id = ? AND item_id = ?",
            (0 if row["in_share"] else 1, novel_id, item_id),
        )
        conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


if __name__ == "__main__":
    app.run(debug=True, port=5050)
