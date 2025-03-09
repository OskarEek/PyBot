import json

from Services import FileService

FILE_PATH = FileService.get_base_file_path() + "/Gamble/challanges.json"

def store_challange(creatorId: str, opponentId: str, points: int):
    FileService.create_file_if_not_exists(FILE_PATH, {})

    with open(FILE_PATH, 'r') as f:
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

    with open(FILE_PATH, 'w') as f:
        json.dump(data, f)

def get_challange(opponentId: str, creatorId: str) -> dict:
    if FileService.create_file_if_not_exists(FILE_PATH, {}):
        return None
    
    with open(FILE_PATH, 'r') as f:
        data = json.load(f)

    challanges = []
    if opponentId in data:
        challanges = data[opponentId]

    for d in challanges:
        if d["creatorId"] == creatorId:
            return d

    return None

def remove_challange(opponentId: str, creatorId: str):
    if FileService.create_file_if_not_exists(FILE_PATH, {}):
        return

    with open(FILE_PATH, 'r') as f:
        data = json.load(f)

    challanges = []
    if opponentId in data:
        challanges = data[opponentId]
    
    for d in challanges:
        if d["creatorId"] == creatorId:
            challanges.remove(d)
            break

    data[opponentId] = challanges

    with open(FILE_PATH, 'w') as f:
        json.dump(data, f)