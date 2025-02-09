# YouTube Video Clipper

A desktop application to download, preview, and clip YouTube videos. This project uses `yt-dlp` to fetch videos, `moviepy` for video editing, and `tkinter` to provide a graphical user interface.

## Features

- Download YouTube videos in the highest quality available.
- Preview specific sections of the video before clipping.
- Clip a portion of the video based on start and end times and save it locally.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/MagicalStorm/YouTube-Clipper.git
   cd YouTube-Clipper
    ```
2. **Install Dependencies: Ensure you have Python 3.8+ installed. Then run:**
   ```bash
   pip install pygame moviepy==1.0.3 yt-dlp
   ```
3. **FFmpeg Setup:**
- Make sure ffmpeg.exe is included in the project directory or installed on your system. If you're running the packaged .exe, FFmpeg is already bundled.

4. **Run the application**
   ```bash
    python main.py
   ```
