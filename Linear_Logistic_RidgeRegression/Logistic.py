from sklearn import linear_model
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
import pandas as pd


#import matplotlib.pyplot as plt
#%matplotlib inline

#Reading CSV file
df = pd.read_csv("winequality-red.csv",sep=';')
#df = pd.read_csv("winequality-red.csv",sep=';')
no_of_folds=5

inp=df.drop(['quality'],axis=1)
out=df['quality']
#For  K-fold cross validation
#kf = KFold(n_splits = no_of_folds)
skf = StratifiedKFold(n_splits = no_of_folds)
#Converting the input and output data into numpy_array
X = np.array(inp)
Y = np.array(out)
fold=0
sum_pre = np.zeros(6)
sum_recall = np.zeros(6)
sum_f_measure = np.zeros(6)
for train_index, test_index in skf.split(X, Y):
    X_train, X_test = X[train_index], X[test_index]
    Y_train, Y_test = Y[train_index], Y[test_index]
    log_r = LogisticRegression()
#for each fold training the model    
    log_r.fit(X_train,Y_train)
    fold+=1
#Predicting the alcohol variable
    
    Y_pred = log_r.predict(X_test)
#confusion matrix    
    conf_mat = confusion_matrix(Y_test, Y_pred)
    print ('FOR FOLD:',fold)
    print ('---------')
    print('\n')
    
# precision, recall and f-measure
    pre = precision_score(Y_test, Y_pred, average = None)
    recall = recall_score(Y_test, Y_pred, average = None)
    f_measure = f1_score(Y_test, Y_pred, average = None)
    
    print("per class precision :")
    print (pre)
    print('\n')
    print("per class recall: ")
    print (recall)
    print('\n')
    print("per class f-measure:")
    print (f_measure)
    print('\n')
    print('confusion matrix : ')
    print (conf_mat)
    print('\n')
    print('Correctly classified instances:', np.trace(conf_mat))
    print('Missclassified instances:      ', np.sum(conf_mat) - np.trace(conf_mat))
    print("********************************************************************************************************************************")
    sum_pre += pre
    sum_recall += recall
    sum_f_measure += f_measure
# Calculating average per-class precision, recall and f-measure for

print('Average  precision',sum_pre / no_of_folds)
print('Average  recall   ',sum_recall / no_of_folds)    
print('Average  f-measure',sum_f_measure / no_of_folds)
 
