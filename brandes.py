#! /usr/bin/env python3

import networkx as nx
import data


def bfse(s: int, g: (nx.DiGraph,nx.Graph)):
    n = g.number_of_nodes()
    dist = [float('inf') for _ in range(n)]
    sigma = [None for _ in range(n)]
    delta = [0 for _ in range(n)]
    que = []
    vis = set()

    f = 0
    que.append(s)
    vis.add(s)
    dist[s] = 0
    sigma[s] = 1

    while f < len(que):
        v = que[f]
        f += 1

        for nv in g[v]:
            if nv in vis:
                if dist[nv] == dist[v] + 1:
                    sigma[nv] += sigma[v]
                continue

            dist[nv] = dist[v] + 1
            sigma[nv] = sigma[v]
            vis.add(nv)
            que.append(nv)

    for v in reversed(que):
        d = 0
        for nv in g[v]:
            if dist[nv] == dist[v] + 1:
                d += sigma[v] / sigma[nv] * (1 + delta[nv])
        delta[v] = d

    delta[s] = 0

    return delta


def brandes(g: (nx.DiGraph,nx.Graph)):
    """
    :param g: Unweighted connected graph
    :return: betweenness values of each node
    """
    n = g.number_of_nodes()
    bc = dict.fromkeys(g.nodes(), 0)

    for v in g.nodes():
        delta_v = bfse(v, g)
        for j in range(n):
            bc[j] += delta_v[j]
    if not nx.is_directed(g):
        bc = {i: p / 2 for i, p in bc.items()}

    return bc


class algo():
    def __init__(self, g: (nx.DiGraph,nx.Graph)):
        self.g = g.copy()

    def update(self, edge):
        self.g.add_edge(edge[0], edge[1])
        nbc = brandes(self.g)
        return nbc

    def remove(self, edge):
        # print(edge, edge in self.g.edges)
        self.g.remove_edge(edge[0], edge[1])
        # print(self.g.number_of_edges())
        nbc = brandes(self.g)
        return nbc

    @staticmethod
    def directed():
        return True


if __name__ == '__main__':
    g = data.gen_random_graph()
    res = brandes(g)
    print(g.edges)
    print(res)
