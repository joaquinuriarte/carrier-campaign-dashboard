# syntax=docker/dockerfile:1
FROM python:3.11-slim

# ── Runtime tweaks ──────────────────────────────────────────
#  • PYTHONUNBUFFERED keeps logs flushing live
#  • PIP_NO_CACHE_DIR keeps the image lean
#  • PORT lets Render skip its port-scan
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8501

# ── Install deps first, then copy source to leverage caching ──
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ── Network & launch ─────────────────────────────────────────
EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
