import os
import typing

import pymongo

import benzinga_api
import common
import rh_api
import sentiment


def get_articles() -> list:
    return []

def main():
    rh_username_key = 'RH_USERNAME'
    rh_username = os.getenv(rh_username_key)
    if not rh_username:
        raise EnvironmentError(f'Expected {rh_username_key} to be in the environment, but none was found.')

    rh_password_key = 'RH_PASSWORD'
    rh_password = os.getenv(rh_password_key)
    if not rh_password:
        raise EnvironmentError(f'Expected {rh_password_key} to be in the environment, but none was found')

    rh_token = rh_api.rh_login(rh_username, rh_password)
    if not rh_token:
        raise EnvironmentError(f'Failed login to RobinHood. Perhaps a wrong username and password?')

    companies_stocks: typing.List[dict] = common.read_stocks_csv_file()
    articles = benzinga_api.get_benzinga_news_articles()
    sentiment_classifier_model = sentiment.get_financial_classifier_pipeline()
    mongo_client: pymongo.MongoClient = common.get_mongo_client()
    for article in articles:
        db_article = common.get_article(mongo_client, article.article_id)
        # we have already processed it; it is in the database
        if db_article is not None and db_article.has_been_processed:
            continue

        full_article_with_title = f'{article.title}\n{article.body}'
        positive_sentiment = sentiment.is_positive_sentiment(sentiment_classifier_model, full_article_with_title)
        if not positive_sentiment:
            article.has_been_processed = True
            common.add_article_to_mongo(mongo_client, article)
            continue

        stock_tickers = article.stocks
        for ticker in stock_tickers:
            print(ticker)





