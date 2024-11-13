import discord
from discord import Message
import random


async def randomizer(message: Message):

    phrases = message.content[len('.random'):].split(',')
    phrases = [phrase.strip() for phrase in phrases if phrase.strip()]

    if phrases:
        chosen_phrase = random.choice(phrases)
        await message.channel.send(f'{chosen_phrase}')

    else:
        await message.channel.send('Skriv ord efter .random.')