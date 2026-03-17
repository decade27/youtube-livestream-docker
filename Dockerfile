FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ /app/

RUN mkdir -p /app/audio /app/video

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    YOUTUBE_URL=rtmp://a.rtmp.youtube.com/live2

CMD ["python", "/app/stream.py"]
