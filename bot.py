import discord
from discord import Message
from BotFunctions import GrabMemory
from BotFunctions import Gamble
from BotFunctions import Random
from BotFunctions import Help
from botToken import botToken
from BotFunctions import Lottery
from BotFunctions import Roulette

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

    if message.content.startswith('.free-points'):
        await Gamble.free_points(message)

    if message.content.startswith('.gamble'):
        await Gamble.gamble(message)

    if message.content.startswith('.points'):
        await Gamble.points(message)

    if message.content.startswith('.challenge'):
        await Gamble.challange(message)

    if message.content.startswith('.respond'):
        await Gamble.respond_challange(message)

    if message.content.startswith('.leaderboard'):
        await Gamble.leaderboard(message)

    if message.content.startswith('.grab-memory'):
        await GrabMemory.grab_memory(message)
    
    if message.content.startswith('.random'):
        await Random.randomizer(message)

    if message.content.startswith('.help'):
        await Help.help(message)

    if message.content.startswith('.lottery'):
        await Lottery.start_lottery(message)
    
    if message.content.startswith('.enter'):
        await Lottery.add_lottery_points(message)

    if message.content.startswith('.end-lottery'):
        await Lottery.end_lottery(message)

    if message.content.startswith('.roulette'):
        await Roulette.roulette(message)
    
    if message.content.startswith('.end-roulette'):
        await Roulette.end_roulette(message)
    

client.run(botToken)