import yt_dlp
import os
import random


def download_youtube_video(url: str) -> tuple[str, bytes]:
    tmp_file_path = f"video{random.randint(1000, 9999)}.mp4"

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': tmp_file_path,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict.get('title', 'video')

    with open(tmp_file_path, "rb") as f:
        video_bytes = f.read()

    os.remove(tmp_file_path)

    return title, video_bytes
