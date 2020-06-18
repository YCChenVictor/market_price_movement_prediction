from time import sleep
from urllib.parse import urlparse
from urllib.parse import parse_qs

def download_yahoo_quotes(ticker, period_seconds, driver):
    """
    :param ticker: the company
    :return: the web including specific csv file I want
    """
    driver.get('https://query1.finance.yahoo.com/v7/finance/download/{0}'
               '?period1=0&period2={1}'
               '&interval=1d&events=history'
               .format(ticker, period_seconds))
    sleep(1)
