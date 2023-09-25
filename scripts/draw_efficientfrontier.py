import matplotlib.pyplot as plt
import numpy as np


y = np.linspace(0.7, 1.7, 100)

x = (y-1)**2 * 25 + 5

y2 = np.linspace(0, 2, 100)

x = (y-1)**2 * 25 + 5
x2 = (y2-1)**2 * 25 + 5
# Create the plot
plt.plot(x, y, color='blue')
plt.plot(x2, y2, linestyle='--', color='blue')
plt.xlabel('Risk')
plt.ylabel('Return')
plt.xlim(0, 20)
plt.ylim(0, 3)

a = [7.5, 14, 12.5, 17.5, 17.5]
b = [1, 1.3, 0.8, 1.22, 0.5]

# Create a scatter plot
plt.scatter(a, b, label='Points', color='green', marker='o')

plt.xticks([])
plt.yticks([])
plt.show()