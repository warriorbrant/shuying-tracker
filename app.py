import hashlib
import mimetypes
import os
import re
import secrets
import subprocess
import tempfile
import time
import uuid
import zipfile
from datetime import date, timedelta
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

import metrics
from ai_scan import ScanError, analyze_screenshot, is_configured
from changelog import CHANGELOG
from db import DATA_DIR, get_db, init_db
from douban import DoubanFetchError, fetch_douban_info
from share_card import build_changelog_share_card, build_day_share_card, build_share_card

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


def app_password():
    return os.environ.get("APP_PASSWORD") or ""


@app.context_processor
def inject_auth_state():
    return {"auth_enabled": bool(app_password())}


@app.context_processor
def inject_asset_version():
    css_path = Path(__file__).parent / "static" / "style.css"
    try:
        version = int(css_path.stat().st_mtime)
    except OSError:
        version = 0
    return {"asset_version": version}


PUBLIC_ENDPOINTS = {
    "login", "static", "changelog", "changelog_more", "changelog_share_image", "index",
    "serve_novel_media", "novels_list", "novel_detail", "novel_chapter_read",
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


@app.before_request
def require_login():
    if not app_password():
        return None
    if request.endpoint in PUBLIC_ENDPOINTS or request.endpoint is None:
        return None
    if not session.get("authed"):
        return redirect(url_for("login", next=request.path))
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if app_password() and secrets.compare_digest(password, app_password()):
            session.clear()
            session["authed"] = True
            session.permanent = True
            return redirect(safe_next(request.form.get("next"), url_for("index")))
        return render_template("login.html", error="密码不对，再试一次", next=request.form.get("next", ""))
    return render_template("login.html", error=None, next=request.args.get("next", ""))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/data/<path:filename>")
def serve_data(filename):
    return send_from_directory(DATA_DIR, filename)


@app.route("/novel-media/<path:filename>")
def serve_novel_media(filename):
    return send_from_directory(NOVEL_MEDIA_DIR, filename)


COVER_CACHE_DIR = DATA_DIR / "cover_cache"


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


def build_heatmap(conn, weeks=HEATMAP_WEEKS):
    today = date.today()
    dow_sunday_first = (today.weekday() + 1) % 7  # Monday=1 ... Sunday=0
    grid_end = today + timedelta(days=6 - dow_sunday_first)  # this week's Saturday
    grid_start = grid_end - timedelta(days=weeks * 7 - 1)  # a Sunday

    rows = conn.execute(
        "SELECT log_date, SUM(minutes_spent) AS minutes FROM ("
        "  SELECT log_date, minutes_spent FROM logs WHERE log_date >= ? AND log_date <= ?"
        "  UNION ALL"
        "  SELECT log_date, minutes_spent FROM moments WHERE log_date >= ? AND log_date <= ?"
        ") GROUP BY log_date",
        (
            grid_start.isoformat(),
            today.isoformat(),
            grid_start.isoformat(),
            today.isoformat(),
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


def build_feed(conn, type_filter, status_filter, offset=0, limit=FEED_PAGE_SIZE):
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
            "FROM logs JOIN items ON logs.item_id = items.id WHERE 1=1"
        )
        params = []
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
            "WHERE NOT EXISTS (SELECT 1 FROM logs WHERE logs.item_id = items.id)"
        )
        params2 = []
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
        moment_query = "SELECT * FROM moments WHERE 1=1"
        params3 = []
        if type_filter in MOMENT_TYPES:
            moment_query += " AND type = ?"
            params3.append(type_filter)
        for row in conn.execute(moment_query, params3).fetchall():
            entry = dict(row)
            entry["kind"] = "moment"
            entry["date"] = entry["log_date"]
            entries.append(entry)

    if show_changelog:
        for i, c in enumerate(CHANGELOG):
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
    lang = request.args.get("lang", "zh")
    if lang not in CHANGELOG_STRINGS:
        lang = "zh"
    t = CHANGELOG_STRINGS[lang]
    days, has_more = group_changelog_by_day(CHANGELOG, lang=lang, limit=CHANGELOG_PAGE_DAYS)
    metrics_summary = metrics.get_stats(60)
    return render_template(
        "changelog.html",
        days=days,
        days_has_more=has_more,
        heatmap=build_changelog_heatmap(lang=lang),
        today=date.today().isoformat(),
        lang=lang,
        t=t,
        metrics_summary=metrics_summary,
        uptime_human=metrics.format_uptime(metrics_summary["uptime_seconds"]),
    )


@app.route("/changelog/more")
def changelog_more():
    lang = request.args.get("lang", "zh")
    if lang not in CHANGELOG_STRINGS:
        lang = "zh"
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
    )


@app.route("/")
def index():
    if app_password() and not session.get("authed"):
        return public_landing()

    type_filter = request.args.get("type", "")
    status_filter = request.args.get("status", "")

    conn = get_db()
    feed, has_more = build_feed(conn, type_filter, status_filter)
    heatmap = build_heatmap(conn)
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
    lang = request.args.get("lang", "zh")
    if lang not in CHANGELOG_STRINGS:
        lang = "zh"
    t = CHANGELOG_STRINGS[lang]
    days, has_more = group_changelog_by_day(CHANGELOG, lang=lang, limit=CHANGELOG_PAGE_DAYS)
    metrics_summary = metrics.get_stats(60)

    return render_template(
        "public_home.html",
        days=days,
        days_has_more=has_more,
        heatmap=build_changelog_heatmap(lang=lang),
        today=date.today().isoformat(),
        lang=lang,
        t=t,
        metrics_summary=metrics_summary,
        uptime_human=metrics.format_uptime(metrics_summary["uptime_seconds"]),
    )


@app.route("/feed/more")
def feed_more():
    type_filter = request.args.get("type", "")
    status_filter = request.args.get("status", "")
    offset = to_int(request.args.get("offset"), 0) or 0

    conn = get_db()
    feed, has_more = build_feed(conn, type_filter, status_filter, offset=offset)
    conn.close()

    html = render_template(
        "_feed_items.html",
        feed=feed,
        moment_types=MOMENT_TYPES,
        changelog_type=CHANGELOG_TYPE,
    )
    return jsonify({"html": html, "has_more": has_more, "count": len(feed)})


def run_search(conn, q):
    like = f"%{q}%"
    results = []

    for row in conn.execute(
        "SELECT * FROM items WHERE title LIKE ? OR creator LIKE ? OR review LIKE ? "
        "ORDER BY created_at DESC",
        (like, like, like),
    ).fetchall():
        entry = dict(row)
        entry["kind"] = "item_match"
        entry["date"] = entry["created_at"][:10]
        results.append(entry)

    for row in conn.execute(
        "SELECT logs.*, items.title AS item_title, items.type AS item_type, "
        "items.cover_url AS item_cover_url, items.unit_label AS item_unit_label "
        "FROM logs JOIN items ON logs.item_id = items.id "
        "WHERE logs.comment LIKE ? ORDER BY logs.log_date DESC",
        (like,),
    ).fetchall():
        entry = dict(row)
        entry["kind"] = "log"
        entry["date"] = entry["log_date"]
        results.append(entry)

    for row in conn.execute(
        "SELECT * FROM moments WHERE title LIKE ? OR content LIKE ? ORDER BY log_date DESC",
        (like, like),
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
        all_results = run_search(conn, q)
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
    all_results = run_search(conn, q)
    conn.close()

    page = all_results[offset : offset + SEARCH_PAGE_SIZE]
    has_more = len(all_results) > offset + SEARCH_PAGE_SIZE
    html = render_template(
        "_feed_items.html", feed=page, moment_types=MOMENT_TYPES, changelog_type=CHANGELOG_TYPE
    )
    return jsonify({"html": html, "has_more": has_more, "count": len(page)})


@app.route("/item/new", methods=["GET", "POST"])
def item_new():
    if request.method == "POST":
        conn = get_db()
        conn.execute(
            "INSERT INTO items (type, title, creator, cover_url, total_units, unit_label, status, rating, review) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
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
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
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
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if item is None:
        conn.close()
        return "未找到该条目", 404

    if request.method == "POST":
        conn.execute(
            "UPDATE items SET type=?, title=?, creator=?, cover_url=?, total_units=?, unit_label=?, "
            "status=?, rating=?, review=? WHERE id=?",
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
                item_id,
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
        conn.execute("UPDATE items SET status=? WHERE id=?", (status, item_id))
        conn.commit()
        conn.close()
    return redirect(safe_next(request.form.get("next"), url_for("index")))


@app.route("/item/<int:item_id>/delete", methods=["POST"])
def item_delete(item_id):
    conn = get_db()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/item/<int:item_id>/log", methods=["POST"])
def log_add(item_id):
    conn = get_db()
    conn.execute(
        "INSERT INTO logs (item_id, log_date, minutes_spent, progress_at, comment) VALUES (?, ?, ?, ?, ?)",
        (
            item_id,
            request.form.get("log_date") or date.today().isoformat(),
            to_int(request.form.get("minutes_spent"), 0),
            to_float(request.form.get("progress_at")),
            request.form.get("comment", "").strip(),
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
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
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
        "WHERE logs.log_date = ? ORDER BY logs.id",
        (date_str,),
    ).fetchall()
    moments = conn.execute(
        "SELECT * FROM moments WHERE log_date = ? ORDER BY id", (date_str,)
    ).fetchall()
    conn.close()

    day_changelog = [c for c in CHANGELOG if c["date"] == date_str]

    total_minutes = sum(row["minutes_spent"] or 0 for row in logs) + sum(
        row["minutes_spent"] or 0 for row in moments
    )

    return render_template(
        "day.html",
        day=day,
        date_str=date_str,
        logs=logs,
        moments=moments,
        day_changelog=day_changelog,
        changelog_type=CHANGELOG_TYPE,
        moment_types=MOMENT_TYPES,
        total_minutes=total_minutes,
        activity_count=len(logs) + len(moments) + len(day_changelog),
        weekday_label=f"星期{WEEKDAY_CN[day.weekday()]}",
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
        "WHERE logs.log_date = ? ORDER BY logs.id",
        (date_str,),
    ).fetchall()
    moments = conn.execute(
        "SELECT * FROM moments WHERE log_date = ? ORDER BY id", (date_str,)
    ).fetchall()
    conn.close()

    buf = build_day_share_card(
        day,
        [dict(row) for row in logs],
        [dict(row) for row in moments],
        MOMENT_TYPES,
    )

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"{date_str}-每日分享.png" if download else None,
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
            "INSERT INTO moments (type, log_date, title, content, image_path, minutes_spent) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                moment_type,
                log_date,
                request.form.get("title", "").strip(),
                request.form.get("content", "").strip(),
                image_path,
                to_int(request.form.get("minutes_spent"), 0),
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
    row = conn.execute("SELECT log_date FROM moments WHERE id = ?", (moment_id,)).fetchone()
    log_date = row["log_date"] if row else None
    conn.execute("DELETE FROM moments WHERE id = ?", (moment_id,))
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
            "INSERT INTO moments (type, log_date, title, content, image_path, minutes_spent) "
            "VALUES (?, ?, ?, ?, ?, 0)",
            (
                moment_type,
                log_date,
                request.form.get(f"title_{i}", "").strip(),
                request.form.get(f"content_{i}", "").strip(),
                request.form.get(f"image_path_{i}", ""),
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
    row = conn.execute("SELECT item_id FROM logs WHERE id = ?", (log_id,)).fetchone()
    item_id = row["item_id"] if row else None
    conn.execute("DELETE FROM logs WHERE id = ?", (log_id,))
    conn.commit()
    conn.close()
    if item_id:
        return redirect(url_for("item_detail", item_id=item_id))
    return redirect(url_for("index"))


NOVEL_STATUSES = ["连载中", "已完结", "暂停"]


@app.route("/novels")
def novels_list():
    conn = get_db()
    novels = conn.execute("SELECT * FROM novels ORDER BY updated_at DESC").fetchall()
    conn.close()
    return render_template("novels_list.html", novels=novels)


@app.route("/novel/<int:novel_id>")
def novel_detail(novel_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
    if novel is None:
        conn.close()
        return "未找到该小说", 404
    chapters = conn.execute(
        "SELECT id, chapter_no, title FROM novel_chapters WHERE novel_id = ? ORDER BY chapter_no ASC",
        (novel_id,),
    ).fetchall()
    characters = conn.execute(
        "SELECT * FROM novel_characters WHERE novel_id = ? ORDER BY sort_order ASC, id ASC", (novel_id,)
    ).fetchall()
    videos = conn.execute(
        "SELECT * FROM novel_videos WHERE novel_id = ? ORDER BY created_at DESC", (novel_id,)
    ).fetchall()
    references = conn.execute(
        "SELECT * FROM novel_references WHERE novel_id = ? ORDER BY id ASC", (novel_id,)
    ).fetchall()
    conn.close()
    return render_template(
        "novel_detail.html", novel=novel, chapters=chapters, characters=characters, videos=videos,
        references=references,
    )


def build_chapter_blocks(content, characters):
    """Split chapter text into paragraphs and slot each character's standee in right
    after the paragraph where their name is first mentioned, so it reveals as the
    reader actually gets there rather than all at once at the top of the page."""
    paragraphs = [p for p in content.split("\n") if p.strip()]
    introduced = set()
    blocks = []
    for p in paragraphs:
        blocks.append({"type": "text", "text": p})
        for ch in characters:
            if ch["id"] in introduced or not ch["name"] or ch["name"] not in p:
                continue
            introduced.add(ch["id"])
            blocks.append({"type": "character", "character": ch})
    unmatched = [ch for ch in characters if ch["id"] not in introduced]
    return blocks, unmatched


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
    chapters = conn.execute(
        "SELECT id, chapter_no, title FROM novel_chapters WHERE novel_id = ? ORDER BY chapter_no ASC",
        (novel_id,),
    ).fetchall()
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
    conn.close()

    ids = [c["id"] for c in chapters]
    idx = ids.index(chapter_id)
    prev_chapter = chapters[idx - 1] if idx > 0 else None
    next_chapter = chapters[idx + 1] if idx < len(chapters) - 1 else None
    blocks, unmatched_characters = build_chapter_blocks(chapter["content"], characters)

    return render_template(
        "novel_chapter.html", novel=novel, chapter=chapter, chapters=chapters,
        blocks=blocks, unmatched_characters=unmatched_characters, videos=videos,
        prev_chapter=prev_chapter, next_chapter=next_chapter,
    )


@app.route("/novel/new", methods=["GET", "POST"])
def novel_new():
    if request.method == "POST":
        cover_path = save_novel_image(request.files.get("cover_file"))
        conn = get_db()
        conn.execute(
            "INSERT INTO novels (title, summary, status, cover_image) VALUES (?, ?, ?, ?)",
            (
                request.form["title"].strip(),
                request.form.get("summary", "").strip(),
                request.form.get("status", "连载中"),
                cover_path,
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
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
    if novel is None:
        conn.close()
        return "未找到该小说", 404

    if request.method == "POST":
        cover_path = save_novel_image(request.files.get("cover_file")) or novel["cover_image"]
        conn.execute(
            "UPDATE novels SET title=?, summary=?, status=?, cover_image=?, updated_at=datetime('now','localtime') "
            "WHERE id=?",
            (
                request.form["title"].strip(),
                request.form.get("summary", "").strip(),
                request.form.get("status", "连载中"),
                cover_path,
                novel_id,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id))

    chapters = conn.execute(
        "SELECT id, chapter_no, title FROM novel_chapters WHERE novel_id = ? ORDER BY chapter_no ASC",
        (novel_id,),
    ).fetchall()
    characters = conn.execute(
        "SELECT * FROM novel_characters WHERE novel_id = ? ORDER BY sort_order ASC, id ASC", (novel_id,)
    ).fetchall()
    videos = conn.execute(
        "SELECT * FROM novel_videos WHERE novel_id = ? ORDER BY created_at DESC", (novel_id,)
    ).fetchall()
    references = conn.execute(
        "SELECT * FROM novel_references WHERE novel_id = ? ORDER BY id ASC", (novel_id,)
    ).fetchall()
    conn.close()
    return render_template(
        "novel_form.html", novel=novel, statuses=NOVEL_STATUSES,
        chapters=chapters, characters=characters, videos=videos, references=references,
        error=request.args.get("error"),
    )


@app.route("/novel/<int:novel_id>/delete", methods=["POST"])
def novel_delete(novel_id):
    conn = get_db()
    conn.execute("DELETE FROM novels WHERE id = ?", (novel_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("novels_list"))


def set_chapter_links(conn, chapter_id, character_ids, video_ids):
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


@app.route("/novel/<int:novel_id>/chapter/new", methods=["GET", "POST"])
def novel_chapter_new(novel_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
    if novel is None:
        conn.close()
        return "未找到该小说", 404

    if request.method == "POST":
        next_no = conn.execute(
            "SELECT COALESCE(MAX(chapter_no), 0) + 1 AS n FROM novel_chapters WHERE novel_id = ?", (novel_id,)
        ).fetchone()["n"]
        conn.execute(
            "INSERT INTO novel_chapters (novel_id, chapter_no, title, content) VALUES (?, ?, ?, ?)",
            (novel_id, next_no, request.form["title"].strip(), request.form.get("content", "")),
        )
        chapter_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        set_chapter_links(
            conn, chapter_id,
            to_int_list(request.form.getlist("character_ids")),
            to_int_list(request.form.getlist("video_ids")),
        )
        conn.execute("UPDATE novels SET updated_at=datetime('now','localtime') WHERE id=?", (novel_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id))

    characters = conn.execute(
        "SELECT * FROM novel_characters WHERE novel_id = ? ORDER BY sort_order ASC, id ASC", (novel_id,)
    ).fetchall()
    videos = conn.execute(
        "SELECT * FROM novel_videos WHERE novel_id = ? ORDER BY created_at DESC", (novel_id,)
    ).fetchall()
    conn.close()
    return render_template(
        "novel_chapter_form.html", novel=novel, chapter=None,
        all_characters=characters, all_videos=videos, selected_character_ids=set(), selected_video_ids=set(),
    )


@app.route("/novel/<int:novel_id>/chapter/<int:chapter_id>/edit", methods=["GET", "POST"])
def novel_chapter_edit(novel_id, chapter_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
    chapter = conn.execute(
        "SELECT * FROM novel_chapters WHERE id = ? AND novel_id = ?", (chapter_id, novel_id)
    ).fetchone()
    if novel is None or chapter is None:
        conn.close()
        return "未找到该章节", 404

    if request.method == "POST":
        conn.execute(
            "UPDATE novel_chapters SET title=?, content=?, updated_at=datetime('now','localtime') WHERE id=?",
            (request.form["title"].strip(), request.form.get("content", ""), chapter_id),
        )
        set_chapter_links(
            conn, chapter_id,
            to_int_list(request.form.getlist("character_ids")),
            to_int_list(request.form.getlist("video_ids")),
        )
        conn.execute("UPDATE novels SET updated_at=datetime('now','localtime') WHERE id=?", (novel_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id))

    characters = conn.execute(
        "SELECT * FROM novel_characters WHERE novel_id = ? ORDER BY sort_order ASC, id ASC", (novel_id,)
    ).fetchall()
    videos = conn.execute(
        "SELECT * FROM novel_videos WHERE novel_id = ? ORDER BY created_at DESC", (novel_id,)
    ).fetchall()
    selected_character_ids = {
        row["character_id"] for row in
        conn.execute("SELECT character_id FROM novel_chapter_characters WHERE chapter_id = ?", (chapter_id,))
    }
    selected_video_ids = {
        row["video_id"] for row in
        conn.execute("SELECT video_id FROM novel_chapter_videos WHERE chapter_id = ?", (chapter_id,))
    }
    conn.close()
    return render_template(
        "novel_chapter_form.html", novel=novel, chapter=chapter,
        all_characters=characters, all_videos=videos,
        selected_character_ids=selected_character_ids, selected_video_ids=selected_video_ids,
    )


@app.route("/novel/<int:novel_id>/chapter/<int:chapter_id>/delete", methods=["POST"])
def novel_chapter_delete(novel_id, chapter_id):
    conn = get_db()
    conn.execute("DELETE FROM novel_chapters WHERE id = ? AND novel_id = ?", (chapter_id, novel_id))
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/character/new", methods=["POST"])
def novel_character_new(novel_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
    if novel is None:
        conn.close()
        return "未找到该小说", 404

    image_path = save_novel_image(request.files.get("image_file"))
    conn.execute(
        "INSERT INTO novel_characters (novel_id, name, description, image_path) VALUES (?, ?, ?, ?)",
        (novel_id, request.form.get("name", "").strip(), request.form.get("description", "").strip(), image_path),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/character/<int:character_id>/edit", methods=["GET", "POST"])
def novel_character_edit(novel_id, character_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
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
    conn.execute("DELETE FROM novel_characters WHERE id = ? AND novel_id = ?", (character_id, novel_id))
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/video/new", methods=["POST"])
def novel_video_new(novel_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
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
            "INSERT INTO novel_videos (novel_id, title, source_type, video_url) VALUES (?, ?, 'link', ?)",
            (novel_id, title, video_url),
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
        "INSERT INTO novel_videos (novel_id, title, source_type, video_path, thumbnail_path, duration_seconds) "
        "VALUES (?, ?, 'upload', ?, ?, ?)",
        (novel_id, title, out_path.name, thumb_path.name if has_thumb else "", int(duration)),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/video/<int:video_id>/delete", methods=["POST"])
def novel_video_delete(novel_id, video_id):
    conn = get_db()
    conn.execute("DELETE FROM novel_videos WHERE id = ? AND novel_id = ?", (video_id, novel_id))
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/reference/new", methods=["POST"])
def novel_reference_new(novel_id):
    conn = get_db()
    novel = conn.execute("SELECT * FROM novels WHERE id = ?", (novel_id,)).fetchone()
    if novel is None:
        conn.close()
        return "未找到该小说", 404

    title = request.form.get("title", "").strip()
    if not title:
        conn.close()
        return redirect(url_for("novel_edit", novel_id=novel_id, error="参考书目需要填写书名"))

    conn.execute(
        "INSERT INTO novel_references (novel_id, title, cover_url, douban_url) VALUES (?, ?, ?, ?)",
        (novel_id, title, request.form.get("cover_url", "").strip(), request.form.get("douban_url", "").strip()),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


@app.route("/novel/<int:novel_id>/reference/<int:reference_id>/delete", methods=["POST"])
def novel_reference_delete(novel_id, reference_id):
    conn = get_db()
    conn.execute("DELETE FROM novel_references WHERE id = ? AND novel_id = ?", (reference_id, novel_id))
    conn.commit()
    conn.close()
    return redirect(url_for("novel_edit", novel_id=novel_id))


if __name__ == "__main__":
    app.run(debug=True, port=5050)
