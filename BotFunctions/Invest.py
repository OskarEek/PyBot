from discord import Message

from StockApi.StockService import StockHandler
from Models.UserInput import PointsInput, StringInput, IntegerInput
from Models.InvestmentModel import InvestmentModel

from Services import PointsService
from Services import UserInputService
from Services import InvestService

def invest(message: Message):
    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)

    #.invest 5000 TSLA bear 20
    inputs = [
        PointsInput(currentPoints), #pointsToInvest
        StringInput(), #ticker
        StringInput(), #certType
        IntegerInput() #multiplier
    ]

    result = UserInputService.get_user_input(message.content, inputs)
    if result.validationError != None:
        return result.validationError

    inputs = result.userInputs
    pointsToInvest: int = inputs[0].get_value()
    ticker: str = inputs[1].get_value()
    certType: str = inputs[2].get_value()
    multiplier: int = inputs[3].get_value()

    if certType != "bear" and certType != "bull":
        return "You need to enter \"bear\" or \"bull\""

    if multiplier <= 0 or multiplier > 20:
        return "Multiplier must be between 1 - 20"
    
    stockHandler = StockHandler(ticker)
    stockPrice = stockHandler.get_price()
    
    if stockPrice == None:
        return "That ticker does not seem to exist"

    investment = InvestmentModel(ticker, stockPrice, pointsToInvest, certType, multiplier)

    InvestService.store_new_investment(userId, investment)
    
    return f"You invested {str(pointsToInvest)} points in {ticker} at ${"{:.2f}".format(stockPrice)}, {certType} x{str(multiplier)}"



def get_investment(message: Message):
    userId = str(message.author.id)
    inputs = [StringInput()] #ticker

    result = UserInputService.get_user_input(message.content, inputs)
    if result.validationError != None:
        return result.validationError

    ticker: str = result.userInputs[0].get_value()

    investment = InvestService.get_investment(userId, ticker)

    if investment == None:
        return f"You have no investment in {ticker}"

    stockHandler = StockHandler(ticker)
    stockPrice = stockHandler.get_price()
    
    if stockPrice == None:
        return "That ticker does not seem to exist"

    result = investment.calculate_change(stockPrice)

    return f"Your investment: {ticker.upper()} {investment.certType} X{str(investment.multiplier)}\nCurrent value: {result["points"]}, Percentage Change: {result["percent"] * 100:.2f}%, Invested: {str(investment.totalPointsInvested)}"



