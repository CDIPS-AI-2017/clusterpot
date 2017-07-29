from collections import Counter
import re
import copy
import heapq
import pprint
import string

book = open("./book3.txt", 'r').read().encode('ascii','ignore').decode('unicode_escape').lower()

keyword = "malfoy"

def findPunc(str, beg, end):
    return min(str.find(".", beg, end), str.find("?", beg, end), str.find("!", beg, end))
    
def rfindPunc(str, beg, end):
    return max(str.rfind(".", beg, end), str.rfind("?", beg, end), str.rfind("!", beg, end))

list = []
for i in re.finditer(keyword, book):
    list.append(i.start())
    
print(list)

i = 0 
while i < len(list):
    newList = [list[i]]
    for j in range(i+1, len(list)):
        if list[j] - list[j-1] < 300:
            newList.append(list[j])
        else:
            i = j-1
            break
    print(newList)
    if(len(newList) >= 4):
        print(book[rfindPunc(book, 0, newList[0])+1:findPunc(book, newList[-1], len(book))+1])
        print()
    i += 1