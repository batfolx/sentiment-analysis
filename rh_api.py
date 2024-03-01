import typing

import requests

base_robinhood_url = 'https://api.robinhood.com'


def rh_login(username: str, password: str) -> str | None:
    """
    Logs into RobinHood with a given username and password

    https://github.com/sanko/Robinhood/blob/master/Authentication.md#logging-in


    :param username: The username
    :param password: The password
    :return: The token to use in subsequent requests
    """
    endpoint = f'{base_robinhood_url}/api-token-auth'
    payload = {
        'username': username,
        'password': password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    r = requests.get(endpoint, headers=headers, data=payload)
    data: dict = r.json()
    return data.get('token')


def rh_place_buy_order(token: str, account_number: str, instrument_id: str, ticker: str):
    """
    Places a buy order on RobinHood

    https://github.com/sanko/Robinhood/blob/master/Order.md#place-an-order

    :param token: The auth token
    :param account_number: The account number for us
    :param instrument_id: The instrument ID (I guess its the ID of the company on RH?)
    :param ticker: The company ticker
    :return: True if could place the order, False otherwise
    """
    endpoint = f'{base_robinhood_url}/orders/'
    headers = {
        "Authorization": f"Token {token}",
        'Accept': 'application/json'
    }

    payload = {
        'account': f'{base_robinhood_url}/accounts/{account_number}',
        'instrument': f'{base_robinhood_url}/instruments/{instrument_id}',
        'symbol': ticker,
        'type': 'market',
        'time_in_force': 'gfd',
        'trigger': 'immediate',
        'price': 5,  # ?
        'quantity': 1,
        'side': 'buy',
    }

    r = requests.post(endpoint, headers=headers, data=payload)
    return r.status_code == 200


def rh_get_account_info(token: str) -> typing.Optional[dict]:
    """
    Gets the account information with the given token

    https://github.com/sanko/Robinhood/blob/master/Account.md

    Assume we will have a 'Normal' account rather than an 'Instant' account

    :param token: The auth token
    :return: Account information or None if something went wrong
    """

    endpoint = f'{base_robinhood_url}/accounts/'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Token {token}'
    }
    try:
        r = requests.get(endpoint, headers=headers)
        data: dict = r.json()
        results = data.get('results', [])
        if not results:
            return None

        result: dict = results[0]
        return result
    except Exception as e:
        print(f'Failed getting account info: {e}')
        return None


def rh_get_instrument_id_with_ticker(ticker: str) -> typing.Optional[dict]:
    """
    Gets the instrument ID with the ticker symbol

    https://github.com/sanko/Robinhood/blob/master/Instrument.md

    :param ticker: The company ticker symbol
    :return: The instrument ID or None
    """
    endpoint = f'{base_robinhood_url}/instruments/?symbol={ticker}'
    headers = {
        'Accept': 'application/json'
    }
    try:
        r = requests.get(endpoint, headers=headers)
        data: dict = r.json()
        results: list = data.get('results', [])
        if not results:
            return None
        result: dict = results[0]
        return result
    except Exception as e:
        print(f'Failed to get instrument with ticker {ticker}: {e}')
        return None
