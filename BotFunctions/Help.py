from discord import Message

async def help(message: Message) -> str:
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
        "       .respond *@user* *integer*\n",
        "\n",
        "   **Lottery**\n",
        "       .lottery *integer*\n",
        "       .enter *integer*\n",
        "       .end-lottery"
    ]

    return "".join(helpMessage)
