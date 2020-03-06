import sys
import os
import operator
from sklearn.model_selection import KFold
from pandas import read_csv
import numpy as np
from sklearn import linear_model as lm




filename = "winequality-red.csv"
dataframe = read_csv(filename,delimiter=";")
inp = dataframe.drop(['alcohol'],axis=1)
out = dataframe.iloc[:,10]
X = np.array(inp)
y = np.array(out)

kf = KFold(n_splits=5)
alpha_rss = []
alpha =[0,1*((10)**-5),2*((10)**-5),3*((10)**-5),4*((10)**-5),5*((10)**-5),6*((10)**-5),7*((10)**-5),8*((10)**-5),9*((10)**-5),10*((10)**-5),11*((10)**-5),12*((10)**-5),13*((10)**-5),14*((10)**-5),15*((10)**-5),16*((10)**-5),17*((10)**-5),18*((10)**-5),19*((10)**-5)]
for i in alpha:
	fold = 1
	tot=0
	print('FOR ALPHA = ',i)
	print('---------------')
	for train_index, test_index in kf.split(X):
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]
		RR = lm.Ridge(alpha=i)
		RR.fit(X_train,y_train)
		y_pred = RR.predict(X_test)
		rss = sum((y_pred-y_test)**2)
		tot=tot+rss
		print('fold : ',fold,'RSS Value : ',rss)
		fold=fold+1
	alpha_rss.append(tot/5)
	print("\n")	
	print('alpha =' ,i, " Average rss value = " ,tot/5)	
	print('*********************************************************************************************************')

min_index, min_value = min(enumerate(alpha_rss), key=operator.itemgetter(1))	
print('alpha = ',alpha[min_index] ,' gives best fit , with average RSS =' ,min_value)
#print(alpha_rss)
#print(min_index)
