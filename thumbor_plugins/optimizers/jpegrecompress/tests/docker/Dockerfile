FROM python:3.12-slim@sha256:12316debbfb86890f6b2d825820612741ba527ad5a44e3902759141d572bfe8f

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
