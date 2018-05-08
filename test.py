import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

g = nx.DiGraph()
g.add_edge('2', '5', weight=1)
g.add_edge('2', '1', weight=3)
g.add_edge('1', '5', weight=2)
g.add_edge('2', '3', weight=6)
g.add_edge('3', '5', weight=7)

print(g.edges(data=True))

a = ['a', 'b', 'c', 'b', 'c', 'd']
print(set(a))