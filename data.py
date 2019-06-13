#! /usr/bin/env python3


import networkx as nx
import random
from networkx.algorithms.community import LFR_benchmark_graph


def gen_random_graph_directed(n: int = 6, seed=0):
    """

    :return: Random Directed Graph
    """
    g = nx.erdos_renyi_graph(n, 0.5, seed=seed, directed=True)
    g = nx.convert_node_labels_to_integers(g)
    return g


def gen_random_graph(n: int = 6, seed=0):
    """

    :return: Random Graph
    """
    g = nx.erdos_renyi_graph(n, 0.5, seed=seed)
    return g


def gen_random_graph_directed_connected(n: int = 6, seed=0):
    """

    :return: Random Directed Weakly Connected Graph
    """
    while True:
        g = nx.erdos_renyi_graph(n, 0.5, seed=seed, directed=True)
        if nx.is_connected(g.to_undirected()):
           break
    return g


def gen_random_graph_connected(n: int = 6, seed=0, prob = 0.5):
    """
    :return: Random Connected Undirected Graph
    """
    while True:
        g = nx.fast_gnp_random_graph(n, prob, seed)
        # g = nx.erdos_renyi_graph(n, prob, seed)
        if nx.is_connected(g):
           break
    return g


def gen_random_graph_social(n: int = 6, seed=0):
    """
    :return: Random Connected Undirected Graph
    """

    tau1, tau2, mu = 3, 1.5, 0.1
    g = nx.connected_caveman_graph(n, 5)
    g = LFR_benchmark_graph(n, tau1, tau2, mu, average_degree=5, min_community=25, seed=seed)
    return g


def gen_new_edge(g, seed=0):
    n = g.number_of_nodes()
    if g.number_of_edges() == n * (n - 1) // 2 and not nx.is_directed(g):
        return None
    if g.number_of_edges() == n * (n - 1) and nx.is_directed(g):
        return None
    while True:
        v1, v2 = random.randint(0, n - 1), random.randint(0, n - 1)
        if v1 == v2 or (v1, v2) in g.edges: continue
        else: break
    return v1, v2


def get_random_edge(g, seed = 0):
    m = g.number_of_edges()
    if g.number_of_edges() == 0:
        return None
    e = random.randint(0, m - 1)
    ee = list(g.edges)[e]
    return ee[0], ee[1]


if __name__ == '__main__':
    pass
