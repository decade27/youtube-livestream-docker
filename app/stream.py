import subprocess
import os
import random

   # YouTube variables
YOUTUBE_URL = os.getenv('YOUTUBE_URL')
YOUTUBE_KEY = os.getenv('YOUTUBE_KEY')  # Expect the key to be provided as an environment variable

if not YOUTUBE_KEY:
    raise Exception("The YOUTUBE_KEY environment variable is not set.")

if not YOUTUBE_URL:
    raise Exception("The YOUTUBE_URL environment variable is not set.")

   # Paths for media files
AUDIO_PATH = "/app/audio"
VIDEO_PATH = "/app/video"

   # Discover available files
audio_files = [f for f in os.listdir(AUDIO_PATH) if f.endswith(".mp3")]
video_files = [f for f in os.listdir(VIDEO_PATH) if f.endswith(".mp4")]

if not audio_files:
    raise Exception("No audio files found!")

if not video_files:
    raise Exception("No video file found!")

   # Randomly shuffle the audio files
random.shuffle(audio_files)

   # Create a playlist for the shuffled MP3s
playlist_file_path = os.path.join(AUDIO_PATH, "playlist.txt")
with open(playlist_file_path, 'w') as playlist_file:
    for audio_file in audio_files:
        playlist_file.write(f"file '{os.path.join(AUDIO_PATH, audio_file)}'\n")

   # Use the first (and only) video in the directory
video_file = os.path.join(VIDEO_PATH, video_files[0])

   # FFmpeg command to stream
command = [
    "ffmpeg",
    "-re",
    "-stream_loop", "-1",          # Loop the video indefinitely
    "-i", video_file,
    "-f", "concat",
    "-safe", "0",
    "-stream_loop", "-1",          # Loop the audio playlist indefinitely
    "-i", playlist_file_path,
    "-c:v", "libx264",             # Encode video using H.264
    "-b:v", "8000k",               # Set video bitrate to 2500 kbps
    "-x264-params", "keyint=50",   # Set keyframe interval to 50 (useful for smooth streaming)
    "-c:a", "aac",                 # Encode audio using AAC
    "-b:a", "128k",                # Set audio bitrate to 128 kbps
    "-strict", "experimental",
    "-f", "flv",
    f"{YOUTUBE_URL}/{YOUTUBE_KEY}"
]

   # Execute the command
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")