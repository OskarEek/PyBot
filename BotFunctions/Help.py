from discord import Message

async def help(message: Message):
    helpMessage = [
        "\n"
        "__**Commands**__\n",
        "   **General**\n",
        "       .grab-memory \n",
        "       .grab-memory all\n",
        "       .random *option1, option2, ...... , optionX*\n"
        "\n"
        "   **Gambling**\n",
        "       .points\n",
        "       .free-points\n",
        "       .gamble *integer*\n",
        "       .gamble all\n",
        "       .challenge *@user* *integer*\n",
        "       .respond-challenge *@user* *integer*",
    ]

    botContent = "".join(helpMessage)
    await message.channel.send(botContent)
