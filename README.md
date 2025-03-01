# YouTube Live Streaming with FFmpeg in Docker

This project allows you to stream to YouTube using FFmpeg inside a Docker container. It plays a shuffled playlist of MP3 audio files over a continuously looping MP4 video file.

## Features

- Stream audio and video content to YouTube Live seamlessly.
- Loop a single video continuously, while playing shuffled audio files.
- Use Docker to encapsulate the environment, ensuring consistency across systems.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) should be installed on your system.

## Setup Instructions

1. **Clone the Repository**

   Open your terminal and run:
   ```bash
   git clone https://github.com/decade27/youtube-livestream-docker.git
   cd youtube-stream
   ```

2. **Prepare Your Media Files**

   - Add your MP3 audio files to the `audio/` directory.
   - Add a single MP4 video file to the `video/` directory. Ensure the video file is named correctly as the script will use the first MP4 it finds for looping.

3. **Configure Your YouTube Stream Key**

   - Update the `YOUTUBE_KEY` and `YOUTUBE_URL` in the `docker-compose.yml` file. Replace `YOUR_YOUTUBE_STREAM_KEY` and `YOUR_YOUTUBE_URL` with your actual YouTube Live streaming key and YouTube Stream URL, respectively.

4. **Build and Run the Docker Container**

   Use Docker Compose to build the image and start the service:
   ```bash
   docker-compose up --build
   ```

## Usage

- Once the container is running, it will continuously stream the video file in a loop and play the MP3 files in shuffled order. The audio and video streams will be sent to YouTube Live.
- To stop the stream, you can interrupt the process (usually with `Ctrl+C` in your terminal) or shut it down gracefully:
  ```bash
  docker-compose down
  ```

## Troubleshooting

- If you encounter errors, ensure all paths are correct and both audio and video files are properly placed in their respective directories.
- Check that your YouTube stream key is correctly set as an environment variable or modified in the `docker-compose.yml`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue if you have ideas for improvements or find bugs.

## License

This project is open-source and available under the MIT License.