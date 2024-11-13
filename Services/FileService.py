
import random
import os
import json
from datetime import datetime

from Models.MessageData import MessageData

BASE_FILE_PATH = "./DataFiles"

def create_file_if_not_exists(file_path: str):
    #Create directory
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Create file
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)
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
