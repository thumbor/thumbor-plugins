FROM python:3.12-slim@sha256:12316debbfb86890f6b2d825820612741ba527ad5a44e3902759141d572bfe8f

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        pngcrush && \
    rm -rf /var/lib/apt/lists/*
