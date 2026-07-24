FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-noto-cjk \
    tzdata \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATA_DIR=/data
EXPOSE 8080

# $PORT is set dynamically by platforms like Railway; falls back to 8080
# (matches fly.toml's internal_port) when unset, e.g. for local docker runs.
# Single worker process with threads (not multiple -w processes) so the
# in-memory /admin/metrics stats are shared across all requests instead of
# being split across isolated worker processes.
# Timeout is 300s (not the default 30-60s) because novel video uploads run
# ffmpeg compression synchronously inside the request.
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8080} -w 1 --threads 4 --timeout 300 app:app"]
