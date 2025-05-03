from discord import Message
import botCommands

def help(message: Message) -> str:
    groups: dict[str, list[str]] = {}
    for key, botCommand in botCommands.botCommands.items():
        if botCommand.group == "":
            continue

        if botCommand.group in groups:
            groups[botCommand.group].append(key)
            continue

        group = [key]
        groups[botCommand.group] = group

    
    helpMessage = "\n__**Commands**__"

    for group, commands in groups.items():
        helpMessage += ("\n  **" + group + "**")
        for command in commands:
            helpMessage += ("\n      " + command + "")
        helpMessage += "\n"


        
        
        


    return "".join(helpMessage)
