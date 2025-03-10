import discord
from discord import Message
import random


def randomizer(message: Message) -> str:

    phrases = message.content[len('.random'):].split(',')
    phrases = [phrase.strip() for phrase in phrases if phrase.strip()]

    if phrases:
        chosen_phrase = random.choice(phrases)
        return f'{chosen_phrase}'

    else:
        return 'Write something after .random.'