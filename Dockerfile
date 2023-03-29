FROM python:3.10.10-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip

COPY ./app/requirements.txt .
RUN apk add --no-cache gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt \
    && apk del gcc musl-dev

COPY ./app /app

FROM python:3.10.10-alpine

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN apk add --no-cache mariadb-connector-c-dev

RUN pip install --no-cache /wheels/* \
    && rm -rf /root/.cache \
    && find /usr/local/lib/python3.10 -name '__pycache__' | xargs rm -rf \
    && find /usr/local/lib/python3.10 -name '*.pyc' -delete

COPY --from=builder /app /app

EXPOSE 8000

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
