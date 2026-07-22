import io
from datetime import date
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

from db import DATA_DIR

STATIC_ROOT = Path(__file__).parent / "static"
WEEKDAY_CN = ["一", "二", "三", "四", "五", "六", "日"]

CARD_W, CARD_H = 1080, 1440
BG = (250, 248, 245)
TEXT = (43, 41, 37)
MUTED = (138, 131, 120)
ACCENT = (181, 101, 74)
ACCENT_SOFT = (241, 227, 220)
CARD_BG = (255, 255, 255)
BORDER = (232, 226, 217)

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


def _font(size, bold=False):
    paths = FONT_BOLD_CANDIDATES if bold else FONT_REGULAR_CANDIDATES
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw, text, font, max_width):
    lines = []
    current = ""
    for ch in text:
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
    try:
        resp = requests.get(
            url,
            timeout=6,
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.douban.com/"},
        )
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert("RGB")
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


def _measure_draw():
    return ImageDraw.Draw(Image.new("RGB", (10, 10)))


def _rounded_paste(base, img, box, radius=18):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
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
    watermark = f"书影追踪 · {date.today().isoformat()}"
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

    watermark = f"书影追踪 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf


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


def build_changelog_share_card(entries, heading):
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

    header_h = pad + 64 + 40 + 24
    footer_h = 70

    blocks = [_build_changelog_card(measure, col_w, e) for e in entries]

    if not blocks:
        H = header_h + 90 + footer_h
        card = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(card)
        draw.text((pad, header_h), "这段时间还没有更新记录", font=empty_font, fill=MUTED)
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
    count_text = f"共 {len(entries)} 条更新" if entries else "这段时间还没有更新记录"
    draw.text((pad, pad + 64), count_text, font=subtitle_font, fill=MUTED)

    watermark = f"书影追踪 开发日志 · {date.today().isoformat()}"
    bbox = draw.textbbox((0, 0), watermark, font=footer_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, H - 50), watermark, font=footer_font, fill=MUTED)

    buf = io.BytesIO()
    card.save(buf, format="PNG")
    buf.seek(0)
    return buf
