import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pensieve
from collections import Counter
import math

def max_degree(G):
    max_deg = 0
    for node in G.nodes():
        if G.degree(node) > max_deg:
            max_deg = G.degree(node)
    return max_deg
    
def sanitize_data_potter(list_of_people):
    if 'Hogwarts' in list_of_people.keys():
        del list_of_people['Hogwarts']
    if 'Don' in list_of_people.keys():
        del list_of_people['Don']
    if 'Yeh' in list_of_people.keys():
        del list_of_people['Yeh']
    return list_of_people
    
def clean_graph(G,str1,str2):
    if str1 not in G.node.keys() or str2 not in G.node.keys():
        return G
    G.node[str1]['weight'] += G.node[str2]['weight']
    for neighbor in G[str2].keys():
        w = G[str2][neighbor]['weight']
        if (str1,neighbor) in G.edges() or (neighbor,str1) in G.edges():
            G[str1][neighbor]['weight'] += w
        else:
            G.add_edge(str1,neighbor,weight=w,thickness=1)
    G.remove_node(str2)
    return G

def clean_potter(G):
    G = clean_graph(G, 'Harry', 'Potter')
    G = clean_graph(G, 'Harry', 'Harry Potter')
    G = clean_graph(G, 'Lockhart', 'Gilderoy Lockhart')
    G = clean_graph(G, 'Aunt Marge', 'Marge')
    G = clean_graph(G, 'Krum', 'Viktor Krum')
    G = clean_graph(G, 'Flamel', 'Nicolas Flamel')
    G = clean_graph(G, 'Hermione', 'Hermione Granger')
    G = clean_graph(G, 'Hermione', 'Granger')
    G = clean_graph(G, 'Dursleys', 'Dursley')
    G = clean_graph(G, 'Dumbledore', 'Albus Dumbledore')
    G = clean_graph(G, 'Voldemort', 'Lord Voldemort')
    G = clean_graph(G, 'Tom Riddle', 'Riddle')
    G = clean_graph(G, 'Draco Malfoy', 'Malfoy')
    G = clean_graph(G, 'Draco', 'Draco Malfoy')
    G = clean_graph(G, 'Scrimgeour', 'Rufus Scrimgeour')
    G = clean_graph(G, 'Neville', 'Neville Longbottom')
    G = clean_graph(G, 'Colin', 'Colin Creevey')
    G = clean_graph(G, 'Moaning Myrtle', 'Myrtle')
    G = clean_graph(G, 'Arthur Weasley', 'Arthur')
    G = clean_graph(G, 'Ginny', 'Ginny Weasley')
    G = clean_graph(G, 'Lucius Malfoy', 'Lucius')
    G = clean_graph(G, 'Pettigrew', 'Peter Pettigrew')
    G = clean_graph(G, 'Lavender', 'Lavender Brown')
    G = clean_graph(G, 'Bagman', 'Ludo Bagman')
    G = clean_graph(G, 'Bagman', 'Ludo')
    G = clean_graph(G, 'Fudge', 'Cornelius Fudge')
    
    return G
    
def create_graph(book,n):
    G = nx.Graph()
    list_of_people = sanitize_data_potter(Counter(book.words['people']))
    list_of_people = dict(list_of_people.most_common(n))
    for key in list_of_people.keys():
        G.add_node(key, weight=list_of_people[key])
    for i in range(len(book.paragraphs)):
        para_ppl = book.paragraphs[i].build_words_dict()['people']
        for person1 in para_ppl.keys():
            if person1 in list_of_people.keys():
                for person2 in para_ppl.keys():
                    if person2 in list_of_people.keys() and person2 != person1:
                        w = para_ppl[person1] + para_ppl[person2]
                        if (person1,person2) in G.edges() or (person2,person1) in G.edges():
                            G[person1][person2]['weight'] += w
                        else:
                            G.add_edge(person1,person2,weight=w,thickness=1)
    print(list_of_people)
    return G
    
book = pensieve.Doc("./book7.txt")
G = clean_potter(create_graph(book,70))

for edge in G.edges(data = True):
    p1 = (edge[2]['weight']/G.node[edge[0]]['weight'])
    p2 = (edge[2]['weight']/G.node[edge[1]]['weight'])
    edge[2]['weight'] = max(p1*math.pow(p2,0.8),p2*math.pow(p1,0.8))
    edge[2]['thickness'] = math.sqrt(edge[2]['weight'])
    
pos=nx.spring_layout(G)

edge_colors = ['blue' for edge in G.edges()]
edge_widths = [d['thickness'] for u,v,d in G.edges(data=True)]

nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors)

node_sizes = [100+50*G.degree(node) for node in G.nodes()]
node_colors = [G.degree(node)/max_degree(G) for node in G.nodes()]
node_labels = {node[0]:node[0] for node in G.nodes(data=True)}

nx.draw_networkx_nodes(G, pos,node_color = node_colors, node_size=node_sizes, node_shape='h', cmap=plt.get_cmap('GnBu'),vmin=0,vmax=1, linewidths=5)
nx.draw_networkx_labels(G, pos, labels=node_labels)

plt.axis('off')
pylab.show()