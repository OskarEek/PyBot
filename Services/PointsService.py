import json

from Services import FileService


FILE_PATH = FileService.get_base_file_path() + "/Gamble/userpoints.json"

def get_user_points(userId: str) -> int:
    if FileService.create_file_if_not_exists(FILE_PATH, {}):
        return 0

    with open(FILE_PATH, 'r') as f:
        data = json.load(f)
        if userId in data:
            return data[userId]
        else:
            return 0

def store_user_points(userId: str, points: int):
    if FileService.create_file_if_not_exists(FILE_PATH, {userId : points}):
        return

    with open(FILE_PATH, 'r') as f:
        data = json.load(f)
    
    data[userId] = points

    with open(FILE_PATH, 'w') as f:
        json.dump(data, f)

def get_leaderboard_points() -> dict:
    if FileService.create_file_if_not_exists(FILE_PATH, {}):
        return {}

    with open(FILE_PATH, 'r') as f:
        data = json.load(f)
        return sorted(data.items(), key=lambda item: item[1], reverse=True)[:3]