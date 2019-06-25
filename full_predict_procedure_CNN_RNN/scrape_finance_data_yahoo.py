from selenium import webdriver
import csv
import os.path
import datetime
import os
from functions.f_scrape_data import get_crumb, download_yahoo_quotes
from functions.about_path import f_parent_path


# the current date
now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
period_end = datetime.datetime(year, month, day)


# return the period that the date of csv file spans
"""
UTC means Temps Universel Coordonné.
utcfromtimestamp returns the UTC datetime corresponding to the POSIX timestamp.
"""
period_end += datetime.timedelta(days=1)
period_begin = datetime.datetime.utcfromtimestamp(0)
period_days = period_end - period_begin
period_seconds = period_days.total_seconds()
period_seconds = str(int(period_seconds))

# this file path
file_path = os.path.dirname(os.path.abspath(__file__))

# the ticker_file
tickers = (file_path + '/docs/index_ticker_yahoo.csv')

# the download location
location = (file_path + '/docs/csv_files_stock_yahoo/')
# location = './yahoo_data'

# Set up Chromedriver
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": location,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

parent_file_path = f_parent_path(file_path, 1)
driver_path = parent_file_path + "/env/bin/chromedriver"
driver = webdriver.Chrome(driver_path, chrome_options=options)


# set the crumb to None
crumb = None

# make sure we get crumb
for i in range(10):
    if not crumb:
        crumb = get_crumb(driver)
    else:
        break

if not crumb:
    raise ValueError("Crumb Not Set")


# delete all the file in the target folder
for the_file in os.listdir(location):
    file_path = os.path.join(location, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        # elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

# download the csv file
with open(tickers) as tickers_file:
    tickers_reader = csv.reader(tickers_file)
    next(tickers_reader)
    for line in tickers_reader:
        ticker = line[0].strip()
        download_yahoo_quotes(ticker, period_seconds, crumb, driver)
        print("finish download %s" % ticker)

"""
# download the csv file if it doesn't exist in the directory
with open(tickers) as tickers_file:
    tickers_reader = csv.reader(tickers_file)
    next(tickers_reader)
    for line in tickers_reader:
        ticker = line[0].strip()
        if not os.path.isfile(location + "{}.csv".format(ticker)):
            download_yahoo_quotes(ticker, period_seconds, crumb)
            print("finish download %s" % ticker)
        else:
            pass
"""

# Identify Whether all the company data is downloaded
errors = {}
with open(tickers) as tickers_file:
    tickers_reader = csv.reader(tickers_file)
    next(tickers_reader)
    for line in tickers_reader:
        ticker = line[0].strip()
        if not os.path.isfile(location + "{}.csv".format(ticker)):
            errors[ticker] = "Quotes not downloaded."

with open("scraping_errors.csv", "w+") as errors_file:
    errors_writer = csv.writer(errors_file)
    errors_writer.writerow(["ticker", "error"])
    for ticker in errors:
        errors_writer.writerow([ticker, errors[ticker]])
