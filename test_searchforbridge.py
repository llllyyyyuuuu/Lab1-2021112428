import pytest
import networkx as nx
import matplotlib.pyplot as plt
import re
import random
import heapq

def draw_graph(G:nx.DiGraph):
    plt.rcParams['figure.figsize']= (120,120)
    fig,ax = plt.subplots()
    pos = nx.kamada_kawai_layout(G, dim=2)
    nx.draw(G, pos, with_labels = True, ax=ax, node_size=200, font_size=6)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels, font_color='c', font_size=6)
    # plt.show()


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


def test_1():
    G1 = creategraph('test.txt')
    r = search_for_bridge('the', 'is', G1)
    assert r == ['fox', 'dog']

def test_2():
    G1 = creategraph('test.txt')
    r = search_for_bridge('the', 'are', G1)
    assert r == "no 'are' in graph!"

def test_3():
    G1 = creategraph('test.txt')
    r = search_for_bridge('but', 'are', G1)
    assert r == "two nodes not in graph!"


def test_4():
    G1 = creategraph('test.txt')
    r = search_for_bridge('123but', 'is', G1)
    assert r == "wrong word!"


def test_5():
    G1 = creategraph('test.txt')
    r = search_for_bridge('', 'is', G1)
    assert r == "empty word!"


def test_6():
    G1 = creategraph('test.txt')
    r = search_for_bridge('very', 'very', G1)
    assert r == "No bridge words from word1 to word2!"


if __name__ == '__main__':
    pytest.main()