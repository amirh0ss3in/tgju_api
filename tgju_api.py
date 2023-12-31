import requests
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict

class CurrencyScraper:
    """
    A web scraper for retrieving currency and gold prices from the tgju.org website.

    Usage:
        1. Instantiate the class:
            scraper = CurrencyScraper()

        2. Retrieve the list of available currencies:
            currencies = scraper.currencies

        3. Scrape data for a specific currency:
            data = scraper.scrape_currency('USD', unix_timestamp=False)

    Attributes:
        currencies_dict (Dict[str, str]): A dictionary mapping currency codes to their corresponding HTML element IDs on the tgju.org website.
        currencies (List[str]): A list of all available currency codes.
        source (str): The base URL of the tgju.org website.
        currency_url (str): The URL path for the currency section of the website.
        profile (str): The URL path for the profile section of the website.

    Methods:
        scrape_currency(currency: str, unix_timestamp: bool = False) -> pd.DataFrame:
            Retrieves historical data for a given currency.

            Args:
                currency (str): The currency code to retrieve data for.
                unix_timestamp (bool): If True, the resulting DataFrame will have a column of Unix timestamps. If False (default), the timestamps will be converted to human-readable format.

            Returns:
                A pandas DataFrame containing the scraped data.
    """

    currencies_dict: Dict[str, str] = {'USD': 'price_dollar_rl',
                    'EUR': 'price_eur', 
                    'AED': 'price_aed',
                    'CNY': 'price_cny', 
                    'GBP': 'price_gbp', 
                    'TRY': 'price_try', 
                    'CHF': 'price_cny', 
                    'JPY': 'price_krw', 
                    'CAD': 'price_cad', 
                    'AUD': 'price_aud', 
                    'NZD': 'price_nzd', 
                    'SGD': 'price_sgd', 
                    'INR': 'price_inr', 
                    'PKR': 'price_pkr', 
                    'IQD': 'price_iqd', 
                    'SYP': 'price_syp', 
                    'AFN': 'price_afn', 
                    'DKK': 'price_dkk', 
                    'SEK': 'price_sek', 
                    'NOK': 'price_nok', 
                    'SAR': 'price_sar', 
                    'QAR': 'price_qar', 
                    'OMR': 'price_omr', 
                    'KWD': 'price_kwd', 
                    'BHD': 'price_bhd', 
                    'MYR': 'price_myr', 
                    'THB': 'price_thb', 
                    'HKD': 'price_hkd', 
                    'RUB': 'price_rub', 
                    'AZN': 'price_azn', 
                    'AMD': 'price_amd', 
                    'GEL': 'price_gel', 
                    'KGS': 'price_kgs', 
                    'TJS': 'price_tjs', 
                    'TMT': 'price_tmt',
                    'gold_24k':'geram24',
                    'gold_18k':'geram18',
                    'mesghal': 'mesghal',
                    }
    currencies: List[str] = list(currencies_dict.keys())
    source: str = 'https://www.tgju.org/'
    currency_url: str = 'currency'
    profile: str = 'profile/'
    
    @staticmethod
    def scrape_currency(currency: str, unix_timestamp: bool = False, resample: bool = False, jalali: bool = False) -> pd.DataFrame:
        url: str = CurrencyScraper.source + CurrencyScraper.profile + CurrencyScraper.currencies_dict[currency]

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')

        chart_data_pattern = re.compile(r'chartData:\s*(\[.*?\]])')

        for script in scripts:
            if script.string:
                match = chart_data_pattern.findall(script.string)
                if match:
                    if len(match) > 2:                  # Here I'm doing something stupid. Don't know how to fix it yet.
                        data = eval(match[2])
                    else:
                        data = eval(match[0])
        data = np.array(data, dtype=np.int64)

        D = data[:, 0] // (24 * 3600 * 1000)
        data[:, 0] = D
        starting_day = pd.Timestamp('1970-01-01')
        df = pd.DataFrame(data, columns=['unix_timestamp', 'price'])
        df['timestamp'] = starting_day + pd.to_timedelta(df['unix_timestamp'], unit='d')
        if not unix_timestamp:
            df.drop(columns=['unix_timestamp'], inplace=True)
        
        if resample:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.set_index('timestamp')

            resampled_df = df.resample('D').mean() 
            resampled_df = resampled_df.interpolate()
            if unix_timestamp:
                resampled_df['unix_timestamp'] = resampled_df['unix_timestamp'].astype('int')
            resampled_df.reset_index(inplace=True)
            df.reset_index(inplace=True)
            assert len(resampled_df) == (df['timestamp'].max() - df['timestamp'].min()).days + 1 , "Resampled dataframe has incorrect length. Sorry. Probably a bug. Please report this bug at https://github.com/amirh0ss3in/tgju_api/issues"
            del df
            df = resampled_df
        
        if jalali:
            df['jalali_timestamp'] = df['timestamp'].apply(CurrencyScraper.to_jalali_date)

        return df

    @staticmethod    
    def to_jalali_date(dt):
        from jdatetime import date as jdate
        j = jdate.fromgregorian(date=dt.date())
        return f"{j.year}/{j.month}/{j.day}"
