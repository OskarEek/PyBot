from discord import Message

from StockApi.StockApiService import StockHandler
from Models.UserInput import PointsInput, StringInput, IntegerInput
from Models.InvestmentModel import InvestmentModel

from Services import PointsService
from Services import UserInputService
from Services import InvestService

def invest(message: Message):
    userId = str(message.author.id)
    currentPoints = PointsService.get_user_points(userId)

    #Format: ".invest 5000 TSLA bear 20"
    inputs = [
        PointsInput(currentPoints), #pointsToInvest
        StringInput(), #ticker
        StringInput(), #certType
        IntegerInput() #multiplier
    ]
    inputs = UserInputService.get_user_input(message.content, inputs)

    pointsToInvest: int = inputs[0].get_value()
    ticker: str = inputs[1].get_value()
    certType: str = inputs[2].get_value()
    multiplier: int = inputs[3].get_value()
    ticker = ticker.upper()
    certType = certType.upper()

    #Validation
    currentInvestment = InvestService.get_investment(userId, ticker)
    if certType != "BEAR" and certType != "BULL":
        return "You need to enter \"bear\" or \"bull\""
    if multiplier <= 0 or multiplier > 20:
        return "Multiplier must be between 1 - 20"
    if currentInvestment != None and currentInvestment.certType != certType:
        position = "long" if certType == "BULL" else "short"
        currentInvestmentPosition = "short" if position == "long" else "long"
        return f"You cant take a {position} position in {ticker} since you already have a {currentInvestmentPosition} investment in this stock"
    if currentInvestment != None and currentInvestment.multiplier != multiplier:
        return f"You cant invest in {ticker} with a different multiplier ({multiplier}) as your current investment {currentInvestment.multiplier}"
    
    stockHandler = StockHandler(ticker)
    stockPrice = stockHandler.get_price()
    if stockPrice == None:
        return "That ticker does not seem to exist"

    investment = InvestmentModel(ticker, stockPrice, pointsToInvest, certType, multiplier)

    InvestService.store_new_investment(userId, investment)
    PointsService.store_user_points(userId, currentPoints - pointsToInvest)
    
    return f"You invested {str(pointsToInvest)} points in {ticker} at ${"{:.2f}".format(stockPrice)}, {certType} x{str(multiplier)}"



def get_investment(message: Message):
    userId = str(message.author.id)

    inputs = [StringInput()] #ticker
    inputs = UserInputService.get_user_input(message.content, inputs)

    ticker: str = inputs[0].get_value()

    investment = InvestService.get_investment(userId, ticker)
    if investment == None:
        return f"You have no investment in {ticker}"

    stockHandler = StockHandler(ticker)
    stockPrice = stockHandler.get_price()
    if stockPrice == None:
        return "That ticker does not seem to exist"

    result = investment.calculate_change(stockPrice)
    return f"Your investment: {ticker.upper()} {investment.certType} X{investment.multiplier}\nStock price: ${stockPrice:.2f}\nInvested: {investment.totalPointsInvested}, Buy price: ${investment.averageBuyPrice:.2f}\nCurrent value: {result["points"]}, Percentage Change: {result["percent"] * 100:.2f}%"



def sell_investment(message: Message):
    userId = str(message.author.id)

    inputs = [StringInput()] #ticker
    inputs = UserInputService.get_user_input(message.content, inputs)

    ticker: str = inputs[0].get_value()
    ticker = ticker.upper()

    investment = InvestService.get_investment(userId, ticker)
    if investment == None:
        return f"You have no investment in {ticker}"

    stockHandler = StockHandler(ticker)
    stockPrice = stockHandler.get_price()
    if stockPrice == None:
        return "That ticker does not seem to exist"

    result = investment.calculate_change(stockPrice)
    points = PointsService.get_user_points(userId)

    points += result["points"]

    PointsService.store_user_points(userId, points)
    InvestService.remove_investment(userId, ticker)

    return f"Sold: {ticker.upper()} {investment.certType} X{investment.multiplier}\nStock price: ${stockPrice:.2f}\nInvested: {investment.totalPointsInvested}, Buy price: ${investment.averageBuyPrice:.2f}\nCurrent value: {result["points"]}, Percentage Change: {result["percent"] * 100:.2f}%\nResult: {result["difference"]}"



def get_investments(message: Message):
    userId = str(message.author.id)

    investments = InvestService.get_all_investments(userId)
    if len(investments) == 0:
        return "You dont have any investments"

    out = "Your investments:\n"
    for x in investments:
        out += "- " + x.ticker + "\n"

    return out
    




