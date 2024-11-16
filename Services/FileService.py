
import random
import os
import json
from datetime import datetime

from Models.MessageData import MessageData

BASE_FILE_PATH = "./DataFiles"

def get_base_file_path():
    return BASE_FILE_PATH

def store_file_data(file_path: str, data):
    if create_file_if_not_exists(file_path, data):
        return
    with open(file_path, 'w') as f:
        json.dump(data, f)

def get_file_data(file_path: str):
    if not file_exists(file_path):
        return None
    with open(file_path, 'r') as f:
        return json.load(f)

def file_exists(file_path: str):
    if os.path.exists(file_path):
        return True
    return False

def create_file_if_not_exists(file_path: str, data = None):
    #Create directory
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Create file
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            if data == None:
                json.dump([], f)
            else:
                json.dump(data, f)
            return True
    else:
        return False

def store_sent_messageId(messageId: str, file: str):
    create_file_if_not_exists(file)   

    with open(file, 'r') as f:
        messages = json.load(f)
    
    messages.append(messageId)
    
    with open(file, 'w') as f:
        json.dump(messages, f)

def store_archive_message(message: MessageData, file: str):
    create_file_if_not_exists(file)   

    with open(file, 'r') as f:
        messages = json.load(f)
    
    messages.append(message.to_dict())
    
    with open(file, 'w') as f:
        json.dump(messages, f)

def id_exists_in_file(messageId: str, file: str) -> bool:
    create_file_if_not_exists(file)

    with open(file, 'r') as f:
        messages = json.load(f)
    
    return messageId in [x.id for x in messages]

def get_sent_messagesIds(file: str) -> list:
    create_file_if_not_exists(file)  # Ensure the file exists
    
    # Read the current list from the JSON file
    with open(file, 'r') as f:
        messages = json.load(f)
    
    return messages

def get_archive_messages(file_path: str):
    if count_items_in_folder(file_path) == 0:
        return []

    create_file_if_not_exists(file_path)

    with open(file_path, 'r') as f:
        data = json.load(f)
        messages = [MessageData.from_dict(data=item) for item in data]
        return messages

def store_user_points(userId: str, points: int):
    file = get_user_points_filename()
    if create_file_if_not_exists(file, {userId : points}):
        return

    with open(file, 'r') as f:
        data = json.load(f)
    
    data[userId] = points

    with open(file, 'w') as f:
        json.dump(data, f)

def get_user_points(userId: str):
    file = get_user_points_filename()
    if create_file_if_not_exists(file, {}):
        return 0

    with open(file, 'r') as f:
        data = json.load(f)
        if userId in data:
            return data[userId]
        else:
            return 0
            
def get_leaderboard_points():
    file = get_user_points_filename()
    if create_file_if_not_exists(file, {}):
        return []

    with open(file, 'r') as f:
        data = json.load(f)
        return sorted(data.items(), key=lambda item: item[1], reverse=True)[:3]

def store_challange(creatorId: str, opponentId: str, points: int):
    file = get_challange_filename()
    create_file_if_not_exists(file, {})

    with open(file, 'r') as f:
        data = json.load(f)

    challanges = []
    if opponentId in data:
        challanges = data[opponentId]
    
    for d in challanges:
        if d["creatorId"] == creatorId:
            challanges.remove(d)
            break  # Exit loop after 

    challanges.append({"creatorId": creatorId, "points": points})
    data[opponentId] = challanges

    with open(file, 'w') as f:
        json.dump(data, f)

def get_challange(opponentId: str, creatorId: str):
    file = get_challange_filename()
    if create_file_if_not_exists(file, {}):
        return None
    
    with open(file, 'r') as f:
        data = json.load(f)

    challanges = []
    if opponentId in data:
        challanges = data[opponentId]

    for d in challanges:
        if d["creatorId"] == creatorId:
            return d

    return None

def remove_challange(opponentId: str, creatorId: str):
    file = get_challange_filename()
    if create_file_if_not_exists(file, {}):
        return

    with open(file, 'r') as f:
        data = json.load(f)

    challanges = []
    if opponentId in data:
        challanges = data[opponentId]
    
    for d in challanges:
        if d["creatorId"] == creatorId:
            challanges.remove(d)
            break

    data[opponentId] = challanges

    with open(file, 'w') as f:
        json.dump(data, f)
    
def count_items_in_folder(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        return 0
    
    return len(os.listdir(directory))

def get_file_by_index(index, file_path):
    directory = os.path.dirname(file_path)

    files = os.listdir(directory)
    
    return os.path.join(directory, files[index])


def get_archive_filename(id: int, fileName: datetime):
    year = str(fileName.year)
    month = str(fileName.month)
    date = f"{year}-{month}"
    return f"{BASE_FILE_PATH}/Archives/{str(id)}/{date}.json"

def get_channel_sent_filename(id: int):
    return f"{BASE_FILE_PATH}/SentMessages/{str(id)}.json"


def get_user_points_filename():
    return f"{BASE_FILE_PATH}/Gamble/userpoints.json"

def get_challange_filename():
    return f"{BASE_FILE_PATH}/Gamble/challanges.json"

def get_lottery_file_path():
    return f"{BASE_FILE_PATH}/Lottery/lottery.json"