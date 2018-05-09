import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import time

# g = nx.DiGraph()
# g.add_edge('2', '5', weight=1)
# g.add_edge('2', '1', weight=3)
# g.add_edge('1', '5', weight=2)
# g.add_edge('2', '3', weight=6)
# g.add_edge('3', '5', weight=7)
# g.add_node('2', time=2)
# d = g.degree()
# print(d['1'])
#
# g1 = nx.fast_gnp_random_graph(80, 0.4)
# # print(g1.nodes())
# print(nx.current_flow_betweenness_centrality_subset(g1, sources=[1, 2], targets=[4, 6]))

# print(g.edges(data=True))
# weight = [d[2]['weight'] for d in g.edges(data=True)]
# print(weight)
# a = g.edges(data=True)
# a.sort(key=lambda x: x[2]['weight'], reverse=True)
# print(a)
# s = 'US2017232811-A1   17 Aug 2017   B60G-009/04   201756Pages: 21   English;  CA2955584-A1   17 Aug 2017' \
#     '   B60B-035/04   201757   English'
# sl = s.split(';  ')
# t = sl[0].split('   ')
# print(t[0])
# print(t[1])
# print(time.mktime(time.strptime(t, "%d %b %Y")))

# df = pd.read_excel('data/experiment_data.xlsx', sheetname=0)
# print(df.loc[55]['PD'])
# b = s.split('--')[1].split(';  ')
# c = [bi.strip().split('   ')[0] for bi in b]
# print(len(c[1].split()))
# # print(list(filter(lambda x: len(x.split(' ')) == 1, c)))
# g2 = nx.read_gpickle('data/homo_academic_network.gpickle')
# print(g2.edges(data=True))
# # print(g2.nodes(data=True))
# # a = {}
# # print(len(a))
a = {1:8, 3:4, 5:5}
print(1 in a)
a[4] =4
print(sorted(a.items(),key = lambda x:x[1],reverse = True))
