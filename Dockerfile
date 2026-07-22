FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATA_DIR=/data
EXPOSE 8080

# $PORT is set dynamically by platforms like Railway; falls back to 8080
# (matches fly.toml's internal_port) when unset, e.g. for local docker runs.
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8080} -w 2 --timeout 60 app:app"]
