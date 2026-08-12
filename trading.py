"""Broker transaction import + realized P&L calculation.

Currently parses Charles Schwab's "Transactions" CSV export. The file has no
realized-P&L column -- each row is just a signed cash flow (Amount) for one
buy/sell/dividend/transfer. Realized daily P&L is computed by FIFO-matching
each closing trade (Sell / Sell to Close) against the opening trade(s) it
closes (Buy / Buy to Open) for the same exact symbol -- for options, Schwab's
symbol string already encodes strike + expiry + right, so different contracts
on the same underlying never get mixed together.
"""

import calendar as calendar_mod
import csv
import hashlib
import io
from collections import defaultdict, deque
from datetime import date

OPEN_ACTIONS = {"Buy", "Buy to Open"}
CLOSE_ACTIONS = {"Sell", "Sell to Close"}
DIVIDEND_ACTIONS = {"Cash Dividend", "Qualified Dividend", "Special Dividend", "Pr Yr Cash Div"}
# Cash movement, not a trade -- explicitly ignored rather than falling into
# "unrecognized" so normal imports don't warn about them every time.
IGNORED_ACTIONS = {
    "Journal", "MoneyLink Transfer", "Bank Transfer", "Wire Funds",
    "Wire Sent", "Service Fee", "Journaled Shares", "Stock Plan Activity",
    "ADR Mgmt Fee", "Credit Interest", "Margin Interest",
}


def _parse_money(raw):
    if raw is None:
        return None
    s = raw.strip()
    if not s:
        return None
    neg = s.startswith("-")
    s = s.lstrip("-").lstrip("$").replace(",", "")
    if not s:
        return None
    try:
        val = float(s)
    except ValueError:
        return None
    return -val if neg else val


def _parse_qty(raw):
    if raw is None:
        return None
    s = raw.strip().replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_date(raw):
    # Schwab writes settlement-pending transfers as "MM/DD/YYYY as of MM/DD/YYYY";
    # the transaction date (first one) is what we want.
    s = raw.split(" as of ")[0].strip()
    parts = s.split("/")
    if len(parts) != 3:
        raise ValueError(f"unrecognized date: {raw}")
    m, d, y = parts
    return date(int(y), int(m), int(d)).isoformat()


def parse_schwab_csv(file_bytes):
    """Returns (rows, warnings). `rows` are dicts ready for INSERT into
    `trades`; `warnings` are human-readable (Chinese) notes about anything
    skipped or not understood, meant to be shown to the user after import."""
    text = file_bytes.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))

    rows = []
    unhandled_actions = set()
    bad_dates = 0
    seen_counts = defaultdict(int)

    for raw in reader:
        action = (raw.get("Action") or "").strip()
        date_raw = (raw.get("Date") or "").strip()
        if not action or not date_raw:
            continue

        try:
            trade_date = _parse_date(date_raw)
        except ValueError:
            bad_dates += 1
            continue

        if action in IGNORED_ACTIONS:
            continue
        if action not in OPEN_ACTIONS and action not in CLOSE_ACTIONS and action not in DIVIDEND_ACTIONS:
            unhandled_actions.add(action)
            continue

        amount = _parse_money(raw.get("Amount"))
        if amount is None:
            continue

        symbol = (raw.get("Symbol") or "").strip() or (raw.get("Description") or "").strip()
        row = {
            "trade_date": trade_date,
            "action": action,
            "symbol": symbol,
            "description": (raw.get("Description") or "").strip(),
            "quantity": _parse_qty(raw.get("Quantity")),
            "price": _parse_money(raw.get("Price")),
            "fees": _parse_money(raw.get("Fees & Comm")),
            "amount": amount,
        }
        # Disambiguate genuinely identical rows (same date/action/symbol/qty/
        # price/amount) within one file via an occurrence counter, so they
        # aren't collapsed into one on insert -- while a re-upload of the same
        # (or an overlapping) export still produces the same key sequence and
        # correctly dedupes against what's already stored.
        key_src = "|".join(
            str(row[k]) for k in ("trade_date", "action", "symbol", "quantity", "price", "amount")
        )
        occurrence = seen_counts[key_src]
        seen_counts[key_src] += 1
        row["dedup_key"] = hashlib.sha256(f"{key_src}|{occurrence}".encode()).hexdigest()
        rows.append(row)

    warnings = []
    if bad_dates:
        warnings.append(f"{bad_dates} 行日期格式无法识别，已跳过")
    if unhandled_actions:
        warnings.append("以下操作类型暂不认识，已跳过：" + "、".join(sorted(unhandled_actions)))

    # Schwab lists transactions newest-first. Reverse to oldest-first so
    # insertion order (and thus the `id` tiebreaker used when re-reading
    # trades from the db, since there's no intraday timestamp to sort by)
    # approximates real chronological order -- needed for FIFO matching to
    # see opens before the closes that consume them.
    rows.reverse()

    return rows, warnings


def compute_daily_pnl(trades):
    """trades: iterable of dict-likes with trade_date/action/symbol/quantity/
    amount/fees, already sorted chronologically (trade_date, then insertion
    order). Returns (daily_pnl: {date: float}, meta: {open_positions,
    unmatched_closes, total_fees}).

    `amount` already nets in fees (a sell's Amount = trade value - fee; a
    buy's Amount = -(trade value + fee)), so daily_pnl is P&L *after* fees
    without any extra work. To separately report fees paid, each lot also
    tracks its fee-exclusive ("gross") cost/proceeds per unit -- derived
    from amount and fees directly (not from Price), which sidesteps having
    to know whether a row is a 100x options contract or a 1x share to get
    the right per-unit scale. The gap between the gross and net match for a
    given piece is exactly the (prorated) fees on both legs of that trade.
    """
    daily = defaultdict(float)
    by_symbol = defaultdict(list)

    for t in trades:
        if t["action"] in DIVIDEND_ACTIONS:
            daily[t["trade_date"]] += t["amount"]
        else:
            by_symbol[t["symbol"]].append(t)

    open_positions = 0
    unmatched_closes = 0
    total_fees = 0.0

    for symbol, txns in by_symbol.items():
        lots = deque()  # each: [remaining_qty, net_cost_per_unit, gross_cost_per_unit]
        for t in txns:
            qty = t["quantity"] or 0
            if qty <= 0:
                continue
            fee_per_unit = (t["fees"] or 0) / qty
            if t["action"] in OPEN_ACTIONS:
                net_cost = abs(t["amount"]) / qty
                lots.append([qty, net_cost, net_cost - fee_per_unit])
            elif t["action"] in CLOSE_ACTIONS:
                net_proceeds = t["amount"] / qty
                gross_proceeds = net_proceeds + fee_per_unit
                remaining = qty
                pnl = 0.0
                while remaining > 1e-9 and lots:
                    lot_qty, lot_net_cost, lot_gross_cost = lots[0]
                    take = min(remaining, lot_qty)
                    net_piece = take * (net_proceeds - lot_net_cost)
                    gross_piece = take * (gross_proceeds - lot_gross_cost)
                    pnl += net_piece
                    total_fees += gross_piece - net_piece
                    lot_qty -= take
                    remaining -= take
                    if lot_qty <= 1e-9:
                        lots.popleft()
                    else:
                        lots[0][0] = lot_qty
                if remaining > 1e-9:
                    # Closed more than we ever saw opened -- the position
                    # predates the imported history. No way to know its real
                    # cost basis, so this leftover quantity contributes no
                    # P&L rather than risk overstating gains.
                    unmatched_closes += 1
                daily[t["trade_date"]] += pnl
        if lots:
            open_positions += 1

    return dict(daily), {
        "open_positions": open_positions,
        "unmatched_closes": unmatched_closes,
        "total_fees": total_fees,
    }


def summarize_daily_pnl(daily_pnl):
    if not daily_pnl:
        return {
            "total": 0.0, "win_days": 0, "loss_days": 0, "best_day": None, "worst_day": None,
            "avg_win": None, "avg_loss": None, "win_loss_ratio": None,
        }
    total = sum(daily_pnl.values())
    wins = [v for v in daily_pnl.values() if v > 0]
    losses = [v for v in daily_pnl.values() if v < 0]
    win_days = len(wins)
    loss_days = len(losses)
    avg_win = sum(wins) / win_days if win_days else None
    avg_loss = sum(losses) / loss_days if loss_days else None  # negative (or None)
    # 盈亏比: average winning day vs. average losing day, e.g. 2.5 means a
    # typical win is 2.5x the size of a typical loss. Undefined (None)
    # without at least one day on each side -- there's nothing to compare.
    win_loss_ratio = (avg_win / abs(avg_loss)) if avg_win is not None and avg_loss else None
    best_date = max(daily_pnl, key=daily_pnl.get)
    worst_date = min(daily_pnl, key=daily_pnl.get)
    return {
        "total": total,
        "win_days": win_days,
        "loss_days": loss_days,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "win_loss_ratio": win_loss_ratio,
        "best_day": (best_date, daily_pnl[best_date]),
        "worst_day": (worst_date, daily_pnl[worst_date]),
    }


def build_month_calendar(year, month, daily_pnl):
    """Mon-Fri only (5 columns) -- markets are closed on weekends, and a
    trading calendar with two permanently-empty weekend columns just wastes
    space. Matches the convention most trading-journal tools use."""
    cal = calendar_mod.Calendar(firstweekday=0)
    weeks = []
    for week in cal.monthdayscalendar(year, month):
        cells = []
        for day in week[:5]:
            if day == 0:
                cells.append(None)
                continue
            d = date(year, month, day).isoformat()
            cells.append({"day": day, "date": d, "pnl": daily_pnl.get(d)})
        weeks.append(cells)
    return weeks


def build_month_summary(daily_pnl):
    """One row per calendar month that has any trade data, most recent
    first -- an at-a-glance overview across all imported history, so you
    don't have to page through the day calendar one month at a time to see
    which months were good or bad."""
    totals = defaultdict(float)
    for d, pnl in daily_pnl.items():
        totals[d[:7]] += pnl  # "YYYY-MM"
    months = []
    for ym in sorted(totals.keys(), reverse=True):
        y, m = ym.split("-")
        months.append({"year": int(y), "month": int(m), "total": totals[ym]})
    return months


def build_cumulative_series(daily_pnl):
    cumulative = 0.0
    series = []
    for d in sorted(daily_pnl.keys()):
        cumulative += daily_pnl[d]
        series.append({"date": d, "pnl": daily_pnl[d], "cumulative": cumulative})
    return series


def build_pnl_chart(series, width=760, height=280, padding=40):
    if not series:
        return None
    values = [p["cumulative"] for p in series]
    min_v = min(values + [0])
    max_v = max(values + [0])
    span = (max_v - min_v) or 1
    n = len(series)
    plot_w = width - padding * 2
    plot_h = height - padding * 2

    def x_for(i):
        return padding + (plot_w * i / (n - 1) if n > 1 else plot_w / 2)

    def y_for(v):
        return padding + plot_h * (1 - (v - min_v) / span)

    points = [(x_for(i), y_for(p["cumulative"])) for i, p in enumerate(series)]
    points_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)

    label_positions = sorted(set([0, n - 1] + [n * k // 4 for k in (1, 2, 3)])) if n > 1 else [0]
    x_labels = [{"x": points[i][0], "label": series[i]["date"][5:]} for i in label_positions]

    return {
        "width": width,
        "height": height,
        "points_str": points_str,
        "zero_y": y_for(0),
        "final_x": points[-1][0],
        "final_y": points[-1][1],
        "final_value": values[-1],
        "positive": values[-1] >= 0,
        "x_labels": x_labels,
    }
