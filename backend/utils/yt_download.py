import io
from pytube import YouTube


def download_youtube_video(url: str) -> bytes:
    yt = YouTube(url)

    stream = yt.streams.filter(
        progressive=True,
        file_extension="mp4"
    ).order_by("resolution").desc().first()

    buffer = io.BytesIO()
    stream.stream_to_buffer(buffer)
    buffer.seek(0)

    return buffer.read()
