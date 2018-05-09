import numpy as np
import networkx as nx


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
                            academic_network[path[i]][path[i+1]]['iter_num_spc'] = \
                                academic_network[path[i]][path[i+1]]['iter_num_spc'] + 1
                            academic_network[path[i]][path[i+1]]['iter_num_back_spc'] = \
                                1.0 / academic_network[path[i]][path[i+1]]['iter_num_spc']
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
    def GMPA(self):
        file_path_spc = 'data/path_spc.txt'
        G = nx.read_gpickle('data/homo_academic_network_local.gpickle')
        with open(file_path_spc) as f_spc:
            lines = f_spc.readlines()
        nodes = list()
        for line in lines:
            nodes.extend(line)
        sub_G = G.subgraph(nodes)
        nx.write_gpickle(sub_G, 'data/homo_academic_network_GMPA.gpickle')

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
        left_path_nodes = nx.current_flow_betweenness_centrality_subset\
            (G, sources=left_nodes, targets=source_list).keys()
        right_path_nodes = nx.current_flow_betweenness_centrality_subset\
            (G, sources=right_nodes, targets=terminus_list).keys()
        sub_G = G.subgraph(set(left_path_nodes.extend(right_path_nodes)))
        nx.write_gpickle(sub_G, 'data/homo_academic_network_GMPA.gpickle')


hca = HomoCitationAnalysis('data/homo_academic_network.gpickle')
# hca.local_main_path_analysis()
hca.find_local_main_path()