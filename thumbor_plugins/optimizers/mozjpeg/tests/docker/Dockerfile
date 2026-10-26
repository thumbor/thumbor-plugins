FROM python:3.12-slim@sha256:12316debbfb86890f6b2d825820612741ba527ad5a44e3902759141d572bfe8f

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        wget \
        cmake \
        gcc \
        libc6-dev \
        nasm \
        make \
        libpng-dev && \
    wget -q -O mozjpeg-v4.0.3.tar.gz https://github.com/mozilla/mozjpeg/archive/refs/tags/v4.0.3.tar.gz && \
    echo "4f22731db2afa14531a5bf2633d8af79ca5cb697a550f678bf43f24e5e409ef0  mozjpeg-v4.0.3.tar.gz" | sha256sum -c - && \
    tar xf mozjpeg-v4.0.3.tar.gz && \
    cd mozjpeg-4.0.3/ && \
    mkdir build && \
    cd build && \
    cmake -G"Unix Makefiles" ../ && \
    make install && \
    cd /app && \
    rm -rf mozjpeg-v4.0.3.tar.gz mozjpeg-4.0.3 && \
    # cjpeg links against libpng, which apt installed only as a dependency of libpng-dev
    apt-mark manual libpng16-16t64 && \
    apt-get purge -y --auto-remove \
        wget \
        cmake \
        gcc \
        libc6-dev \
        nasm \
        make \
        libpng-dev && \
    rm -rf /var/lib/apt/lists/* && \
    /opt/mozjpeg/bin/cjpeg -version
