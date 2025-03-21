
class InvestmentModel():
    ticker: str
    stockPrice: float
    points: int
    certType: str
    multiplier: int

    def __init__(self, ticker: str, stockPrice: float, points: int, certType: str, multiplier: int):
        self.ticker = ticker.upper()
        self.stockPrice = stockPrice
        self.points = points
        self.certType = certType.upper()
        self.multiplier = multiplier

    def to_dict(self):
        return {
            "ticker": self.ticker,
            "points": self.points,
            "price": self.stockPrice,   
            "certType": self.certType,
            "multiplier": self.multiplier
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['ticker'],
            price=data['stockPrice'],
            points=data['points'],
            certType=data['certType'],
            multiplier=data['multiplier']
        )