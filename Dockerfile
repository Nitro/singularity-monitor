FROM python:3.7-alpine

ADD  . /app
WORKDIR /app

RUN \
    apk --update-cache -v add py3-pip py3-setuptools && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    python3 setup.py install && \
    apk --purge -v del py3-pip && \
    rm /var/cache/apk/*

LABEL   description="Docker image for singularity-monitor" \
        maintainer="sofian.brabez@gonitro.com" \
        repository="https://github.com/Nitro/singularity-monitor"

EXPOSE 8888

CMD ["/app/singularity-monitor.sh"]
