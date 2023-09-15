import argparse

import os
import pandas as pd
import random
import datetime

DEFAULT_END_DATE = '2023-09-01' 

def write_scenarios_to_file(tickers, scenarios, num_scenarios):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # Construct the filename with the timestamp
    filename = f'problem_instance_{timestamp}.txt'

    with open(filename, 'w') as file:
        num_tickers = len(tickers)

        # Write the number of tickers and number of scenarios as the first line
        file.write(f"{num_tickers} {num_scenarios}\n")

        # Write each ticker and its scenarios
        for ticker, scenario_list in scenarios.items():
            scenario_str = ' '.join(map(str, scenario_list)).replace('[', '').replace(']', '')
            file.write(f"{ticker} {scenario_str}\n")


def get_daily_returns_by_ticker(data_dir='sp500_data', date_limit=None):
    daily_returns_by_ticker = {}

    # Convert the date limit to a datetime object if provided
    if date_limit:
        date_limit = pd.to_datetime(date_limit)

    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            ticker_name = os.path.splitext(filename)[0]
            file_path = os.path.join(data_dir, filename)
            df = pd.read_csv(file_path, parse_dates=['Date'])
            
            if date_limit:
                # Filter the DataFrame to include only rows earlier than the date limit
                df = df[df['Date'] < date_limit]

            # Calculate the daily returns using the Open and Close prices
            df['Daily_Return'] = ((df['Close'] - df['Open']) / df['Open']).round(5)

            # Extract the list of daily returns
            returns = df['Daily_Return'].tolist()

            # Store the daily returns in the dictionary
            daily_returns_by_ticker[ticker_name] = returns

    return daily_returns_by_ticker

def get_ticker_names(data_dir='sp500_data'):
    ticker_names = []
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            ticker_names.append(os.path.splitext(filename)[0])
    
    return ticker_names

def generate_boot_scenario(num_scenarios, end_date):
    #generate num_scenarios for each asset
    ticker_names = get_ticker_names()
    daily_returns = get_daily_returns_by_ticker(data_dir='sp500_data', date_limit=end_date)

    boot_scenarios_by_ticker = {}

    for ticker_name in ticker_names:
        asset_returns = daily_returns[ticker_name]
        boot_scenarios = []

        for _ in range(num_scenarios):
            # Randomly sample daily returns with replacement
            boot_scenario = random.choices(asset_returns)
            boot_scenarios.append(boot_scenario)

        # Store the boot scenarios for the asset
        boot_scenarios_by_ticker[ticker_name] = boot_scenarios
        print(ticker_name, " ", boot_scenarios)

    write_scenarios_to_file(ticker_names, boot_scenarios_by_ticker, num_scenarios)
    return boot_scenarios_by_ticker

def generate_block_scenario(block_size, num_scenarios, end_date):
    ticker_names = get_ticker_names()
    daily_returns = get_daily_returns_by_ticker(data_dir='sp500_data', date_limit=end_date)

    # Initialize a dictionary to store block scenarios
    block_scenarios_by_ticker = {}

    # Generate block scenarios for each asset
    for ticker_name in ticker_names:
        asset_returns = daily_returns.get(ticker_name, [])
        block_scenarios = []

        while num_scenarios > 0:
            # Determine the block size for this iteration
            current_block_size = min(block_size, num_scenarios)

            # Randomly sample a block of daily returns
            block_scenario = random.sample(asset_returns, k=current_block_size)
            block_scenarios.append(block_scenario)

            # Decrement the remaining scenarios
            num_scenarios -= current_block_size

        # Store the block scenarios for the asset
        block_scenarios_by_ticker[ticker_name] = block_scenarios
        print(block_scenarios)

    write_scenarios_to_file(ticker_names, block_scenarios_by_ticker, num_scenarios)
    return block_scenarios_by_ticker



def main():
    parser = argparse.ArgumentParser(description='Scenario Generation for S&P 500 Stocks')
    
    # Add a parameter for the scenario type
    parser.add_argument('generation_type', choices=['boot', 'block'], help='Specify the scenario generation type')
    
    # Add an optional parameter for the block_size (only for 'block' scenario)
    parser.add_argument('--block_size', type=int, help='Specify the number for the "block_size" scenario')
    
    # Add parameters for the number of scenarios and end date
    parser.add_argument('--num_scenarios', type=int, required=True, help='Specify the number of scenarios')
    parser.add_argument('--end_date', default=DEFAULT_END_DATE, help='Specify the end date in YYYY-MM-DD format')
    
    args = parser.parse_args()
    
    if args.generation_type == 'boot':
        # Call the function for boot scenario
        generate_boot_scenario(args.num_scenarios, args.end_date)
    elif args.generation_type == 'block':
        if args.number is None:
            print('Error: For "block" scenario, you must specify a block_size using the --block_size parameter.')
        else:
            # Call the function for block scenario with the specified number
            generate_block_scenario(args.block_size, args.num_scenarios, args.end_date)

if __name__ == '__main__':
    main()
