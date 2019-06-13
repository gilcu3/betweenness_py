#! /usr/bin/env python3

import networkx as nx

from enum import Enum
from collections import defaultdict

class ops(Enum):
    ADD = 0
    DELETE = 1


def _bfse(s, g: nx.DiGraph, n):
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


def _bfs_all(g: nx.DiGraph, comp, articulation_points):
    n = g.number_of_nodes()
    dist = [float('inf') for _ in range(n)]
    sigma = [0 for _ in range(n)]
    delta = [0 for _ in range(n)]
    reach = [0 for _ in range(n)]
    ancester = [None for _ in range(n)]
    for s in comp:
        if not articulation_points[s]:
            continue
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

            ancester[v] = s

            for nv in g[v]:
                if nv in comp:
                    continue
                if nv in vis:
                    if dist[nv] == dist[v] + 1:
                        sigma[nv] += sigma[v]
                    continue

                dist[nv] = dist[v] + 1
                sigma[nv] = sigma[v]

                vis.add(nv)
                que.append(nv)

        # for v in que:
        #     delta[v] = 0

        for v in reversed(que):
            d = 0
            for nv in g[v]:
                if dist[nv] == dist[v] + 1:
                    d += sigma[v] / sigma[nv] * (1 + delta[nv])
            delta[v] = d

        reach[s] = len(que) - 1
        delta[s] = 0

    return reach, delta, ancester


def _icentral_directed(g: nx.DiGraph, bc, e, op):
    nbc = bc.copy()
    u, v = e
    ng = g.copy()
    n = g.number_of_nodes()

    if op == ops.ADD:
        ng.add_edge(u, v)
        nbic = list(nx.biconnected_components(ng.to_undirected()))
        articulation_points_set = set(nx.articulation_points(ng.to_undirected()))
    # elif op == ops.DELETE:
    #   ng.remove_edge(u, v)
    #   nbic = list(nx.biconnected_components(g.to_undirected()))
    #   articulation_points_set = set(nx.articulation_points(g.to_undirected()))
    articulation_points = [False for _ in range(n)]
    for i in articulation_points_set:
        articulation_points[i] = True
    # print(nbic)

    id_B_e, nB_e, B_e = None, None, None
    for i, cc in enumerate(nbic):
        if u in cc and v in cc:
            nB_e = nx.induced_subgraph(ng, cc).copy()
            B_e = nx.induced_subgraph(g, cc).copy()
            id_B_e = i
            break
    assert id_B_e is not None

    affected_component = set(nbic[id_B_e])

    reach, odelta, ancester = _bfs_all(g, affected_component, articulation_points)
    reach_r, odelta_r, ancester_r = _bfs_all(nx.reverse(g), affected_component, articulation_points)

    dist_v1, _, _, _ = _bfse(u, nx.reverse(B_e), n)
    dist_v2, _, _, _ = _bfse(v, nx.reverse(B_e), n)

    Q = []
    for s in B_e.nodes():
        if s != v and dist_v1[s] != float('inf') and dist_v1[s] + 1 <= dist_v2[s]:
            Q.append(s)



    # print(Q, gsizes)
    root = {}
    root_r = {}
    for s in affected_component:
        if articulation_points[s]:
            root[s] = []
            root_r[s] = []
    for v in g.nodes():
        if v not in affected_component:
            if ancester[v] is not None:
                root[ancester[v]].append(v)
            if ancester_r[v] is not None:
                root_r[ancester_r[v]].append(v)

    mark = defaultdict(int)
    mark_r = defaultdict(int)

    for s in Q:

        _, sigma, ordered, P = _bfse(s, B_e, n)

        # delta = dict.fromkeys(B_e.nodes(), 0)
        delta = [0 for _ in range(n)]
        for w in reversed(ordered):
            if w != s and articulation_points[w]:
                delta[w] += reach[w]
            for p in P[w]:
                delta[p] += sigma[p] / sigma[w] * (1 + delta[w])
            if w != s:
                nbc[w] -= delta[w]
            if articulation_points[s]:
                nbc[w] -= delta[w] * reach_r[s]

        for w in ordered:
            if articulation_points[w]:
                if articulation_points[s]:
                    mark[s] -= reach[w]
                if w == s:
                    mark[w] -= len(ordered)
                else:
                    mark_r[w] -= 1
                    if articulation_points[s]:
                        mark_r[w] -= reach_r[s]

    for s in Q:

        _, sigma, ordered, P = _bfse(s, nB_e, n)

        # delta = dict.fromkeys(B_e.nodes(), 0)
        delta = [0 for _ in range(n)]
        # if s not in reach_r:
        #     reach_r[s] = 0
        for w in reversed(ordered):
            if w != s and articulation_points[w]:
                delta[w] += reach[w]
            for p in P[w]:
                delta[p] += sigma[p] / sigma[w] * (1 + delta[w])
            if w != s:
                nbc[w] += delta[w]
            if articulation_points[s]:
                nbc[w] += delta[w] * reach_r[s]

        for w in ordered:
            if articulation_points[w]:
                if articulation_points[s]:
                    mark[s] += reach[w]
                if w == s:
                    mark[w] += len(ordered)
                else:
                    mark_r[w] += 1
                    if articulation_points[s]:
                        mark_r[w] += reach_r[s]
    for w, a in mark.items():
        assert a >= 0
        for v in root_r[w]:
            nbc[v] += odelta_r[v] * a
    for w, a in mark_r.items():
        assert a >= 0
        for v in root[w]:
            nbc[v] += odelta[v] * a

    return nbc


def icentral_directed(g: nx.DiGraph, bc, edge, opst):
    """
    Gil-Pons, Reynaldo

    2018
    """
    if opst == ops.ADD:
        if edge not in g.edges():
            return _icentral_directed(g, bc, edge, opst)
        else:
            return bc
    elif opst == ops.DELETE:
        # TODO not implemented
        if edge in g.edges():
            return _icentral_directed(g, bc, edge, opst)
        else:
            return bc
    else:
        assert False


class algo():
    def __init__(self, dg: nx.DiGraph):
        self.g = dg
        self.bc = nx.betweenness_centrality(dg, normalized=False)

    def update(self, edge):
        nbc = _icentral_directed(self.g, self.bc, edge, ops.ADD)
        return nbc

    @staticmethod
    def directed():
        return True


def main():
    # g = data.gen_random_graph(6)
    g = nx.DiGraph([(0, 2), (1, 2), (2, 1)])
    # nx.nx_agraph.view_pygraphviz(g)
    bc = nx.betweenness_centrality(g, normalized=False)
    print(bc)
    edge = (2, 0)
    nbc = _icentral_directed(g, bc, edge, ops.ADD)
    g.add_edge(edge[0], edge[1])
    # nx.nx_agraph.view_pygraphviz(g)
    bc = nx.betweenness_centrality(g, normalized=False)
    print(bc, '\n', nbc)


if __name__ == '__main__':
    main()