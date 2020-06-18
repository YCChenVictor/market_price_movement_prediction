from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import os.path
import datetime
import os
from functions.f_scrape_data import download_yahoo_quotes

# the current date
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
period_end = datetime.datetime(year, month, day)

# return the period that the date of csv file spans
period_end += datetime.timedelta(days=1)
period_begin = datetime.datetime.utcfromtimestamp(0)
period_days = period_end - period_begin
period_seconds = period_days.total_seconds()
period_seconds = str(int(period_seconds))

# the ticker_file
tickers = './docs/index_ticker_yahoo.csv'

# the download location
location = './docs/market_price'

# Set up Chromedriver
prefs = {'download.default_directory' : location}
chrome_options = Options()
chrome_options.add_argument('--headless') # 這步可以規避很多 chrome bug
chrome_options.add_experimental_option('prefs', prefs)

driver_path = "./env/bin/chromedriver"
driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)

# delete all the file in the target folder
for the_file in os.listdir(location):
    file_path = os.path.join(location, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

# download the csv file
with open(tickers) as tickers_file:
    tickers_reader = csv.reader(tickers_file)
    next(tickers_reader)
    for line in tickers_reader:
        ticker = line[0].strip()
        download_yahoo_quotes(ticker, period_seconds, driver)
        print("finish download %s" % ticker)
