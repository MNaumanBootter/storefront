# builder image
FROM python:3.10.10-alpine as builder
LABEL maintainer="mnaumanbootter@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./src/requirements.txt /tmp/requirements.txt
COPY ./src /src
COPY ./scripts /scripts
WORKDIR /src

## building dependencies
RUN python -m pip install --upgrade pip
RUN apk add --update --no-cache gcc linux-headers python3-dev musl-dev
RUN apk add --update --no-cache mariadb-dev
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /src/wheels -r /tmp/requirements.txt
RUN apk del gcc musl-dev
RUN rm -rf /tmp


# production image
FROM python:3.10.10-alpine

WORKDIR /src

COPY --from=builder /src/wheels /wheels
COPY --from=builder /src .
COPY --from=builder /scripts /scripts

## installing dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --no-cache mariadb-connector-c-dev && \
    /py/bin/pip install --no-cache /wheels/* && \
    rm -rf /root/.cache && \
    find /usr/local/lib/python3.10 -name '__pycache__' | xargs rm -rf && \
    find /usr/local/lib/python3.10 -name '*.pyc' -delete && \
    rm -rf /wheels

EXPOSE 8000

RUN adduser -u 5678 --disabled-password --no-create-home --gecos "" appuser && chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER appuser

CMD ["run.sh"]