FROM python:3.11-slim

WORKDIR /app

# =========================
# System dependencies
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Install dependencies FIRST (for caching)
# =========================
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =========================
# Copy source code LAST (important for cache)
# =========================
COPY . .

# =========================
# CI / Dev tools (optional but recommended)
# =========================
RUN pip install --no-cache-dir \
    flake8 \
    bandit \
    pytest

# =========================
# Runtime config
# =========================
EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]