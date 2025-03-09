import discord
from discord import Message
from botToken import botToken
from botCommands import botCommands

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
    
    command = get_command(message.content)
    botCommand = botCommands[command]

    await botCommand.execute(message)
    

def get_command(messageContent: str) -> str:
    result = messageContent.split(" ")[-1]
    return result if not result == None else ""

client.run(botToken)

