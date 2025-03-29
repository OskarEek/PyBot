import discord
import yt_dlp
from yt_dlp import YoutubeDL
import asyncio


ytdl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
}

ytdl: YoutubeDL = yt_dlp.YoutubeDL(ytdl_opts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, stream=False):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url=url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        
        audio_url = None
        for fmt in data.get('formats', []):
            if fmt.get('acodec') != 'none':  # Ensure format contains an audio codec
                audio_url = fmt.get('url')
                break  # Select the first valid audio format

        if not audio_url:
            raise Exception("No valid audio stream found!")
        #filename = data['url'] if stream else ytdl.prepare_filename(data)
        ffmpeg_opts = {
            'options': '-vn',
        }
        return cls(discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts), data=data)