from datetime import datetime

class MessageData:
    id: str
    authorId: str
    authorName: str
    channelId: str
    hasAttachments: bool
    created_at: datetime

    def __init__(self, id: str, authorId: str, authorName: str, channelId: str, hasAttachments: bool, created_at: datetime):
        self.id = id
        self.authorId = authorId
        self.authorName = authorName
        self.channelId = channelId
        self.hasAttachments = hasAttachments
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "authorId": self.authorId,
            "authorName": self.authorName,
            "channelId": self.channelId,
            "hasAttachments": self.hasAttachments,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            authorId=data['authorId'],
            authorName=data['authorName'],
            channelId=data['channelId'],
            hasAttachments=data['hasAttachments'],
            created_at= datetime.strptime(data['created_at'], "%Y-%m-%d %H:%M:%S")
        )