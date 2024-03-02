import datetime
import os
import time
import typing
import pymongo
import benzinga_api
import common
import rh_api
import sentiment


def place_rh_order(client: pymongo.MongoClient, article: common.FinancialArticle, ticker: str) -> bool:
    """
    Places a Buy Order on RobinHood
    :param client: The MongoDB client to add the stock entry in
    :param article: The referencing article
    :param ticker: The ticker symbol
    :return: True if placed buy order, False otherwise
    """
    auth_token = os.getenv("RH_TOKEN")
    if not auth_token:
        return False

    instrument: typing.Optional[dict] = rh_api.rh_get_instrument_id_with_ticker(ticker)
    if not instrument:
        return False

    instrument_id = instrument.get("id")
    if not instrument_id:
        return False

    account_info = rh_api.rh_get_account_info(auth_token)
    if not account_info:
        return False

    quote = rh_api.rh_get_quote_data_with_ticker(auth_token, ticker)
    if not quote:
        return False

    account_number: str = account_info.get('account_number', '')
    account_cash: float = account_info.get('cash', 0.0)
    ask_price: float = quote.get('ask_price', 0.0)

    # we can't buy if the stock price is bigger
    if ask_price > account_cash:
        return False

    print(f'Buying 1 share of {ticker} with price {ask_price}. Amount of cash we have in is {account_cash}')
    order_resp = rh_api.rh_place_buy_order(auth_token, account_number, instrument_id, ticker, ask_price)
    if not order_resp:
        return False
    print(f'Ordered 1 share of {ticker} with response {order_resp}')
    s = common.StockEntry(article.article_id, ticker, instrument, account_info, ask_price, 1, datetime.datetime.now(),
                          order_resp, quote)

    common.add_stock_entry_to_mongo(client, s)
    return True


def analyze_articles():
    """
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

    #companies_stocks: typing.List[dict] = common.read_stocks_csv_file()
    """

    sleepy_time = 5
    articles: typing.List[common.FinancialArticle] = benzinga_api.get_benzinga_news_articles()
    mongo_client: pymongo.MongoClient = common.get_mongo_client()
    for article in articles:
        db_article = common.get_article(mongo_client, article.article_id)
        # we have already processed it; it is in the database, continue to next article
        if db_article is not None and db_article.has_been_processed:
            continue

        # get chatgpt's response and sentiment
        full_article_with_title = f'{article.title}\n{article.body}'
        print(
            f'({common.get_formatted_time()}){common.get_calling_func_name()}: Processing article with ID {article.article_id}.')
        gpt_response = sentiment.extract_company_names_openai(article.article_id, full_article_with_title)
        if gpt_response is None:
            article.has_been_processed = True
            common.add_article_to_mongo(mongo_client, article)
            print(
                f'({common.get_formatted_time()}){common.get_calling_func_name()}: Article with ID {article.article_id} has got no response from ChatGPT.')
            time.sleep(sleepy_time)
            continue

        # if the article sentiment is not positive, do not buy anything
        print(
            f'({common.get_formatted_time()}){common.get_calling_func_name()}: Processed article with ID {article.article_id} with response {gpt_response}')
        article_sentiment = gpt_response.get('sentiment', '').lower()
        article.sentiment = article_sentiment
        article.gpt_response = gpt_response
        if article_sentiment != 'positive':
            article.has_been_processed = True
            common.add_article_to_mongo(mongo_client, article)
            print(
                f'({common.get_formatted_time()}){common.get_calling_func_name()}: Article with ID {article.article_id} does NOT have positive sentiment. Continuing to next article.')
            time.sleep(sleepy_time)
            continue

        # if we get down here, lets buy some I suppose
        stock_tickers = article.stocks
        for ticker in stock_tickers:
            place_rh_order(mongo_client, article, ticker)

        print(
            f'({common.get_formatted_time()}){common.get_calling_func_name()}: Finished article with article ID {article.article_id}. Sleeping for {sleepy_time} seconds before processing next article...')
        common.add_article_to_mongo(mongo_client, article)
        # wait some time before sending another article to OpenAI to avoid throttling
        time.sleep(sleepy_time)

    mongo_client.close()


if __name__ == '__main__':
    analyze_articles()
