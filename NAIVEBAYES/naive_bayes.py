import re
import random
import string
import os,sys
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords 
import itertools
#from nltk.stem import WordNetLemmatizer
#wordnet_lemmatizer = WordNetLemmatizer()




#Read Data
#f1 = open('Dataset.txt',"rb")
f1 = open('Dataset.txt',errors="ignore")	
data = f1.read()
#print('Initial data:{}'.format(data))

#Removing unnecessary blank spaces
data=re.sub(' +', ' ', data)
print('Blank removal done')

#Removing URLs, Hashtag and mentions
text = re.sub(r"(^https?:\/\/.*[\r\n]*)|(?:\#+[\w_]+[\w\'_\-]*[\w_]+)|(?:@[\w_]+)", '', data, flags=re.MULTILINE)
print('URL, Hashtags and Mentions Removal done')

#Replace apexes by 'not'
text = re.sub(r"\b(\w+n't)\b", 'not', text)
print('Apexes conversion Removal done')

#Replace Positive smileys by 'smile_positive'
text = re.sub(r":\)|:‑\)|:-]|:-3|:->|8-\)|:-}|:o\)|:c\)|:^\)|=]|=\)|:\)|:]|:3|:>|8\)|:}|:‑D|:D|8‑D|8D|x‑D|X‑D|=D|=3|B^D|:-\)\)|:'‑\)|:'\):‑O|:O|:‑o|:o|:-0|8‑0|>:O|:-\*|:\*|:×|;‑\)|;\)|\*-\)|\*\|;‑]|;]|;^\)|:‑,|;D\|:‑P|:P|X‑P|x‑p|:‑p|:p|:‑Þ|:‑Þ|:‑þ|:þ|:Þ|:Þ|:‑b|:b|d:|=p|>:P\|O:‑\)|O:\)|0:‑3|0:3|0:‑\)|0:\)|0;^\)|;‑\)|:‑J|#‑\)|%‑\)|%\)|<3|@};-|@}->--|@}‑;‑'‑‑‑|@>‑‑>‑‑", " smilepositive ", text)

#Replace Negative smileys by 'smile_negative'
text = re.sub(r":‑\(|:\(|:‑c|:c|:‑<|:<|:‑\[|:\[|:-\|\||>:\[|:{|:@|>:\(|:'‑\(|:'\(|D‑':|D:<|D:|D;|D=|:‑/|:/|:‑.|>:\|:L|=L|:S|:‑\||:\||:‑X|:X|:‑#|:#|:‑&|:&|>:‑\)|>:\)|}:‑\)|}:\)|3:‑\)|3:\)|>;\)|',:-l|',:-\||>_>|<_<|<\\3|</3", " smilenegative ", text)

#print('After treating smileys:{}'.format(text))

#Remove punctuations from the text

#punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
'''
no_punct = ""
for char in text:
   if char not in punctuations:
       no_punct = no_punct + char
text = no_punct
'''
translator = str.maketrans('', '', string.punctuation)# retrun a table which maps each punctuation to NONE
text=text.translate(translator)

#Replace some special Positive involving letters by 'smile_positive' this is done because we don't want "xplore" to replaced as "smilepositiveplore" 
text = re.sub(r"xD |XD |XP |xp ", " smilepositive ", text)

#Replace Negative special smileys by 'smile_negative' this is done because we don't want "DX275" to replaced as "smilenegative275"
text = re.sub(r"D8 |DX ", " smilenegative ", text)
#Replace any unsolicited charecters apart from alphaneumeric and spaces
text=re.sub(r'[^a-zA-Z0-9]+ ', ' ', text)

text = re.sub(r"smilepositive", 'smile_positive', text)
text = re.sub(r"smilenegative", 'smile_negative', text)

#print('After punctuations Removal:{}'.format(text))

#Converting to lowercase
text=text.lower()
print('After converting to lowercase done')
f2 = open("preprocessed.txt","w")
print(text,file=f2)
f2.close()

#Stemming (Sentence wise) 
f3 = open("preprocessed.txt",'r')
text=f3.readlines()
ps = PorterStemmer()
stems1=[]
for line in text:
    tokens = word_tokenize(line)
    stems=[]
    for word in tokens:
        #print("Actual: %s  Stem: %s"  % (word,ps.stem(word)))
        #print("Actual: %s  Lemma: %s"  % (word,wordnet_lemmatizer.lemmatize(word)))
        stems.append(ps.stem(word))
    stems1.append(stems)
print('stemming done')
#for i in range(len(stems1)):
#    print(" ".join(stems1[i]))
#f3.close()

#Stemmed data is written to file
f2 = open("preprocessed.txt","w")
for i in range(len(stems1)):
    print(" ".join(stems1[i]),file=f2)
f2.close()

#Removal of Stop Words
f2 = open("preprocessed.txt")
text=f2.readlines()
stop_words = set(stopwords.words('english'))
stop1 = [] 
for line in text:
    word_tokens = word_tokenize(line) 
#    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w)
    stop1.append(filtered_sentence) 
print('removal of stop words done')
#for i in range(len(stop1)):
#    print(" ".join(stop1[i]))
f2.close()
#Pre-processed data is written to file
print("preprocessing completed")
print("preprocessed data strored into file preprocessed.txt")
f2 = open("preprocessed.txt","w")
for i in range(len(stop1)):
    print(" ".join(stop1[i]),file=f2)
f2.close()
#removing any other unnecessary charecters
f0 = open('preprocessed.txt',"r")	
data = f0.read()
data= re.sub(r'([^\s\w]|_)+', '', data)
f01 = open("preprocessed.txt","w")
print(data,file=f01)
f01.close()
#split data into train and test parts
print("splitting the data into train and test ratio 75% 25% respectively")
f3 = open("preprocessed.txt","r")
dataset = f3.readlines()
splitRatio=0.75
trainSize = int(len(dataset) * splitRatio)
trainSet = []
copy = dataset
#print("number of data",len(copy))
while len(trainSet) < trainSize:
  # print(" ".join(copy(index)))
   index = random.randrange(len(copy))
   trainSet.append(copy.pop(index))
testSet=copy
f4 = open("train.txt","w")
f5 = open("test.txt","w")
#print("number tweets in trainset",len(trainSet))
#print("number tweets testset",len(testSet))

trainSet = map(lambda s: s.strip(), trainSet)#removing unneccesary new lines added
testSet = map(lambda s: s.strip(), testSet)#removing unneccesary new lines added
for line in trainSet:
   print(line,file=f4)
f4.close() 
for line in testSet:
   print(line,file=f5)
f5.close() 
print("train data is stored in train.txt")
print("test data is stored in test.txt")

#separating the classes
'''
f6 = open("train.txt","r")
dataset = f6.readlines()
separated = {}
for i in range(len(dataset)):
   vector = dataset[i]
   if (vector[0] not in separated):
      separated[vector[0]] = []
   separated[vector[0]].append(vector[1:].rstrip())
print('Separated instances:'.format(separated))
#print(testset,file=f4)'''

#Collecting postive class words /negative class words in lists and set containing unique words:
print("Reading train data")
f6 = open("train.txt","r")
dataset = f6.readlines()
uniquewordset = set()
positiveclass =[]
negativeclass =[]
N_positive=0
N_negative=0
#ib=[]
for line in dataset:
    word_tokens = word_tokenize(line[1:])# dropping initial class level
    if line[0]=='0':
        N_negative+=1 # Count negative class i.e 0
        for w in word_tokens:
            negativeclass.append(w)
            uniquewordset.add(w)
            #ib.append(w)
    else:
        N_positive+=1 #Count positive class i.e 1
        for w in word_tokens:
            positiveclass.append(w)
            uniquewordset.add(w)
            
N = len(uniquewordset)
count_pos_word=len(positiveclass)#total number of words in positive class for train data
count_neg_word=len(negativeclass)#total number of words in negative class for test data
#calculating prior class probability
Prior_pos=N_positive/(N_positive+N_negative)
Prior_neg=N_negative/(N_positive+N_negative)
print("prior probability positive class",Prior_pos)
print("prior probability negative class",Prior_neg)
#print(count_pos_word)
#print(count_neg_word)


print("reading test data")
f7 = open("test.txt","r")
f8 = open("output.txt","w")
dataset = f7.readlines()
for line in dataset:
    #print(line)
    word_tokens = word_tokenize(line[1:])
    posterior_negative=Prior_neg
    posterior_positive=Prior_pos
    for w in word_tokens:
  #      print("w",w)
        freq1=0
        freq2=0
        for w1 in negativeclass:
            if w==w1:
             #   print("w1",w1)
                freq1+=1
      #  print("freq1",freq1)
        posterior_negative=posterior_negative*((freq1+1)/(count_neg_word+N))#N is total number of unique words in train data, 1 is added in denominator for smooting
        for w2 in positiveclass:
            if w==w2:
              #  print("w2",w2)
                freq2+=1
   #     print("freq2",freq2)
        posterior_positive=posterior_positive*((freq2+1)/(count_pos_word+N))#N is total number of unique words in train data, 1 is added in denominator for smooting
   # print(line,posterior_negative,posterior_positivetive)
    if posterior_positive > posterior_negative: #assigning class based on Naive bayes
        print(line[0]+" 1 "+ line[1:].rstrip(),file=f8)#adding predicted class level and removing addition new line by rstrip()
    else:
        print(line[0]+" 0 "+line[1:].rstrip(),file=f8)#adding predicted class level and removing addition new line by rstrip()
f7.close
f8.close
#calculate parameters
f8 = open("output.txt","r")
dataset = f8.readlines()
TP=TN=FP=FN=0

for line in dataset:
    if line[0]=='1': #actual positive
        if line[2]=='1': #actual positive classified positive
            TP+=1
        elif line[2]=='0': #actual positive classified negative
            FN+=1
    elif line[0]=='0': #actual negative 
        if line[2]=='1': #actual negative classified positive
            FP+=1
        elif line[2]=='0': #actual negative classified negative
            TN+=1
accuracy = (TP+TN)/(TP+TN+FP+FN)
precision=(TP)/(TP+FP)
recall=(TP)/(TP+FN)
F_measure=(2*precision*recall)/(precision + recall)
print("output is stored in output.txt")
print("confusion matrix:-")
print("TP:",TP,"FN:",FN)
print("FP:",FP,"TN:",TN)
print("******************metric*************")
print("accuracy:",accuracy)
print("precision:",precision)
print("recall:",recall)
print("F-Measure",F_measure)
input()

    

        
     






        
        





