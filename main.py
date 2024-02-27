import os

import rh_api
import sentiment


def get_articles() -> list:
    return []


def analyze_article(title: str, article: str):
    """
    Analyzes an article (or just some text) with the given title and article content
    :param title: The title of the article
    :param article: The actual article
    :return: None
    """
    is_positive = sentiment.is_positive_sentiment(f'{title}\n{article}')
    if not is_positive:
        return


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



