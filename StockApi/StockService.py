from typing import Optional
import yfinance as yf
class StockHandler:
    _ticker: str
    def __init__(self, ticker:str):
        self._ticker = ticker

    def get_price(self) -> Optional[float]:
        msft = yf.Ticker(self._ticker)
        history = msft.history(period="1d", interval="1m")

        result: Optional[float] = None

        dataList = []
        for index, row in history.iterrows():
            dataList.append(row)

        if len(dataList) > 0:
            result = dataList[-1]["Close"]


        return result
