import time
import typing
import pymongo
import benzinga_api
import common
import rh_api
import sentiment


def main():
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
            print(
                f'({common.get_formatted_time()}){common.get_calling_func_name()}: Article with ID {article.article_id} has already been processed. Continuing...')
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
            instrument: typing.Optional[dict] = rh_api.rh_get_instrument_id_with_ticker(ticker)
            if not instrument:
                continue

            instrument_id = instrument.get("id")
            if not instrument_id:
                continue








        print(
            f'({common.get_formatted_time()}){common.get_calling_func_name()}: Finished article with article ID {article.article_id}. Sleeping for {sleepy_time} seconds before processing next article...')
        common.add_article_to_mongo(mongo_client, article)
        # wait some time before sending another article to OpenAI to avoid throttling
        time.sleep(sleepy_time)


if __name__ == '__main__':
    main()
