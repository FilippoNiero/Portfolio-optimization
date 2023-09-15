import yfinance as yf
import datetime
import os
from tqdm import tqdm
import pandas as pd

import bs4 as bs
import requests
import datetime

resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})

ticker_list = [""]

# for row in table.findAll('tr')[1:]:
#     ticker = row.findAll('td')[0].text
#     ticker_list.append(ticker)

# ticker_list = [s.replace('\n', '') for s in ticker_list]

print(ticker_list)
# Calculate the start date 12 years ago from the current date
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=20 * 365)

# Create a directory to store the CSV files
data_dir = 'sp500_data'
os.makedirs(data_dir, exist_ok=True)

# Create a tqdm progress bar
progress_bar = tqdm(ticker_list, unit="stock")

# Fetch historical data for each stock and save it to a CSV file
for ticker in progress_bar:
    try:
        # Download data for the current stock
        data = yf.download(ticker, start=start_date, end=end_date)
        
        data = data[['Open', 'Close']] # Only keep open, close

        # Define the filename for the CSV file
        filename = os.path.join(data_dir, f"{ticker}.csv")
        
        # Save the data to the CSV file
        data.to_csv(filename)
        
        # Update the progress bar description to show the current ticker
        progress_bar.set_description(f"Fetching {ticker}")
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")

# Close the tqdm progress bar
progress_bar.close()
