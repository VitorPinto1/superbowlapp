FROM python:3.9

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \
    python3-dev \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev \
    zlib1g-dev libjpeg-dev libfreetype6-dev \
    libgl1-mesa-glx libgles2-mesa-dev x11-xserver-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

ENV DISPLAY=:0

CMD ["python", "main.py"]

