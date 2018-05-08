import numpy as np
import networkx as nx
import pandas as pd

class CitationAnalysis:

    def __init__(self, data_path):
        self.data_path = data_path
        self.homo_academic_network = self.create_homo_academic_network()

    def create_homo_academic_network(self):
        df = pd.read_excel(self.data_path, sheetname=0)
        print(df.head())
        print(df.columns.values)
        print(df.loc[0, 'PN'])
        G = nx.DiGraph()


ca = CitationAnalysis('data/experiment_data.xlsx')
