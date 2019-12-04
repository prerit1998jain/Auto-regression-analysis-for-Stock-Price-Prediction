# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 17:47:44 2019

@author: KARTIK THAKKER
"""
import pandas as pd
import numpy as np
from pandas import Series
from matplotlib import pyplot as plt
from scipy.stats.stats import pearsonr 
import datetime
import multiprocessing
import math

#input file, formatted as having 2 columns: position, and value
txn = pd.read_csv(r'C:\Users\KARTIK THAKKER\Desktop\Sem5\Data Analytics\CS4003 Projects\CS4003 Projects\Data Set\STOCK.txt')
#txn = txn.drop_duplicates()
txn_original = txn.copy()
txn.drop(['High','Low','Close','Volume','OpenInt'],axis = 1, inplace = True)
txn.columns = ['coord', 'value']
#txn = txn.set_index('coord')

MAX_LAG = 1000

LENGTH_GENOME = max(txn.index)

#For each lag, this for loop identifies pairs of loci in the genome with that lag, and saves their expression values in a list. Then it computes the correlations between the 2 lists.

def pearson_correlation(numbers_x, numbers_y):
    x = numbers_x - np.mean(numbers_x)
    y = numbers_y - np.mean(numbers_y)
    return (x * y).sum() / np.sqrt((x**2).sum() * (y**2).sum())

def get_corr(lag):
#	print(lag)
#	print(datetime.datetime.now())
	exp1 = []
	exp2 = []
	for i in txn.index:
		e1 = txn.value[i]
		if (i + lag) > LENGTH_GENOME:
			break
		if (i + lag) in txn.index:
			e2 = txn.value[i+lag]
	#		print(e2)
			if  hasattr(e1,"__len__"):
				e1 = e1.iloc[0]
			if  hasattr(e2,"__len__"):
				e2 = e2.iloc[0]
			exp1.append(e1)
			exp2.append(e2)
	return [lag, pearson_correlation(exp1,exp2)]

RES=[]
print(datetime.datetime.now())
RES = [get_corr(i) for i in range(MAX_LAG)]
print(datetime.datetime.now())


lags = []
cors = []
for i in range(0, len(RES)):
	lags.append(RES[i][0])
	cors.append(RES[i][1])

#Display auto-correlation plot
plt.scatter(lags, cors)
plt.show()

 