import re

import requests
from bs4 import BeautifulSoup

DESKTOP_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
)
TIMEOUT = 8

SUBJECT_ID_RE = re.compile(r"/subject/(\d+)")


class DoubanFetchError(Exception):
    pass


def _get(url, headers, referer="https://www.douban.com/"):
    resp = requests.get(
        url,
        headers={"User-Agent": headers, "Referer": referer},
        timeout=TIMEOUT,
        allow_redirects=False,
    )
    if resp.status_code != 200:
        raise DoubanFetchError(f"豆瓣返回了非预期状态（{resp.status_code}），可能触发了反爬限制，请手动填写")
    resp.encoding = resp.apparent_encoding or "utf-8"
    return resp.text


def _meta(soup, prop):
    tag = soup.find("meta", attrs={"property": prop})
    return tag["content"].strip() if tag and tag.get("content") else ""


def _normalize_cover(url):
    if not url:
        return url
    # m.douban.com's og:image is hard-cropped to a 300x300 square via imageView2 mode 1
    # (crop-to-fill). Switch to mode 2 (scale only, keeps original aspect ratio) so
    # posters/covers aren't squished into a square before we crop them again in the UI.
    return re.sub(r"imageView2/1/[^\s]*", "imageView2/2/w/500", url)


def fetch_book(subject_id):
    html = _get(f"https://book.douban.com/subject/{subject_id}/", DESKTOP_UA)
    soup = BeautifulSoup(html, "lxml")

    title = _meta(soup, "og:title")
    cover_url = _meta(soup, "og:image")
    description = _meta(soup, "og:description")

    author = ""
    total_units = None
    info = soup.find("div", id="info")
    if info:
        text = info.get_text("\n")
        author_match = re.search(r"作者\s*\n?\s*[:：]?\s*\n?\s*(.+)", text)
        # prefer the linked author names if present
        author_span = info.find(string=re.compile("作者"))
        if author_span:
            links = []
            node = author_span.parent
            for sib in node.find_next_siblings():
                if sib.name != "a":
                    break
                links.append(sib.get_text(strip=True))
            if links:
                author = " / ".join(links)
        if not author and author_match:
            author = author_match.group(1).strip().splitlines()[0]

        pages_match = re.search(r"页数[:：]\s*(\d+)", text)
        if pages_match:
            total_units = int(pages_match.group(1))

    if not title:
        raise DoubanFetchError("未能解析该豆瓣页面，请确认链接是否正确")

    return {
        "type": "book",
        "title": title,
        "creator": author,
        "cover_url": cover_url,
        "total_units": total_units,
        "unit_label": "页",
        "review_draft": description,
    }


def fetch_show(subject_id):
    html = _get(f"https://m.douban.com/movie/subject/{subject_id}/", MOBILE_UA)
    soup = BeautifulSoup(html, "lxml")

    raw_title = _meta(soup, "og:title")
    title = re.split(r"\s*-\s*(电影|电视剧|综艺)$", raw_title)[0].strip() if raw_title else ""
    cover_url = _normalize_cover(_meta(soup, "og:image"))
    description = _meta(soup, "og:description")

    if not title:
        raise DoubanFetchError("未能解析该豆瓣页面，请确认链接是否正确")

    total_units = None
    try:
        suggest = requests.get(
            "https://movie.douban.com/j/subject_suggest",
            params={"q": title},
            headers={"User-Agent": DESKTOP_UA, "Referer": "https://www.douban.com/"},
            timeout=TIMEOUT,
        )
        if suggest.status_code == 200:
            for candidate in suggest.json():
                if str(candidate.get("id")) == str(subject_id):
                    ep = candidate.get("episode")
                    if ep and ep.isdigit():
                        total_units = int(ep)
                    break
    except (requests.RequestException, ValueError):
        pass

    return {
        "type": "show",
        "title": title,
        "creator": "",
        "cover_url": cover_url,
        "total_units": total_units,
        "unit_label": "集",
        "review_draft": description,
    }


def fetch_douban_info(url):
    url = url.strip()
    match = SUBJECT_ID_RE.search(url)
    if not match:
        raise DoubanFetchError("看起来不是有效的豆瓣链接（找不到 subject id）")
    subject_id = match.group(1)

    if "book.douban.com" in url:
        return fetch_book(subject_id)
    if "movie.douban.com" in url:
        return fetch_show(subject_id)
    raise DoubanFetchError("只支持豆瓣读书（book.douban.com）或豆瓣电影/剧集（movie.douban.com）链接")
