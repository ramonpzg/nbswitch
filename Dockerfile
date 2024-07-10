FROM python:3.11.9 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . .



RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

FROM python:3.11.9-slim

WORKDIR /app
COPY --from=builder /app .

CMD ["/app/.venv/bin/fastapi", "run"]
