import os
import secrets
import uuid
from datetime import date, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    session,
    url_for,
)

from ai_scan import ScanError, analyze_screenshot, is_configured
from changelog import CHANGELOG
from db import DATA_DIR, get_db, init_db
from douban import DoubanFetchError, fetch_douban_info
from share_card import build_changelog_share_card, build_day_share_card, build_share_card

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024  # 12MB upload limit
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.permanent_session_lifetime = timedelta(days=30)

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

UPLOAD_DIR = DATA_DIR / "uploads"
ALLOWED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


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


@app.before_request
def require_login():
    if not app_password():
        return None
    if request.endpoint in ("login", "static") or request.endpoint is None:
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


@app.route("/cover-proxy")
def cover_proxy():
    url = request.args.get("url", "")
    if not url or "doubanio.com" not in url:
        return "", 404
    try:
        resp = requests.get(
            url,
            timeout=6,
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.douban.com/"},
        )
        resp.raise_for_status()
    except requests.RequestException:
        return "", 502
    return Response(
        resp.content,
        mimetype=resp.headers.get("Content-Type", "image/jpeg"),
        headers={"Cache-Control": "public, max-age=86400"},
    )


def cover_src(url):
    if url and "doubanio.com" in url:
        return url_for("cover_proxy", url=url)
    return url


app.jinja_env.globals["cover_src"] = cover_src


def save_upload(file_storage):
    if not file_storage or not file_storage.filename:
        return ""
    ext = Path(file_storage.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXT:
        return ""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    file_storage.save(UPLOAD_DIR / filename)
    return f"uploads/{filename}"


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


def build_changelog_heatmap(weeks=HEATMAP_WEEKS):
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
            month_label = f"{month_num}月"
            last_month = month_num
        weeks_data.append({"month_label": month_label, "days": days})
        cursor += timedelta(days=7)

    return {
        "weeks": weeks_data,
        "total_days": len(lines_by_date),
        "total_lines": sum(lines_by_date.values()),
        "total_updates": len(CHANGELOG),
    }


def group_changelog_by_day(entries):
    by_date = {}
    for e in entries:
        by_date.setdefault(e["date"], []).append(e)
    days = []
    for d in sorted(by_date.keys(), reverse=True):
        day_entries = by_date[d]
        days.append(
            {
                "date": d,
                "entries": day_entries,
                "count": len(day_entries),
                "total_lines": sum(e.get("lines_changed") or 0 for e in day_entries),
            }
        )
    return days


def safe_next(next_url, fallback):
    if next_url and next_url.startswith("/") and not next_url.startswith("//"):
        return next_url
    return fallback


def build_feed(conn, type_filter, status_filter, limit=60):
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
        key=lambda e: (e["date"], e.get("log_id") or e.get("id") or e.get("_seq") or 0),
        reverse=True,
    )
    return entries[:limit]


@app.route("/changelog")
def changelog():
    return render_template(
        "changelog.html",
        days=group_changelog_by_day(CHANGELOG),
        heatmap=build_changelog_heatmap(),
        today=date.today().isoformat(),
    )


@app.route("/changelog/share.png")
def changelog_share_image():
    range_ = request.args.get("range", "recent")
    if range_ == "today":
        today_str = date.today().isoformat()
        entries = [c for c in CHANGELOG if c["date"] == today_str]
        heading = f"{date.today().month}月{date.today().day}日的更新"
    else:
        range_ = "recent"
        entries = sorted(CHANGELOG, key=lambda c: c["date"], reverse=True)[:10]
        heading = "最近 10 条更新"

    buf = build_changelog_share_card(entries, heading)

    download = request.args.get("download")
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=bool(download),
        download_name=f"changelog-{range_}.png" if download else None,
    )


@app.route("/")
def index():
    type_filter = request.args.get("type", "")
    status_filter = request.args.get("status", "")

    conn = get_db()
    feed = build_feed(conn, type_filter, status_filter)
    heatmap = build_heatmap(conn)
    conn.close()

    return render_template(
        "index.html",
        feed=feed,
        statuses=STATUSES,
        type_filter=type_filter,
        status_filter=status_filter,
        heatmap=heatmap,
        moment_types=MOMENT_TYPES,
        changelog_type=CHANGELOG_TYPE,
        today=date.today().isoformat(),
    )


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
        "SELECT * FROM logs WHERE item_id = ? ORDER BY log_date DESC, id DESC", (item_id,)
    ).fetchall()
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
        current_progress=current,
        total_minutes=totals["total_minutes"],
        log_count=totals["log_count"],
        pct=pct,
        today=date.today().isoformat(),
        statuses=STATUSES,
    )


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


if __name__ == "__main__":
    app.run(debug=True, port=5050)
