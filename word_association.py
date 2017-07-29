from collections import Counter
import re
import copy
import heapq
import pprint
import string

book = open("./book3.txt", 'r').read().encode('ascii','ignore').decode('unicode_escape').lower()

def strip_all_punctuation(text):
    stripped_text = ""
    for c in text:
        if (ord(c) < 97 or ord(c) > 122) and ord(c) != 39:
            c = " "
        stripped_text += c
    return stripped_text

book = strip_all_punctuation(book)
#print(book)

def wordcount_from_book(book):
    wordDict = Counter()
    for word in book.split():
        wordDict[word] += 1
    return wordDict
    
c = wordcount_from_book(book)

keyword = "malfoy"

c_keyword = copy.deepcopy(c)
c_keyword.subtract(c_keyword)

for m in re.finditer(keyword, book):
    slice = book[m.start()-100:m.start()+100].split()
    for word in slice:
        if word in c.keys() and c[word] > 2 and len(word) > 2:
            c_keyword[word] += 1
            

result = Counter()
for k in c.keys():
    if (c_keyword[k] != 0):
        result[k] = c_keyword[k]/c[k]
    
print(result.most_common(40))


    