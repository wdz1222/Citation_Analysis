import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import time


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
    3、利用专利的申请日期，计算不同引用之间的引用时间差，便于挖掘
    专利号生成的专利节点
    '''
    def create_homo_academic_network(self):
        df = pd.read_excel(self.data_path, sheetname=0)
        col_num = df.shape[0]
        homo_G = nx.DiGraph()
        print()
        for i in range(col_num):
            patent_infos = df.loc[i, 'PD'].split(';  ')
            for patent_info in patent_infos:
                patent_info_detail = patent_info.split('   ')
                application_time = time.mktime(time.strptime(patent_info_detail[1], "%d %b %Y"))/3600.0
                homo_G.add_node(patent_info_detail[0], application_time=application_time)
            if not pd.isnull(df.loc[i, 'CP']):
                patent_id = df.loc[i, 'PN'].split('; ')
                cited_infos = df.loc[i, 'CP'].split('--')[1].split(';  ')
                cited_list = [ci.strip().split('   ')[0] for ci in cited_infos]
                cited_list = list(filter(lambda x: len(x.split(' ')) == 1, cited_list))
                for cited_element in cited_list:
                    for pid in patent_id:
                        homo_G.add_edge(cited_element, pid)
        sum_time_difference = 0
        count = 0.0
        for edge in homo_G.edges():
            if 'application_time' in homo_G.node[edge[0]] and 'application_time' in homo_G.node[edge[1]]:
                time_difference = abs(homo_G.node[edge[0]]['application_time'] - homo_G.node[edge[1]]['application_time'])
                homo_G[edge[0]][edge[1]]['time_difference'] = time_difference
                count += 1
                sum_time_difference += time_difference
        ave_time_difference = sum_time_difference/count
        print(count)
        for edge in homo_G.edges():
            if not 'time_difference' in homo_G[edge[0]][edge[1]]:
                homo_G[edge[0]][edge[1]]['time_difference'] = ave_time_difference
        nx.write_gpickle(homo_G, 'data/homo_academic_network.gpickle')
        return homo_G

    '''
    根据同质网络进行绘图
    '''
    @staticmethod
    def plot_homo_academic_network(network_path):
        G = nx.read_gpickle(network_path)
        nx.draw(G, pos=nx.spring_layout(G))
        plt.draw()


# chan = CreateHomoAcademicNetwork('data/experiment_data.xlsx')
CreateHomoAcademicNetwork.plot_homo_academic_network('data/homo_academic_network.gpickle')