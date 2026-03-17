import os
import random
import subprocess
import sys
from pathlib import Path

AUDIO_PATH = Path("/app/audio")
VIDEO_PATH = Path("/app/video")
DEFAULT_YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
SUPPORTED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}
SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}


def require_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or not value.strip():
        raise RuntimeError(f"The {name} environment variable is not set.")
    return value.strip()


def find_media_files(directory: Path, extensions: set[str]) -> list[Path]:
    if not directory.exists():
        raise RuntimeError(f"Directory does not exist: {directory}")

    files = [
        path for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in extensions
    ]
    return sorted(files)


def build_playlist_file(audio_files: list[Path], playlist_file: Path) -> None:
    random.shuffle(audio_files)
    with playlist_file.open("w", encoding="utf-8") as handle:
        for audio_file in audio_files:
            escaped = str(audio_file).replace("'", r"'\\''")
            handle.write(f"file '{escaped}'\n")


def build_ffmpeg_command(video_file: Path, playlist_file: Path, output_url: str) -> list[str]:
    return [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        os.getenv("FFMPEG_LOGLEVEL", "info"),
        "-re",
        "-stream_loop",
        "-1",
        "-i",
        str(video_file),
        "-stream_loop",
        "-1",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(playlist_file),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        os.getenv("FFMPEG_PRESET", "veryfast"),
        "-maxrate",
        os.getenv("VIDEO_MAXRATE", "6000k"),
        "-bufsize",
        os.getenv("VIDEO_BUFSIZE", "12000k"),
        "-pix_fmt",
        "yuv420p",
        "-g",
        os.getenv("VIDEO_GOP", "60"),
        "-c:a",
        "aac",
        "-b:a",
        os.getenv("AUDIO_BITRATE", "192k"),
        "-ar",
        os.getenv("AUDIO_SAMPLE_RATE", "44100"),
        "-ac",
        os.getenv("AUDIO_CHANNELS", "2"),
        "-f",
        "flv",
        output_url,
    ]


def main() -> int:
    youtube_key = require_env("YOUTUBE_KEY")
    youtube_url = require_env("YOUTUBE_URL", DEFAULT_YOUTUBE_URL)
    output_url = f"{youtube_url.rstrip('/')}/{youtube_key}"

    audio_files = find_media_files(AUDIO_PATH, SUPPORTED_AUDIO_EXTENSIONS)
    video_files = find_media_files(VIDEO_PATH, SUPPORTED_VIDEO_EXTENSIONS)

    if not audio_files:
        raise RuntimeError(
            f"No supported audio files found in {AUDIO_PATH}. "
            f"Expected one of: {', '.join(sorted(SUPPORTED_AUDIO_EXTENSIONS))}"
        )
    if not video_files:
        raise RuntimeError(
            f"No supported video files found in {VIDEO_PATH}. "
            f"Expected one of: {', '.join(sorted(SUPPORTED_VIDEO_EXTENSIONS))}"
        )

    video_file = video_files[0]
    playlist_file = AUDIO_PATH / "playlist.txt"
    build_playlist_file(audio_files, playlist_file)

    command = build_ffmpeg_command(video_file, playlist_file, output_url)
    print("Starting stream with video:", video_file)
    print("Audio tracks in playlist:", len(audio_files))
    print("Streaming to:", youtube_url)

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"FFmpeg exited with status {exc.returncode}", file=sys.stderr)
        return exc.returncode or 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
