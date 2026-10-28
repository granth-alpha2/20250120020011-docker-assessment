FROM python:3.12.12-alpine3.22

WORKDIR /app

COPY requirements.txt .
RUN apk upgrade --no-cache \
    && pip install --no-cache-dir -r requirements.txt \
    && pip uninstall --yes pip \
    && addgroup -S app \
    && adduser -S -G app app

COPY app.py .

ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER app

EXPOSE 5000

CMD ["python", "app.py"]
