import pytest
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
    # plt.show()


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


def test_1():
    G1 = creategraph('test.txt')
    path = random_walk(G1, "for")
    assert path == ['for', 'bones']


def test_2():
    G1 = creategraph('test.txt')
    path = random_walk(G1, "bones")
    assert path == ['bones']


def test_3():
    G1 = creategraph('test.txt')
    path = random_walk(G1, "love")
    assert path == ['love', 'for', 'bones']


# def test_4():
#     G1 = creategraph('test.txt')
#     path = random_walk(G1, "however")
#     assert path == ['however', 'he', 'hates', 'however', 'he']


if __name__ == '__main__':
    pytest.main()