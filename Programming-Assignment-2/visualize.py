import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('outputs.csv')
plt.scatter(data['p'], data['max_size'])
plt.title('$S_{n,p}$ v/s $p$')
plt.xlabel('$p$')
plt.ylabel('$S_{n,p}$')
plt.show()