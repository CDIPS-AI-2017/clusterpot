from spacy.en import English
import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import yaml
from fuzzywuzzy import fuzz
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import string
from collections import Counter
import json
import spacy
import requests
import textacy
from spacy.symbols import nsubj, VERB, dobj
from pprint import pprint
import nltk
from nltk import sentiment
from collections import defaultdict
import nltk.data
import copy

parser = English()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
SA = nltk.sentiment.vader.SentimentIntensityAnalyzer()

# Parse the book; takes in a file name and a dictionary {title, tag} and returns an array of scene numbers, which are dictionaries consisting of a title key and an text key.
def parseBook(filename, bookname):
    f = open(filename)
    book = dict()
    timewords = ["morning", "day", "days", "evening", "night", "week", "weeks", "afternoon"]
    scene_number = 0
    c = str()
    chapter_number = 0
    book[scene_number] = dict()
    book[scene_number]["title"] = bookname["title"]
    for l in f:
        #l =str(l)
        if "CHAPTER" in l:
            # strip out chapter headings
            pass
        elif l.isupper() and ("." not in l) and ("?" not in l) and ("!" not in l):
            # new chapter
            scene_number += 1
            book[scene_number] = dict()
            book[scene_number]["title"] = l
            c = str()
        else:
            isTimeskip = False
            for tw in timewords:
                if (("next " + tw) in l) or (("Next " + tw) in l):
                    scene_number += 1
                    book[scene_number] = dict()
                    book[scene_number]["title"] = l
                    c = str()
            c += l
            book[scene_number]["text"] = c
    book[scene_number] = {"title": l, "text":c}
    return book

#takes a doc that has been nlp'd and returns a Counter of people by number of mentions.
def people_info(doc):
    people = Counter()
    for ent in doc.ents:
        if ent.label_ in ('CARDINAL', 'ORDINAL'):
            continue
        elif ent.label_ == 'PERSON':
            people[ent.lemma_] += 1
    return people

#returns a dictionary of people in a book, by number of mentions.
def makeList(book):
    nlp = spacy.load('en')
    list_of_people = Counter()
    for scene_num in range(1,len(book)):
        #print(book[scene_num]["title"])
        if 'text' in book[scene_num].keys():
            doc = nlp(book[scene_num]["text"])
            list_of_people += people_info(doc)
    list_of_people = {key: value for key, value in list_of_people.items() if len(key) > 2} #cleans data
    return list_of_people

'''for scene_num in range(1,len(book)):
    print(book[scene_num]["title"]) #TODO: This isn't helpful, print relevant keywords instead?
    if 'text' in book[scene_num].keys():
        sentences = tokenizer.tokenize(book[scene_num]["text"])
        #sentences = book[scene_num]["text"].split(enterkey)
        #print(sentences)
        n_counter = 0
        p_counter = 0
        numSentences = 0
        numCharged = 0
        for sentence in sentences: 
            #print("Hello world")
            d = SA.polarity_scores(sentence)
            #print(d)
            numSentences += 1
            if(d == None):
                #print("Nne")
                pass
            elif(d['neu']<0.92 and (d['neu']<0.8 or abs(d['neg']-d['pos']) > 0.05)):
                #print(sentence)
                #print(d)
                numCharged += 1
                #n_counter += d['neg']
                #p_counter += d['pos']
                if d['neg'] < d['pos']:
                    p_counter +=1
                else:
                    n_counter += 1
        print()
    if numSentences >= 3 and numCharged != 0:
        print(numCharged/numSentences)
        print(n_counter/numCharged)
        print(p_counter/numCharged)
    print()'''
    

#takes a book and a list and ranks the 100 most common names on that list by positive/negative sentiment.
def rateSentiments(book, list_of_people):
    list_of_people = Counter(dict(Counter(list_of_people).most_common(100)))
    nCounter = copy.deepcopy(list_of_people)
    pCounter = copy.deepcopy(list_of_people)
    nCounter.subtract(nCounter)
    pCounter.subtract(pCounter)

    for scene_num in range(1,len(book)):
        if 'text' in book[scene_num].keys():
            sentences = tokenizer.tokenize(book[scene_num]["text"])
            for sentence in sentences: 
                d = SA.polarity_scores(sentence)
                if(d == None):
                    pass
                elif(d['neu']<0.92 and (d['neu']<0.8 or abs(d['neg']-d['pos']) > 0.05)):
                    for key in list_of_people.keys():
                        if key in sentence.lower():
                            if d['neg'] < d['pos']:
                                pCounter[key] +=1
                            else:
                                nCounter[key] += 1


    x= copy.deepcopy(pCounter)
    x.subtract(nCounter)
    return x
    
book = parseBook("./book1.txt", {"title": "Harry Potter and the Philosopher's Stone", "tag": "book1"})
list_of_people = makeList(book)
#print(list_of_people)
print(rateSentiments(book, list_of_people))
book = parseBook("./book2.txt", {"title": "Harry Potter and the Chamber of Secrets", "tag": "book2"})
list_of_people = makeList(book)
print(rateSentiments(book, list_of_people))
book = parseBook("./book3.txt", {"title": "Harry Potter and the Prisoner of Azkaban", "tag": "book3"})
list_of_people = makeList(book)
print(rateSentiments(book, list_of_people))