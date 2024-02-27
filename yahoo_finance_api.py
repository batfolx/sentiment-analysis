import yfinance
import typing
import time
import random
from bot_types import FinancialArticle

companies = [
    'TLSA',
    'NVDA'
]


def get_latest_news_articles_yahoo() -> typing.List[FinancialArticle]:
    for company in companies:
        tick = yfinance.ticker.Ticker(company)
        company_news = tick.get_news()
        print(company_news)
        sleep_interval = random.uniform(2, 7)
        time.sleep(sleep_interval)

    return []


print(get_latest_news_articles_yahoo())
