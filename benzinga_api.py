import os
import typing

from common import FinancialArticle
from benzinga import news_data


def get_benzinga_news_articles() -> typing.List[FinancialArticle]:
    """
    Gets Benzinga news articles and makes a common list of FinancialArticle objects
    :return: List of FinancialArticle objects
    """
    benzinga_api_key = os.getenv('BENZINGA_API_KEY')
    if not benzinga_api_key:
        raise EnvironmentError("No BENZINGA_API_KEY found in the environment variables.")

    news = news_data.News(benzinga_api_key)
    stories = news.news(pagesize=25, display_output='full')
    return [
        FinancialArticle(story["id"],
                         story["author"],
                         story['created'],
                         story['updated'],
                         story['title'],
                         story['teaser'],
                         story['body'],
                         story['url'],
                         story['image'],
                         story['channels'],
                         story['stocks'],
                         story['tags'],
                         'Benzinga') for story in stories
    ]
