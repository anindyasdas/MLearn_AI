import sys
import os
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
fold = 1
tot=0
for train_index, test_index in kf.split(X):
	X_train, X_test = X[train_index], X[test_index]
	y_train, y_test = y[train_index], y[test_index]
	
	LR = lm.LinearRegression()
	LR.fit(X_train,y_train)
	y_pred = LR.predict(X_test)
	rss = sum((y_pred-y_test)**2)
	tot=tot+rss
	print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
	print('Fold :',fold)
	print('RSS Value :', rss)
	print("Predicted Alcohol Value " , y_pred )
	print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')	
	fold=fold+1
print('Average RSS value', tot/5)

	



