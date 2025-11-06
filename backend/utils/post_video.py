import os
from moviepy import VideoFileClip

import config


def save_and_split_video(
        video_bytes: bytes,
        file_name: str,
        chunk_length: int = 60,
):
    full_video_path = os.path.join(
        config.Paths.videos_storage_path,
        config.Paths.full_videos_storage_path,
        file_name,
    )
    chunks_dir = os.path.join(
        config.Paths.videos_storage_path,
        config.Paths.short_videos_storage_path,
        file_name[:file_name.rfind(".")],
    )

    os.makedirs(chunks_dir, exist_ok=True)

    with open(full_video_path, "wb") as f:
        f.write(video_bytes)

    clip = VideoFileClip(full_video_path)
    duration = int(clip.duration)

    num_chunks = duration // chunk_length

    for i in range(num_chunks):
        start = i * chunk_length
        end = min((i + 1) * chunk_length, duration)
        subclip = clip.subclipped(start, end)

        chunk_path = os.path.join(chunks_dir, f"chunk_{i+1:03d}.mp4")

        subclip.write_videofile(
            chunk_path,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None,
        )

    clip.close()
