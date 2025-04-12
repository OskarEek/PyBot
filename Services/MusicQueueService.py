from typing import Optional
from Services import FileService

def fetch_queue(voicechannelId: str) -> list[str]:
    filePath = FileService.get_music_queue_file_path(voicechannelId)
    data = FileService.get_file_data(filePath)
    if data != None:
        return data["queue"]
    else:
        return []

def queue_link(voiceChannelId: str, link: str):
    filePath = FileService.get_music_queue_file_path(voiceChannelId)
    data = FileService.get_file_data(filePath)
    if data != None:
        queue: list[str] = data["queue"]
        queue.append(link)
        data["queue"] = queue
    else:
        data = {"queue": [link]}
    FileService.store_file_data(filePath, data)

def dequeue_first_link(voiceChannelId: str):
    filePath = FileService.get_music_queue_file_path(voiceChannelId)
    data = FileService.get_file_data(filePath)
    if data == None:
        return
    
    queue: list[str] = data["queue"]
    if len(queue > 0):
        queue.pop(0)

    data["queue"] = queue
    FileService.store_file_data(filePath, data)

def get_first_link(voiceChannelId: str) -> Optional[str]:
    filePath = FileService.get_music_queue_file_path(voiceChannelId)
    data = FileService.get_file_data(filePath)
    if data == None:
        return None
    
    queue: list[str] = data["queue"]
    if len(queue > 0):
        return queue[0]
    else:
        return None