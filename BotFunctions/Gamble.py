import discord
from discord import Message
import random
import time

from Services import FileService
from Services import PointsService
from Services import ChallangeService

FREE_POINTS_COOLDOWN = 5 #Minutes

TEST = False

async def free_points(message: Message):
    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)
    currentTime = time.time()

    if currentPoints > 0:
        await message.channel.send("You already have: " + str(currentPoints) + " points")
        return

    if user_in_lottery(userId):
        await message.channel.send("You cant get free points while in a lottery")
        return

    if user_in_roulette(userId):
        await message.channel.send("You cant get free points while in a roulette")
        return
    
    cooldowns = FileService.get_cooldowns()
    if not TEST and userId in cooldowns:
        time_since_last_use = currentTime - cooldowns[userId]
        if time_since_last_use < FREE_POINTS_COOLDOWN * 60:  # 15 minutes in seconds
            remaining_time = FREE_POINTS_COOLDOWN * 60 - time_since_last_use
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            await message.channel.send(f"You can claim free points again in {minutes} minutes and {seconds} seconds.")
            return

    PointsService.store_user_points(userId, 500)
    cooldowns[userId] = currentTime
    FileService.save_cooldowns(cooldowns)
    await message.channel.send("500 points were given to: " + message.author.global_name)

async def points(message: Message):
    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)
    botContent = message.author.global_name + " has " + str(currentPoints) + " points."
    if currentPoints <= 0:
        botContent += "\n Run \".free-points\" to get some free points"
    await message.channel.send(botContent)

async def gamble(message: Message):
    userId = str(message.author.id)
    try:
        userInput = message.content.split(" ")[-1]
        poinstToGamble = 0
        currentPoints = PointsService.get_user_points(userId)

        if userInput == "all":
            if currentPoints == 0:
                await message.channel.send("You dont have any points to gamble")
                return
            poinstToGamble = currentPoints
        else:
            poinstToGamble = int(userInput)

        if poinstToGamble <= 0:
            raise Exception("Invalid value")

        if currentPoints < poinstToGamble:
            await message.channel.send(f"You dont have enough points ({currentPoints})")
            return

        x = random.randint(0, 1)
        if x == 1:
            result = currentPoints + poinstToGamble
            PointsService.store_user_points(userId, result)
            await message.channel.send(f"{message.author.global_name} won {poinstToGamble}!, he now have {result} points")
        else:
            result = currentPoints - poinstToGamble
            PointsService.store_user_points(userId, result)
            await message.channel.send(f"{message.author.global_name} lost {poinstToGamble} points, he now have {result} points")

    except:
        await message.channel.send("You did not enter a valid amount")


async def challange(message: Message):
    userId = str(message.author.id)
    userInputs = message.content.split(" ")
    try:
        opponentId = userInputs[1].replace("@", "").replace(">", "").replace("<", "")
        pointsToGambleInput = userInputs[2]

        currentPoints = PointsService.get_user_points(userId)

        pointsToGamble = 0
        if currentPoints == 0:
            await message.channel.send("You dont have any points to gamble")
            return
        else:
            pointsToGamble = int(pointsToGambleInput)

        if pointsToGamble <= 0:
            raise Exception("Invalid value")

        if currentPoints < pointsToGamble:
            await message.channel.send(f"You dont have enough points ({currentPoints})")
            return

        existingChallange = PointsService.get_challange(opponentId=userId, creatorId=opponentId)
        if existingChallange != None:
            points = existingChallange['points']
            await message.channel.send(f"<@{opponentId}> has already challanged you to a bet, he bet you: {points} points")
            return

        ChallangeService.store_challange(userId, opponentId=opponentId, points=pointsToGamble)
    except:
        await message.channel.send("Wrong syntax")

async def respond_challange(message: Message):
    userId = str(message.author.id)
    userInputs = message.content.split(" ")

    try:
        creatorId = userInputs[1].replace("@", "").replace(">", "").replace("<", "")
        pointsToGambleInput = int(userInputs[2])

        currentPoints = PointsService.get_user_points(userId)

        pointsToGamble = 0
        if currentPoints == 0:
            await message.channel.send("You dont have any points to gamble")
            return
        else:
            pointsToGamble = int(pointsToGambleInput)

        if pointsToGamble <= 0:
            raise Exception("Invalid value")

        if currentPoints < pointsToGamble:
            await message.channel.send(f"You dont have enough points ({currentPoints})")
            return

        challange = ChallangeService.get_challange(userId, creatorId=creatorId)

        if challange == None:
            await message.channel.send(f"<@{creatorId}> has not challanged you to any bets")
            return

        creatorPointsToGamble = challange['points']
        creatorCurrentPoints = PointsService.get_user_points(creatorId)

        if creatorCurrentPoints < creatorPointsToGamble:
            await message.channel.send(f"This bet is no longer available, <@{creatorId}> bet {creatorPointsToGamble} points but only has {creatorCurrentPoints} right now.")
            ChallangeService.remove_challange(userId, creatorId=creatorId)
            return

        totalPoints = creatorPointsToGamble + pointsToGamble
        winChance = (pointsToGamble / totalPoints) * 100
        x = random.randint(0, 99)
        if x < winChance:
           result = currentPoints + creatorPointsToGamble
           creatorResult = creatorCurrentPoints - creatorPointsToGamble
           PointsService.store_user_points(userId, result)
           PointsService.store_user_points(creatorId, creatorResult)
           await message.channel.send(f"<@{userId}> wins {creatorPointsToGamble} points from <@{creatorId}> with a win chance of {winChance}%")
        else:
           result = currentPoints - pointsToGamble
           creatorResult = creatorCurrentPoints + pointsToGamble
           PointsService.store_user_points(userId, result)
           PointsService.store_user_points(creatorId, creatorResult)
           await message.channel.send(f"<@{creatorId}> wins {pointsToGamble} points from <@{userId}> with a win chance of {100 - winChance}%")
           

        ChallangeService.remove_challange(userId, creatorId=creatorId)
    except:
        await message.channel.send("Wrong syntax")
        

async def leaderboard(message: Message):
    topThree = PointsService.get_leaderboard_points()
    content = ""
    i = 1
    for key, value in topThree:
        user = await message.guild.fetch_member(int(key))
        content += f"**{i}**. {user.global_name} {value} points \n"
        i += 1

    await message.channel.send(content)

def user_in_lottery(userId: str):
    file_path = FileService.get_lottery_file_path()
    data = FileService.get_file_data(file_path)

    if data == None or len(data) == 0:
        return False

    entries = data["entries"]
    for userEntry in entries:
        if userEntry["userId"] == userId:
            return True
    
    return False

def user_in_roulette(userId: str):
    file_path = FileService.get_roulette_file_path()
    data = FileService.get_file_data(file_path)

    if data == None or len(data) == 0:
        return False

    entries = data["entries"]
    for userEntry in entries:
        if userEntry["userId"] == userId:
            return True
    
    return False