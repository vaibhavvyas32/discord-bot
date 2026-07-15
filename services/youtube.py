import asyncio
import yt_dlp


YDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "noplaylist": True
}


def extract_audio_sync(query):

    with yt_dlp.YoutubeDL(
        YDL_OPTIONS
    ) as ydl:

        info = ydl.extract_info(
            query,
            download=False
        )

        if "entries" in info:

            if not info["entries"]:
                raise ValueError(
                    "No YouTube results found."
                )

            info = info["entries"][0]

        return {
            "title": info.get(
                "title",
                "Unknown"
            ),

            "url": info["url"],

            "webpage_url": info.get(
                "webpage_url"
            ),

            "duration": info.get(
                "duration"
            ),

            "thumbnail": info.get(
                "thumbnail"
            ),

            "uploader": info.get(
                "uploader"
            )
        }


async def extract_audio(query):

    return await asyncio.to_thread(
        extract_audio_sync,
        query
    )