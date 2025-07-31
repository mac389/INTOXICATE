
import pylab 
import scipy.stats as stats
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm


data = pd.read_csv('synthetic_patients_1.csv')
sm.qqplot(data['risk'].dropna(), line='s')
plt.title("Risk Score QQ Plot")
plt.show()

#stats.probplot(data,, plot=pylab)
plt.savefig('results/QQplot.png')  

