# TGJU-API
TGJU-API is a Python web scraper for retrieving currency and gold prices from the tgju.org website. It uses the BeautifulSoup and js2xml libraries to parse the HTML and JavaScript on the website.

# Installation

## Dependencies

Before using TGJU-API, make sure you have the following dependencies installed:
- BeautifulSoup
- js2xml

You can install the dependencies using pip:
```
pip install beautifulsoup4 js2xml
```
## Install from GitHub
You can clone the repository from GitHub and install it manually:
```
git clone https://github.com/amirh0ss3in/tgju_api.git
cd tgju-api
pip install .
```

## Install using PIP [TODO] 
[TODO] Alternatively, you can install TGJU-API using pip:
```
pip install tgju-api
```

## Usage
Here's an example of how to use TGJU-API to retrieve currency data for the US dollar:
```
from tgju_api import CurrencyScraper

scraper = CurrencyScraper()
currencies = scraper.currencies
print(currencies)

usd_data = scraper.scrape_currency('USD', unix_timestamp=False)
print(usd_data.head())
```

This code snippet will display a list of all available currencies:
```
['USD', 'EUR', 'AED', 'GBP', 'TRY', 'CHF', 'JPY', 'CAD', 'AUD', 'NZD', 'SGD', 'INR', 'PKR', 'IQD', 'SYP', 'AFN', 'DKK', 'SEK', 'NOK', 'SAR', 'QAR', 'OMR', 'KWD', 'BHD', 'MYR', 'THB', 'HKD', 'RUB', 'AZN', 'AMD', 'GEL', 'KGS', 'TJS', 'TMT', 'gold_24k', 'gold_18k', 'mesghal']
```
And the initial few rows of historical data for the US dollar:
```
price  timestamp
0  13700 2011-11-26
1  13440 2011-11-27
2  13350 2011-11-28
3  13400 2011-11-29
4  13500 2011-11-30
```
