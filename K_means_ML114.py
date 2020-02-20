################################K-Means Clustering algorithm############################################################
#######################################################################################################################

import os
import random
import numpy as np
from matplotlib import style
import pandas as pd
import fileinput
import fileinput



class K_Means:
        def __init__(self, k, tol_value = 0.05, max_iter = 100):
                self.k = k
                self.tol_value = tol_value
                self.max_iter = max_iter

        def kfit(self, dataframe):

                self.centroids = {}
        #Randomly shuffling datapoints        
                np.random.shuffle(dataframe)

        #initializing the centroids, the first k elemtnts of the random shuffled dataset will be default centroids
                count=0
                for i in range(self.k):
                        self.centroids[i] = dataframe[i][2:]


                for i in range(self.max_iter):
                        count+=1
                        self.k_classes = {}
                        for i in range(self.k):
                                self.k_classes[i] = []

                #Assigning the data to the classes for which the distance between the datapoint and  centroid is minimum
                        for data in dataframe:
                                dist = [np.linalg.norm(data[2:] - self.centroids[index]) for index in self.centroids]
                                #print(distances)
                                class_index = dist.index(min(dist))
                                self.k_classes[class_index].append(data)

                        pre = dict(self.centroids)

                # Evaluating new centroids by averaging the datapoints of a class
                        for class_index in self.k_classes:
                                temp=[]
                                for data in self.k_classes[class_index]:
                                        temp.append(data[2:])
                                self.centroids[class_index] = np.average(temp, axis = 0)

                        tol_matched = True

                        for index in self.centroids:

                                old = pre[index]
                                curr = self.centroids[index]
                                #print(np.mean(np.abs((curr - old)/old)),self.tol_value,count)
                                #if np.sum((curr - old)/old) > self.tol_value:
                                try:
                                        m= np.mean(np.abs((curr - old)/old))
                                        if m > self.tol_value:
                                                tol_matched = False
                                except ZeroDivisionError :
                                        tol_matched = False
                                
                                        
                #if the convergence criteria for tolerance matched break the lopp
                        if tol_matched:
                                break

        
def main():
        
        #Data Cleaning BCLL.txt has trailing spaces in each line, the following paragraph removes Trailing spaces and creates a file BCLL1
        f = open("BCLL1.txt", "w")
        for lines in fileinput.FileInput("BCLL.txt"):
            lines = lines.strip()
            #print(lines)
            f.write(lines + '\n')
        f.close()

        
        df = pd.read_csv("BCLL1.txt",delimiter='\t')
        #normalizing data
        df1=df.iloc[:,0:2]
        df2=df.iloc[:,2:]
        normalized_df=(df2-df2.min())/(df2.max()-df2.min())
        df3=pd.concat([df1,normalized_df],axis=1)
        
        X = df3.values #returns a numpy array
        (row,col)=X.shape
        cluster=[]
        SSE_list=[]
        for i in range(10):
                SSE=0
                K_value=random.randint(2,round(np.sqrt(row)))
                kmeans = K_Means(K_value)
                kmeans.kfit(X)

                path=os.getcwd()
                print("the current working directory is :%s"%path)
                path1= path + '\\Cluster_number_%d'%K_value
        
                try:
                                os.mkdir(path1)
                except OSError:  
                                print ("Creation of the directory %s failed,PLEASE REMOVE THE FOLDER IF ALREADY PRESENT" % path1)
                else:  
                                print ("Successfully created the directory %s  " % path1)

                
                '''for class_index in kmeans.k_classes:
                        cluster_distances=0
                        for data in kmeans.k_classes[class_index]:
                                cluster_distances += np.linalg.norm(data[2:] - kmeans.centroids[class_index])
                        SSE+=np.square(cluster_distances)'''
                for class_index in kmeans.k_classes:
                        cluster_distances=0
                        name=path1+'//cluster%d.txt'%class_index
                        l=open(name,"w")
                        for data in kmeans.k_classes[class_index]:
                                cluster_distances += np.linalg.norm(data[2:] - kmeans.centroids[class_index])
                                l.write(data[0] + '\n')
                        l.close()
                        SSE+=np.square(cluster_distances)
                print("\n")
                print("K values :",K_value,"SSE:",SSE)
                print('------------------------------------------------------------------------------------------------')
                cluster.append(K_value)
                SSE_list.append(SSE)
        min_index = SSE_list.index(min(SSE_list))
        print("\n")
        print("Minimum SSE:",SSE_list[min_index],"for K:",cluster[min_index])
        print('*********************************************************************************************************')
        input("press enter to exit")

if __name__ == "__main__":
        main()
