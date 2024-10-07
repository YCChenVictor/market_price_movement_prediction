import pandas as pd
from src.functions.f_scrape_data import (
    get_historical_price_with_yfinace,
)

symbols = [
    "AAPL",
    "AMZN",
    "AUDCAD=X",
    "AUDCHF=X",
    "AUDJPY=X",
    "AUDNZD=X",
    "AUDUSD=X",
    # "^AXJO",
    # "CADCHF=X",
    # "CADJPY=X",
    # "CHFJPY=X",
    # "DX-Y.NYB",
    # "EURAUD=X",
    # "EURCAD=X",
    # "EURCHF=X",
    # "EURGBP=X",
    # "EURJPY=X",
    # "EURNZD=X",
    # "EURUSD=X",
    # "^STOXX50E",
    # "GBPAUD=X",
    # "GBPCAD=X",
    # "GBPCHF=X",
    # "GBPJPY=X",
    # "GBPNZD=X",
    # "GBPUSD=X",
    # "^GDAXI",
    # "GOOGL",
    # "^N225",
    # "MSFT",
    # "NQ=F",
    # "NZDCAD=X",
    # "NZDCHF=X",
    # "NZDJPY=X",
    # "NZDUSD=X",
    # "^SPX",
    # "TSLA",
    # "^FTSE",
    # "USDCAD=X",
    # "USDCHF=X",
    # "USDJPY=X",
    # "USO",
    # "SI=F",
    # "GC=F",
]

for symbol in symbols:
    result = get_historical_price_with_yfinace(symbol)
    pd.DataFrame(result).to_csv(f"./docs/market_prices/{symbol}.csv")
    print(result)

# The following is the old way
# # the current date
# now = datetime.datetime.now()
# year = now.year
# month = now.month
# day = now.day
# period_end = datetime.datetime(year, month, day)

# # return the period that the date of csv file spans
# period_end += datetime.timedelta(days=1)
# period_begin = datetime.datetime.utcfromtimestamp(0)
# period_days = period_end - period_begin
# period_seconds = period_days.total_seconds()
# period_seconds = str(int(period_seconds))

# # create docs dir if not exist
# if not os.path.exists('./docs'):
#     os.makedirs('./docs')

# # the ticker_file
# tickers = 'index_ticker_yahoo.csv'

# # the download location
# location = './docs/market_price'
# if not os.path.exists(location):
#     os.makedirs(location)

# # Set up Chromedriver
# prefs = {'download.default_directory' : location}
# chrome_options = Options()
# chrome_options.add_argument('--headless') # 這步可以規避很多 chrome bug
# chrome_options.add_experimental_option('prefs', prefs)

# driver_path = "./env/bin/chromedriver"
# cService = webdriver.ChromeService(executable_path=driver_path)
# driver = webdriver.Chrome(service = cService)

# # delete all the file in the target folder
# for the_file in os.listdir(location):
#     file_path = os.path.join(location, the_file)
#     try:
#         if os.path.isfile(file_path):
#             os.unlink(file_path)
#     except Exception as e:
#         print(e)

# # download the csv file
# with open(tickers) as tickers_file:
#     tickers_reader = csv.reader(tickers_file)
#     next(tickers_reader)
#     for line in tickers_reader:
#         ticker = line[0].strip()
#         download_yahoo_quotes(ticker, period_seconds, driver)
#         print("finish download %s" % ticker)
