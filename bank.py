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


def summarize(transactions):
    """transactions: iterable of dict-likes with tx_date/amount/category.
    Returns overall stats + a category breakdown (支出 side only, since
    that's what "spending" means -- income categories like 银联入账 aren't
    "spending" and would just clutter a spending breakdown)."""
    total_expense = 0.0
    total_income = 0.0
    by_category = defaultdict(float)
    last_balance = None
    last_date = None

    for t in transactions:
        amt = t["amount"]
        if amt < 0:
            total_expense += -amt
            by_category[t["category"] or "其他"] += -amt
        else:
            total_income += amt
        if t["balance"] is not None and (last_date is None or t["tx_date"] >= last_date):
            last_date = t["tx_date"]
            last_balance = t["balance"]

    category_breakdown = sorted(by_category.items(), key=lambda kv: kv[1], reverse=True)

    return {
        "total_expense": total_expense,
        "total_income": total_income,
        "net": total_income - total_expense,
        "last_balance": last_balance,
        "category_breakdown": category_breakdown,
    }


# The bank's own "摘要" (category) label for an actual purchase, as opposed
# to a transfer to another account (银证转账 -- often just money moved to a
# brokerage account the person also owns, not spending), wealth-management
# purchases (理财), bill payments (缴费), deposits (银联入账), etc. The
# calendar and monthly summary are scoped to just this -- "how much did I
# actually spend on things" -- while the overview stats cards above them
# keep showing the full picture across every category for context.
SPENDING_CATEGORY = "消费"


def filter_spending(transactions):
    return [t for t in transactions if t["category"] == SPENDING_CATEGORY]


def build_daily_totals(transactions):
    """{date: {"expense": float, "income": float}}"""
    daily = defaultdict(lambda: {"expense": 0.0, "income": 0.0})
    for t in transactions:
        amt = t["amount"]
        if amt < 0:
            daily[t["tx_date"]]["expense"] += -amt
        else:
            daily[t["tx_date"]]["income"] += amt
    return dict(daily)


def build_month_calendar(year, month, daily_totals):
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
            totals = daily_totals.get(d)
            cells.append({"day": day, "date": d, "totals": totals})
        weeks.append(cells)
    return weeks


def build_month_summary(daily_totals):
    totals = defaultdict(lambda: {"expense": 0.0, "income": 0.0})
    for d, t in daily_totals.items():
        ym = d[:7]
        totals[ym]["expense"] += t["expense"]
        totals[ym]["income"] += t["income"]
    months = []
    for ym in sorted(totals.keys(), reverse=True):
        y, m = ym.split("-")
        months.append({"year": int(y), "month": int(m), **totals[ym]})
    return months
