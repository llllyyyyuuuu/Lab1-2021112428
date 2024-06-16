import networkx as nx
import matplotlib.pyplot as plt
import re
import random
import heapq


def draw_graph(G: nx.DiGraph):
    plt.rcParams['figure.figsize'] = (120, 120)
    fig, ax = plt.subplots()
    pos = nx.kamada_kawai_layout(G, dim=2)
    nx.draw(G, pos, with_labels=True, ax=ax, node_size=200, font_size=6)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels, font_color='c', font_size=6)
    plt.show()


# 创建图形
def creategraph(path, draw=True):
    # 读取文本文件
    with open(path, 'r', encoding='gbk') as f:
        content = f.read()
        words_list = re.split(r'[^a-zA-Z]+', content.lower())
        # print(words_list)
    if '' in words_list:
        words_list.remove('')
    G = nx.DiGraph()
    for i, word in enumerate(words_list):
        G.add_node(word)
        if i+1 < len(words_list):
            word_next = words_list[i+1]
            if G.has_edge(word, word_next):
                weight = G.get_edge_data(word, word_next)["weight"]
                G.add_edge(word, word_next, weight=weight + 1)
            else:
                G.add_edge(word, word_next, weight=1)
    if draw:
        draw_graph(G)
    return G


# 生成桥接词
def generatebridge(G: nx.DiGraph):
    bridgelist = []
    for i, word1 in enumerate(G.nodes):
        for j,word2 in enumerate(G.nodes):
            out_edges = G.out_edges(word1)
            for bridge in out_edges:
                if G.has_edge(bridge[1], word2):
                    # bridges_dict.update({(word1,word2):bridge[1]})
                    # bridges_dict[(word1,word2)]=bridge[1]
                    bridgelist.append((word1, word2, bridge[1]))
    return bridgelist


# 查询桥接词
def search_for_bridge(node1, node2, G: nx.DiGraph):
    if not node1:
        print("empty word!")
        return "empty word!"
    if not node2:
        print("empty word!")
        return "empty word!"
    n1 = node1.isalpha()
    n2 = node2.isalpha()
    if n1 is False or n2 is False:
        print("wrong word!")
        return "wrong word!"

    bridges_list = generatebridge(G)
    bridge = []
    nodes = G.nodes()
    if node1 in nodes:
        if node2 in nodes:
            for node in nodes:
                if (node1, node2, node) in bridges_list:
                    bridge.append(node)
        else:
            print(f"no '{node2}' in graph!")
            return f"no '{node2}' in graph!"
    else:
        if node2 in nodes:
            print(f"no '{node1}' in graph!")
            return f"no '{node1}' in graph!"
        else:
            print("two nodes not in graph!")
            return "two nodes not in graph!"
    if len(bridge) == 0:
        print("No bridge words from word1 to word2!")
        return "No bridge words from word1 to word2!"
    print(f'The bridge word from {node1} to {node2}: {bridge}')
    return bridge


# 功能需求4：根据bridge word生成新文本
def add_bridge(G1, path):
    bridges_list = generatebridge(G1)
    words_list = []
    words_list_new = []
    G1node = G1.nodes()
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            cleaned_line = re.findall(r'\b\w+\b', line)
            words_list.extend(cleaned_line)
    i = 0
    while i + 1 < len(words_list):
        bridge_add = []
        for node in G1node():
            if (words_list[i], words_list[i + 1], node) in bridges_list:
                bridge_add.append(node)
            if len(bridge_add) != 0:
                random_node = random.choice(bridge_add)

        if len(bridge_add) == 0:
            words_list_new.append(words_list[i])
        else:
            words_list_new.append(words_list[i])
            words_list_new.append(random_node)
        i = i + 1
    words_list_new.append(words_list[i])
    return words_list_new


def dijkstra(G, source, source2):
    dj = []
    # 初始化距离字典，将所有节点的距离设为无穷大，源点到自身的距离设为0
    if source in G.nodes() and source2 in G.nodes():
        null_list = []
        distances = {v: {"distance": float('infinity'), "v_list": null_list} for v in G}
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
    for i, j in enumerate(distances[source2]['v_list']):
        dj.append(distances[source2]['v_list'][i][0])
    dj.append(distances[source2]['v_list'][i][1])
    print(dj)
    return 0


def random_walk(G: nx.DiGraph, start_node):
    # G_out = nx.DiGraph()
    # 随机选择一个节点作为起点
    # start_node = random.choice(list(G.nodes))
    path = [start_node]
    edges = []
    out_edges = list(G.out_edges(start_node))
    if out_edges:
        # 随机选择一个出边
        edge = random.choice(out_edges)
        edges.append(edge)

        # 移动到下一个节点
        start_node = edge[1]
        path.append(start_node)
    else: edge = (1, 2)
    while edges.count(edge) <= 1:
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

    return path


if __name__ == '__main__':
    G1 = creategraph('test.txt')
    nx.write_graphml(G1, "graph.graphml")    # 保存图形文件

    resu = search_for_bridge('', 'are', G1)
    # print(resu)
    path = "test2.txt"
    text_new = add_bridge(G1, path)
    print(text_new)

    # 展示节点不存在的情况
    print("----------------------------------------")
    dijkstra(G1, "wrong node1", "wrong node1")
    print("----------------------------------------")
    # 展示节点不连通的情况
    dijkstra(G1, "bones", "love")
    # 展示节点连通情况
    print("----------------------------------------")
    dijkstra(G1, "both", "together")
    print("----------------------------------------")

    path = random_walk(G1, "however")
    print(path)
    with open('random_walk', 'w', encoding='gbk') as f:
        for item in path:
            f.write(item + ' ')
