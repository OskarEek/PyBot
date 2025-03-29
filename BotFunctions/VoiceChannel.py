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

    if message.author.voice:
        channel = message.author.voice.channel
        client = await channel.connect()

        player = await YTDLSource.from_url(url=url, stream=True)
        print(player)
        client.play(player)
        
        
        