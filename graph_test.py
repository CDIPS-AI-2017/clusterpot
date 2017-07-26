import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pprint, pickle
import re
from collections import Counter

pkl_file = open('pickledPeople.pkl', 'rb')

list_of_people = pickle.load(pkl_file)
print(list_of_people)
list_of_people = Counter(dict(list_of_people.most_common(20))) #150?
pprint.pprint(list_of_people)

f = open("./Book1ThePhilosophersStone_clean.txt")
book = f.read().lower()
G = nx.Graph()

for key in list_of_people.keys():
    for m in re.finditer(key, book):
        #print(key, m.start(), m.end())
        for key2 in list_of_people.keys():
            slice = book[m.start():m.start()+500]
            if (key2 is not key) and (key2 in slice):
                if ((key,key2) in G.edges()) or ((key2,key) in G.edges()):
                    #if(key1 is 'harry') and (key2 is 'quirrell'):
                    print("Hello world")
                    G[key][key2]['weight'] += 1
                else:
                    G.add_edge(key, key2, weight=1)

pprint.pprint(G.edges())
print(G['harry']['quirrell']['weight'])
print()

val_map = {'A': 1.0, 'D': 0.5714285714285714, 'H': 0.0}

values = [val_map.get(node, 0.45) for node in G.nodes()]
edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
edge_colors = ['black' for edge in G.edges()]
#node_colors = ['red' if (G.degree(node) <=7) else 'blue' for node in G.nodes()]
node_colors = ['blue' for node in G.nodes()]
node_sizes = [500+200*G.degree(node) for node in G.nodes()]

pos=nx.spring_layout(G)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
nx.draw(G,pos, node_color = node_colors, node_size=node_sizes,edge_color=edge_colors,edge_cmap=plt.cm.Reds)
node_labels = {node:node for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels)

#for node, adjacencies in enumerate(G.adjacency_list()):
#    node_trace['marker']['color'].append(len(adjacencies))
#    node_trace['marker']['size'].append(len(adjacencies))
#    node_info = '# of connections: '+str(len(adjacencies))
#    node_trace['text'].append(node_info)

pylab.show()