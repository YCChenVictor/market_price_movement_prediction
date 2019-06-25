from time import sleep
from urllib.parse import urlparse
from urllib.parse import parse_qs


def get_crumb(driver):
    """
    crumb will be user-specific.
    It’s a cookie how Yahoo uses to identify users.
    """
    driver.get('https://finance.yahoo.com/quote/AAPL/' +
               'history?period1=0' +
               '&period2=2000000000' +
               '&interval=1d&filter=history' +
               '&frequency=1d')

    # avoid attack
    sleep(10)
    el = driver.find_element_by_xpath(
         "// a[. // span[text() = 'Download Data']]")
    link = el.get_attribute("href")
    a = urlparse(link)
    crumb = parse_qs(a.query)["crumb"][0]
    return crumb


def download_yahoo_quotes(ticker, period_seconds, crumb, driver):
    """
    :param ticker: the company
    :return: the web including specific csv file I want
    """
    driver.get('https://query1.finance.yahoo.com/v7/finance/download/{0}'
               '?period1=0&period2={1}'
               '&interval=1d&events=history&crumb={2}'
               .format(ticker, period_seconds, crumb))
    # print('https://query1.finance.yahoo.com/v7/finance/download/{0}'
    #       '?period1=0&period2={1}'
    #       '&interval=1d&events=history&crumb={2}'
    #       .format(ticker, period_seconds, crumb))
    sleep(1)
