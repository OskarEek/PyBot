
class InvestmentStorageModel():
    ticker: str
    totalPointsInvested: int
    ownedShares: float
    averageBuyPrice: float
    certType: str
    multiplier: int

    def __init__(self, ticker: str, certType: str, multiplier: int):
        self.ticker = ticker.upper()
        self.totalPointsInvested = 0
        self.ownedShares = 0
        self.averageBuyPrice = 0
        self.certType = certType.upper()
        self.multiplier = multiplier

    def add_new_investment(self, points: int, stockPrice: float):
        if self.totalPointsInvested == 0:
            #First investment
            self.averageBuyPrice = stockPrice
            self.totalPointsInvested += points
            self.ownedShares += points / stockPrice
        else:
            newShares = points / stockPrice
            self.ownedShares += newShares
            self.totalPointsInvested += points
            self.averageBuyPrice = self.totalPointsInvested / self.ownedShares
            
    def calculate_change(self, currentStockPrice) -> dict:
        # Determine direction based on certType
        direction = 1 if self.certType == "BULL" else -1  # Bull = 1, Bear = -1
        
        # Calculate percentage change in stock price from average buy price
        stockPricePercentChange = (currentStockPrice - self.averageBuyPrice) / self.averageBuyPrice if self.averageBuyPrice else 0
        
        # Apply multiplier to the percentage change
        investmentPercentChange = stockPricePercentChange * self.multiplier * direction
        
        # Calculate the current total points
        totalPoints = self.totalPointsInvested * (1 + investmentPercentChange)
        
        # Calculate the difference in points
        pointsDifference = int(totalPoints - self.totalPointsInvested)
        
        return {
            "points": int(totalPoints),
            "percent": investmentPercentChange,
            "difference": pointsDifference
        }


    def to_dict(self):
        return {
            "ticker": self.ticker,
            "totalPointsInvested": self.totalPointsInvested,
            "ownedShares": self.ownedShares,
            "averageBuyPrice": self.averageBuyPrice,
            "certType": self.certType,
            "multiplier": self.multiplier
        }

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls(
            ticker=data['ticker'],
            certType=data['certType'],
            multiplier=data['multiplier']
        )
        #Following need to be assigned separately since they're not able to be set in constructor
        obj.totalPointsInvested = data.get('totalPointsInvested', 0)
        obj.ownedShares = data.get('ownedShares', 0)
        obj.averageBuyPrice = data.get('averageBuyPrice', 0)
        return obj
