import yfinance as yf
import asyncio
import datetime as dt
import pandas as pd


class StockTracker:
    def __init__(self, stocks: list[str], period: int, interval: int):
        """
        tracks list of stocks
        :param stocks: list of stock names
        :param period: time in days to
        :param interval:
        """
        self.stocks = stocks
        self.period = period
        self.interval = interval

    @property
    def stock_value(self) -> pd.DataFrame:
        """
        get value of specified stock
        :return:
        """
        return yf.download(self.stocks, period=f"{self.period}d", interval=f"{self.interval}m")


if __name__ == '__main__':
    stock_tracker = StockTracker(['AAPL', 'WMT', 'IBM', 'MU', 'BA', 'AXP'], 1, 1)
    print(values := stock_tracker.stock_value)

