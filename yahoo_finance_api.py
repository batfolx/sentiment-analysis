import yfinance as yf
import typing
import time
import random
from bot_types import FinancialArticle


def get_latest_news_articles_yahoo() -> typing.List[FinancialArticle]:
    companies = []
    for company in companies:
        tick = yf.ticker.Ticker(company)
        company_news = tick.get_news()
        print(company_news)
        sleep_interval = random.uniform(2, 7)
        time.sleep(sleep_interval)

    return []
