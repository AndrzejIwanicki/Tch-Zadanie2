FROM python:3.12-alpine AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-alpine

LABEL org.opencontainers.image.authors="Andrzej Iwanicki"
LABEL org.opencontainers.image.title="Aplikacja Pogodowa Laboratorium"
LABEL org.opencontainers.image.description="Zadanie 1 - Kotneneryzacja"

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000


HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1

CMD ["python", "app.py"]