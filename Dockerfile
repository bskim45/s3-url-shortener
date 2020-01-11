FROM python:3.8-alpine

ARG VCS_REF
ARG BUILD_DATE
ARG APP_VERSION

ENV APP_VERSION ${APP_VERSION}
ENV BUILD_DATE ${BUILD_DATE}

# Metadata
LABEL org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.name="bskim45/s3-url-shortener" \
    org.label-schema.url="https://hub.docker.com/r/bskim45/s3-url-shortener" \
    org.label-schema.vcs-url="https://github.com/bskim45/s3-url-shortener" \
    org.label-schema.build-date=$BUILD_DATE

RUN apk add --no-cache --virtual .build-deps gcc libc-dev \
    && pip install --no-cache-dir meinheld gunicorn \
    && apk del .build-deps gcc libc-dev \
    && rm -rf /var/cache/apk/*

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY scripts/start_app.sh /start_app.sh
RUN chmod +x /start_app.sh

COPY scripts/gunicorn_conf.py /gunicorn_conf.py

COPY ./app /app/app
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ENV PYTHONPATH=/app

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start_app.sh"]
