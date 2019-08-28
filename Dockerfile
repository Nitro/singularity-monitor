FROM python:3.7-alpine

ENV HTTP_PORT=8888

ADD  . /app
WORKDIR /app

RUN \
    apk --update-cache -v add py3-pip py3-setuptools curl && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    python3 setup.py install && \
    apk --purge -v del py3-pip && \
    rm /var/cache/apk/*

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl --fail http://localhost:$HTTP_PORT/health || exit 1

LABEL   description="Docker image for singularity-monitor" \
        maintainer="sofian.brabez@gonitro.com" \
        repository="https://github.com/Nitro/singularity-monitor"

EXPOSE $HTTP_PORT

CMD ["/app/singularity-monitor.sh"]
