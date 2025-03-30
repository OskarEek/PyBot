from discord import Message
import asyncio
import yt_dlp

from Models.YTDLSource import YTDLSource
from Models.UserInput import StringInput

from Services import UserInputService

async def play(message: Message):
    inputs = [StringInput()]
    inputs = UserInputService.get_user_input(message.content, inputs)
    url = inputs[0].get_value()

    if not "youtube.com/" in url:
        return "You need to enter a youtube link"
    if not message.author.voice:
        return "You need to be in a voice channel"

    player = await YTDLSource.from_url(url=url, stream=True)

    if player == None:
        return "Max 15 minute video"

    channel = message.author.voice.channel
    client = await channel.connect()

    def after_play(error):
        coro = client.disconnect()
        asyncio.run_coroutine_threadsafe(coro, client.loop)

    client.play(player, after=after_play)
        
        