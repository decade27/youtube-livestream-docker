# YouTube Live Streaming with FFmpeg in Docker

This project streams a looping video together with a shuffled audio playlist to YouTube Live from a Docker container.

## What was fixed

- Rebuilt the broken `stream.py` file so it is valid Python again.
- Fixed the malformed `Dockerfile` and `docker-compose.yml` formatting.
- Added safer defaults for YouTube RTMP output.
- Added better validation for missing media files and missing environment variables.
- Added support for more common audio and video file extensions.
- Added `.env.example` for easier configuration.

## Folder layout

```text
.
├── app/
│   ├── requirements.txt
│   └── stream.py
├── audio/
├── video/
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

## Setup

1. Copy `.env.example` to `.env`.
2. Put your audio files in `audio/`.
3. Put one video file in `video/`.
4. Build and start the container:

```bash
docker compose up --build
```

## Notes

- The first supported video file found in `video/` is used for the livestream.
- Audio files are shuffled each time the container starts.
- Default RTMP target is YouTube Live: `rtmp://a.rtmp.youtube.com/live2`.

## Stop

```bash
docker compose down
```
