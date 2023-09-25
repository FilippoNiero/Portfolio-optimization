import os
import re
import matplotlib.pyplot as plt  # Importa la libreria matplotlib
import numpy as np
# Define the regular expression pattern to match file names

patterns = [
    r'markowitz_performance_\d{6}', 
    r'cdd_beta_0_performance_\d{6}', 
    r'cdd_beta_1_performance_\d{6}',
    r'cdd_beta_2_performance_\d{6}',
    r'cdd_beta_3_performance_\d{6}',
    r'cdd_beta_4_performance_\d{6}', 
    r'cdd_beta_5_performance_\d{6}'
]

series_names = [
    'MV',
    'CDD0',
    'CDD1',
    'CDD2',
    'CDD3',
    'CDD4',
    'CDD5',
]


def latex_table(total_times):
    for i in range(len(total_times)): 
        print('') 

def toYearly(mu):
    return  float('%.3f' %((1 + mu) ** (252) - 1))
# Get a list of all files in the current directory
all_files = os.listdir()

# Initialize an empty list to store matching file names
toProcess = {}
# Iterate through all files and check if they match the pattern
for file_name in all_files:
    for p in patterns:
        if re.match(p, file_name):
            toProcess[p] = file_name


map_pattern_to_total_time = {}

mu0_values = []
times = {}

total_times_map = {}
content = ''
for i in range(len(patterns)):
    time_values = []
    with open(toProcess[patterns[i]], 'r') as file:
        content = file.read()
        
        # Pattern matching for total_time
        time_matches = re.findall(r'^time\(us\)=([\d.]+)', content, flags=re.MULTILINE)
        time_values.extend([float('%.4f' %( float(match) / 1e6)) for match in time_matches])
        
        times[series_names[i]] = time_values

        total_time_match = re.search(r'total_time\(us\)=([\d.]+)', content)
        total_times_map[series_names[i]] = float('%.4f'%(float(total_time_match.group(1)) / 1e6))


mu0_matches = re.findall(r'mu0=([\d.e-]+)', content)
mu0_values.extend([toYearly(float('%.6f' % float(match))) for match in mu0_matches])
        
print(mu0_values)
print(times)
xLabels = []

for i in range(len(mu0_values)):
    if i % 5 == 0:
        xLabels.append(mu0_values[i])
T = 10

# write out latex table data 
for i in range(len(series_names)): 
    print(total_times_map[series_names[i]],  end=' & ' if i < len(series_names) - 1 else ' \\\\')




linestyles = ['-', '--', '-.', '--', '-.', '--', '-.']
for i in range(len(times)):
    plt.plot(mu0_values, times[series_names[i]], label=series_names[i],linestyle=linestyles[i])
# Add labels and a title
plt.xlabel('Minimum expected return, annualized [%]')
plt.ylabel('Total time [s]')

plt.xticks(xLabels, [tick for tick in xLabels])

# Display a legend
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
