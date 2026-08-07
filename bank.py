"""ICBC (中国工商银行) debit-account statement PDF import + spending summary.

The PDF's password-protected and encrypted (handled by pdfplumber/pdfminer's
`password=` support). Its table also has an anti-forgery watermark baked
into the *same text layer* as the real data: a large diagonal stamp of stray
digits/letters, rendered at a different font size and, crucially, rotated --
its text matrix has nonzero off-diagonal terms, unlike every real character
on the page which is upright (matrix (1,0,0,1,x,y)). Naive text/table
extraction interleaves the watermark's characters into whatever cell they
visually overlap, corrupting numbers mid-string (an extra digit inserted
into an account number, etc). Filtering to upright-only characters before
table extraction removes the watermark cleanly without touching real data
(some of which is genuinely rendered in a small font -- small font size
alone is not a reliable signal, only the rotation is).

Two export variants have been seen, differing only in whether the
counterparty columns are present; parsing is done by header name so either
works, and any columns not recognized are just carried along unused.
"""

import hashlib
from collections import defaultdict
from datetime import date

import pdfplumber

# The "地区" (region) column has shown up as a constant, seemingly-spurious
# value (a substring of the account number) on every real export seen so
# far, not an actual region name -- not trustworthy enough to surface.
IGNORED_COLUMNS = {"地区", "账号", "储种", "序号", "币种", "钞汇"}


def _is_upright(obj):
    if obj.get("object_type") != "char":
        return True
    matrix = obj["matrix"]
    return abs(matrix[1]) < 1e-6 and abs(matrix[2]) < 1e-6


def _parse_amount(raw):
    s = (raw or "").strip().replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_icbc_pdf(file_bytes, password):
    """Returns (rows, warnings). Raises ValueError if the password is wrong
    or the file isn't a PDF pdfplumber can open at all."""
    import io

    rows = []
    warnings = []
    header_map = None
    seen_counts = defaultdict(int)

    try:
        pdf = pdfplumber.open(io.BytesIO(file_bytes), password=password or "")
    except Exception as exc:
        raise ValueError(str(exc))

    with pdf:
        for page in pdf.pages:
            filtered = page.filter(_is_upright)
            for table in filtered.extract_tables():
                if not table:
                    continue
                header, *data_rows = table
                if header_map is None:
                    header_map = {name: i for i, name in enumerate(header) if name}
                    required = {"交易日期", "收入/支出金额", "余额"}
                    missing = required - set(header_map)
                    if missing:
                        raise ValueError(f"表头缺少必要的列：{'、'.join(missing)}")
                for cells in data_rows:
                    if len(cells) <= header_map.get("交易日期", 0):
                        continue

                    def get(col):
                        i = header_map.get(col)
                        if i is None or i >= len(cells):
                            return ""
                        return (cells[i] or "").strip()

                    date_raw = get("交易日期")
                    if not date_raw:
                        continue
                    date_part, _, time_part = date_raw.partition("\n")
                    try:
                        y, m, d = (int(x) for x in date_part.split("-"))
                        date(y, m, d)
                    except ValueError:
                        warnings.append(f"跳过日期无法识别的行：{date_raw!r}")
                        continue

                    amount = _parse_amount(get("收入/支出金额"))
                    if amount is None:
                        continue
                    balance = _parse_amount(get("余额"))

                    row = {
                        "tx_date": f"{y:04d}-{m:02d}-{d:02d}",
                        "tx_time": time_part.strip(),
                        "category": get("摘要"),
                        "amount": amount,
                        "balance": balance,
                        "counterparty_name": get("对方户名").replace("\n", ""),
                        "counterparty_account": get("对方账号"),
                        "channel": get("渠道"),
                    }
                    key_src = "|".join(
                        str(row[k])
                        for k in ("tx_date", "tx_time", "category", "amount", "balance", "channel")
                        # Deliberately excludes counterparty_name/account: ICBC has
                        # at least two export variants, one with those columns and
                        # one without, so the same real transaction would otherwise
                        # get a different key (and thus a duplicate row) depending
                        # on which export it came from. Date+time+amount+balance is
                        # already enough to pin down a specific real transaction, so
                        # dropping counterparty from the key doesn't weaken dedup.
                    )
                    occurrence = seen_counts[key_src]
                    seen_counts[key_src] += 1
                    row["dedup_key"] = hashlib.sha256(f"{key_src}|{occurrence}".encode()).hexdigest()
                    rows.append(row)

    return rows, warnings


# The bank's own "摘要" (category) labels for an actual purchase and its
# reversal -- confirmed from a real statement that a refund is *not* filed
# under the same "消费" label as the purchase it offsets, it gets its own
# "退款" label instead. Both belong to the same underlying concept ("money
# spent on things, net of anything refunded") and are folded together
# everywhere below; treating 退款 as its own separate category would leave
# a purchase and its refund sitting in two different unrelated buckets that
# never cancel out.
SPENDING_CATEGORY = "消费"
REFUND_CATEGORY = "退款"


def _spending_bucket(category):
    """Normalizes 退款 into the 消费 bucket so a purchase and its refund net
    against each other everywhere spending is tallied, instead of showing up
    as two unrelated categories that don't offset."""
    return SPENDING_CATEGORY if category == REFUND_CATEGORY else (category or "其他")


def summarize(transactions):
    """transactions: iterable of dict-likes with tx_date/amount/category.
    Returns overall stats + a category breakdown. Netted per category rather
    than just summing negative amounts, so a refund correctly reduces the
    cost of the purchase it reverses instead of silently padding "income"
    with money that was never really earned."""
    by_category = defaultdict(float)  # positive = net cost, negative = net inflow
    last_balance = None
    last_date = None

    for t in transactions:
        by_category[_spending_bucket(t["category"])] += -t["amount"]
        if t["balance"] is not None and (last_date is None or t["tx_date"] >= last_date):
            last_date = t["tx_date"]
            last_balance = t["balance"]

    total_expense = sum(v for v in by_category.values() if v > 0)
    total_income = sum(-v for v in by_category.values() if v < 0)
    category_breakdown = sorted(
        ((c, v) for c, v in by_category.items() if v > 0), key=lambda kv: kv[1], reverse=True
    )
    income_breakdown = sorted(
        ((c, -v) for c, v in by_category.items() if v < 0), key=lambda kv: kv[1], reverse=True
    )

    return {
        "total_expense": total_expense,
        "total_income": total_income,
        "net": total_income - total_expense,
        "last_balance": last_balance,
        "income_breakdown": income_breakdown,
        "category_breakdown": category_breakdown,
    }


def build_daily_spending(transactions):
    """{date: net_spend}. Nets refunds against purchases automatically -- see
    _spending_bucket for why 消费 and 退款 are treated as the same thing."""
    daily = defaultdict(float)
    for t in transactions:
        if t["category"] in (SPENDING_CATEGORY, REFUND_CATEGORY):
            daily[t["tx_date"]] += -t["amount"]
    return dict(daily)


def build_month_calendar(year, month, daily_spending):
    """Full Mon-Sun week, unlike the trading calendar -- bank activity
    (transfers, automatic payments) isn't confined to weekdays."""
    import calendar as calendar_mod

    cal = calendar_mod.Calendar(firstweekday=0)
    weeks = []
    for week in cal.monthdayscalendar(year, month):
        cells = []
        for day in week:
            if day == 0:
                cells.append(None)
                continue
            d = date(year, month, day).isoformat()
            cells.append({"day": day, "date": d, "spend": daily_spending.get(d)})
        weeks.append(cells)
    return weeks


def list_years(daily_spending):
    """Every year with at least one day of spending data, most recent first."""
    return sorted({int(d[:4]) for d in daily_spending.keys()}, reverse=True)


def build_year_calendar(year, daily_spending):
    """12 cells, Jan-Dec, each the month's net spend (None if no data that
    month) -- a year-at-a-glance view to sit alongside the day-level
    calendar rather than a flat list, so multiple years of history are easy
    to page through and compare."""
    monthly = defaultdict(float)
    has_data = set()
    for d, spend in daily_spending.items():
        if int(d[:4]) == year:
            mm = int(d[5:7])
            monthly[mm] += spend
            has_data.add(mm)
    return [{"month": m, "spend": monthly[m] if m in has_data else None} for m in range(1, 13)]


def year_total(year, daily_spending):
    return sum(spend for d, spend in daily_spending.items() if int(d[:4]) == year)


def build_year_bar_chart(year_calendar, width=760, height=280, padding_x=30, padding_y=28):
    """12 bars (Jan-Dec) from the same data as build_year_calendar. Bars grow
    up from a zero baseline for a net-cost month (red) and down for a
    net-refund month (green), so it reads the same way the calendar cells'
    colors already do."""
    values = [m["spend"] or 0 for m in year_calendar]
    max_v = max(values + [0])
    min_v = min(values + [0])
    span = (max_v - min_v) or 1
    plot_w = width - padding_x * 2
    plot_h = height - padding_y * 2
    n = len(year_calendar)
    gap = 6
    bar_w = (plot_w - gap * (n - 1)) / n

    def y_for(v):
        return padding_y + plot_h * (1 - (v - min_v) / span)

    zero_y = y_for(0)
    bars = []
    for i, m in enumerate(year_calendar):
        x = padding_x + i * (bar_w + gap)
        v = m["spend"]
        if v is None:
            bars.append({"x": x, "y": zero_y, "width": bar_w, "height": 0, "value": None, "label": m["label"]})
            continue
        y_top = y_for(max(v, 0))
        y_bottom = y_for(min(v, 0))
        bars.append({
            "x": x,
            "y": y_top,
            "width": bar_w,
            "height": max(y_bottom - y_top, 1.5),
            "value": v,
            "is_cost": v > 0,
            "label": m["label"],
            "label_y": (y_top - 6) if v > 0 else (y_bottom + 14),
        })

    return {"width": width, "height": height, "zero_y": zero_y, "bars": bars}
