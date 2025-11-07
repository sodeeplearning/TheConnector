import os
from moviepy import VideoFileClip

import config


def save_and_split_video(
        video_bytes: bytes,
        file_name: str,
        video_category: str,
        chunk_length: int = 60,
):
    file_name = file_name

    full_video_dir = os.path.join(
        config.Paths.videos_storage_path,
        config.Paths.full_videos_storage_path,
        video_category,
    )

    full_video_path = os.path.join(full_video_dir, file_name)

    chunks_dir = os.path.join(
        config.Paths.videos_storage_path,
        config.Paths.short_videos_storage_path,
        file_name[:file_name.rfind(".")],
    )

    os.makedirs(full_video_dir, exist_ok=True)
    os.makedirs(chunks_dir, exist_ok=True)

    with open(file_name, "wb") as writing_file:
        writing_file.write(video_bytes)

    clip = VideoFileClip(file_name)

    clip.write_videofile(
        full_video_path,
        audio_codec="aac",
    )

    duration = int(clip.duration)

    num_chunks = duration // chunk_length

    for i in range(num_chunks):
        start = i * chunk_length
        end = min((i + 1) * chunk_length, duration)
        subclip = clip.subclipped(start, end)

        chunk_path = os.path.join(chunks_dir, f"chunk_{i+1:03d}.mp4")

        subclip.write_videofile(
            chunk_path,
            audio_codec="aac",
        )

    clip.close()

    os.remove(file_name)
