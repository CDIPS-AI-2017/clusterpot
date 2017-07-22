f = open('./SentiWordNet_3.0.0_20130122.txt')
text = ''
for l in f:
    text += "%s\n" %l.split('#')[0]
f = open('./Senti_clean.txt','w+')
f.write(text)
f.flush()
f.close()
