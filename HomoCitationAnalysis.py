import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class HomoCitationAnalysis:

    def __init__(self, network_path):
        self.network_path = network_path

    '''
    初始化引用链接遍历数
    需要注意的是同时保存了遍历数的倒数，便于将主路径查找转化为最小路径的查找
    '''

    def init_iter_num(self, network):
        for edge in network.edges():
            network[edge[0]][edge[1]]['iter_num_nppc'] = 0
            network[edge[0]][edge[1]]['iter_num_back_nppc'] = 999
            network[edge[0]][edge[1]]['iter_num_splc'] = 0
            network[edge[0]][edge[1]]['iter_num_back_splc'] = 999
            network[edge[0]][edge[1]]['iter_num_spnp'] = 0
            network[edge[0]][edge[1]]['iter_num_back_spnp'] = 999
            network[edge[0]][edge[1]]['iter_num_spc'] = 0
            network[edge[0]][edge[1]]['iter_num_back_spc'] = 999
        return network

    '''
    用于确定引文网络中的源点集合与终点集合
    确定源点集合与终点的规则如下：
    1、如果该节点只有出度没有入度，则该节点为源点集合
    2、如果该节点只有入度没有出度，则该节点为终点结合
    3、如果不满足上述两个条件的都为中间节点
    '''

    def find_source_and_terminus(self, network):
        in_degree = network.in_degree(weight=None)
        out_degree = network.out_degree(weight=None)
        source_list = []
        terminus_list = []
        for node in network.nodes():
            if out_degree[node] == 0:
                terminus_list.append(node)
            if in_degree[node] == 0:
                source_list.append(node)
        return source_list, terminus_list

    '''
    局部遍历权重计算模型（nppc,splc,spnp,spc）
    '''

    def local_main_path_analysis(self):
        academic_network = nx.read_gpickle(self.network_path)
        academic_network = self.init_iter_num(academic_network)
        source_list, terminus_list = self.find_source_and_terminus(academic_network)
        print(len(source_list))
        print(len(terminus_list))
        for s in source_list:
            for t in terminus_list:
                paths = list(nx.all_simple_paths(academic_network, s, t))
                if len(paths) != 0:
                    print(paths)
                    for path in paths:
                        for i in range(len(path) - 1):
                            # spc
                            academic_network[path[i]][path[i + 1]]['iter_num_spc'] = \
                                academic_network[path[i]][path[i + 1]]['iter_num_spc'] + 1
                            academic_network[path[i]][path[i + 1]]['iter_num_back_spc'] = \
                                1.0 / academic_network[path[i]][path[i + 1]]['iter_num_spc']
                            # nppc
                            academic_network[path[i]][path[i + 1]]['iter_num_nppc'] = \
                                academic_network[path[i]][path[i + 1]]['iter_num_nppc'] + len(path) - i - 1
                            academic_network[path[i]][path[i + 1]]['iter_num_back_nppc'] = \
                                1.0 / academic_network[path[i]][path[i + 1]]['iter_num_nppc']
                            # splc
                            academic_network[path[i]][path[i + 1]]['iter_num_splc'] = \
                                academic_network[path[i]][path[i + 1]]['iter_num_splc'] + len(path) - 1
                            academic_network[path[i]][path[i + 1]]['iter_num_back_splc'] = \
                                1.0 / academic_network[path[i]][path[i + 1]]['iter_num_splc']
                            # spnp
                            academic_network[path[i]][path[i + 1]]['iter_num_spnp'] = \
                                academic_network[path[i]][path[i + 1]]['iter_num_spnp'] + i + 1
                            academic_network[path[i]][path[i + 1]]['iter_num_back_spnp'] = \
                                1.0 / academic_network[path[i]][path[i + 1]]['iter_num_spnp']
        nx.write_gpickle(academic_network, 'data/homo_academic_network_local.gpickle')

    '''
    局部主路径搜索
    搜索原则：总是按照遍历权重最大的边游走
    '''

    def find_local_main_path(self):
        academic_network = nx.read_gpickle('data/homo_academic_network_local.gpickle')
        source_list, terminus_list = self.find_source_and_terminus(academic_network)
        file_path_spc = 'data/path_spc.txt'
        file_path_nppc = 'data/path_nppc.txt'
        file_path_splc = 'data/path_splc.txt'
        file_path_spnp = 'data/path_spnp.txt'
        for source_node in source_list:
            for terminus_node in terminus_list:
                paths = list(nx.all_simple_paths(academic_network, source_node, terminus_node))
                if len(paths) != 0:
                    path_spc = list(nx.shortest_path(academic_network, source_node, terminus_node,
                                                     weight='iter_num_back_spc'))
                    path_nppc = list(nx.shortest_path(academic_network, source_node, terminus_node,
                                                      weight='iter_num_back_nppc'))
                    path_splc = list(nx.shortest_path(academic_network, source_node, terminus_node,
                                                      weight='iter_num_back_splc'))
                    path_spnp = list(nx.shortest_path(academic_network, source_node, terminus_node,
                                                      weight='iter_num_back_spnp'))
                    with open(file_path_spc, 'a') as f_spc:
                        for i in range(len(path_spc)):
                            f_spc.write(path_spc[i] + '  ')
                        f_spc.write('\n')
                    with open(file_path_nppc, 'a') as f_nppc:
                        for i in range(len(path_nppc)):
                            f_nppc.write(path_nppc[i] + '  ')
                        f_nppc.write('\n')
                    with open(file_path_splc, 'a') as f_splc:
                        for i in range(len(path_splc)):
                            f_splc.write(path_splc[i] + '  ')
                        f_splc.write('\n')
                    with open(file_path_spnp, 'a') as f_spnp:
                        for i in range(len(path_spnp)):
                            f_spnp.write(path_spnp[i] + '  ')
                        f_spnp.write('\n')

    '''
    全局主路径（Global Main Path）
    GMPA方法与LMPA方法相比，更加关注引文路径在整体知识流动中的重要作用，主要流程如下：
    1、由搜索路径数（SPC）方法产生遍历数，生成全局主路径
    2、将生成的全局主路径经过的节点及其连边从专利网中抽取联通子图
    '''

    def GMPA(self, k):
        spc_sorted = 'data/spc_importance_sorted.txt'
        G = nx.read_gpickle('data/homo_academic_network_local.gpickle')
        nodes = list()
        itr = 0
        with open(spc_sorted) as f_spc:
            for line in f_spc:
                itr += 1
                nodes.extend(line.split(':  ')[0].split('  '))
                if itr == k:
                    break
        sub_G = G.subgraph(set(nodes))
        print(sub_G.number_of_nodes())
        print(sub_G.number_of_edges())
        nx.write_gpickle(sub_G, 'data/homo_academic_network_GMPA_%d.gpickle' % (k))

    '''
    K-route主路径（K-route Main Path Analysis）
    初始化K个具有最大遍历数的链接，以每条链接为中心，以遍历数为优先权，在引文网络中双向随机游走，
    直至抵达源点和会点，生成K-route主路径。多重主路径与全局主路径相比，除了搜索最重要的引文路径
    还会搜索遍历数累加和小于最大遍历数累加和的若干重要路径
    '''

    def k_route_MPA(self, k):
        G = nx.read_gpickle('data/homo_academic_network_local.gpickle')
        source_list, terminus_list = self.find_source_and_terminus(G)
        edges = G.edges(data=True)
        edges.sort(key=lambda x: x[2]['iter_num_spc'], reverse=True)
        edges = edges[0: k]
        left_nodes = [i[0] for i in edges]
        right_nodes = [i[1] for i in edges]
        nodes = []
        for ln in left_nodes:
            for sn in source_list:
                paths = list(nx.all_simple_paths(G, sn, ln))
                if len(paths) != 0:
                    for path in paths:
                        nodes.extend(path)
        for rn in right_nodes:
            for tn in terminus_list:
                paths = list(nx.all_simple_paths(G, rn, tn))
                if len(paths) != 0:
                    for path in paths:
                        nodes.extend(path)
        sub_G = G.subgraph(set(nodes))
        print(sub_G.number_of_nodes())
        print(sub_G.number_of_edges())
        op = 'data/homo_academic_network_kroute_%d.gpickle' % (k)
        print(op)
        nx.write_gpickle(sub_G, op)

    '''
    P-Index
    计算路径重要度的步骤
    1、首先计算专利对被引专利的贡献度
    2、其次计算每个专利的重要度
    3、计算每种主路径的重要性程度
    '''

    def P_index(self, param):
        G = nx.read_gpickle('data/homo_academic_network_local.gpickle')
        file_path_spc = 'data/path_spc.txt'
        file_path_nppc = 'data/path_nppc.txt'
        file_path_splc = 'data/path_splc.txt'
        file_path_spnp = 'data/path_spnp.txt'
        for edge in G.edges():
            G[edge[0]][edge[1]]['contribute_degree'] = np.exp(-param * G[edge[0]][edge[1]]['time_difference'])
        nx.write_gpickle(G, 'data/homo_academic_network_global.gpickle')
        important_of_nodes = G.in_degree(weight='contribute_degree')
        with open('data/important_of_nodes.txt', 'a') as f:
            for item in important_of_nodes.items():
                f.write(item[0] + ' ' + str(item[1]) + '\n')
        HomoCitationAnalysis.save_path_importancace(file_path_spc, 'data/spc_importance_sorted.txt', important_of_nodes)
        HomoCitationAnalysis.save_path_importancace(file_path_nppc, 'data/nppc_importance_sorted.txt',
                                                    important_of_nodes)
        HomoCitationAnalysis.save_path_importancace(file_path_splc, 'data/splc_importance_sorted.txt',
                                                    important_of_nodes)
        HomoCitationAnalysis.save_path_importancace(file_path_spnp, 'data/spnp_importance_sorted.txt',
                                                    important_of_nodes)

    @staticmethod
    def save_path_importancace(input_file_path, output_file_path, important_of_nodes):
        dic = dict()
        with open(input_file_path) as f:
            for line in f:
                importance_path = 0
                for key in line.strip().split('  '):
                    importance_path += important_of_nodes[key.strip()]
                dic[line.strip()] = importance_path
        dic_sorted = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        with open(output_file_path, 'a') as f:
            for pt in dic_sorted:
                f.write(pt[0] + ':  ' + str(pt[1]) + '\n')

    '''
    根据同质网络进行绘图
    '''

    @staticmethod
    def plot_homo_academic_network(network_path):
        plt.figure(figsize=(10, 10))
        G = nx.read_gpickle(network_path)
        nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=10, linewidths=0.6, font_size=5, arrows=False)
        plt.show()


hca = HomoCitationAnalysis('data/homo_academic_network.gpickle')
# hca.local_main_path_analysis()
# hca.find_local_main_path()
# hca.GMPA(50)
# hca.k_route_MPA(50)
# hca.plot_homo_academic_network('data/homo_academic_network_kroute_50.gpickle')
hca.plot_homo_academic_network('data/homo_academic_network_GMPA_50.gpickle')
# hca.P_index(0.0001)
