  TGJU-API
TGJU-API is a Python web scraper for retrieving currency and gold prices from the tgju.org website. It uses the BeautifulSoup and js2xml libraries to parse the HTML and JavaScript on the website.

Installation
You can install TGJU-API using pip:
```
pip install tgju-api
```

Alternatively, you can clone the repository from GitHub and install it manually:
```
git clone https://github.com/your_username/tgju-api.git
cd tgju-api
pip install .
```

Usage
Here's an example of how to use TGJU-API to retrieve currency data for the US dollar:
```
python
from tgju_api import CurrencyScraper

scraper = CurrencyScraper()
currencies = scraper.currencies
print(currencies)

usd_data = scraper.scrape_currency('USD', unix_timestamp=False)
print(usd_data.head())
```

This will print out a list of all available currencies, and the first few rows of the historical data for the US dollar.
