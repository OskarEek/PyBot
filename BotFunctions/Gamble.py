from discord import Message
import random
import time
import config

from Models.UserInput import UserIdInput, PointsInput

from Services import FileService
from Services import PointsService
from Services import ChallangeService
from Services import UserInputService

FREE_POINTS_COOLDOWN = 5 #Minutes

def free_points(message: Message):
    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)
    currentTime = time.time()

    if currentPoints > 0:
        return "You already have: " + str(currentPoints) + " points"

    if user_in_lottery(userId):
        return "You cant get free points while in a lottery"

    if user_in_roulette(userId):
        return "You cant get free points while in a roulette"
    
    cooldowns = FileService.get_cooldowns()
    if not config.debug and userId in cooldowns:
        time_since_last_use = currentTime - cooldowns[userId]
        if time_since_last_use < FREE_POINTS_COOLDOWN * 60:  # 15 minutes in seconds
            remaining_time = FREE_POINTS_COOLDOWN * 60 - time_since_last_use
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            return f"You can claim free points again in {minutes} minutes and {seconds} seconds."

    PointsService.store_user_points(userId, 500)
    cooldowns[userId] = currentTime
    FileService.save_cooldowns(cooldowns)
    return "500 points were given to: " + message.author.global_name

def points(message: Message) -> str:
    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)
    botContent = message.author.global_name + " has " + str(currentPoints) + " points."
    if currentPoints <= 0:
        botContent += "\n Run \".free-points\" to get some free points"
    return botContent

def gamble(message: Message) -> str:
    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)

    inputs = [PointsInput(currentPoints)]
    inputs = UserInputService.get_user_input(message.content, inputs)

    pointsToGamble = inputs[0].get_value()

    x = random.randint(0, 1)
    if x == 1:
        result = currentPoints + pointsToGamble
        PointsService.store_user_points(userId, result)
        return f"{message.author.global_name} won {pointsToGamble}!, he now have {result} points"
    else:
        result = currentPoints - pointsToGamble
        PointsService.store_user_points(userId, result)
        return f"{message.author.global_name} lost {pointsToGamble} points, he now have {result} points"   


def challange(message: Message) -> str:
    userId = str(message.author.id)

    currentPoints = PointsService.get_user_points(userId)

    inputs = [UserIdInput(), PointsInput(currentPoints)]
    inputs = UserInputService.get_user_input(message.content, inputs)
    opponentId: str = inputs[0].get_value()
    pointsToGamble: int = inputs[1].get_value()

    existingChallange = ChallangeService.get_challange(opponentId=userId, creatorId=opponentId)
    if existingChallange != None:
        points = existingChallange['points']
        return f"<@{opponentId}> has already challanged you to a bet, he bet you: {points} points"

    ChallangeService.store_challange(userId, opponentId=opponentId, points=pointsToGamble)

def respond_challange(message: Message) -> str:
    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)

    inputs = [UserIdInput(), PointsInput(currentPoints)]
    inputs = UserInputService.get_user_input(message.content, inputs)
    creatorId: str = inputs[0].get_value()
    pointsToGamble: int = inputs[1].get_value()

    challange = ChallangeService.get_challange(userId, creatorId=creatorId)
    if challange == None:
        return f"<@{creatorId}> has not challanged you to any bets"

    creatorPointsToGamble = challange['points']
    creatorCurrentPoints = PointsService.get_user_points(creatorId)

    if creatorCurrentPoints < creatorPointsToGamble:
        ChallangeService.remove_challange(userId, creatorId=creatorId)
        return f"This bet is no longer available, <@{creatorId}> bet {creatorPointsToGamble} points but only has {creatorCurrentPoints} right now."

    totalPoints = creatorPointsToGamble + pointsToGamble
    winChance = (pointsToGamble / totalPoints) * 100
    x = random.randint(0, 99)
    returnMessage: str
    if x < winChance:
       result = currentPoints + creatorPointsToGamble
       creatorResult = creatorCurrentPoints - creatorPointsToGamble
       PointsService.store_user_points(userId, result)
       PointsService.store_user_points(creatorId, creatorResult)
       returnMessage = f"<@{userId}> wins {creatorPointsToGamble} points from <@{creatorId}> with a win chance of {winChance}%"
    else:
       result = currentPoints - pointsToGamble
       creatorResult = creatorCurrentPoints + pointsToGamble
       PointsService.store_user_points(userId, result)
       PointsService.store_user_points(creatorId, creatorResult)
       returnMessage = f"<@{creatorId}> wins {pointsToGamble} points from <@{userId}> with a win chance of {100 - winChance}%"
       
    ChallangeService.remove_challange(userId, creatorId=creatorId)
    return returnMessage
        

async def leaderboard(message: Message):
    topThree = PointsService.get_leaderboard_points()
    content = ""
    i = 1
    for key, value in topThree:
        user = await message.guild.fetch_member(int(key))
        content += f"**{i}**. {user.global_name} {value} points \n"
        i += 1

    await message.channel.send(content)








#======Helper functions=====================================================
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