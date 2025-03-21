import json
from typing import Optional

#Models
from Models.InvestmentModel import InvestmentModel
from Models.InvestmentStorageModel import InvestmentStorageModel

#Services
from Services import FileService


FILE_PATH = FileService.get_base_file_path() + "/Investments/investments.json"

def store_new_investment(userId: str, newInvestment: InvestmentModel):
    FileService.create_file_if_not_exists(FILE_PATH, {})

    with open(FILE_PATH, 'r') as f:
        data = json.load(f)

    investments = []
    if userId in data:
        investments = data[userId]
    
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
        if investment.certType != investment.certType:
            raise Exception("Cant store new investment at same ticker with different certType")
        if investment.multiplier != investment.multiplier:
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

    with open(FILE_PATH, 'w') as f:
        json.dump(data, f)

def get_investment(userId: str, ticker: str) -> Optional[InvestmentStorageModel]:
    with open(FILE_PATH, 'r') as f:
        data = json.load(f)

    investments = []
    if userId in data:
        investments = data[userId]
    
    if len(investments) == 0:
        return None
    
    investment: Optional[InvestmentStorageModel] = None
    for d in investments:
        storedInvestment = InvestmentStorageModel.from_dict(data=d)
        if storedInvestment.ticker == ticker.upper():
            investment = storedInvestment

    return investment





