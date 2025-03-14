from typing import Optional
from Models.UserInput import UserInput

class UserInputResult:
    userInputs: list[UserInput]
    validationError: Optional[str]

    def __init__(self, userInputs: list[UserInput] = [], validationError: Optional[str] = None):
        self.userInputs = userInputs
        self.validationError = validationError