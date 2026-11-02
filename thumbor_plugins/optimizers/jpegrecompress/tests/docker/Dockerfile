FROM python:3.15-slim@sha256:94d3426f1def7db4a106a232ac121bfd975393e5dfd40a619b955fae45fe7913

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        bzip2 && \
    wget -q https://github.com/danielgtaylor/jpeg-archive/releases/download/2.1.1/jpeg-archive-2.1.1-linux.tar.bz2 && \
    echo "45752066061c065d698666a44380374a3c27e1192c6cc3d496e716bfba1d7e47  jpeg-archive-2.1.1-linux.tar.bz2" | sha256sum -c - && \
    tar -jxf jpeg-archive-2.1.1-linux.tar.bz2 jpeg-recompress && \
    mv jpeg-recompress /usr/bin/ && \
    rm jpeg-archive-2.1.1-linux.tar.bz2 && \
    apt-get purge -y --auto-remove wget bzip2 && \
    rm -rf /var/lib/apt/lists/* && \
    /usr/bin/jpeg-recompress --version
