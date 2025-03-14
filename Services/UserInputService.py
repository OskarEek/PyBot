from discord import Message


from Services import PointsService
from Models.UserInput import UserInput
from Models.UserInputResult import UserInputResult


def get_user_input(messageContent: str, typesInOrder: list[UserInput]) -> UserInputResult:
    messageInputs = messageContent.split(" ")
    del messageInputs[0]
    result = UserInputResult()

    if len(typesInOrder) != len(messageInputs):
        result.validationError = "Wrong syntax"
        return result

    userInputs = []
    i = 0
    for inputType in typesInOrder:
        userInput = messageInputs[i]

        try:
            inputType.input(userInput)
        except:
            result.validationError = "Wrong Syntax"
            return result

        validationError = inputType.validate()

        if validationError != None:
            result.validationError = validationError
            return result
        
        userInputs.append(inputType)
        i += 1

    result.userInputs = userInputs
    return result