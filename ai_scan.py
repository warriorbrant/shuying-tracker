import base64
import json
import os
from datetime import date

import anthropic

from db import DATA_DIR

MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-4-5-20251001")
MOMENT_TYPE_VALUES = {"stock", "exercise", "photo", "thought"}
MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

PROMPT_TEMPLATE = """这是一张微信朋友圈截图（用户自己发布的动态）。请阅读其中的文字内容，提取这条朋友圈动态，只返回如下 JSON，不要输出任何多余文字或代码块标记：

{{
  "type": "stock 或 exercise 或 photo 或 thought 之一，根据内容判断最贴切的一种",
  "title": "简短标题，比如股票代码/名称、运动类型；不确定就返回空字符串",
  "content": "这条朋友圈的文字内容，尽量保留原文；如果图片里能看到运动数据（公里数/时长/配速等）也归纳写入",
  "log_date": "如果截图中能看到发布日期或相对时间（如'3天前'、'8月2日'），据此换算成 YYYY-MM-DD 格式；完全看不出来就返回空字符串"
}}

今天的日期是 {today}。"""


class ScanError(Exception):
    pass


def is_configured():
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def _extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end == -1:
            raise
        return json.loads(text[start : end + 1])


def analyze_screenshot(image_rel_path):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ScanError("未配置 ANTHROPIC_API_KEY")

    full_path = DATA_DIR / image_rel_path
    media_type = MEDIA_TYPES.get(full_path.suffix.lower(), "image/jpeg")
    image_b64 = base64.standard_b64encode(full_path.read_bytes()).decode("utf-8")

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": media_type, "data": image_b64},
                    },
                    {"type": "text", "text": PROMPT_TEMPLATE.format(today=date.today().isoformat())},
                ],
            }
        ],
    )
    raw_text = "".join(block.text for block in response.content if block.type == "text")

    try:
        parsed = _extract_json(raw_text)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ScanError(f"AI 返回内容无法解析：{exc}") from exc

    moment_type = parsed.get("type") if parsed.get("type") in MOMENT_TYPE_VALUES else "thought"

    log_date = (parsed.get("log_date") or "").strip()
    try:
        date.fromisoformat(log_date)
    except ValueError:
        log_date = ""

    return {
        "type": moment_type,
        "title": (parsed.get("title") or "").strip(),
        "content": (parsed.get("content") or "").strip(),
        "log_date": log_date,
    }
