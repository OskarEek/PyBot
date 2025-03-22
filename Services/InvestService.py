from typing import Optional

#Models
from Models.InvestmentModel import InvestmentModel
from Models.InvestmentStorageModel import InvestmentStorageModel

#Services
from Services import FileService


FILE_PATH = FileService.get_base_file_path() + "/Investments/investments.json"

def store_new_investment(userId: str, newInvestment: InvestmentModel):
    data = FileService.get_file_data(FILE_PATH) 
    data = data if data != None else {}
    
    investments: list = data.get(userId, [])
    
    investment: Optional[InvestmentStorageModel] = None
    index: Optional[int] = None
    i = 0
    for d in investments:
        x = InvestmentStorageModel.from_dict(data=d)
        if x.ticker == newInvestment.ticker:
            investment = x
            index = i
        i += 1
    
    #Previous investment in this ticker already exists
    if investment != None:
        if investment.certType != newInvestment.certType:
            raise Exception("Cant store new investment at same ticker with different certType")
        if investment.multiplier != newInvestment.multiplier:
            raise Exception("Cant store new investment at same ticker with different multiplier")
        
        investment.add_new_investment(newInvestment.points, newInvestment.stockPrice)
        investments[index] = investment.to_dict()
    else:
        investment = InvestmentStorageModel(
            newInvestment.ticker,
            newInvestment.certType,
            newInvestment.multiplier
            )
        investment.add_new_investment(newInvestment.points, newInvestment.stockPrice)
        investments.append(investment.to_dict())
    
    data[userId] = investments

    FileService.store_file_data(FILE_PATH, data)

def get_investment(userId: str, ticker: str) -> Optional[InvestmentStorageModel]:
    data = FileService.get_file_data(FILE_PATH)
    data = data if data != None else {}

    investments = data.get(userId, [])
    
    if len(investments) == 0:
        return None
    
    for d in investments:
        storedInvestment = InvestmentStorageModel.from_dict(data=d)
        if storedInvestment.ticker == ticker.upper():
            return storedInvestment

    return None

def remove_investment(userId: str, ticker: str):
    data = FileService.get_file_data(FILE_PATH) 
    data = data if data != None else {}

    investments: list = data.get(userId, [])
    
    if len(investments) == None:
        return
    
    for i, investment_dict in enumerate(investments):
        x = InvestmentStorageModel.from_dict(data=investment_dict)
        if x.ticker == ticker.upper():
            investments.pop(i)
            data[userId] = investments
            FileService.store_file_data(FILE_PATH, data)
            return


def get_all_investments(userId: str) -> list[InvestmentStorageModel]:
    data = FileService.get_file_data(FILE_PATH)
    data = data if data != None else {}

    investments = data.get(userId, [])
    
    if len(investments) == 0:
        return None
    
    investmentStorageModels: list[InvestmentStorageModel] = []
    for d in investments:
        storedInvestment = InvestmentStorageModel.from_dict(data=d)
        investmentStorageModels.append(storedInvestment)

    return investmentStorageModels

