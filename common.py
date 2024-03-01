import datetime
import typing
import pathlib
import csv
import inspect
from pymongo import MongoClient

MONGO_DATABASE = 'PySentia'
MONGO_ARTICLES_COLLECTION = 'Articles'
MONGO_STOCKS_COLLECTION = 'Stocks'


class FinancialArticle:
    def __init__(self, article_id: int, author: str, created: str, updated: str, title: str, teaser: str, body: str,
                 url: str, image: list, channels: list, stocks: list, tags: list, source: str,
                 has_been_processed: bool = False, sentiment: str = 'unknown'):
        self.article_id = article_id
        self.author = author
        self.created = created
        self.updated = updated
        self.title = title
        self.teaser = teaser
        self.body = body
        self.url = url
        self.image = image
        self.channels = channels
        self.stocks = stocks
        self.tags = tags
        self.source = source
        self.has_been_processed = has_been_processed
        self.sentiment = sentiment
        self.gpt_response = {}

    def to_dict(self) -> dict:
        return {
            'articleId': self.article_id,
            'author': self.author,
            'created': self.created,
            'updated': self.updated,
            'title': self.title,
            'teaser': self.teaser,
            'body': self.body,
            'url': self.url,
            'image': self.image,
            'channels': self.channels,
            'stocks': self.stocks,
            'tags': self.source,
            'source': self.source,
            'hasBeenProcessed': self.has_been_processed,
            'sentiment': self.sentiment,
            'gptResponse': self.gpt_response
        }


def get_calling_func_name() -> str:
    """
    Gets the calling function name of this function. For logging purposes
    :return: a string
    """
    return inspect.currentframe().f_back.f_code.co_name


def get_formatted_time() -> str:
    d = datetime.datetime.now()
    return d.strftime("%I:%M %p %A, %B %dth, %Y")


def get_company_with_ticker(stocks: typing.List[dict], ticker: str) -> typing.Optional[dict]:
    """
    Gets the company information with the given ticker
    :param stocks: The stock_info.csv loaded into memory as a list of dictionaries
    :param ticker: The ticker symbol
    :return: None if no company could be found with that ticker, or the company data in a dict
    """
    company = list(filter(lambda x: x['Ticker'] == ticker, stocks))
    if not company:
        return None
    return company[0]


def get_ticker_with_company(stocks: typing.List[dict], company_name: str) -> typing.Optional[dict]:
    """
    Gets the company information with a given company name
    :param stocks: The stock_info.csv loaded into memory as a list of dictionaries
    :param company_name: The company name
    :return: None if no company was found with that company, or the company data in a dict
    """
    ticker = list(filter(lambda x: x['Name'] == company_name, stocks))
    if not ticker:
        return None
    return ticker[0]


def read_stocks_csv_file(f: pathlib.Path = pathlib.Path("./stocks/stock_info.csv")) -> typing.List[dict]:
    """
    Reads the stocks file into memory
    :param f: The filepath of the stocks csv file
    :return: A list of dictionaries
    """
    with open(f, mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)

        # Read each row into a list of dictionaries
        data: typing.List[dict] = [row for row in csv_reader]

    return data


def get_mongo_client() -> MongoClient:
    # use default for now
    return MongoClient()


def add_articles_to_mongo(client: MongoClient, articles: typing.List[FinancialArticle]):
    """
    Adds a bunch of articles to Mongo
    :param client: The MongoClient
    :param articles: The articles to add
    :return: None
    """
    collection = client[MONGO_DATABASE][MONGO_ARTICLES_COLLECTION]
    collection.insert_many([f.to_dict() for f in articles])


def add_article_to_mongo(client: MongoClient, article: FinancialArticle):
    """
    Adds an article to Mongo
    :param client: MongoClient
    :param article: The article to add
    :return: None
    """
    collection = client[MONGO_DATABASE][MONGO_ARTICLES_COLLECTION]
    collection.insert_one(article.to_dict())


def get_article(client: MongoClient, article_id: int) -> typing.Optional[FinancialArticle]:
    """
    Gets an article from the database
    :param client: The MongoClient
    :param article_id: The article ID
    :return: None if no article could be found, Finaicl
    """
    collection = client[MONGO_DATABASE][MONGO_ARTICLES_COLLECTION]
    res = collection.find_one({'articleId': article_id})
    if not res:
        return None

    f = FinancialArticle(
        res['articleId'],
        res['author'],
        res['created'],
        res['updated'],
        res['title'],
        res['teaser'],
        res['body'],
        res['url'],
        res['image'],
        res['channels'],
        res['stocks'],
        res['tags'],
        res['source'],
        res['hasBeenProcessed'],
        res['sentiment']
    )
    f.gpt_response = res['gptResponse']
    return f


def get_prompt():
    return "Given a financial article title, can you identify its sentiment, and if it has positive sentiment, can you try and extract the company that is announcing the news as well as any companies that it is aquiring? Give the answer to me in pure JSON,  with a key being 'sentiment' showing the sentiment, and another key being 'company' that is announcing the news, and any sub companies it may be investing or inquiring in with the key 'subCompanies'. If there are any actual numbers, represent them as floats"
