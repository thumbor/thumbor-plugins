FROM python:3.15-slim@sha256:94d3426f1def7db4a106a232ac121bfd975393e5dfd40a619b955fae45fe7913

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        pngcrush && \
    rm -rf /var/lib/apt/lists/*
