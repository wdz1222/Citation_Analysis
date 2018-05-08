import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


class CreateHomoAcademicNetwork:

    def __init__(self, data_path):
        self.data_path = data_path
        self.homo_academic_network = self.create_homo_academic_network()
        print(self.homo_academic_network.number_of_nodes())
        print(self.homo_academic_network.number_of_edges())

    '''
    构造同构学术网络即专利引用网络
    需要注意：
    1、同构学术网络仅存在专利节点
    2、相同专利可能有不同的专利号，以不同专利号生成新的学术网络节点，被引专利同时指向不同
    专利号生成的专利节点
    '''
    def create_homo_academic_network(self):
        df = pd.read_excel(self.data_path, sheetname=0)
        col_num = df.shape[0]
        homo_G = nx.DiGraph()
        for i in range(col_num):
            if pd.isnull(df.loc[i, 'CP']):
                homo_G.add_nodes_from(df.loc[i, 'PN'].split('; '))
            else:
                cited_list = df.loc[i, 'CP'].split('--')[1].split(';')
                patent_id = df.loc[i, 'PN'].split('; ')
                for cited_element in cited_list:
                    for pid in patent_id:
                        homo_G.add_edge(cited_element.strip().split(' ')[0], pid)
        nx.write_gpickle(homo_G, 'data/homo_academic_network.gpickle')
        return homo_G

    '''
    根据同质网络进行绘图
    '''
    def plot_homo_academic_network(self):
        nx.draw(self.homo_academic_network, pos=nx.spring_layout(self.homo_academic_network))
        plt.draw()


chan = CreateHomoAcademicNetwork('data/experiment_data.xlsx')
# chan.plot_homo_academic_network()