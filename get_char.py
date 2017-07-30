from collections import Counter
import re
import copy
import heapq
import pprint
import string
from spacy.en import English
import spacy
from spacy.symbols import nsubj, VERB, dobj
#import nltk
#from nltk import sentiment
#import nltk.data


def findPunc(str, beg, end):
    return min(str.find(".", beg, end), str.find("?", beg, end), str.find("!", beg, end))
    
def rfindPunc(str, beg, end):
    return max(str.rfind(".", beg, end), str.rfind("?", beg, end), str.rfind("!", beg, end))

def getSentence(str, index):
    return str[rfindPunc(book, 0, index)+1:findPunc(book, index, len(book))+1]


#SA = nltk.sentiment.vader.SentimentIntensityAnalyzer()

def getKeyMemories(keyword, book):
    list = []
    for i in re.finditer("\W"+keyword+"\W", book):
        list.append(i.start())
    #print(list)

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
            #print(newList[0])
            start = rfindPunc(book, 0, newList[0])+1
            end = findPunc(book, newList[-1]+len(keyword), len(book))+1
            if start == -1:
                start = 0
            if end >= len(book) or end == 0:
                end = len(book)
            memory = book[start:end]
            if memory[0] is "\"":
                mem.append(book[book.rfind("\"", 0, start-1):end])
            else:
                mem.append(memory)
        i += 1
    return mem


def getKeySentences(memList, keyword):
    keySentenceList = []
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
            if sentence[0] =="\"":
                keySentenceList.append(memList[i-1]+sentence)
            else:
                keySentenceList.append(sentence)
    return keySentenceList


book = open("./book5.txt", 'r').read().encode('ascii','ignore').decode('unicode_escape').lower()
nlp = spacy.load('en')

characters = open("./list_of_people.txt", 'r').read()
list_of_people = characters.split("\n")
#print(list_of_people)

people_in_book = Counter()

for person in list_of_people:
    sum = 0
    list = person.split()
    if (person.lower() in book) or (len(list) > 1 and "professor "+list[1].lower() in book):
        if (list[0] == "Mr.") or (list[0] == "Mrs."):
            print(list)
            sum += len(getKeyMemories(person.lower(), book))
        else:
            for word in list:
                sum += len(getKeyMemories(word.lower(), book))
    #print(person)
    if sum != 0:
        #print(sum)
        people_in_book[person] = sum

print(people_in_book)
#print(getKeyMemories("mr. weasley", book))
'''keyword = "mcgonagall"

mem = getKeyMemories(keyword, book)

print(mem[2])
print()

memList = re.split("[\!\?\.]", mem[2])

print(getKeySentences(memList,keyword))'''

#this misses instances of things done where he is referred to as 'he' instead of "Malfoy".