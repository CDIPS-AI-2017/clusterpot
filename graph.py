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
import pickle

bookname = {"title": "Harry Potter and the Philosopher's Stone", "tag": "book1"}
#bookname = "Harry Potter and the Chamber of Secrets"
parser = English()
f = open("./Book1ThePhilosophersStone_clean.txt")
book = f.read()
print("Book has been read")

import json
import spacy
import requests
import textacy
from spacy.symbols import nsubj, VERB, dobj
from pprint import pprint

from collections import Counter
def people_info(doc):
    people = Counter()
    for ent in doc.ents:
        if ent.label_ in ('CARDINAL', 'ORDINAL'):
            continue
        elif ent.label_ == 'PERSON':
            people[ent.lemma_] += 1
    return people

nlp = spacy.load('en')
doc = nlp(book)
list_of_people = people_info(doc)
print(list_of_people)

output = open('pickledPeople.pkl', 'wb')

# Pickle dictionary using protocol 0.
pickle.dump(list_of_people, output)
