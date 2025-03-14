from discord import Message


from Services import PointsService
from Models.UserInput import UserInput
from Models.UserInputResult import UserInputResult


def get_user_input(messageContent: str, typesInOrder: list[UserInput]) -> UserInputResult:
    messageInputs = messageContent.split(" ")
    del messageInputs[0]

    if len(typesInOrder) != len(messageInputs):
        raise ValueError("Wrong syntax")

    result = UserInputResult()
    userInputs = []
    i = 0
    for inputType in typesInOrder:
        userInput = messageInputs[i]

        inputType.input(userInput)
        validationError = inputType.validate()

        if validationError != None:
            result.validationError = validationError
            return result

    result.userInputs = userInputs
    return result