import hashlib
import io
import math
import mimetypes
from datetime import date
from functools import lru_cache
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

from db import DATA_DIR

STATIC_ROOT = Path(__file__).parent / "static"
WEEKDAY_CN = ["一", "二", "三", "四", "五", "六", "日"]
COVER_CACHE_DIR = DATA_DIR / "cover_cache"

CARD_W, CARD_H = 1080, 1440
BG = (250, 248, 245)
TEXT = (43, 41, 37)
MUTED = (138, 131, 120)
ACCENT = (181, 101, 74)
ACCENT_SOFT = (241, 227, 220)
CARD_BG = (255, 255, 255)
BORDER = (232, 226, 217)
# Same green/red as .pnl-positive/.pnl-negative in style.css, kept in sync by eye.
POSITIVE_COLOR = (61, 122, 81)
NEGATIVE_COLOR = (163, 74, 61)

HEAT_COLORS = [
    (235, 231, 224),  # level 0 — no activity
    (240, 212, 200),  # level 1
    (227, 169, 140),  # level 2
    (207, 122, 84),  # level 3
    ACCENT,  # level 4
]

FONT_BOLD_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",  # macOS (local dev)
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",  # Debian/Ubuntu fonts-noto-cjk
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Songti.ttc",
]

FONT_REGULAR_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Light.ttc",  # macOS (local dev)
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Debian/Ubuntu fonts-noto-cjk
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Songti.ttc",
]


@lru_cache(maxsize=None)
def _font(size, bold=False):
    paths = FONT_BOLD_CANDIDATES if bold else FONT_REGULAR_CANDIDATES
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw, text, font, max_width):
    # PIL's textlength() can't measure a string containing a newline, so wrap each
    # user-entered line (textareas allow line breaks) separately, keeping the breaks.
    # Normalize CRLF/CR first — a stray trailing \r has no glyph and renders as a
    # tofu box, and browsers commonly submit textarea content with \r\n.
    lines = []
    for paragraph in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for ch in paragraph:
            trial = current + ch
            if draw.textlength(trial, font=font) > max_width and current:
                lines.append(current)
                current = ch
            else:
                current = trial
        if current:
            lines.append(current)
    return lines


def _fetch_cover(url):
    if not url:
        return None

    cache_key = hashlib.sha256(url.encode()).hexdigest()
    try:
        COVER_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cached = next(COVER_CACHE_DIR.glob(f"{cache_key}.*"), None)
        if cached:
            return Image.open(cached).convert("RGB")
    except Exception:
        pass

    try:
        resp = requests.get(
            url,
            timeout=6,
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.douban.com/"},
        )
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert("RGB")
        try:
            ext = mimetypes.guess_extension(resp.headers.get("Content-Type", "image/jpeg")) or ".jpg"
            (COVER_CACHE_DIR / f"{cache_key}{ext}").write_bytes(resp.content)
        except Exception:
            pass
        return img
    except Exception:
        return None


def _load_local_image(rel_path):
    if not rel_path:
        return None
    try:
        return Image.open(DATA_DIR / rel_path).convert("RGB")
    except Exception:
        return None


def _load_changelog_image(filename):
    if not filename:
        return None
    try:
        return Image.open(STATIC_ROOT / "changelog" / filename).convert("RGB")
    except Exception:
        return None


def _load_novel_media(filename):
    """Loads a novel-media file preserving its alpha channel (character concept
    art is often uploaded as transparent-background PNG); callers are responsible
    for compositing onto a background before use."""
    if not filename:
        return None
    try:
        img = Image.open(DATA_DIR / "novel_media" / filename)
        img.load()
        return img
    except Exception:
        return None


def _contain_paste(base, img, box, radius=14, bg=None):
    """Like _rounded_paste but fits the whole image inside the box (may letterbox)
    instead of cropping — used for character standees/book covers, where cropping
    could cut off the subject. Composites transparent-background images (e.g. a
    character cutout) using their own alpha channel, instead of showing black."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if bg is None:
        bg = (241, 227, 220)
    tile = Image.new("RGB", (w, h), bg)
    src_ratio = img.width / img.height
    dst_ratio = w / h
    if src_ratio > dst_ratio:
        new_w = w
        new_h = int(w / src_ratio)
    else:
        new_h = h
        new_w = int(h * src_ratio)
    resized = img.resize((max(1, new_w), max(1, new_h)))
    paste_pos = ((w - new_w) // 2, (h - new_h) // 2)
    if resized.mode in ("RGBA", "LA"):
        resized = resized.convert("RGBA")
        tile.paste(resized, paste_pos, resized)
    else:
        tile.paste(resized.convert("RGB"), paste_pos)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    base.paste(tile, (x0, y0), mask)


def _measure_draw():
    return ImageDraw.Draw(Image.new("RGB", (10, 10)))


def _rounded_paste(base, img, box, radius=18):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if img.mode in ("RGBA", "LA", "P"):
        rgba = img.convert("RGBA")
        flat = Image.new("RGB", rgba.size, BG)
        flat.paste(rgba, (0, 0), rgba)
        img = flat
    img = _cover_fit(img, w, h)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    base.paste(img, (x0, y0), mask)


def _cover_fit(img, w, h):
    src_ratio = img.width / img.height
    dst_ratio = w / h
    if src_ratio > dst_ratio:
        new_h = h
        new_w = int(h * src_ratio)
    else:
        new_w = w
        new_h = int(w / src_ratio)
    img = img.resize((new_w, new_h))
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return img.crop((left, top, left + w, top + h))


def build_share_card(item, current_progress, total_minutes, comment_text):
    card = Image.new("RGB", (CARD_W, CARD_H), BG)
    draw = ImageDraw.Draw(card)

    pad = 64
    y = pad

    # cover
    cover_w, cover_h = 320, 440
    cover_x = (CARD_W - cover_w) // 2
    cover_img = _fetch_cover(item["cover_url"])
    if cover_img:
        _rounded_paste(card, cover_img, (cover_x, y, cover_x + cover_w, y + cover_h), radius=20)
    else:
        draw.rounded_rectangle(
            [cover_x, y, cover_x + cover_w, y + cover_h], radius=20, fill=ACCENT_SOFT
        )
        placeholder_font = _font(90)
        label = "书" if item["type"] == "book" else "剧"
        bbox = draw.textbbox((0, 0), label, font=placeholder_font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            (cover_x + (cover_w - tw) / 2, y + (cover_h - th) / 2 - bbox[1]),
            label,
            font=placeholder_font,
            fill=ACCENT,
        )
    y += cover_h + 36

    # title
    title_font = _font(52, bold=True)
    title_lines = _wrap(draw, item["title"], title_font, CARD_W - pad * 2)[:2]
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        tw = bbox[2] - bbox[0]
        draw.text(((CARD_W - tw) / 2, y), line, font=title_font, fill=TEXT)
        y += (bbox[3] - bbox[1]) + 14
    y += 6

    # creator
    if item["creator"]:
        creator_font = _font(30)
        bbox = draw.textbbox((0, 0), item["creator"], font=creator_font)
        tw = bbox[2] - bbox[0]
        draw.text(((CARD_W - tw) / 2, y), item["creator"], font=creator_font, fill=MUTED)
        y += (bbox[3] - bbox[1]) + 26
    else:
        y += 10

    # status + rating pill row
    status_font = _font(28)
    status_text = f"  {item['status']}  "
    bbox = draw.textbbox((0, 0), status_text, font=status_font)
    pill_w, pill_h = bbox[2] - bbox[0] + 20, bbox[3] - bbox[1] + 24
    pill_x = (CARD_W - pill_w) // 2
    draw.rounded_rectangle(
        [pill_x, y, pill_x + pill_w, y + pill_h], radius=pill_h // 2, fill=ACCENT_SOFT
    )
    draw.text((pill_x + 10, y + 10), status_text, font=status_font, fill=ACCENT)
    y += pill_h + 24

    if item["rating"]:
        stars = "★" * item["rating"] + "☆" * (5 - item["rating"])
        star_font = _font(36)
        bbox = draw.textbbox((0, 0), stars, font=star_font)
        tw = bbox[2] - bbox[0]
        draw.text(((CARD_W - tw) / 2, y), stars, font=star_font, fill=ACCENT)
        y += (bbox[3] - bbox[1]) + 26

    # progress bar
    if item["total_units"]:
        pct = min(100, round((current_progress or 0) / item["total_units"] * 100))
        bar_w = CARD_W - pad * 2
        bar_x = pad
        bar_h = 16
        draw.rounded_rectangle([bar_x, y, bar_x + bar_w, y + bar_h], radius=8, fill=ACCENT_SOFT)
        fill_w = int(bar_w * pct / 100)
        if fill_w > 0:
            draw.rounded_rectangle([bar_x, y, bar_x + fill_w, y + bar_h], radius=8, fill=ACCENT)
        y += bar_h + 14
        progress_font = _font(26)
        progress_text = f"{current_progress:g} / {item['total_units']} {item['unit_label']}（{pct}%）"
        bbox = draw.textbbox((0, 0), progress_text, font=progress_font)
        tw = bbox[2] - bbox[0]
        draw.text(((CARD_W - tw) / 2, y), progress_text, font=progress_font, fill=MUTED)
        y += (bbox[3] - bbox[1]) + 30

    # comment card
    if comment_text:
        box_x0, box_x1 = pad, CARD_W - pad
        comment_font = _font(30)
        inner_pad = 28
        lines = _wrap(draw, comment_text, comment_font, box_x1 - box_x0 - inner_pad * 2)[:5]
        line_h = 44
        box_h = inner_pad * 2 + line_h * len(lines)
        draw.rounded_rectangle([box_x0, y, box_x1, y + box_h], radius=18, fill=CARD_BG, outline=BORDER, width=2)
        ty = y + inner_pad
        for line in lines:
            draw.text((box_x0 + inner_pad, ty), line, font=comment_font, fill=TEXT)
            ty += line_h
        y += box_h + 30

    # footer stats
    footer_font = _font(26)
    footer_text = f"共用时 {total_minutes} 分钟"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((CARD_W - tw) / 2, CARD_H - 120), footer_text, font=footer_font, fill=MUTED)

    watermark_font = _font(24)
    watermark = f"知行合一AI实验室 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=watermark_font)
    tw = bbox[2] - bbox[0]
    draw.text(((CARD_W - tw) / 2, CARD_H - 70), watermark, font=watermark_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


def _build_log_card(measure, col_w, log):
    body_font = _font(27)
    meta_font = _font(23)
    inner_pad = 16
    thumb_w, thumb_h = 84, 112
    text_w = col_w - inner_pad * 2 - thumb_w - 14

    type_label = "剧" if log.get("item_type") == "show" else "书"
    title_lines = _wrap(measure, f"【{type_label}】{log.get('item_title', '')}", body_font, text_w)[:2]

    meta = f"用时 {log.get('minutes_spent', 0)} 分钟"
    if log.get("progress_at") is not None:
        meta += f" · {log['progress_at']:g}{log.get('item_unit_label') or ''}"
    meta_lines = _wrap(measure, meta, meta_font, text_w)[:2]

    comment = (log.get("comment") or "").strip()
    comment_lines = _wrap(measure, comment, meta_font, text_w)[:3] if comment else []

    text_h = len(title_lines) * 34 + len(meta_lines) * 30 + len(comment_lines) * 30
    height = inner_pad * 2 + max(thumb_h, text_h)

    def draw_fn(card, draw, x, y):
        draw.rounded_rectangle(
            [x, y, x + col_w, y + height], radius=16, fill=CARD_BG, outline=BORDER, width=2
        )
        tx, ty = x + inner_pad, y + inner_pad
        cover_img = _fetch_cover(log.get("item_cover_url"))
        if cover_img:
            _rounded_paste(card, cover_img, (tx, ty, tx + thumb_w, ty + thumb_h), radius=10)
        else:
            draw.rounded_rectangle([tx, ty, tx + thumb_w, ty + thumb_h], radius=10, fill=ACCENT_SOFT)

        tx2 = tx + thumb_w + 14
        ty2 = y + inner_pad
        for line in title_lines:
            draw.text((tx2, ty2), line, font=body_font, fill=TEXT)
            ty2 += 34
        for line in meta_lines:
            draw.text((tx2, ty2), line, font=meta_font, fill=MUTED)
            ty2 += 30
        for line in comment_lines:
            draw.text((tx2, ty2), line, font=meta_font, fill=TEXT)
            ty2 += 30

    return height, draw_fn


def _build_moment_card(measure, col_w, m, moment_types):
    body_font = _font(27)
    inner_pad = 18
    text_w = col_w - inner_pad * 2

    mtype = moment_types.get(m["type"], {"label": m["type"]})
    header_text = f"【{mtype['label']}】"
    if m.get("title"):
        header_text += f" {m['title']}"
    header_lines = _wrap(measure, header_text, body_font, text_w)[:2]

    content = (m.get("content") or "").strip()
    content_lines = _wrap(measure, content, body_font, text_w)[:5] if content else []

    thumb = None
    thumb_h = 0
    if m.get("image_path"):
        img = _load_local_image(m["image_path"])
        if img:
            thumb_h = int(col_w * 0.75)
            thumb = _cover_fit(img, text_w, thumb_h)

    height = (
        inner_pad * 2
        + len(header_lines) * 38
        + len(content_lines) * 36
        + (thumb_h + 14 if thumb else 0)
    )

    def draw_fn(card, draw, x, y):
        draw.rounded_rectangle(
            [x, y, x + col_w, y + height], radius=16, fill=CARD_BG, outline=BORDER, width=2
        )
        iy = y + inner_pad
        for line in header_lines:
            draw.text((x + inner_pad, iy), line, font=body_font, fill=ACCENT)
            iy += 38
        for line in content_lines:
            draw.text((x + inner_pad, iy), line, font=body_font, fill=TEXT)
            iy += 36
        if thumb:
            iy += 6
            card.paste(thumb, (x + inner_pad, iy))

    return height, draw_fn


def build_day_share_card(day, logs, moments, moment_types):
    W = 1080
    pad = 48
    gap = 20
    columns = 2
    col_w = (W - pad * 2 - gap * (columns - 1)) // columns
    measure = _measure_draw()

    title_font = _font(52, bold=True)
    subtitle_font = _font(28)
    empty_font = _font(30)
    footer_font = _font(24)

    total_minutes = sum(item.get("minutes_spent") or 0 for item in logs) + sum(
        item.get("minutes_spent") or 0 for item in moments
    )
    activity_count = len(logs) + len(moments)

    date_label = f"{day.month}月{day.day}日 星期{WEEKDAY_CN[day.weekday()]}"

    header_h = pad + 66 + 42 + 24
    footer_h = 70

    entries = []
    for log in logs:
        entries.append(_build_log_card(measure, col_w, log))
    for m in moments:
        entries.append(_build_moment_card(measure, col_w, m, moment_types))

    if not entries:
        H = header_h + 90 + footer_h
        card = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(card)
        draw.text((pad, header_h), "这一天还没有记录，去添加点什么吧", font=empty_font, fill=MUTED)
    else:
        col_heights = [0] * columns
        placements = []  # (draw_fn, x, y)
        for height, draw_fn in entries:
            c = col_heights.index(min(col_heights))
            x = pad + c * (col_w + gap)
            y = header_h + col_heights[c]
            placements.append((draw_fn, x, y))
            col_heights[c] += height + gap

        H = header_h + max(col_heights) + footer_h
        card = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(card)
        for draw_fn, x, y in placements:
            draw_fn(card, draw, x, y)

    draw.text((pad, pad), date_label, font=title_font, fill=TEXT)
    draw.text(
        (pad, pad + 66),
        f"共记录 {activity_count} 项 · 用时 {total_minutes} 分钟",
        font=subtitle_font,
        fill=MUTED,
    )

    watermark = f"知行合一AI实验室 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


def _draw_mini_heatmap(draw, x, y, heatmap):
    cell = 10
    gap = 2
    step = cell + gap
    month_font = _font(18)

    for wi, week in enumerate(heatmap["weeks"]):
        cx = x + wi * step
        if week["month_label"]:
            draw.text((cx, y - 20), week["month_label"], font=month_font, fill=MUTED)
        for di, day in enumerate(week["days"]):
            if day["level"] == -1:
                continue
            cy = y + di * step
            color = HEAT_COLORS[max(0, min(4, day["level"]))]
            draw.rounded_rectangle([cx, cy, cx + cell, cy + cell], radius=2, fill=color)

    grid_width = len(heatmap["weeks"]) * step - gap
    grid_height = 7 * step - gap
    return grid_width, grid_height


CHANGELOG_DEFAULT_STRINGS = {
    "empty": "这段时间还没有更新记录",
    "count_label": "共 {count} 条更新",
    "watermark": "知行合一AI实验室 开发日志",
}


def _build_changelog_card(measure, col_w, e):
    entry_title_font = _font(28, bold=True)
    date_font = _font(22)
    body_font = _font(24)
    inner_pad = 16
    thumb_w, thumb_h = 92, 92

    text_w = col_w - inner_pad * 2 - (thumb_w + 14 if e.get("image") else 0)
    title_lines = _wrap(measure, e["title"], entry_title_font, text_w)[:2]
    summary_lines = _wrap(measure, e["summary"], body_font, text_w)[:4]

    text_h = 28 + len(title_lines) * 34 + len(summary_lines) * 30
    thumb_col_h = thumb_h if e.get("image") else 0
    height = inner_pad * 2 + max(thumb_col_h, text_h)

    def draw_fn(card, draw, x, y):
        draw.rounded_rectangle(
            [x, y, x + col_w, y + height], radius=16, fill=CARD_BG, outline=BORDER, width=2
        )
        tx2 = x + inner_pad
        if e.get("image"):
            img = _load_changelog_image(e["image"])
            ty = y + inner_pad
            if img:
                thumb = _cover_fit(img, thumb_w, thumb_h)
                _rounded_paste(card, thumb, (tx2, ty, tx2 + thumb_w, ty + thumb_h), radius=10)
            else:
                draw.rounded_rectangle([tx2, ty, tx2 + thumb_w, ty + thumb_h], radius=10, fill=ACCENT_SOFT)
            tx2 += thumb_w + 14

        ty2 = y + inner_pad
        draw.text((tx2, ty2), e["date"], font=date_font, fill=ACCENT)
        ty2 += 28
        for line in title_lines:
            draw.text((tx2, ty2), line, font=entry_title_font, fill=TEXT)
            ty2 += 34
        for line in summary_lines:
            draw.text((tx2, ty2), line, font=body_font, fill=MUTED)
            ty2 += 30

    return height, draw_fn


def build_changelog_share_card(entries, heading, heatmap=None, t=None):
    t = {**CHANGELOG_DEFAULT_STRINGS, **(t or {})}
    W = 1080
    pad = 48
    gap = 20
    columns = 2
    col_w = (W - pad * 2 - gap * (columns - 1)) // columns
    measure = _measure_draw()

    title_font = _font(50, bold=True)
    subtitle_font = _font(28)
    empty_font = _font(30)
    footer_font = _font(24)

    heatmap_top = pad + 64 + 40 + 30
    heatmap_h = 34 + (7 * 12 - 2) + 20 if heatmap else 0
    header_h = heatmap_top + heatmap_h
    footer_h = 70

    blocks = [_build_changelog_card(measure, col_w, e) for e in entries]

    if not blocks:
        H = header_h + 90 + footer_h
        card = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(card)
        draw.text((pad, header_h), t["empty"], font=empty_font, fill=MUTED)
    else:
        col_heights = [0] * columns
        placements = []
        for height, draw_fn in blocks:
            c = col_heights.index(min(col_heights))
            x = pad + c * (col_w + gap)
            y = header_h + col_heights[c]
            placements.append((draw_fn, x, y))
            col_heights[c] += height + gap

        H = header_h + max(col_heights) + footer_h
        card = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(card)
        for draw_fn, x, y in placements:
            draw_fn(card, draw, x, y)

    draw.text((pad, pad), heading, font=title_font, fill=TEXT)
    count_text = t["count_label"].format(count=len(entries)) if entries else t["empty"]
    draw.text((pad, pad + 64), count_text, font=subtitle_font, fill=MUTED)

    if heatmap:
        _draw_mini_heatmap(draw, pad, heatmap_top + 24, heatmap)

    watermark = f"{t['watermark']} · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


NOVEL_MAX_CHAPTERS = 12
NOVEL_MAX_REFERENCES = 10
SECTION_HEADING_H = 66  # height consumed by _section_heading before section content starts


def _section_heading(draw, text, x, y, w):
    font = _font(32, bold=True)
    draw.text((x, y), text, font=font, fill=TEXT)
    line_y = y + 44
    draw.line([(x, line_y), (x + w, line_y)], fill=BORDER, width=2)
    return line_y + 22


def _build_novel_header(measure, w, novel, total_words):
    cover_w, cover_h = 292, 389  # fills the full content width (no side margin)
    title_font = _font(46, bold=True)
    status_font = _font(26)

    title_lines = _wrap(measure, novel["title"], title_font, w - 40)[:2]

    h = cover_h + 26
    h += len(title_lines) * 58 + 10
    h += 64

    def draw_fn(card, draw, x0, y0):
        y = y0
        cover_x = x0 + (w - cover_w) // 2
        cover_img = _load_novel_media(novel["cover_image"])
        if cover_img:
            _rounded_paste(card, cover_img, (cover_x, y, cover_x + cover_w, y + cover_h), radius=20)
        else:
            draw.rounded_rectangle([cover_x, y, cover_x + cover_w, y + cover_h], radius=20, fill=ACCENT_SOFT)
            label_font = _font(90)
            bbox = draw.textbbox((0, 0), "小说", font=label_font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(
                (cover_x + (cover_w - tw) / 2, y + (cover_h - th) / 2 - bbox[1]),
                "小说", font=label_font, fill=ACCENT,
            )
        y += cover_h + 26

        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            tw = bbox[2] - bbox[0]
            draw.text((x0 + (w - tw) / 2, y), line, font=title_font, fill=TEXT)
            y += 58
        y += 10

        status_text = f"  {novel['status']}  "
        word_text = f"  共 {total_words} 字  "
        status_font_bbox = draw.textbbox((0, 0), status_text, font=status_font)
        word_font_bbox = draw.textbbox((0, 0), word_text, font=status_font)
        pill_gap = 16
        status_pill_w = status_font_bbox[2] - status_font_bbox[0] + 20
        word_pill_w = word_font_bbox[2] - word_font_bbox[0] + 20
        pill_h = status_font_bbox[3] - status_font_bbox[1] + 24
        total_w = status_pill_w + pill_gap + word_pill_w
        pill_x = x0 + (w - total_w) / 2
        draw.rounded_rectangle([pill_x, y, pill_x + status_pill_w, y + pill_h], radius=pill_h // 2, fill=ACCENT_SOFT)
        draw.text((pill_x + 10, y + 10), status_text, font=status_font, fill=ACCENT)
        word_pill_x = pill_x + status_pill_w + pill_gap
        draw.rounded_rectangle([word_pill_x, y, word_pill_x + word_pill_w, y + pill_h], radius=pill_h // 2, fill=ACCENT_SOFT)
        draw.text((word_pill_x + 10, y + 10), word_text, font=status_font, fill=ACCENT)

    return h, draw_fn


def _group_chapters_by_volume(chapters):
    """Same bucketing as app.py's group_chapters_by_volume (adjacent chapters
    sharing a volume_id become one group) — duplicated locally rather than
    imported, since share_card.py is imported by app.py, not the other way."""
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


def _build_chapter_list(measure, w, chapters):
    shown = chapters[:NOVEL_MAX_CHAPTERS]
    extra = len(chapters) - len(shown)
    columns = 2
    col_w = (w - 30) // columns
    row_h = 42
    sub_h = 40
    has_volumes = any(c["volume_id"] for c in chapters)
    groups = _group_chapters_by_volume(shown)

    body_h = 0
    for g in groups:
        if g["volume_id"] or has_volumes:
            body_h += sub_h
        body_h += -(-len(g["chapters"]) // columns) * row_h

    h = SECTION_HEADING_H + body_h
    if extra > 0:
        h += 36

    def draw_fn(card, draw, x0, y0):
        y = _section_heading(draw, f"章节目录（共 {len(chapters)} 章）", x0, y0, w)
        item_font = _font(26)
        sub_font = _font(22, bold=True)
        for g in groups:
            if g["volume_id"]:
                draw.text((x0, y), f"第{g['volume_no']}卷 · {g['volume_title']}", font=sub_font, fill=ACCENT)
                y += sub_h
            elif has_volumes:
                draw.text((x0, y), "未分卷", font=sub_font, fill=MUTED)
                y += sub_h
            for i, c in enumerate(g["chapters"]):
                col, row = i % columns, i // columns
                tx = x0 + col * (col_w + 30)
                ty = y + row * row_h
                label = f"第{c['chapter_no']}章 · {c['title']}"
                line = _wrap(measure, label, item_font, col_w)[:1]
                text = (line[0] + "…") if line and len(line[0]) < len(label) else label
                draw.text((tx, ty), text, font=item_font, fill=TEXT)
            y += -(-len(g["chapters"]) // columns) * row_h
        if extra > 0:
            draw.text((x0, y), f"还有 {extra} 章…", font=_font(24), fill=MUTED)

    return h, draw_fn


def _build_reference_row(measure, w, references):
    shown = references[:NOVEL_MAX_REFERENCES]
    extra = len(references) - len(shown)
    tile_w, tile_h, name_h, gap = 140, 187, 34, 20
    per_row = max(1, (w + gap) // (tile_w + gap))
    rows = -(-len(shown) // per_row) if shown else 0
    h = SECTION_HEADING_H + rows * (tile_h + name_h + gap)
    if extra > 0:
        h += 36

    def draw_fn(card, draw, x0, y0):
        y = _section_heading(draw, "参考书目", x0, y0, w)
        name_font = _font(20)
        for i, ref in enumerate(shown):
            col, row = i % per_row, i // per_row
            tx = x0 + col * (tile_w + gap)
            ty = y + row * (tile_h + name_h + gap)
            img = _fetch_cover(ref["cover_url"])
            if img:
                _rounded_paste(card, img, (tx, ty, tx + tile_w, ty + tile_h), radius=10)
            else:
                draw.rounded_rectangle([tx, ty, tx + tile_w, ty + tile_h], radius=10, fill=ACCENT_SOFT)
            name_lines = _wrap(measure, ref["title"], name_font, tile_w)[:1]
            if name_lines:
                bbox = draw.textbbox((0, 0), name_lines[0], font=name_font)
                tw = bbox[2] - bbox[0]
                draw.text((tx + (tile_w - tw) / 2, ty + tile_h + 8), name_lines[0], font=name_font, fill=MUTED)
        if extra > 0:
            extra_y = y + rows * (tile_h + name_h + gap)
            draw.text((x0, extra_y), f"还有 {extra} 本…", font=_font(24), fill=MUTED)

    return h, draw_fn


def build_chapter_share_card(novel, chapter, blocks=None, unmatched_routes=None):
    """blocks: the same {"type": "text"/"route", ...} list build_chapter_blocks()
    produces (pass None to fall back to plain paragraph splitting, no route
    art -- kept for callers that don't have blocks handy). Any route block --
    whether it's inline because its title showed up in the text, or tacked on
    via unmatched_routes because it's attached to the chapter but never
    mentioned by name -- gets its own outline share image (built the same way
    a standalone route share does, city labels and all) scaled down to the
    card's content width and pasted in, so the shape of the trip shows up
    right in the chapter screenshot instead of only being a click-through link
    on the live page."""
    W = 1080
    pad = 64
    content_w = W - pad * 2
    measure = _measure_draw()

    novel_title_font = _font(28)
    chapter_title_font = _font(44, bold=True)
    body_font = _font(30)
    footer_font = _font(24)

    line_h = 46
    para_gap = 18
    route_gap = 26

    novel_title_lines = _wrap(measure, novel["title"], novel_title_font, content_w)[:1]
    chapter_label = f"第 {chapter['chapter_no']} 章 · {chapter['title']}"
    chapter_title_lines = _wrap(measure, chapter_label, chapter_title_font, content_w)

    if blocks is None:
        paragraphs = [p for p in chapter["content"].replace("\r\n", "\n").replace("\r", "\n").split("\n") if p.strip()]
        blocks = [{"type": "text", "text": p} for p in paragraphs]

    def route_image(route):
        img = Image.open(build_route_outline_card(route["title"], route["points"])).convert("RGB")
        scale = content_w / img.width
        return img.resize((content_w, round(img.height * scale)), Image.LANCZOS)

    # First pass: turn each block into something with a known height, so the
    # canvas can be sized before anything is actually drawn.
    prepared = []
    for block in blocks:
        if block["type"] == "text":
            lines = _wrap(measure, block["text"], body_font, content_w)
            prepared.append(("text", lines, len(lines) * line_h + para_gap))
        elif block["type"] == "route":
            img = route_image(block["route"])
            prepared.append(("route", img, img.height + route_gap))
    for route in (unmatched_routes or []):
        img = route_image(route)
        prepared.append(("route", img, img.height + route_gap))

    header_h = 0
    if novel_title_lines:
        header_h += len(novel_title_lines) * 38 + 12
    header_h += len(chapter_title_lines) * 58 + 30  # includes divider + gap below title

    body_h = sum(h for _, _, h in prepared)

    footer_h = 70
    H = pad + header_h + body_h + footer_h + pad

    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    y = pad
    for line in novel_title_lines:
        draw.text((pad, y), f"《{line}》", font=novel_title_font, fill=MUTED)
        y += 38
    y += 12
    for line in chapter_title_lines:
        draw.text((pad, y), line, font=chapter_title_font, fill=TEXT)
        y += 58
    y += 6
    draw.line([(pad, y), (W - pad, y)], fill=BORDER, width=2)
    y += 24

    for kind, payload, h in prepared:
        if kind == "text":
            for line in payload:
                draw.text((pad, y), line, font=body_font, fill=TEXT)
                y += line_h
            y += para_gap
        else:
            card.paste(payload, (pad, y))
            y += h

    watermark = f"知行合一AI实验室 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


def build_novel_share_card(novel, chapters, references, total_words=0):
    W = 1080
    pad = 64
    section_gap = 40
    content_w = W - pad * 2
    measure = _measure_draw()

    sections = []
    header_h, header_draw = _build_novel_header(measure, content_w, novel, total_words)
    sections.append((header_h, header_draw))

    if chapters:
        sections.append(_build_chapter_list(measure, content_w, chapters))
    if references:
        sections.append(_build_reference_row(measure, content_w, references))

    footer_h = 70
    H = pad + sum(h for h, _ in sections) + section_gap * (len(sections) - 1) + footer_h + pad

    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    y = pad
    for h, draw_fn in sections:
        draw_fn(card, draw, pad, y)
        y += h + section_gap

    footer_font = _font(24)
    watermark = f"知行合一AI实验室 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


def build_trading_share_card(series, stats, trade_stats=None, open_positions=None):
    """series: list of {"date","pnl","cumulative"} from trading.build_cumulative_series.
    stats: dict from trading.summarize_daily_pnl (by-day win/loss counts,
    win rate, win/loss ratio). trade_stats: dict from trading.summarize_trades
    (the same three stats, but per closing trade instead of per day -- the
    two often disagree, same as the "按天统计"/"按笔统计" cards on the page,
    so both get their own line here). Like the expense bar card, this
    deliberately omits every dollar figure -- just the title, the shape of
    the curve, date labels, and these non-monetary ratios/counts.

    open_positions: optional -- pass match_meta["open_position_list"] to add
    a "目前持仓" section listing each open symbol with its opened date. Only
    those two fields are drawn, never quantity or cost (still no dollar
    figures, and position size is arguably even more sensitive than a P&L
    ratio). Opt-in only: omit or pass None/[] to leave this off entirely,
    same as before this was added."""
    W = 1080
    pad = 64
    header_h = 244
    chart_h = 560
    footer_h = 70

    # chart_top + chart_h + 12 is where the chart's own date-axis labels sit
    # (see below); this section has to clear well past that before it starts
    # drawing anything, or the two overlap.
    positions_axis_clearance = 70
    positions_title_to_rows = 50
    positions_row_h = 40
    positions_h = (
        (positions_axis_clearance + positions_title_to_rows + len(open_positions) * positions_row_h + 24)
        if open_positions else 0
    )

    H = header_h + chart_h + positions_h + footer_h + pad

    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    title_font = _font(52, bold=True)
    subtitle_font = _font(28)

    draw.text((pad, pad), "累计盈亏走势", font=title_font, fill=TEXT)

    day_line = f"按天：{stats.get('win_days', 0)} 盈利日 · {stats.get('loss_days', 0)} 亏损日"
    win_rate = stats.get("win_rate")
    if win_rate is not None:
        day_line += f" · 胜率 {win_rate * 100:.1f}%"
    ratio = stats.get("win_loss_ratio")
    if ratio is not None:
        day_line += f" · 盈亏比 {ratio:.2f} : 1"
    draw.text((pad, pad + 74), day_line, font=subtitle_font, fill=MUTED)

    if trade_stats is not None:
        trade_line = f"按笔：{trade_stats.get('win_trades', 0)} 盈利笔 · {trade_stats.get('loss_trades', 0)} 亏损笔"
        t_win_rate = trade_stats.get("win_rate")
        if t_win_rate is not None:
            trade_line += f" · 胜率 {t_win_rate * 100:.1f}%"
        t_ratio = trade_stats.get("win_loss_ratio")
        if t_ratio is not None:
            trade_line += f" · 盈亏比 {t_ratio:.2f} : 1"
        draw.text((pad, pad + 112), trade_line, font=subtitle_font, fill=MUTED)

    chart_top = header_h
    chart_left = pad
    chart_right = W - pad

    if series:
        values = [p["cumulative"] for p in series]
        min_v = min(values + [0])
        max_v = max(values + [0])
        span = (max_v - min_v) or 1
        n = len(series)

        def x_for(i):
            return chart_left + (chart_right - chart_left) * i / (n - 1) if n > 1 else (chart_left + chart_right) / 2

        def y_for(v):
            return chart_top + chart_h * (1 - (v - min_v) / span)

        zero_y = y_for(0)
        draw.line([(chart_left, zero_y), (chart_right, zero_y)], fill=BORDER, width=2)

        points = [(x_for(i), y_for(p["cumulative"])) for i, p in enumerate(series)]
        line_color = POSITIVE_COLOR if values[-1] >= 0 else NEGATIVE_COLOR
        if len(points) > 1:
            draw.line(points, fill=line_color, width=5, joint="curve")
        last_x, last_y = points[-1]
        r = 9
        draw.ellipse([last_x - r, last_y - r, last_x + r, last_y + r], fill=line_color)

        label_font = _font(22)
        idxs = sorted(set([0, n - 1] + [n * k // 4 for k in (1, 2, 3)])) if n > 1 else [0]
        for i in idxs:
            label = series[i]["date"][5:]
            x = points[i][0]
            bbox = draw.textbbox((0, 0), label, font=label_font)
            tw = bbox[2] - bbox[0]
            draw.text((x - tw / 2, chart_top + chart_h + 12), label, font=label_font, fill=MUTED)
    else:
        empty_font = _font(30)
        draw.text((pad, chart_top + chart_h / 2 - 15), "还没有交易记录", font=empty_font, fill=MUTED)

    if open_positions:
        section_top = chart_top + chart_h + positions_axis_clearance
        positions_title_font = _font(30, bold=True)
        draw.text((pad, section_top), "目前持仓", font=positions_title_font, fill=TEXT)
        row_font = _font(24)
        rows_top = section_top + positions_title_to_rows
        for i, pos in enumerate(open_positions):
            y = rows_top + i * positions_row_h
            draw.text((pad, y), pos["symbol"], font=row_font, fill=TEXT)
            date_label = pos.get("opened_date", "")
            bbox = draw.textbbox((0, 0), date_label, font=row_font)
            tw = bbox[2] - bbox[0]
            draw.text((W - pad - tw, y), date_label, font=row_font, fill=MUTED)

    footer_font = _font(24)
    watermark = f"知行合一AI实验室 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


def build_expense_bar_share_card(year, year_bar_chart):
    """year_bar_chart: dict from bank.build_year_bar_chart. Dollar value labels
    are deliberately left off this card -- it's meant to be shareable without
    revealing exact spending figures, just the shape of the year's spending
    month to month (which the caller asked for explicitly)."""
    W = 1080
    pad = 64
    header_h = 130
    chart_h = 560
    footer_h = 70
    H = header_h + chart_h + footer_h + pad

    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    title_font = _font(52, bold=True)
    draw.text((pad, pad), f"{year} 年消费", font=title_font, fill=TEXT)

    chart_top = header_h
    hscale = (W - pad * 2) / year_bar_chart["width"]
    vscale = chart_h / year_bar_chart["height"]
    label_font = _font(24)

    zero_y = chart_top + year_bar_chart["zero_y"] * vscale
    draw.line([(pad, zero_y), (W - pad, zero_y)], fill=BORDER, width=2)

    for bar in year_bar_chart["bars"]:
        x = pad + bar["x"] * hscale
        w = bar["width"] * hscale
        if bar["value"] is not None and bar["height"] > 0:
            y = chart_top + bar["y"] * vscale
            h = max(bar["height"] * vscale, 3)
            color = NEGATIVE_COLOR if bar["is_cost"] else POSITIVE_COLOR
            draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=color)
        bbox = draw.textbbox((0, 0), bar["label"], font=label_font)
        tw = bbox[2] - bbox[0]
        draw.text((x + w / 2 - tw / 2, chart_top + chart_h + 12), bar["label"], font=label_font, fill=MUTED)

    footer_font = _font(24)
    watermark = f"知行合一AI实验室 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


def build_showcase_card(features):
    """A poster-style card introducing the app's main features, for the user
    to share when showing the site to someone else. `features` is a list of
    (title, description) pairs. Unlike the data cards above there are no
    numbers to hide here -- it's just marketing copy -- so nothing is
    omitted. Emoji are deliberately left out of the drawn text (unlike the
    HTML page, which uses them freely): the CJK fonts this module falls back
    to don't carry color emoji glyphs and would render them as blank boxes,
    so numbered badges stand in for icons instead."""
    W = 1080
    pad = 64
    header_h = 210
    row_h = 190
    footer_h = 90
    H = header_h + row_h * len(features) + footer_h

    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    title_font = _font(56, bold=True)
    subtitle_font = _font(28)
    draw.text((pad, pad), "知行合一AI实验室", font=title_font, fill=TEXT)
    draw.text((pad, pad + 74), "交易 · 消费 · 创作 · 生活点滴，都在这一个地方", font=subtitle_font, fill=MUTED)
    draw.line([(pad, header_h - 20), (W - pad, header_h - 20)], fill=BORDER, width=2)

    badge_r = 34
    title_font2 = _font(34, bold=True)
    desc_font = _font(24)
    num_font = _font(30, bold=True)

    for i, (title, desc) in enumerate(features):
        y0 = header_h + i * row_h
        cy = y0 + row_h / 2
        cx = pad + badge_r
        draw.ellipse([cx - badge_r, cy - badge_r, cx + badge_r, cy + badge_r], fill=ACCENT_SOFT)
        num = str(i + 1)
        bbox = draw.textbbox((0, 0), num, font=num_font)
        nw, nh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - nw / 2 - bbox[0], cy - nh / 2 - bbox[1]), num, font=num_font, fill=ACCENT)

        text_x = pad + badge_r * 2 + 32
        draw.text((text_x, cy - 40), title, font=title_font2, fill=TEXT)
        for j, line in enumerate(_wrap(draw, desc, desc_font, W - pad - text_x)):
            draw.text((text_x, cy + 4 + j * 32), line, font=desc_font, fill=MUTED)

        if i < len(features) - 1:
            draw.line([(pad, y0 + row_h), (W - pad, y0 + row_h)], fill=BORDER, width=1)

    footer_font = _font(24)
    watermark = f"知行合一AI实验室 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 56), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


ROUTE_MAP_STYLES = {
    "standard": {
        "url_template": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "attribution": "地图数据 © OpenStreetMap 贡献者",
    },
    "terrain": {
        # staticmap's url_template only substitutes {z}/{x}/{y} (plain
        # str.format) -- unlike Leaflet, it has no {s} subdomain rotation,
        # so a fixed single subdomain is used here instead of route-map.js's
        # {s} version. Fine for a one-off server-side render (no need for
        # a browser's multi-subdomain parallel tile loading).
        "url_template": "https://a.tile.opentopomap.org/{z}/{x}/{y}.png",
        "attribution": "地图数据 © OpenStreetMap 贡献者、SRTM · 样式 © OpenTopoMap (CC-BY-SA)",
    },
}


def build_route_share_card(title, points, style="standard"):
    """points: list of {"lat":, "lng":} dicts (already validated -- see
    app.py's _parse_route_points). style: "standard" or "terrain", matching
    the two base layers on the interactive map (see route-map.js) -- picks
    which tile source staticmap renders from. Unlike every other card in
    this file, which draws its own abstract chart, this one renders the
    actual OSM/OpenTopoMap basemap via the `staticmap` library (pure
    Python, Pillow-based -- fetches real map tiles over the network) with
    the route drawn on top, then composes that onto a branded card matching
    the rest of this module's look."""
    from staticmap import CircleMarker, Line, StaticMap

    style_info = ROUTE_MAP_STYLES.get(style, ROUTE_MAP_STYLES["standard"])

    W = 1080
    pad = 48
    header_h = 100
    map_w = W - pad * 2
    map_h = 760
    attribution_h = 28
    footer_h = 70
    H = header_h + map_h + attribution_h + footer_h + pad

    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    title_font = _font(44, bold=True)
    draw.text((pad, pad - 10), title or "我的路线", font=title_font, fill=TEXT)

    if points:
        m = StaticMap(
            map_w, map_h, padding_x=30, padding_y=30,
            url_template=style_info["url_template"],
            headers={"User-Agent": "zhixingheyi-app/1.0 (+personal project, contact via GitHub issues)"},
        )
        coords = [(p["lng"], p["lat"]) for p in points]  # staticmap wants (lon, lat)
        # White casing drawn first (staticmap draws lines/markers in the
        # order added, later on top) so the accent brown line and markers
        # don't disappear into terrain style's brown hillshading.
        if len(coords) >= 2:
            m.add_line(Line(coords, "#ffffff", 8))
            m.add_line(Line(coords, "#b5654a", 5))
        m.add_marker(CircleMarker(coords[0], "#ffffff", 16))
        m.add_marker(CircleMarker(coords[0], "#3d7a51", 12))
        if len(coords) >= 2:
            m.add_marker(CircleMarker(coords[-1], "#ffffff", 16))
            m.add_marker(CircleMarker(coords[-1], "#a34a3d", 12))
        map_img = m.render()
        card.paste(map_img, (pad, header_h))
    else:
        empty_font = _font(28)
        draw.text((pad, header_h + map_h / 2 - 15), "这条路线还没有点", font=empty_font, fill=MUTED)

    attribution_font = _font(18)
    draw.text((pad, header_h + map_h + 6), style_info["attribution"], font=attribution_font, fill=MUTED)

    footer_font = _font(24)
    watermark = f"知行合一AI实验室 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


def build_route_outline_card(title, points):
    """Like build_route_share_card, but with no real map tiles at all --
    just the route's own shape (points projected with a simple
    latitude-corrected equirectangular scale, not a real map projection)
    connected in order, with each named point's city label drawn next to
    it. For when the shape and the sequence of places matter more than the
    surrounding geography -- faster too, since there's no tile fetching.

    Sized well beyond the usual 1080-wide share card -- the whole route's
    extent gets fit into this canvas at one uniform scale, so a route
    spanning a long distance with a tight local cluster of points (a few
    cities close together early in a long trip, say) leaves that cluster
    only a handful of pixels across no matter how good the label placement
    is. A bigger canvas gives every degree more pixels to work with, which
    is what actually helps."""
    W = 1500
    pad = 64
    header_h = 110
    plot_h = 1000
    footer_h = 70
    H = header_h + plot_h + footer_h + pad

    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    title_font = _font(44, bold=True)
    draw.text((pad, pad - 10), title or "我的路线", font=title_font, fill=TEXT)

    plot_top = header_h
    plot_left = pad
    plot_right = W - pad
    plot_bottom = plot_top + plot_h

    if points:
        lats = [p["lat"] for p in points]
        lngs = [p["lng"] for p in points]
        lat_min, lat_max = min(lats), max(lats)
        lng_min, lng_max = min(lngs), max(lngs)
        lat_mid = (lat_min + lat_max) / 2
        lng_mid = (lng_min + lng_max) / 2
        # cos(latitude) keeps longitude degrees from looking stretched
        # relative to latitude degrees at higher latitudes -- a common
        # simple correction, not a real map projection.
        lon_scale = math.cos(math.radians(lat_mid)) or 0.01
        span_x = (lng_max - lng_min) * lon_scale or 0.001
        span_y = (lat_max - lat_min) or 0.001

        margin = 90  # room for point labels near the plot edges
        avail_w = (plot_right - plot_left) - margin * 2
        avail_h = plot_h - margin * 2
        scale = min(avail_w / span_x, avail_h / span_y)
        cx = (plot_left + plot_right) / 2
        cy = plot_top + plot_h / 2

        def project(p):
            x = cx + (p["lng"] - lng_mid) * lon_scale * scale
            y = cy - (p["lat"] - lat_mid) * scale  # north is up
            return x, y

        def boxes_overlap(a, b):
            return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]

        def segment_hits_box(p1, p2, box):
            # Sampled rather than solved exactly (segment/rectangle
            # intersection has enough edge cases to get wrong) -- cheap
            # enough at a route's scale, and the label boxes are small
            # relative to a 4px sampling step, so nothing slips through.
            x1, y1 = p1
            x2, y2 = p2
            steps = max(1, int(math.hypot(x2 - x1, y2 - y1) / 4))
            for i in range(steps + 1):
                t = i / steps
                x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
                if box[0] <= x <= box[2] and box[1] <= y <= box[3]:
                    return True
            return False

        coords = [project(p) for p in points]
        line_segments = list(zip(coords, coords[1:]))

        # Try a ring of candidate positions around a point for a label,
        # widening the ring each pass, and return the first spot that
        # doesn't collide with anything already placed *and* doesn't sit on
        # top of the route line itself (a label's opaque background would
        # otherwise paper over whatever line segment happened to run under
        # it). Straight-below at the smallest radius is tried first, so an
        # isolated point's label looks exactly like the old fixed placement
        # -- only a point with something already nearby, or the line
        # itself, gets pushed outward. needs_leader is False only for that
        # first straight-below case, so the caller knows when a connector
        # line back to the point is needed to keep the label legible as
        # belonging to it.
        label_directions = [
            (0, 1), (0, -1), (1.3, 0.15), (-1.3, 0.15),
            (1, 0.9), (-1, 0.9), (1, -0.9), (-1, -0.9),
        ]

        def place_label(x, y, text, font, reserved):
            bbox = draw.textbbox((0, 0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            fallback = None
            for pass_i, radius in enumerate((28, 48, 72, 100)):
                for dir_i, (dx, dy) in enumerate(label_directions):
                    ox, oy = x + dx * radius, y + dy * radius
                    lx = min(max(ox - tw / 2, plot_left), plot_right - tw)
                    ly = min(max(oy - th / 2, plot_top), plot_bottom - th)
                    box = (lx - 5, ly - 3, lx + tw + 5, ly + th + 5)
                    if fallback is None:
                        fallback = (lx, ly, box)
                    if any(boxes_overlap(box, other) for other in reserved):
                        continue
                    if any(segment_hits_box(p1, p2, box) for p1, p2 in line_segments):
                        continue
                    return lx, ly, box, not (pass_i == 0 and dir_i == 0)
            return fallback[0], fallback[1], fallback[2], True  # everything collided; use it anyway

        if len(coords) >= 2:
            draw.line(coords, fill=(255, 255, 255), width=10, joint="curve")
            draw.line(coords, fill=ACCENT, width=5, joint="curve")

        label_font = _font(22)
        r = 8
        reserved_boxes = []
        city_labels = []  # (icon_x, icon_y, label_x, label_y, label, box, needs_leader)
        for i, (pt, (x, y)) in enumerate(zip(points, coords)):
            if i == 0:
                dot_color = POSITIVE_COLOR
            elif i == len(points) - 1 and len(points) > 1:
                dot_color = NEGATIVE_COLOR
            else:
                dot_color = ACCENT
            draw.ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], fill=(255, 255, 255))
            draw.ellipse([x - r, y - r, x + r, y + r], fill=dot_color)

            raw_label = pt.get("label")
            if not raw_label:
                continue
            # Numbered so a route that revisits the same place (an out-and-back
            # trip, say) doesn't show the identical name twice with no way to
            # tell which stop is which -- the number is the point's order
            # along the route, not a distance or ranking.
            label = f"{i + 1}. {raw_label}"
            lx, ly, box, needs_leader = place_label(x, y, label, label_font, reserved_boxes)
            reserved_boxes.append(box)
            city_labels.append((x, y, lx, ly, label, box, needs_leader))

        for icon_x, icon_y, lx, ly, label, box, needs_leader in city_labels:
            if needs_leader:
                label_cx, label_cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
                draw.line([(icon_x, icon_y), (label_cx, label_cy)], fill=MUTED, width=1)
            draw.rectangle([box[0], box[1], box[2], box[3]], fill=BG)
            draw.text((lx, ly), label, font=label_font, fill=TEXT)
    else:
        empty_font = _font(28)
        draw.text((pad, plot_top + plot_h / 2 - 15), "这条路线还没有点", font=empty_font, fill=MUTED)

    footer_font = _font(24)
    watermark = f"知行合一AI实验室 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf
