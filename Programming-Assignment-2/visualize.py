import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('outputs.csv')

# scatter plot each run
plt.scatter(data['p'], data['max_size'])
plt.title('$S_{n,p}$ v/s $p$')
plt.xlabel('$p$')
plt.ylabel('$S_{n,p}$')
plt.show()

# plots avg. stat
data = data.groupby('p').mean()
plt.scatter(data['max_size'].index, data['max_size'])
plt.title('$S_{n,p}$ v/s $p$')
plt.xlabel('$p$')
plt.ylabel('$S_{n,p}$')
plt.show()

# for p <= 1/n
tempdata = data.loc[data['max_size'].index <= 0.9E-7]
plt.scatter(tempdata['max_size'].index, tempdata['max_size'])
plt.title('$S_{n,p}$ v/s $p$')
plt.xlabel('$p$')
plt.ylabel('$S_{n,p}$')
plt.show()

# for p=0.9/n to 1.1/n
tempdata = pd.read_csv('outputs-mid.csv').groupby('p').mean()
plt.scatter(tempdata['max_size'].index, tempdata['max_size'])
plt.title('$S_{n,p}$ v/s $p$')
plt.xlabel('$p$')
plt.ylabel('$S_{n,p}$')
plt.show()