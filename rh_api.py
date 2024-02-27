import requests
base_robinhood_url = 'https://api.robinhood.com'


def rh_login(username: str, password: str) -> str | None:
    """

    https://github.com/sanko/Robinhood/blob/master/Authentication.md#logging-in

    Logs into RobinHood with a given username and password
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



