from tgju_api import CurrencyScraper
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

scraper = CurrencyScraper()
currencies = scraper.currencies
print(currencies)

usd_data = scraper.scrape_currency('USD', unix_timestamp=False)
print(usd_data.head())

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(usd_data['timestamp'], usd_data['price'], color='#1f77b4', linewidth=2)
ax.set_xlabel('Date', fontsize=14)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.tick_params(axis='x', labelsize=12, rotation=45)
ax.set_ylabel('Price (Rials)', fontsize=14)
ax.yaxis.set_major_formatter('{x:,.0f} Rls')
ax.tick_params(axis='y', labelsize=12)
ax.set_title('Price of USD over time', fontsize=16)
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('USD.svg')
plt.show()