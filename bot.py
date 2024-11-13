import discord
from discord import Message
from BotFunctions.GrabMemory import grab_memory
from botToken import botToken

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: Message):
    if message.author.bot:
        return

    if message.content.startswith('.test'):
        print(message.author)
        await message.channel.send("Working")
    
    if message.content.startswith('.expose'):
        pass

    if message.content.startswith('.grab-memory'):
        await grab_memory(message)





client.run(botToken)