import networkx as nx
import matplotlib.pyplot as plt
import re
import random
import heapq

def draw_graph(G:nx.DiGraph):
    plt.rcParams['figure.figsize']= (120,120)
    fig,ax = plt.subplots()
    pos = nx.kamada_kawai_layout(G, dim=2)
    nx.draw(G, pos, with_labels = True,ax = ax, node_size=200, font_size=6)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels, font_color='c', font_size=6)
    plt.show()


# 创建图形
def creategraph(path, draw = True):
    # 读取文本文件
    with open(path,'r',encoding='gbk') as f:
        content = f.read()
        words_list = re.split(r'[^a-zA-Z]+',content.lower())
        # print(words_list)
    if '' in words_list:
        words_list.remove('')
    G = nx.DiGraph()
    for i,word in enumerate(words_list):
        G.add_node(word)
        if i+1 <len(words_list):
            word_next = words_list[i+1]
            if G.has_edge(word,word_next):
                weight = G.get_edge_data(word, word_next)["weight"]
                G.add_edge(word, word_next, weight = weight + 1)
            else:
                G.add_edge(word, word_next, weight = 1)
    if draw:
        draw_graph(G)
    return G

# 生成桥接词
def generatebridge(G:nx.DiGraph):
    bridgelist = []
    for i,word1 in enumerate(G.nodes):
        for j,word2 in enumerate(G.nodes):
            out_edges = G.out_edges(word1)
            for bridge in out_edges:
                if G.has_edge(bridge[1],word2):
                    # bridges_dict.update({(word1,word2):bridge[1]})
                    # bridges_dict[(word1,word2)]=bridge[1]
                    bridgelist.append((word1,word2,bridge[1]))
    return bridgelist

# 查询桥接词
def search_for_bridge(node1,node2,G:nx.DiGraph):
    bridge = []
    nodes = G.nodes()
    if node1 in nodes:
        if node2 in nodes:
            for node in nodes:
                if (node1,node2,node) in bridges_list:
                    bridge.append(node)
        else:
            print(f"no '{node2}' in graph!")
            return 
    else:
        print(f"no '{node1}' in graph!")
        return
    if len(bridge) == 0:
        print('No bridge words from word1 to word2!')
        return
    print(f'The bridge word from {node1} to {node2}: {bridge}')

#功能需求4：根据bridge word生成新文本
def add_brigde(G1:nx.DiGraph,G2:nx.DiGraph):
    G3 = nx.DiGraph()
    # G3 = G2.copy()
    for node in G2.nodes:
        G3.add_node(node)
    for edge in G2.edges:
        G3.add_edge(*edge)
    edges_list = G2.edges()
    G1node = G1.nodes()
    for (node1,node2) in edges_list:
        bridge_add = []
        if node1 in G1node():
            if node2 in G1node():
                for node in G1node():
                    if (node1,node2,node) in bridges_list:
                        bridge_add.append(node)
                if len(bridge_add) != 0:
                    random_node = random.choice(bridge_add)
                    if random_node in G2.nodes():
                        G3.remove_edge(node1,node2)
                        G3.add_edge(node1,random_node)
                        G3.add_edge(random_node,node2)
                    else:
                        G3.add_node(random_node)
                        G3.remove_edge(node1,node2)
                        G3.add_edge(node1,random_node)
                        G3.add_edge(random_node,node2)
    return G3

# def nearest_paths(G:nx.DiGraph, node1, node2):
#     try:
#         paths = list(nx.shortest_simple_paths(G, node1, node2, weight="weight"))
#         print(f"{paths[0]}, len:{len(paths[0])}")
#         return paths[0]
#     except nx.exception.NodeNotFound:
#         print(f"at least one node in ({node1}, {node2}) not in graph")
#     except nx.exception.NetworkXNoPath:
#         print(f"no edges between {node1}, {node2}")


def dijkstra(G, source, source2):
    # 初始化距离字典，将所有节点的距离设为无穷大，源点到自身的距离设为0
    if source in G.nodes() and source2 in G.nodes():
            null_list = []
            distances = {v: {"distance":float('infinity'), "v_list":null_list} for v in G}
            distances[source]["distance"] = 0
            # 使用优先队列（小顶堆）来存储待处理的节点及其距离
            priority_queue = [(0, source)]

            while priority_queue:
                # 弹出当前距离最小的节点
                current_distance, current_vertex = heapq.heappop(priority_queue)

                # 节点已经被处理过，则跳过
                if current_distance > distances[current_vertex]["distance"]:
                    continue

                # 遍历当前节点的所有邻居
                for neighbor, weight in G[current_vertex].items():
                    # print(type(current_distance), type(weight))
                    distance = current_distance + weight["weight"]          

                    # 如果找到了更短的路径，则更新距离并将其加入优先队列
                    if distance < distances[neighbor]["distance"]:
                        distances[neighbor]["distance"] = distance
                        # try:
                        distances[neighbor]["v_list"] = distances[current_vertex]["v_list"]+[(current_vertex, neighbor)]
                        # except:
                        #     distances[neighbor]["v_list"] = [(current_vertex, neighbor)]
                        heapq.heappush(priority_queue, (distance, neighbor))
    else:
        print("node not in graph")
        return 0
    # 假设G是一个NetworkX的DiGraph对象
    # 计算从节点A到所有其他节点的最短距离
    if distances[source2]["distance"] == float('infinity'):
        print("no edges between nodes")
        return 0

    print(distances[source2])
    return 0

def random_walk(G:nx.DiGraph):
    # G_out = nx.DiGraph()
    # 随机选择一个节点作为起点
    start_node = random.choice(list(G.nodes))
    path = [start_node]
    edges = []

    while True:
        # 获取当前节点的所有出边
        out_edges = list(G.out_edges(start_node))
        if not out_edges:
            # 如果当前节点没有出边，就停止遍历
            break

        # 随机选择一个出边
        edge = random.choice(out_edges)
        edges.append(edge)

        # 移动到下一个节点
        start_node = edge[1]
        path.append(start_node)

        # 如果遇到重复的边，就停止遍历
        if edges.count(edge) > 1:
            break

    return path, edges

    


if __name__=='__main__':
    G1 = creategraph('test.txt')
    nx.write_graphml(G1, "graph.graphml")    # 保存图形文件


    bridges_list = generatebridge(G1)
    search_for_bridge('the','is',G1)
    G2 = creategraph('test2.txt')
    # print(bridges_list)
    G3 = add_brigde(G1,G2)
    draw_graph(G3)

    #展示节点不存在的情况
    print("----------------------------------------")
    dijkstra(G1, "wrong node1", "wrong node1")
    print("----------------------------------------")
    #展示节点不连通的情况
    dijkstra(G1, "bones", "love")
    #展示节点连通情况
    print("----------------------------------------")
    dijkstra(G1, "both", "together")
    print("----------------------------------------")

    path, _ = random_walk(G1)
    print(path)
    with open('random_walk','w',encoding='gbk') as f:
        for item in path:
            f.write(item + ' ')
