from discord import Message
import asyncio
import yt_dlp

from Models.YTDLSource import YTDLSource
from Models.UserInput import StringInput

from Services import MusicQueueService

from Services import UserInputService

async def play(message: Message):
    inputs = [StringInput()]
    inputs = UserInputService.get_user_input(message.content, inputs)
    url = inputs[0].get_value()

    if not "youtube.com/" in url:
        return "You need to enter a youtube link"
    if not message.author.voice:
        return "You need to be in a voice channel"

    channel = message.author.voice.channel
    channelId = str(channel.id)

    queue: list[str] = MusicQueueService.fetch_queue(channelId)

    if len(queue) >= 10:
        return "Queue is full"

    MusicQueueService.queue_link(channelId, url)

    if len(queue) == 0:
        print("Queue is empty, joining voice channel")
        client = await channel.connect()
    else:
        return "Link queued"
    
    def after_play(error):
        queue = MusicQueueService.fetch_queue(channelId)
        if len(queue) > 0:
            return
        coro = client.disconnect()
        asyncio.run_coroutine_threadsafe(coro, client.loop)

    while len(queue) > 0:
        link = MusicQueueService.get_first_link()
        print("Getting first link from queue: " + link)

        if link == None:
            return "No links in queue"

        player = await YTDLSource.from_url(url=link, stream=True)

        if player == None:
            await message.channel.send(f"Max 15 minute video, skipping {link}")
            continue

        link = MusicQueueService.dequeue_first_link(channelId)

        client.play(player, after=after_play)