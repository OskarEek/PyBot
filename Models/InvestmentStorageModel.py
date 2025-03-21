
class InvestmentStorageModel():
    ticker: str
    totalPointsInvested: int
    ownedShares: float
    certType: str
    multiplier: int

    def __init__(self, ticker: str, certType: str, multiplier: int):
        self.ticker = ticker.upper()
        self.totalPointsInvested = 0
        self.ownedShares = 0
        self.certType = certType.upper()
        self.multiplier = multiplier

    def add_new_investment(self, points: int, stockPrice: float):
        self.totalPointsInvested += points
        self.ownedShares += points / stockPrice

    def calculate_change(self, currentStockPrice) -> dict:
        # Determine direction based on certType
        direction = 1 if self.certType == "BULL" else -1  # Bull = 1, Bear = -1

        # Calculate total points considering the leverage and direction
        totalPoints = int((currentStockPrice * self.multiplier * direction) * self.ownedShares)

        # Calculate the difference in points
        pointsDifference = totalPoints - self.totalPointsInvested

        # Prevent division by zero
        percentChange = (pointsDifference / self.totalPointsInvested) if self.totalPointsInvested else 0

        return {
            "points": totalPoints,
            "percent": percentChange
        }
        

    def to_dict(self):
        return {
            "ticker": self.ticker,
            "totalPointsInvested": self.totalPointsInvested,
            "ownedShares": self.ownedShares,
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
        return obj
