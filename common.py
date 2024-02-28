import typing
import pathlib
import csv


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
