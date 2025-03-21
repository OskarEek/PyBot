from Models.BotCommand import BotCommand, AsyncBotCommand
from BotFunctions import GrabMemory
from BotFunctions import Gamble
from BotFunctions import Random
from BotFunctions import Help
from BotFunctions import Lottery
from BotFunctions import Roulette
from BotFunctions import Invest

botCommands: dict[str, BotCommand] = {
    ".free-points": BotCommand(".free-points", "Gives user 500 free points", Gamble.free_points),
    ".gamble": BotCommand(".gamble", "Gamble the number of coins you input with 50/50 chance to win", Gamble.gamble),
    ".points": BotCommand(".points", "Check how many points you have", Gamble.points),
    ".challange": BotCommand(".challange", "", Gamble.challange),
    ".respond": BotCommand(".respond", "", Gamble.respond_challange),
    ".leaderboard": AsyncBotCommand(".leaderboard", "", Gamble.leaderboard),
    ".grab-memory": AsyncBotCommand(".grab-memory", "", GrabMemory.grab_memory),
    ".random": BotCommand(".random", "", Random.randomizer),
    ".help": BotCommand(".help", "", Help.help),
    ".lottery": AsyncBotCommand(".lottery", "", Lottery.start_lottery),
    ".enter": AsyncBotCommand(".enter", "", Lottery.add_lottery_points),
    ".end-lottery": BotCommand(".end-lottery", "", Lottery.end_lottery),
    ".roulette": AsyncBotCommand(".roulette", "", Roulette.roulette),
    ".end-roulette": AsyncBotCommand(".end-roulette", "", Roulette.end_roulette),
    ".invest": BotCommand(".invest", "", Invest.invest),
    ".get-investment": BotCommand(".get-investment", "", Invest.get_investment)
}