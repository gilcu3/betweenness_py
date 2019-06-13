#! /usr/bin/env python3

import networkx as nx

from enum import Enum


class ops(Enum):
    ADD = 0
    DELETE = 1


def _bfse(s, g: nx.Graph, n):
    dist = [float('inf') for _ in range(n)]
    sigma = [0 for _ in range(n)]
    P = [None for _ in range(n)]
    que = []
    vis = set()

    f = 0
    que.append(s)
    vis.add(s)
    dist[s] = 0
    sigma[s] = 1
    P[s] = []

    while f < len(que):
        v = que[f]
        f += 1

        for nv in g[v]:
            if nv in vis:
                if dist[nv] == dist[v] + 1:
                    P[nv].append(v)
                    sigma[nv] += sigma[v]
                continue

            dist[nv] = dist[v] + 1
            sigma[nv] = sigma[v]
            P[nv] = [v]
            vis.add(nv)
            que.append(nv)
    return dist, sigma, que, P


def connected_components_sizes(biconnected_components, id, articulation_points):
    n = len(articulation_points)
    ap2bcc = {i: [] for i in range(n) if articulation_points[i]}

    for i, bcc in enumerate(biconnected_components):
        for v in bcc:
            if articulation_points[v]:
                ap2bcc[v].append(i)

    que = []
    origin = {}
    vis = set()
    f = 0
    que.append(id)

    ans = dict.fromkeys([v for v in biconnected_components[id] if articulation_points[v]], 0)

    while f < len(que):
        i = que[f]
        f += 1
        bcc = biconnected_components[i]
        for v in bcc:
            if not articulation_points[v] or v in vis:
                continue
            vis.add(v)
            for j in ap2bcc[v]:
                if j == i:
                    continue
                if i == id:
                    origin[j] = v
                    ans[v] += len(biconnected_components[j]) - 1
                else:
                    origin[j] = origin[i]
                    ans[origin[i]] += len(biconnected_components[j]) - 1
                que.append(j)
    # print(biconnected_components, ans, id)
    return ans


def _icentral(g: nx.Graph, bc, e, op):
    nbc = bc.copy()
    v1, v2 = e
    ng = g.copy()
    n = g.number_of_nodes()
    if op == ops.ADD:
        ng.add_edge(v1, v2)
        nbic = list(nx.biconnected_components(ng))
        articulation_points_set = set(nx.articulation_points(ng))
    elif op == ops.DELETE:
        ng.remove_edge(v1, v2)
        nbic = list(nx.biconnected_components(g))
        articulation_points_set = set(nx.articulation_points(g))

    articulation_points = [False for _ in range(n)]
    for i in articulation_points_set:
        articulation_points[i] = True

    id_B_e, nB_e, B_e = None, None, None
    for i, cc in enumerate(nbic):
        if v1 in cc and v2 in cc:
            nB_e = nx.induced_subgraph(ng, cc).copy()
            B_e = nx.induced_subgraph(g, cc).copy()
            id_B_e = i
            break
    assert id_B_e is not None

    gsizes = connected_components_sizes(nbic, id_B_e, articulation_points)

    dist_v1, _, _, _ = _bfse(v1, B_e, n)
    dist_v2, _, _, _ = _bfse(v2, B_e, n)

    Q = []
    for s in B_e.nodes():
        if dist_v1[s] != dist_v2[s]:
            Q.append(s)

    # print(Q, gsizes)

    for s in Q:

        _, sigma, ordered, P = _bfse(s, B_e, n)

        # delta = dict.fromkeys(B_e.nodes(), 0)
        delta = [0 for _ in range(n)]
        for w in reversed(ordered):
            for p in P[w]:
                delta[p] += sigma[p] / sigma[w] * (1 + delta[w])
            if w != s:
                nbc[w] -= delta[w] / 2

        if articulation_points[s]:
            # delta_gs = dict.fromkeys(B_e.nodes(), 0)
            delta_gs = [0 for _ in range(n)]
            for w in reversed(ordered):
                if w == s:
                    continue
                if articulation_points[w]:
                    delta_gs[w] += gsizes[s] * gsizes[w]
                for p in P[w]:
                    delta_gs[p] += sigma[p] / sigma[w] * delta_gs[w]
                nbc[w] -= delta[w] * gsizes[s]
                nbc[w] -= delta_gs[w] / 2

        _, sigma, ordered, P = _bfse(s, nB_e, n)

        # delta = dict.fromkeys(nB_e.nodes(), 0)
        delta = [0 for _ in range(n)]
        for w in reversed(ordered):
            for p in P[w]:
                delta[p] += sigma[p] / sigma[w] * (1 + delta[w])
            if w != s:
                nbc[w] += delta[w] / 2

        if articulation_points[s]:
            # delta_gs = dict.fromkeys(nB_e.nodes(), 0)
            delta_gs = [0 for _ in range(n)]
            for w in reversed(ordered):
                if w == s:
                    continue
                if articulation_points[w]:
                    delta_gs[w] += gsizes[s] * gsizes[w]
                for p in P[w]:
                    delta_gs[p] += sigma[p] / sigma[w] * delta_gs[w]
                nbc[w] += delta[w] * gsizes[s]
                nbc[w] += delta_gs[w] / 2

    return nbc


def icentral(g: nx.Graph, bc, edge, opst):
    """
    Parallel Algorithm for Incremental Betweenness Centrality on Large Graphs

    Jamour, Fuad
    Skiadopoulos, Spiros
    Kalnis, Panos

    2017
    """
    if opst == ops.ADD:
        if edge not in g.edges():
            return _icentral(g, bc, edge, opst)
        else:
            return bc
    elif opst == ops.DELETE:
        if edge in g.edges():
            return _icentral(g, bc, edge, opst)
        else:
            return bc
    else:
        assert False


class algo():
    def __init__(self, g: nx.Graph):
        self.g = g
        self.bc = nx.betweenness_centrality(g, normalized=False)

    def update(self, edge):
        nbc = _icentral(self.g, self.bc, edge, ops.ADD)
        self.g.add_edge(edge[0], edge[1])
        return nbc

    def remove(self, edge):
        nbc = _icentral(self.g, self.bc, edge, ops.DELETE)
        self.g.remove_edge(edge[0], edge[1])
        return nbc

    @staticmethod
    def directed():
        return False


if __name__ == '__main__':
    # g = data.gen_random_graph(6)
    g = nx.Graph([(0, 2), (1, 2)])
    # nx.nx_agraph.view_pygraphviz(g)
    bc = nx.betweenness_centrality(g, normalized=False)
    print(bc)
    edge = (0, 1)
    nbc = icentral(g, bc, edge, ops.ADD)
    g.add_edge(edge[0], edge[1])
    nx.nx_agraph.view_pygraphviz(g)
    bc = nx.betweenness_centrality(g, normalized=False)
    print(bc, '\n', nbc)
