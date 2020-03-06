# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 16:00:33 2019

@author: Anindya
"""
################### HMM model##########################
################### states : 10 ( tags ) 'company','facility','geo-loc','movie', 'musicartist',
#####       'person','product','sportsteam','tvshow',
#####       'other','O'
#####################observations : words######
import re
#import nltk
#nltk.download('punkt')
import string
from nltk.stem import WordNetLemmatizer
import numpy as np
import math
import pandas as pd
#from nltk.stem import PorterStemmer
#from nltk.tokenize import sent_tokenize, word_tokenize
import collections
import os
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt

def train_model(ind):
    print('hi')
    df0 = pd.read_csv('train.txt', header = None, sep= '\t')
    df2 = pd.read_csv('test.txt', header = None, sep= '\t')
    entity = df0[:][0]
    tags= df0[:][1]
    tags_modified = df0[:][2]
    entity_test = df2[:][0]
    tags_modified_test = df2[:][2]
    print('train size',len(entity))
    print('test size',len(entity_test))
    ####################################################################
############################################
#### dictionary to calculate starting probability#####
####################################################
### inorder to avoid zero probability count has been initialized
    start= {'company': 0.01, 'facility': 0.01, 'geo-loc': 0.01, 'movie': 0.01, 'musicartist' :0.01,
       'person': 0.01, 'product': 0.01, 'sportsteam' :0.01, 'tvshow' :0.01,
       'other': 0.01,'O': 0.01}
    sentence_count=0.01*11 # smooting for all 11 entries
#Counting the Number of sentences starting with a particular tag and
#counting total number of sentences
    for i in range(len(tags)):
        if(tags[i] == 'O' and ((i==0) or (entity[i-1]=='stoptag' and tags[i-1]== 'stoptag'))):
            start[tags[i]]+=1
            sentence_count+=1
        elif((i==0) or (entity[i-1]=='stoptag' and tags[i-1]== 'stoptag')):
            start[tags[i][2:]]+=1
            sentence_count+=1
    for key in start:
        start[key] = (float)(start[key])/sentence_count
    print("\n Starting probability calculated***************")
    print("\n the start probabilities are :\n", start)
    ###################################################################
############################################################################
############# TRANSITION PROB VALCULATION#########################
#############################################################
    list_tags =['company','facility','geo-loc','movie', 'musicartist',
       'person','product','sportsteam','tvshow',
       'other','O']
    transition = collections.defaultdict(dict) # two dimentional dictionary
    tag_count = dict() # dictionary for counting 
    for tag in list_tags:
        tag_count[tag] = 0.00001*len(list_tags) # initializing tag count # smooting for all 11 entries
        for tag1 in list_tags:
            transition[tag][tag1] = 0.00001 # initializing don't want to end up zero prob
        
    for i in range(len(tags)-1):
        if(tags_modified[i] != 'stoptag' and tags_modified[i+1] != 'stoptag'):
            transition[tags_modified[i]][tags_modified[i+1]] += 1
            tag_count[tags_modified[i]] +=1

    transition = {key: {key_: (float)(val_)/tag_count[key] for key_, val_ in val.items()} 
             for key, val in transition.items()}

    print("\n transition probability calculated***************")
    print("\n the transition probabilities are :\n", transition)  
    ###################DEBUGGING to check any misread#####################
#   for i in range(len(entity)):
#       if (len(entity[i])>20):
#           print(i, entity[i])
################################################################
##############################################################
######################## Emmission probability calculation#########
#################################################################
    emit = collections.defaultdict(dict)
#initialization from vocab
    for tag in list_tags:
        tag_count[tag] = 0.000001*len(vocab)
        for word in vocab:
            emit[tag][word]= 0.000001
######################################################################  
#### Counting no of occurances of a word associated with a tag######
    for i in range(len(entity)):
        if(tags_modified[i] != 'stoptag'):
            emit[tags_modified[i]][entity[i]]+=1 # corresponding tag and word
            tag_count[tags_modified[i]] +=1

    emit = {key: {key_: (float)(val_)/tag_count[key] for key_, val_ in val.items()} 
             for key, val in emit.items()}
    ###################### DEBUG to check emmission probability###############
    '''
    for tag in list_tags:
        sum1=0
        for i in vocab:
            sum1 += emit[tag][i]
        print(sum1)
        '''
#######################################################################
    print("\n emission probability calculated")
##########################################
    #######################################################################
####################VITERBI ALGO###################################
######################################################################
    try:
        os.remove("output.txt")#### deleting output file
        print(" output file output.txt File Removed!")
    except:
        print("output file does not exist ,it  will be created")



    for i in range(len(entity_test)): # this will be on test dataset
        if(i== 0 or (i!=0 and tags_modified_test[i-1]== 'stoptag')):# tags modified should be replaced by testing labels
            temp = []
            viterbi_prob =[] # this list stores maximum prob for upto each state for every possible state
            j = i
            for tag in list_tags:    
                temp.append(start[tag]*emit[tag][entity_test[i]])
            viterbi_prob.append(temp)
        elif(tags_modified_test[i]== 'stoptag'):
            #a=1
            backtrack(viterbi_prob,j,entity_test,tags_modified_test,list_tags,ind)
        else:
            temp= []
            temp1=viterbi_prob[-1]## collection of maximum probability of all the states till prior-observation point
            for tag1 in list_tags:
                temp2=[]
                for k in range(len(temp1)):
                    temp2.append(temp1[k]*(transition[list_tags[k]][tag1])*(emit[tag1][entity_test[i]]))
                temp.append(max(temp2))
            viterbi_prob.append(temp)
    analysis_plot(ind)
####################################   
#### this method splits a list
def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return(out)

#import tensorflow as tf
def backtrack(v_prob,index,e_test,tag_test,list_tags,ind):
    outfile = 'output%d.txt'%ind
    f = open(outfile,'a+')
    for p in v_prob:
        if tag_test[index]== 'O':
            orig = tag_test[index]
        else:
            orig = 'B-' + tag_test[index]
            
        if list_tags[np.argmax(p)]== 'O':
            pred = list_tags[np.argmax(p)]
        else:
            pred = 'B-' + list_tags[np.argmax(p)]
    
        line1 = e_test[index] + '\t' + orig + '\t' + pred
        print(line1, file=f)
        index +=1
 #   line1 = 'stoptag' + '\t' + 'stoptag' + '\t' + 'stoptag' # no need to add stoptag tag at output
  #  print(line1, file=f)
    f.close()
##### function used for plotting#####
def analysis_plot(ind):
    outfile= 'output%d.txt'%ind
    f = open('report2.txt','a+')
    df3= pd.read_csv(outfile, header = None, sep= '\t')
    y_test= df3[:][1]
    y_pred= df3[:][2]
    matrix = confusion_matrix(y_test, y_pred)
    '''
    class_names = ['company','facility','geo-loc','movie', 'musicartist',
       'person','product','sportsteam','tvshow',
       'other','O']
    '''
    class_names = ['B-company','B-facility','B-geo-loc','B-movie', 'B-musicartist',
       'B-person','B-product','B-sportsteam','B-tvshow',
       'B-other','O']
    matrix = confusion_matrix(y_test, y_pred, labels = class_names)
    ig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(matrix, annot=True, fmt='d',
            xticklabels=class_names, yticklabels=class_names)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()
    #print(np.unique(y_test),np.unique(y_pred))
    print('\n classification report: ', file =f)
    print('\n'+classification_report(y_test, y_pred), file =f)
    print('\n overall accuracy:',file =f)
    print(accuracy_score(y_test, y_pred), file=f)
    f.close()
######################################################








#######################################################################
##############################MAIN######################
##################################################
train_path='NER-Dataset-10Types.txt'
f1 = open('NER-Dataset-10Types.txt',errors="ignore")	
data=f1.readlines()
###############################

#data=f1.readlines()[0:20] #reading only first 20 lines
#data = f1.readlines()
content_list = [x.rstrip() for x in data] #removing trailing white space into a list
#content_list = [str1.replace('\t', ' ') for str1 in content_list] #removing tab space in each string
#############################Marking the end of sentences####################
f2= open('proc.txt', 'w')
for lines in content_list:
    if lines == '':
        print('stoptag',file=f2) #marking end of sentences
    else:
        lines = re.sub(r'"', '.."', lines) # " symbol is replaced to read data correctly
        lines = re.sub(r'!|#|~||#|$', '', lines)
        print(lines, file=f2)
f2.close()
df6= pd.read_csv('proc.txt', header = None, sep= '\t')
df6.fillna('stoptag',inplace= True) # End of the sentences tag for NaN in tag field
entity1 = df6[:][0]
tags1= df6[:][1]
f2= open('proc.txt', 'w')
for i in range(len(entity1)):
    text = re.sub(r"(^https?:\/\/.*[\r\n]*)|(?:\#+[\w_]+[\w\'_\-]*[\w_]+)|(?:@[\w_]+)", 'url', entity1[i])
    text = re.sub(r"\b(\w+n't)\b", 'not', text)
    text = re.sub(r":\)|:‑\)|:-]|:-3|:->|8-\)|:-}|:o\)|:c\)|:^\)|=]|=\)|:\)|:]|:3|:>|8\)|:}|:‑D|:D|8‑D|8D|x‑D|X‑D|=D|=3|B^D|:-\)\)|:'‑\)|:'\):‑O|:O|:‑o|:o|:-0|8‑0|>:O|:-\*|:\*|:×|;‑\)|;\)|\*-\)|\*\|;‑]|;]|;^\)|:‑,|;D\|:‑P|:P|X‑P|x‑p|:‑p|:p|:‑Þ|:‑Þ|:‑þ|:þ|:Þ|:Þ|:‑b|:b|d:|=p|>:P\|O:‑\)|O:\)|0:‑3|0:3|0:‑\)|0:\)|0;^\)|;‑\)|:‑J|#‑\)|%‑\)|%\)|<3|@};-|@}->--|@}‑;‑'‑‑‑|@>‑‑>‑‑", " smilepositive ", text)
#Replace Negative smileys by 'smile_negative'
    text = re.sub(r":‑\(|:\(|:‑c|:c|:‑<|:<|:‑\[|:\[|:-\|\||>:\[|:{|:@|>:\(|:'‑\(|:'\(|D‑':|D:<|D:|D;|D=|:‑/|:/|:‑.|>:\|:L|=L|:S|:‑\||:\||:‑X|:X|:‑#|:#|:‑&|:&|>:‑\)|>:\)|}:‑\)|}:\)|3:‑\)|3:\)|>;\)|',:-l|',:-\||>_>|<_<|<\\3|</3", " smilenegative ", text)
    translator = str.maketrans('', '', string.punctuation)# retrun a table which maps each punctuation to NONE
    text=text.translate(translator)
    text = re.sub(r"xD |XD |XP |xp ", " smilepositive ", text)
    text = re.sub(r"D8 |DX ", " smilenegative ", text)
    text=re.sub(r'[^a-zA-Z0-9]+ ', ' ', text)
    text=text.lower()
    print(text +'\t'+tags1[i],file=f2)
f2.close()
df= pd.read_csv('proc.txt', header = None, sep= '\t')
df.fillna('exclmpunct',inplace= True) # replaceing blank spaces with punctuation
#df= pd.read_csv('NER-Dataset-10Types.txt', header = None, sep= '\t')
########
#np.unique(df[:][1])
'''
different tags
array(['B-company', 'B-facility', 'B-geo-loc', 'B-movie', 'B-musicartist',
       'B-other', 'B-person', 'B-product', 'B-sportsteam', 'B-tvshow',
       'I-company', 'I-facility', 'I-geo-loc', 'I-movie', 'I-musicartist',
       'I-other', 'I-person', 'I-product', 'I-sportsteam', 'I-tvshow',
       'O'], dtype=object)
'''

entity = df[:][0]
tags= df[:][1]
tags_modified = tags.copy(deep= True) # if false it shares data and index with original dataframe, deep copy has its own memory
###################################
####################report file######################
try:
    os.remove("report2.txt")#### deleting output file
    print(" Analysis report file report2.txt File Removed!")
except:
    print("report file does not exist ,it  will be created")
#######################Vocabulary train +test ###################
vocab = np.unique(entity)

######################Removing prefixes B- or I-
for i in range(len(tags)):
    if (tags[i]== 'O' or tags[i] =='stoptag'):
        tags_modified.at[i] = tags[i] # modifying data frame
    else:
        tags_modified.at[i] = tags[i][2:]
####################################################
#TEST train split
cross_val_size =3
sentence_index= [] # contains index of sentence ending
for index in range(len(tags_modified)):
    if (tags_modified[index]== 'stoptag'):
        sentence_index.append(index)
# chunking sentence-ending endexes into 3 cross_val_size=3 lists
chunk_index = chunkIt(sentence_index, cross_val_size)
split=[]
for index in chunk_index:
    split.append(max(index))
#######################first train -test pair##############################
f = open('report2.txt','a+')
print('\n cross validation iteration:1',file =f)
f.close()
f3= open('test.txt', 'w')
f4= open('train.txt', 'w')
for i in range(len(entity)):
    if(i<=split[0]):
        print(entity[i]+'\t'+tags[i] + '\t' + tags_modified[i], file=f3)
    else:
        print(entity[i]+'\t'+tags[i] + '\t' + tags_modified[i], file=f4)
f3.close()
f4.close()
train_model(1)


#######################second train -test pair##############################
f = open('report2.txt','a+')
print('\n cross validation iteration:2',file =f)
f.close()
f3= open('test.txt', 'w')
f4= open('train.txt', 'w')
for i in range(len(entity)):
    if(i<=split[1]):
        print(entity[i]+'\t'+tags[i]+ '\t' + tags_modified[i], file=f4)
    else:
        print(entity[i]+'\t'+tags[i]+ '\t' + tags_modified[i], file=f3)
f3.close()
f4.close()
train_model(2)
#######################third train -test pair##############################
f = open('report2.txt','a+')
print('\n cross validation iteration:3',file =f)
f.close()
f3= open('test.txt', 'w')
f4= open('train.txt', 'w')
for i in range(len(entity)):
    if(i>split[0] and i<= split[1]):
        print(entity[i]+'\t'+tags[i] + '\t' + tags_modified[i], file=f3)
    else:
        print(entity[i]+'\t'+tags[i]+ '\t' + tags_modified[i], file=f4)
f3.close()
f4.close()
train_model(3)

####################################    
