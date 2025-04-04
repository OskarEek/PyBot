from discord import Message
from datetime import datetime, timedelta
import random

from Models.UserInput import PointsInput

from Services import FileService
from Services import PointsService
from Services import UserInputService

async def start_lottery(message: Message):
    if ongoing_lottery():
        await message.delete()
        return "There is already an ongoing lottery"

    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)

    inputs = [PointsInput(currentPoints)]
    inputs = UserInputService.get_user_input(message.content, inputs)
    poinstToGamble = inputs[0].get_value()

    file_path = FileService.get_lottery_file_path()

    entries = [{"userId": userId ,"username": message.author.global_name, "points": poinstToGamble}]
    calculate_winchance_percentages(entries)
    data = {
        "lotteryMessageId": "",
        "entries": entries,
        "creatorId": userId,
        "startTime": datetime.now().isoformat()
    }
    FileService.store_file_data(file_path, data)

    #Remove points
    PointsService.store_user_points(userId, currentPoints - poinstToGamble)

    await update_lottery_message(message)
    await message.delete()

async def add_lottery_points(message: Message):
    if not ongoing_lottery():
        return "There is no ongoing lottery"

    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)
        
    inputs = [PointsInput(currentPoints)]
    inputs = UserInputService.get_user_input(message.content, inputs)
    poinstToGamble = inputs[0].get_value()

    file_path = FileService.get_lottery_file_path()
    data = FileService.get_file_data(file_path)
    entries: list[dict] = data["entries"]

    userEntryExists = False
    for userEntry in entries:
        if userEntry["userId"] == userId:
            userEntry["points"] = userEntry["points"] + poinstToGamble
            userEntryExists = True
            break
        
    if not userEntryExists:
        entries.append({"userId": userId ,"username": message.author.global_name, "points": poinstToGamble})

    calculate_winchance_percentages(entries)
    data["entries"] = entries
    FileService.store_file_data(file_path, data)

    PointsService.store_user_points(userId, currentPoints - poinstToGamble)
    await update_lottery_message(message)
    await message.delete()


def end_lottery(message: Message) -> str:
    if not ongoing_lottery():
        return "There is no ongoing lottery"
    
    userId = str(message.author.id)
    file_path = FileService.get_lottery_file_path()

    data = FileService.get_file_data(file_path)
    creatorId = data["creatorId"]
    isoTime = data["startTime"]
    startTime = datetime.fromisoformat(isoTime)
    endTime = startTime + timedelta(minutes=5)

    minutes = 0
    seconds = 0
    now = datetime.now()
    if endTime > now:
        time_difference = endTime - now
        total_seconds = time_difference.total_seconds()

        minutes = total_seconds // 60
        seconds = total_seconds % 60

    if creatorId != userId:
        if minutes != 0 and seconds != 0:
            return f"Only the creator can end this lottery early.\n Anybody will be able to end the lottery after: {minutes} minutes and {seconds} seconds"

    entries = data["entries"]
    ids = [userEntry["userId"] for userEntry in entries]
    win_chances = [userEntry["winChance"] for userEntry in entries]
    winnerId = random.choices(ids, weights=win_chances, k=1)[0]

    totalPoints = get_total_lottery_points(entries)
    currentPoints = PointsService.get_user_points(winnerId)
    PointsService.store_user_points(winnerId, currentPoints + totalPoints)

    FileService.store_file_data(file_path, {})

    i = ids.index(winnerId)
    winChance = win_chances[i] * 100
    return f"<@{winnerId}> is the winner of the Lottery with a win percentage of {winChance}%!\nTotal: {totalPoints} points"









#=====Helper functions==========================================
def calculate_winchance_percentages(entries: list):
    totalPoints = get_total_lottery_points(entries)
    for userEntry in entries:
        points = userEntry["points"]
        userEntry["winChance"] = points / totalPoints

async def update_lottery_message(message: Message):
    file_path = FileService.get_lottery_file_path()
    data = FileService.get_file_data(file_path)
    entries = data["entries"]

    botContent = "Lottery:\n"
    botContent += "```"
    for userEntry in entries:
        username = userEntry["username"]
        points = userEntry["points"]
        winChance = userEntry["winChance"] * 100
        botContent += f"    {username}: {points} points   |   {winChance}%\n"
    botContent += "```"

    currentMessageId = data["lotteryMessageId"]
    update = False
    if currentMessageId == "":
        newLotteryMessage = await message.channel.send(botContent)
        data["lotteryMessageId"] = str(newLotteryMessage.id)
        update = True
    else:
        lotteryMessage = await message.channel.fetch_message(int(data["lotteryMessageId"]))
        if lotteryMessage != None:
            await lotteryMessage.edit(content=botContent)
        else:
            newLotteryMessage = await message.channel.send(botContent)
            data["lotteryMessageId"] = str(newLotteryMessage.id)
            update = True
    
    if update:
        FileService.store_file_data(file_path, data)
    


def ongoing_lottery():
    file_path = FileService.get_lottery_file_path()
    data = FileService.get_file_data(file_path)
    if data == None:
        return False
    if len(data) > 0:
        return True
    return False

def get_total_lottery_points(entries: list):
    return sum(userEntry["points"] for userEntry in entries)

