# ---- builder: install dependencies into a virtualenv ----
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


# ---- runtime: lean image that only runs the FastAPI server ----
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN groupadd --system ghgist-scraper && \
    useradd --system --gid ghgist-scraper --create-home \
        --home-dir /home/ghgist-scraper ghgist-scraper

COPY --from=builder /opt/venv /opt/venv
COPY app.py .
COPY gh_user_public_gists_scraper ./gh_user_public_gists_scraper

RUN chown -R ghgist-scraper:ghgist-scraper /app

USER ghgist-scraper

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
