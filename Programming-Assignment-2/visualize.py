import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('outputs.csv')
plt.scatter(data['p'], data['max_size'])
plt.show()