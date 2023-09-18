import argparse

import os
import pandas as pd
import random
import datetime

DEFAULT_END_DATE = '2023-09-01' 

def write_scenarios_to_file(tickers, scenarios, num_scenarios, file_name=''):
    if len(file_name) < 1:
        # Construct the filename with the timestamp

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')                    
        file_name = f'problem_instance_{timestamp}.txt'

    with open(file_name, 'w') as file:
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
                df = df[df['Date'] <= date_limit]

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
    ticker_names.sort()
    return ticker_names

def generate_boot_scenario(num_scenarios, end_date, file_name=''):
    #generate num_scenarios for each asset
    ticker_names = get_ticker_names()
    daily_returns = get_daily_returns_by_ticker(data_dir='sp500_data', date_limit=end_date)


    boot_scenarios_by_ticker = {}
    daily_returns_length = len(daily_returns[ticker_names[0]])

    # Check that all assets have the same number of days
    for ticker_name in ticker_names:
        assert daily_returns_length == len(daily_returns[ticker_name]), 'Wrong daily return length for asset ' + ticker_name
        boot_scenarios_by_ticker[ticker_name] = []


    for i in range(num_scenarios):
        day = random.randrange(daily_returns_length)

        for ticker_name in ticker_names:
            # Store the boot scenarios for the asset
            boot_scenarios_by_ticker[ticker_name].append(daily_returns[ticker_name][day])
            
    write_scenarios_to_file(ticker_names, boot_scenarios_by_ticker, num_scenarios, file_name)
    return boot_scenarios_by_ticker

def generate_block_scenario(block_size, num_scenarios, end_date, file_name=''):
    ticker_names = get_ticker_names()
    daily_returns = get_daily_returns_by_ticker(data_dir='sp500_data', date_limit=end_date)



    # Initialize a dictionary to store block scenarios
    block_scenarios_by_ticker = {}
    daily_returns_length = len(daily_returns[ticker_names[0]])

    for ticker_name in ticker_names:
        assert daily_returns_length == len(daily_returns[ticker_name]), 'Wrong daily return length for asset ' + ticker_name
        block_scenarios_by_ticker[ticker_name] = []

    assert block_size > 0, 'Block size should be at least 1'

    # Generate block scenarios for each asset
    while num_scenarios > 0:
        # Determine the block size for this iteration
        current_block_size = min(block_size, num_scenarios)
        day = random.randrange(daily_returns_length - current_block_size + 1)
        for ticker_name in ticker_names:
            for i in range(current_block_size):
                block_scenarios_by_ticker[ticker_name].append(daily_returns[ticker_name][day + i])
        num_scenarios -= current_block_size

    write_scenarios_to_file(ticker_names, block_scenarios_by_ticker, num_scenarios, file_name)
    return block_scenarios_by_ticker



def main():
    parser = argparse.ArgumentParser(description='Scenario Generation for S&P 500 Stocks')

    
    # Add a parameter for the scenario type
    parser.add_argument('generation_type', choices=['boot', 'block'], help='Specify the scenario generation type')
    
    # Add an optional parameter for the block_size (only for 'block' scenario)
    parser.add_argument('--block_size', type=int, help='Specify the number for the "block_size" scenario')
    parser.add_argument('--file_name', default='',type=str, help='Specify the output file name')
    
    # Add parameters for the number of scenarios and end date
    parser.add_argument('--num_scenarios', type=int, required=True, help='Specify the number of scenarios')
    parser.add_argument('--end_date', default=DEFAULT_END_DATE, help='Specify the end date in YYYY-MM-DD format')
    
    args = parser.parse_args()
    
    random.seed(args.num_scenarios) # fixed random seed to reproduce the same instance
    
    if args.generation_type == 'boot':
        # Call the function for boot scenario
        generate_boot_scenario(args.num_scenarios, args.end_date, args.file_name)
    elif args.generation_type == 'block':
        if args.block_size is None:
            print('Error: For "block" scenario, you must specify a block_size using the --block_size parameter.')
        else:
            # Call the function for block scenario with the specified number
            generate_block_scenario(args.block_size, args.num_scenarios, args.end_date, args.file_name)

if __name__ == '__main__':
    main()
