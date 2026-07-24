import threading
import time
from collections import deque

_LOCK = threading.Lock()
_REQUESTS = deque(maxlen=5000)  # (timestamp, endpoint, status, duration_ms)
START_TIME = time.time()


def record(endpoint, status, duration_ms):
    with _LOCK:
        _REQUESTS.append((time.time(), endpoint or "?", status, duration_ms))


def _recent(window_seconds):
    cutoff = time.time() - window_seconds
    with _LOCK:
        return [r for r in _REQUESTS if r[0] >= cutoff]


def _percentile(sorted_vals, pct):
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * pct
    f, c = int(k), min(int(k) + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def get_stats(window_seconds=60):
    recent = _recent(window_seconds)
    durations = sorted(r[3] for r in recent)
    count = len(recent)

    status_buckets = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0}
    endpoints = {}
    for _, endpoint, status, dur in recent:
        bucket = f"{status // 100}xx"
        if bucket in status_buckets:
            status_buckets[bucket] += 1
        e = endpoints.setdefault(endpoint, {"count": 0, "total_ms": 0.0})
        e["count"] += 1
        e["total_ms"] += dur

    top_endpoints = sorted(
        ({"endpoint": k, "count": v["count"], "avg_ms": v["total_ms"] / v["count"]} for k, v in endpoints.items()),
        key=lambda e: e["count"],
        reverse=True,
    )[:10]

    return {
        "window_seconds": window_seconds,
        "count": count,
        "tps": count / window_seconds if window_seconds else 0.0,
        "avg_ms": (sum(durations) / count) if count else 0.0,
        "p50_ms": _percentile(durations, 0.5),
        "p95_ms": _percentile(durations, 0.95),
        "p99_ms": _percentile(durations, 0.99),
        "status": status_buckets,
        "top_endpoints": top_endpoints,
        "uptime_seconds": time.time() - START_TIME,
    }


def format_uptime(seconds):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}小时{m}分钟"
    if m:
        return f"{m}分{s}秒"
    return f"{s}秒"
