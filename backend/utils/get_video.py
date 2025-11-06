import os
import random
from typing import Self
from dataclasses import dataclass

import config


@dataclass
class Video:
    full_video_path: str
    short_video_path: str

    @property
    def full_video(self) -> Self:
        return Video(self.full_video_path, self.full_video_path)


def get_video_from_category(video_category: str) -> Video:
    full_videos_dir = os.path.join(
        config.Paths.videos_storage_path,
        config.Paths.full_videos_storage_path,
        video_category,
    )
    full_videos_names_list = os.listdir(full_videos_dir)
    full_video_name = random.choice(full_videos_names_list)
    full_video_path = os.path.join(full_videos_dir, full_video_name)

    short_videos_dir = os.path.join(
        config.Paths.videos_storage_path,
        config.Paths.short_videos_storage_path,
        full_video_name[:full_video_name.rfind(".")],
    )
    short_videos_names_list = os.listdir(short_videos_dir)
    short_video_name = random.choice(short_videos_names_list)
    short_video_path = os.path.join(short_videos_dir, short_video_name)

    return Video(full_video_path, short_video_path)
