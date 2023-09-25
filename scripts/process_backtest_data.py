import pandas as pd
import matplotlib.pyplot as plt
import matplotlib 
import os
import math

# Define the start date
start_date_str = '2020-01-02'
start_date = pd.to_datetime(start_date_str)

# Define the end date (1 year after the start date)
end_date = start_date + pd.DateOffset(months=8)

EPS = 0.00001 # 0.001%
# RESULT_FILENAMES = ['markowitz_block01012020','cdd_beta_0_block01012020','cdd_beta_1_block01012020','cdd_beta_2_block01012020']
# RESULT_FILENAMES = ['markowitz_boot01012020','cdd_beta_0_boot01012020','cdd_beta_1_boot01012020','cdd_beta_2_boot01012020']
RESULT_FILENAMES = ['markowitz_block15062022','cdd_beta_0_block15062022','cdd_beta_1_block15062022','cdd_beta_2_block15062022']
# RESULT_FILENAMES = ['markowitz_boot15062022','cdd_beta_0_boot15062022','cdd_beta_1_boot15062022','cdd_beta_2_boot15062022']
RESULT_DISPLAYNAMES = [
    'MV',
    'CDD 0',
    'CDD 1',
    'CDD 2'
]
RESULT_COLOR = [
    'green',
    'blue',
    'yellow',
    'red',
]
LINESTYLES = ['-', '--', '-.', '--']

def latex_table(mat):
    for i in range(0, len(mat[0]), 2): 
        for j in range(len(mat)):
            print(mat[j][i] + ' & ' + "{:.2f}".format(mat[j][i+1]*100) + '\%',  end=' & ' if j < len(mat) - 1 else ' \\\\')
        print('')
    print('\hline') 

    
def printWeightsTables(model_portfolio_weights, limit=5):
    numCols = len(RESULT_FILENAMES) * 2
    print('\\begin{tabular}{|c|' + ('r|') * (numCols-1) + '}')
    print('\hline')
    for i in range(len(RESULT_DISPLAYNAMES)):
        print('\multicolumn{2}{|c|}{' + RESULT_DISPLAYNAMES[i] + '} & ',end='')

    print()
    print('\hline')

    mat = []

    for i in range(len(RESULT_DISPLAYNAMES)):
        sorted_tickers = sorted(model_portfolio_weights[i].keys(), key=lambda x: model_portfolio_weights[i][x], reverse=True)
        tmp = [] 
    
        for j in range(limit):
            tmp.append(sorted_tickers[j])            
            tmp.append(model_portfolio_weights[i][sorted_tickers[j]]) 
        

        mat.append(tmp)
    latex_table(mat)
    print('\end{tabular}')
    

def printInfoTable(return_percentages, sortino_ratios, max_drawdowns):
    numCols = len(RESULT_FILENAMES) + 1
    headers = []
    headers.extend(RESULT_DISPLAYNAMES)
    headers.append('S\&P500')
    print('\\begin{tabular}{|c|' + ('r|') * (numCols) + '}')
    print('\hline')
    print(' & ', end='')
    # headers
    for i in range(numCols):
        print(headers[i],  end=' & ' if i < numCols - 1 else ' \\\\')
    print()
    print('\hline')
    # return percentages
    print('$R$ & ', end='')
    for i in range(numCols):
        print("{:.2f}\%".format(return_percentages[i]*100),  end=' & ' if i < numCols - 1 else ' \\\\')
    print()
    
    # sortino ratios
    print('$S$ & ', end='')
    for i in range(numCols):
        print("{:.2f}".format(sortino_ratios[i]),  end=' & ' if i < numCols - 1 else ' \\\\')
    print()
    # max drawdowns
    print('$MDD$ & ', end='')
    for i in range(numCols):
        print("{:.2f}\%".format(max_drawdowns[i]*100),  end=' & ' if i < numCols - 1 else ' \\\\')
    print()
    print('\hline')
    print('\end{tabular}')
    



def fromAnnualToDaily(r):
    return (1+r) ** (1/252) - 1

def fromDailyToAnnual(d):
    return ((d + 1) ** 252) - 1

def calcMdd(values):
    max_peak = values[0] 
    max_drawdown = 0

    for value in values:
        if value > max_peak:
            max_peak = value
    
        drawdown = (max_peak - value) / max_peak
    
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return max_drawdown

def calcDD(df, risk_free):
    yest_close = df['Close'].shift(1)

    ret = df['Close'] / yest_close - 1
    returns = ret.to_list()[1:]
    lower = 0
    standard = 0
    for x in returns:
        if x - risk_free < 0:
            lower += (x - risk_free) ** 2
        standard += (x - risk_free) ** 2
    downside_dev = math.sqrt(lower / len(returns))
    std_dev = math.sqrt(standard / len(returns))
    return downside_dev

def calcSortino(portfolio_weights, portfolio_values, asset_to_dd, risk_free):
    portfolio_dd = 0

    for ticker in portfolio_weights.keys():
        portfolio_dd += portfolio_weights[ticker] * asset_to_dd[ticker]

    portfolio_return_annual = portfolio_values[-1]/portfolio_values[0] -1 
    portfolio_return_daily = fromAnnualToDaily(portfolio_return_annual)
    
    return (portfolio_return_daily - risk_free) / portfolio_dd * math.sqrt(252)

def calcSP500Sortino(sp500_df, risk_free):
    dd = calcDD(sp500_df, risk_free)

    sp500annual = sp500_df.iloc[-1]['Close']/sp500_df.iloc[0]['Close'] - 1
    sp500daily = fromAnnualToDaily(sp500annual)

    return (sp500daily - risk_free) / dd * math.sqrt(252)


def parseWeights(filename):
    solution_numbers = []
    ticker_strings = []

    # Open the file for reading
    with open('./portfolio_results/' + filename, 'r') as file:
        lines = file.readlines()  # Read all lines into a list
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("solution"):
                # Extract numbers from the line starting with "solution"
                numbers = [float(num) for num in line.split(' ')[1:]]
                solution_numbers.extend(numbers)
            
            elif line.startswith("tickers="):
                ticker_strings = lines[i+1].strip().split(' ')
                
            
            i += 1
        
    portfolioWeights = {}
    assert len(solution_numbers) == len(ticker_strings)
    totWeight = 0

    for i in range(len(solution_numbers)):
        if solution_numbers[i] > EPS:
            portfolioWeights[ticker_strings[i]] = solution_numbers[i]
            totWeight += solution_numbers[i]
    return portfolioWeights


def fromWeightsToValue(portfolio_weights, ticker_data, dates):
    portfolio_values = []
    # Iterate through dates in the date range
    for date in dates:
        # Calculate the portfolio value for the current date
        date_str = date.strftime('%Y-%m-%d')
        portfolio_value = sum(
            portfolio_weights[ticker] * ticker_data[ticker].loc[ticker_data[ticker]['Date'] == date_str, 'Close'].values[0]
            for ticker in portfolio_weights
        )
        portfolio_values.append(portfolio_value)
    return portfolio_values


def plotPortfolio(plt, portfolio_values, dates, portfolio_name, color):
    plt.plot(pd.date_range(start=start_date, periods=len(dates), freq='D'), portfolio_values/portfolio_values[0], label=portfolio_name, color=color, linestyle=LINESTYLES[i])


# Read the S&P 500 data
sp500_df = pd.read_csv('SP500.csv', parse_dates=['Date'])
sp500_df = sp500_df[(sp500_df['Date'] >= start_date) & (sp500_df['Date'] <= end_date)]
# Initialize a dictionary to store ticker DataFrames
ticker_data = {}

startSP500Price = sp500_df.iloc[0]['Close']


tickers = []
# Read data for each ticker from the sp500_data folder
data_folder = 'sp500_data'
for filename in os.listdir(data_folder):
    if filename.endswith('.csv'):
        ticker_name = os.path.splitext(filename)[0]  # Extract ticker name from filename
        ticker_df = pd.read_csv(os.path.join(data_folder, filename), parse_dates=['Date'])
        filtered_df = ticker_df[(ticker_df['Date'] >= start_date) & (ticker_df['Date'] <= end_date)]
        tickers.append(ticker_name)
        ticker_data[ticker_name] = filtered_df


dates = ticker_data['A']['Date'].tolist()

# calculate sortino ratio
risk_free_return = fromAnnualToDaily(0.015)
map_asset_to_dd = {}

for ticker in tickers:
    map_asset_to_dd[ticker] = calcDD(ticker_data[ticker], risk_free_return)
    # print(ticker, ' ', map_asset_to_dd[ticker])

# Draw the chart

# Plot S&P 500 data
plt.plot(pd.date_range(start=start_date, periods=len(dates), freq='D'), sp500_df['Close']/startSP500Price, label='S&P 500', color='black')

sortinos = []
modelWeights = []
modelValues = []
for i in range(len(RESULT_FILENAMES)):
    weights = parseWeights(RESULT_FILENAMES[i])
    modelWeights.append(weights)
    values = fromWeightsToValue(weights, ticker_data, dates)
    modelValues.append(values)
    sortinos.append(calcSortino(weights, values, map_asset_to_dd, risk_free_return))
    # Plot portfolio value
    plotPortfolio(plt, values, dates, RESULT_DISPLAYNAMES[i], RESULT_COLOR[i])

sortinos.append(calcSP500Sortino(sp500_df, risk_free_return))

plt.xlabel('Dates')
plt.ylabel('Performance')
plt.legend()
plt.grid(True)


# TABLES

printWeightsTables(modelWeights)

returnpcts = []
for i in range(len(RESULT_FILENAMES)):
    returnpcts.append(modelValues[i][-1]/modelValues[i][0] - 1)

returnpcts.append(sp500_df.iloc[-1]['Close']/sp500_df.iloc[0]['Close'] - 1)
print(returnpcts)

mdds = []
for i in range(len(RESULT_FILENAMES)):
    mdds.append(calcMdd(modelValues[i]))

print(mdds)
mdds.append(calcMdd((sp500_df['Close']/startSP500Price).to_list()))
print(mdds)

printInfoTable(returnpcts, sortinos, mdds)

# Show the plot

# plt.show()
# plt.savefig('tmp.png')