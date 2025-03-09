
import random
import os
import json
from datetime import datetime

BASE_FILE_PATH = "./DataFiles"

def get_base_file_path() -> str:
    return BASE_FILE_PATH

def store_file_data(file_path: str, data):
    if create_file_if_not_exists(file_path, data):
        return
    with open(file_path, 'w') as f:
        json.dump(data, f)

def get_file_data(file_path: str) -> dict:
    if not file_exists(file_path):
        return None
    with open(file_path, 'r') as f:
        return json.load(f)

def file_exists(file_path: str) -> bool:
    if os.path.exists(file_path):
        return True
    return False

def create_file_if_not_exists(file_path: str, data = None) -> bool:
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


def count_items_in_folder(file_path) -> int:
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        return 0
    
    return len(os.listdir(directory))

def get_file_by_index(index, file_path) -> str:
    directory = os.path.dirname(file_path)

    files = os.listdir(directory)
    
    return os.path.join(directory, files[index])

#def id_exists_in_file(messageId: str, file: str) -> bool:
#    create_file_if_not_exists(file)
#
#    with open(file, 'r') as f:
#        messages = json.load(f)
#    
#    return messageId in [x.id for x in messages]

def get_lottery_file_path() -> str:
    return f"{BASE_FILE_PATH}/Lottery/lottery.json"

def get_cooldown_file_path() -> str:
    return f"{BASE_FILE_PATH}/Gamble/cooldowns.json"

def get_roulette_file_path() -> str:
    return f"{BASE_FILE_PATH}/Roulette/roulette.json"

def get_cooldowns() -> dict:
    file = get_cooldown_file_path()

    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_cooldowns(cooldowns):
    file = get_cooldown_file_path()
    if create_file_if_not_exists(file, cooldowns):
        return
    with open(file, "w") as f:
        json.dump(cooldowns, f)