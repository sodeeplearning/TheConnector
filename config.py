from dataclasses import dataclass
from os import environ
from dotenv import load_dotenv


load_dotenv()

categories = [
    "Motivation",
    "IT",
    "Maths",
    "AI",
]


@dataclass
class Secrets:
    yandex_api_key = environ["YANDEX_API_KEY"]
    yandex_folder_id = environ["YANDEX_FOLDER_ID"]
    bot_token = environ["BOT_TOKEN"]


@dataclass
class Paths:
    videos_storage_path = "videos"
    short_videos_storage_path = "short_videos"
    full_videos_storage_path = "full_videos"


@dataclass
class Links:
    yandex_gpt_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
