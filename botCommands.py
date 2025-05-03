from Models.BotCommand import BotCommand, AsyncBotCommand
from BotFunctions import GrabMemory
from BotFunctions import Gamble
from BotFunctions import Random
from BotFunctions import Help
from BotFunctions import Lottery
from BotFunctions import Roulette
from BotFunctions import Invest
from BotFunctions import Hue
from BotFunctions import VoiceChannel

botCommands: dict[str, BotCommand] = {
    ".free-points":     BotCommand(".free-points", "points", "Gives user 500 free points", Gamble.free_points),
    ".gamble":          BotCommand(".gamble", "gamble","Gamble the number of coins you input with 50/50 chance to win", Gamble.gamble),
    ".points":          BotCommand(".points", "points","Check how many points you have", Gamble.points),
    ".challange":       BotCommand(".challange", "gamble", "", Gamble.challange),
    ".respond":         BotCommand(".respond", "gamble", "", Gamble.respond_challange),
    ".leaderboard":     AsyncBotCommand(".leaderboard", "points", "", Gamble.leaderboard),
    ".grab-memory":     AsyncBotCommand(".grab-memory", "general", "", GrabMemory.grab_memory),
    ".random":          BotCommand(".random", "general", "", Random.randomizer),
    ".help":            BotCommand(".help", "general", "", Help.help),
    ".lottery":         AsyncBotCommand(".lottery", "lottery", "", Lottery.start_lottery),
    ".enter":           AsyncBotCommand(".enter", "lottery", "", Lottery.add_lottery_points),
    ".end-lottery":     BotCommand(".end-lottery", "lottery", "", Lottery.end_lottery),
    ".roulette":        AsyncBotCommand(".roulette", "roulette", "", Roulette.roulette),
    ".end-roulette":    AsyncBotCommand(".end-roulette", "roulette", "", Roulette.end_roulette),
    ".invest":          BotCommand(".invest", "investing", "", Invest.invest),
    ".get-investment":  BotCommand(".get-investment", "investing", "", Invest.get_investment),
    ".sell-investment": BotCommand(".sell-investment", "investing", "", Invest.sell_investment),
    ".all-investments": BotCommand(".all-investments", "investing", "", Invest.get_investments),
    ".play":            AsyncBotCommand(".play", "music", "", VoiceChannel.play),
}