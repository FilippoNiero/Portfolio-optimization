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

precalc_values = []
total_time_values = []
memory_values = []

def extract_values(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
        precalc_match = re.search(r'precalc\(us\)=([\d.]+)', content)
        total_time_match = re.search(r'total_time\(us\)=([\d.]+)', content)
        memory_match = re.search(r'memory\(KB\)=([\d.]+)', content)
        if precalc_match:
            precalc_values.append(float('%.2f'%(float(precalc_match.group(1)) / 1e6)))
        if total_time_match:
            total_time_values.append(float('%.2f'%(float(total_time_match.group(1)) / 1e6)))
        if memory_match:
            memory_values.append(float('%.2f'%(float(memory_match.group(1)) / 1024)))

def latex_table(mat, first_col):
    for i in range(len(mat[0])): 
        print(first_col[i], end=' & ')
        for j in range(len(mat)):
            print(mat[j][i],  end=' & ' if j < len(mat) - 1 else ' \\\\')
        print('') 
# Get a list of all files in the current directory
all_files = os.listdir()

# Initialize an empty list to store matching file names
toProcess = {}
# Iterate through all files and check if they match the pattern
for file_name in all_files:
    for p in patterns:
        toProcess.setdefault(p, [])
        if re.match(p, file_name):
            toProcess[p].append(file_name)

precalc = []
total_time = []
memory = []

for p in patterns:
    toProcess[p].sort()
    precalc_values = []
    total_time_values = []
    memory_values = []
    for f in toProcess[p]:
        print(f)
        extract_values(f)
    precalc.append(precalc_values)
    total_time.append(total_time_values)
    memory.append(memory_values)

print(precalc)
print(total_time)
print(memory)


first_col = []
T = 10
for i in range(len(precalc[0])):
    first_col.append(T)
    T *= 2
print("precalc:")
latex_table(precalc, first_col)
print("\ntotaltime:")
latex_table(total_time, first_col)
print("\nmemory:")
latex_table(memory, first_col)


linestyles = ['-', '--', '-.', '--', '-.', '--', '-.']
for i in range(len(precalc)):
    plt.plot(first_col, total_time[i], label=series_names[i],linestyle=linestyles[i])
# Add labels and a title
plt.xlabel('Number of scenarios')
plt.ylabel('Total time')

plt.xscale('log')
plt.yscale('log')
plt.xticks(first_col, [tick for tick in first_col])

# Display a legend
plt.legend()

# Display the plot
plt.grid(True)
# plt.show()
