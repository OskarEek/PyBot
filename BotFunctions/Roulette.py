from discord import Message
import random
import time
from Services import FileService
from Services import PointsService
from datetime import datetime, timedelta

WIDTH = 7 

MIDDLE_SYMBOL = ":large_orange_diamond:"
BOARDER_SYMBOL = ":fog:"
BLACK_SYMBOL = ":black_large_square:"
RED_SYMBOL = ":red_square:"
GREEN_SYMBOL = ":green_square:"

async def roulette(message: Message):
    try:
        userId = str(message.author.id)
        color = message.content.split(" ")[1].lower()
        points = message.content.split(" ")[2].lower()
        if color not in ["red", "black", "green"]:
            raise Exception("Invalid input")

        pointsToGamble = 0
        currentPoints = PointsService.get_user_points(userId)

        if points == "all":
            if currentPoints == 0:
                await message.channel.send("You dont have any points to gamble")
                return
            pointsToGamble = currentPoints
        else:
            pointsToGamble = int(points)

        if pointsToGamble <= 0:
            raise Exception("Invalid value")

        if currentPoints < pointsToGamble:
            await message.channel.send(f"You dont have enough points ({currentPoints})")
            return

        if not ongoing_roulette():
            start_roulette(userId, message.author.global_name, color, pointsToGamble)
        else:
            file_path = FileService.get_roulette_file_path()
            data = FileService.get_file_data(file_path)
            entries: list[dict] = data["entries"]

            userEntryExists = False
            for userEntry in entries:
                if userEntry["userId"] == userId and userEntry["color"] == color:
                    userEntry["points"] = userEntry["points"] + pointsToGamble
                    userEntryExists = True
                    break

            if not userEntryExists:
                entries.append({"userId": userId ,"username": message.author.global_name, "color": color, "points": pointsToGamble})

            data["entries"] = entries
            FileService.store_file_data(file_path, data)

        PointsService.store_user_points(userId, currentPoints - pointsToGamble)
        await message.delete()
        await update_roulette_message(message)
    except:
        await message.channel.send("Wrong syntax")

def start_roulette(userId: str, userName:str, color: str, points: int):
        file_path = FileService.get_roulette_file_path()

        entries = [{"userId": userId ,"username": userName, "points": points, "color": color}]
        data = {
            "rouletteMessageId": "",
            "entries": entries,
            "creatorId": userId,
            "startTime": datetime.now().isoformat()
        }
        FileService.store_file_data(file_path, data)


async def end_roulette(message: Message):
    userId = str(message.author.id)
    file_path = FileService.get_roulette_file_path()

    data = FileService.get_file_data(file_path)
    creatorId = data["creatorId"]
    isoTime = data["startTime"]
    startTime = datetime.fromisoformat(isoTime)
    endTime = startTime + timedelta(minutes=1)

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
            await message.channel.send(f"Only the creator can end this roulette early.\n Anybody will be able to end the lottery after: {minutes} minutes and {seconds} seconds")
            return

    half: int = int((WIDTH - 1)/2)
    middle = half 

    topRowList = [BOARDER_SYMBOL for i in range(0, half)]
    topRowList.append(MIDDLE_SYMBOL)
    topRowList.extend([BOARDER_SYMBOL for i in range(0, half)])
    topRow = " ".join(topRowList)

    playingCards = [GREEN_SYMBOL, RED_SYMBOL, BLACK_SYMBOL, RED_SYMBOL, BLACK_SYMBOL,
                    RED_SYMBOL, BLACK_SYMBOL, RED_SYMBOL, BLACK_SYMBOL, RED_SYMBOL,
                    BLACK_SYMBOL,RED_SYMBOL, BLACK_SYMBOL, RED_SYMBOL, BLACK_SYMBOL] 

    startingPoint = random.randint(0, len(playingCards)) 

    middleRowList = generate_middle_row(startingPoint, playingCards)
    middleRow = " ".join(middleRowList)

    bottomRowList = [BOARDER_SYMBOL for i in range(0, WIDTH)]
    bottomRow = " ".join(bottomRowList)
    
    topMessage = await message.channel.send(topRow)
    middleMessage = await message.channel.send(middleRow)
    bottomMessage = await message.channel.send(bottomRow)

    numberOfLoops = random.randint(6, 20)
    speed = 0.2
    endSpeed = 1.5
    for i in range(1, numberOfLoops):
        if numberOfLoops - i <= 4:
            speed += endSpeed / 4
        time.sleep(speed)
        middleRowList = generate_middle_row(startingPoint + i, playingCards)
        middleRow = " ".join(middleRowList)
        await middleMessage.edit(content=middleRow)
        

    winColor = ""
    if middleRowList[middle] == RED_SYMBOL:
        winColor = "red"
        title = "Red Won!"
    elif middleRowList[middle] == BLACK_SYMBOL:
        winColor = "black"
        title = "Black Won!"
    else:
        winColor = "green"
        title = "Green Won!"

    winMessage = title + "\n"
    entries = data["entries"]
    winEntries = [x for x in entries if x["color"] == winColor]
    for entry in winEntries:
        userId = entry["userId"]
        username = entry["username"]
        points = entry["points"]
        result = points * 2 if winColor != "green" else points * 14
        currentPoints = PointsService.get_user_points(userId)
        PointsService.store_user_points(userId, currentPoints + result)
        winMessage += f"    {username} won {result} points\n"

    await message.channel.send(winMessage)

    FileService.store_file_data(file_path, {})

    time.sleep(5)

    await topMessage.delete()
    await middleMessage.delete()
    await bottomMessage.delete()




def generate_middle_row(startPoint: int, playingCards: list) -> list:
    middleRow = [BOARDER_SYMBOL]
    for i in range(0, WIDTH-2):
        listIndex = startPoint + i
        listIndex = listIndex % len(playingCards)
        middleRow.append(playingCards[listIndex])
    
    middleRow.append(BOARDER_SYMBOL)
    return middleRow



def ongoing_roulette():
    file_path = FileService.get_roulette_file_path()
    data = FileService.get_file_data(file_path)
    if data == None:
        return False
    if len(data) > 0:
        return True
    return False

async def update_roulette_message(message: Message):
    file_path = FileService.get_roulette_file_path()
    data = FileService.get_file_data(file_path)
    entries = data["entries"]

    redList = [x for x in entries if x["color"] == "red"]
    blackList = [x for x in entries if x["color"] == "black"]
    greenList = [x for x in entries if x["color"] == "green"]
    pointsDict = {
        "Red": redList,
        "Black": blackList,
        "Green": greenList
    }

    botContent = "Roulette:\n"
    botContent += "```"
    for key in pointsDict:
        botContent += f"    {key}:\n"
        for userEntry in pointsDict[key]:
            username = userEntry["username"]
            points = userEntry["points"]
            botContent += f"        {username}: {points} points\n"
        botContent += "\n"
    botContent += "```"

    currentMessageId = data["rouletteMessageId"]
    update = False
    if currentMessageId == "":
        newLotteryMessage = await message.channel.send(botContent)
        data["rouletteMessageId"] = str(newLotteryMessage.id)
        update = True
    else:
        lotteryMessage = await message.channel.fetch_message(int(data["rouletteMessageId"]))
        if lotteryMessage != None:
            await lotteryMessage.edit(content=botContent)
        else:
            newLotteryMessage = await message.channel.send(botContent)
            data["rouletteMessageId"] = str(newLotteryMessage.id)
            update = True
    
    if update:
        FileService.store_file_data(file_path, data)