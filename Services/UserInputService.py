from Models.UserInput import UserInput

#If not handled in a unique way, ValueErrors raised by this function will be catched in the BotCommand.execute function
def get_user_input(messageContent: str, typesInOrder: list[UserInput]) -> list[UserInput]:
    messageInputs = messageContent.split(" ")
    del messageInputs[0]

    if len(typesInOrder) != len(messageInputs):
        raise ValueError("Wrong syntax")

    userInputs = []
    i = 0
    for inputType in typesInOrder:
        userInput = messageInputs[i]

        try:
            inputType.input(userInput)
        except:
            raise ValueError("Wrong syntax")

        validationError = inputType.validate()

        if validationError != None:
            raise ValueError(validationError)
        
        userInputs.append(inputType)
        i += 1

    return userInputs