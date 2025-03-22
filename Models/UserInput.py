import asyncio
from typing import Optional
from discord import Message, Guild

class UserInput:
    def input(self, input: str):
        pass

    def get_value(self):
        pass

    def validate(self) -> Optional[str]:
        pass


class StringInput(UserInput):
    _input: str

    def input(self, input: str):
        self._input = input

    def get_value(self):
        return self._input

    def validate(self) -> Optional[str]:
        return None

class IntegerInput(UserInput):
    _input: str

    def input(self, input: str):
        self._input = int(input)
    
    def get_value(self) -> int:
        return self._input
    
    def validate(self) -> Optional[str]:
        return None

class PointsInput(UserInput):
    _input: int
    _currentUserPoints: int

    def __init__(self, currentUserPoints: int):
        self._currentUserPoints = currentUserPoints

    def input(self, input: str):
        if input == "all":
            self._input = self._currentUserPoints
        else:
            self._input = int(input)

    def get_value(self) -> int:
        return self._input

    def validate(self) -> Optional[str]:
        if self._input <= 0:
            return "You did not enter a valid amount"
        if self._currentUserPoints < self._input:
            return f"You dont have enough points ({self._currentUserPoints})"
        return None


class UserIdInput(UserInput):
    _rawInput: str
    _input: str

    def input(self, input: str):
        self._rawInput = input
        self._input = self._rawInput.replace("@", "").replace(">", "").replace("<", "")

    def get_value(self) -> str:
        return self._input
    
    def validate(self) -> Optional[str]:
        if "@" not in self._rawInput or ">" not in self._rawInput or "<" not in self._rawInput:
            return "This does not seem to be a user"
        return None
    
