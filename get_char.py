from collections import Counter
import re
import copy
import heapq
import pprint
import string
import nltk
from nltk import sentiment
import nltk.data

book = open("./book3.txt", 'r').read().encode('ascii','ignore').decode('unicode_escape').lower()

keyword = "malfoy"

def findPunc(str, beg, end):
    return min(str.find(".", beg, end), str.find("?", beg, end), str.find("!", beg, end))
    
def rfindPunc(str, beg, end):
    return max(str.rfind(".", beg, end), str.rfind("?", beg, end), str.rfind("!", beg, end))

def getSentence(str, index):
    return str[rfindPunc(book, 0, index)+1:findPunc(book, index, len(book))+1]
list = []
for i in re.finditer(keyword, book):
    list.append(i.start())
    
print(list)

SA = nltk.sentiment.vader.SentimentIntensityAnalyzer()

mem = []

i = 0 
while i < len(list):
    newList = [list[i]]
    for j in range(i+1, len(list)):
        if list[j] - list[j-1] < 300:
            newList.append(list[j])
        else:
            i = j-1
            break
    if(len(newList) >= 4):
        print(newList)
        mem.append(book[rfindPunc(book, 0, newList[0])+1:findPunc(book, newList[-1], len(book))+1])
    i += 1
    
#for scene in mem:
#    print(scene)
#    print(SA.polarity_scores(scene))
    
from spacy.symbols import nsubj, VERB
from spacy.en import English
import spacy

nlp = spacy.load('en')

print(mem[5])
print()

memList = re.split("[\!\?\.]", mem[5])
#print("i split the memlist")

for i in range(0, len(memList)):
    sentence = memList[i]
    #print(sentence)
    doc = nlp(sentence)
    boolVar= False
    verbs = set()
    for possible_subject in doc:
        if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
            for w in possible_subject.head.lefts:
                if keyword in w.text:
                    verbs.add(possible_subject.head)
                    boolVar = True
                    
    for possible_verb in doc:
        if possible_verb.pos == VERB:
            for possible_subject in possible_verb.children:
                if possible_subject.dep == nsubj:
                    for w in possible_subject.head.rights:
                        if keyword in w.text:
                            verbs.add(possible_verb)
                            boolVar = True
                            
    if boolVar:
        print(verbs)
        if sentence[0] =="\"":
            print(memList[i-1]+sentence)
        else:
            print(sentence)

#this misses instances of things done where he is referred to as 'he' instead of "Malfoy".