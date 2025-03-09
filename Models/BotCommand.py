from discord import Message
from typing import Callable, Optional, Awaitable

class BotCommand:
    command: str
    operation: Callable[[Optional[Message]], Optional[str]]
    explanation: str

    def __init__(
            self,
            command: str,
            explanation: str,
            operation: Callable[[Optional[Message]], Optional[str]],
            ):
        self.command = command
        self.operation = operation
        self.explanation = explanation

    async def execute(self, message: Message):
        result = self.operation(message)
        await self.handle_result(result, message)

    async def handle_result(self, result: Optional[str], message: Message):
        if result != None:
            await message.channel.send(result)



class AsyncBotCommand(BotCommand):
    asyncOperation: Callable[[Optional[Message]], Awaitable[Optional[str]]]

    def __init__(self,
                command: str,
                explanation: str,
                operation: Callable[[Optional[Message]], Awaitable[Optional[str]]]
                ):
        self.command = command
        self.explanation = explanation
        self.asyncOperation = operation

    async def execute(self, message):
        result = await self.asyncOperation(message)
        await self.handle_result(result, message)