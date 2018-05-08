import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

g = nx.DiGraph()
g.add_edge('2', '5')
g.add_edge('2', '1')
g.add_edge('1', '5')
g.add_edge('2', '3')
g.add_edge('3', '5')

print(list(nx.all_simple_paths(g, '2', '5')))
print(list(nx.all_simple_paths(g, '1', '3')))