import json
import datetime

#Services
from Services import FileService

#Models
from Models.MessageData import MessageData

def get_archive_filename(id: int, created_at: datetime) -> str:
    year = str(created_at.year)
    month = str(created_at.month)
    date = f"{year}-{month}"
    return f"{FileService.get_base_file_path()}/Archives/{str(id)}/{date}.json"

def get_channel_sent_filename(channelId: int) -> str:
    return f"{FileService.get_base_file_path()}/SentMessages/{str(channelId)}.json"

def store_sent_messageId(messageId: str, file: str):
    FileService.create_file_if_not_exists(file)   

    with open(file, 'r') as f:
        messages = json.load(f)
    
    messages.append(messageId)
    
    with open(file, 'w') as f:
        json.dump(messages, f)

def store_archive_message(message: MessageData, file: str):
    FileService.create_file_if_not_exists(file)   

    with open(file, 'r') as f:
        messages = json.load(f)
    
    messages.append(message.to_dict())
    
    with open(file, 'w') as f:
        json.dump(messages, f)


def get_sent_messagesIds(file: str) -> list:
    FileService.create_file_if_not_exists(file)  # Ensure the file exists
    
    # Read the current list from the JSON file
    with open(file, 'r') as f:
        messages = json.load(f)
    
    return messages

def get_archive_messages(file_path: str) -> list[MessageData]:
    if FileService.count_items_in_folder(file_path) == 0:
        return []

    FileService.create_file_if_not_exists(file_path)

    with open(file_path, 'r') as f:
        data = json.load(f)
        messages = [MessageData.from_dict(data=item) for item in data]
        return messages