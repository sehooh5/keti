FROM python:3.7

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i 's/geteuid/getppid/' /usr/bin/vlc

RUN pip3 install psutil requests json

WORKDIR /app
COPY cpu_mem_test_client.py /app/cpu_mem_test_client.py

EXPOSE 5321
CMD ["python3", "cpu_mem_test_client.py"]