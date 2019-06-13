#! /usr/bin/env python3


import networkx as nx
import heapq as pq


class BC_incremental():
    """
    Faster Betweenness Centrality Updates in Evolving Networks

    Bergamini, Elisabetta
    Meyerhenke, Henning
    Ortmann, Mark
    Slobbe, Arie

    2017
    """

    def __init__(self, g: nx.DiGraph):
        self.g = g
        self.n = g.number_of_nodes()
        self._preprocess()

    def _bfse(self, s):
        dist = [float('inf') for _ in range(self.n)]
        sigma = [0 for _ in range(self.n)]
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

            for nv in self.g[v]:
                if nv in vis:
                    if dist[nv] == dist[v] + 1:
                        sigma[nv] += sigma[v]
                    continue
                dist[nv] = dist[v] + 1
                sigma[nv] = sigma[v]
                vis.add(nv)
                que.append(nv)

        delta = [0 for _ in range(self.n)]
        for v in reversed(que):
            d = 0
            for nv in self.g[v]:
                if dist[nv] == dist[v] + 1:
                    d += sigma[v] / sigma[nv] * (1 + delta[nv])
            delta[v] = d
        delta[s] = 0
        return dist, sigma, delta

    def _preprocess(self):
        self.dist = [float('inf') for _ in range(self.n)]
        self.sigma = [0 for _ in range(self.n)]
        self.bc = {i: 0 for i in range(self.n)}
        for s in self.g.nodes():
            self.dist[s], self.sigma[s], deltas = self._bfse(s)
            for i in range(self.n):
                self.bc[i] += deltas[i]

    def _find_affected_sources(self, u, v):
        Q = []
        f = 0
        Q.append(u)
        vis = set()
        vis.add(u)
        while f < len(Q):
            cv = Q[f]
            f += 1
            for nv in self.g.predecessors(cv):
                if nv not in vis and self.dist[cv][v] >= self.dist[cv][u] + 1:
                    vis.add(nv)
                    Q.append(nv)
        # print(Q)
        return Q

    def betweenness_add_edge(self, edge):
        if edge in self.g.edges():
            return self.bc
        u, v = edge
        vis = [False for _ in range(self.n)]
        S = [set() for _ in range(self.n)]
        S[v] = set(self._find_affected_sources(u, v))
        Q = []
        f = 0
        p = [None for _ in range(self.n)]
        p[v] = v
        Q.append(v)
        vis[v] = True
        ndist = {}
        nsigma = {}

        T = [set() for _ in range(self.n)]

        while f < len(Q):
            t = Q[f]
            f += 1

            for s in S[p[t]]:
                if self.dist[s][t] >= self.dist[s][u] + 1 + self.dist[v][t]:
                    if self.dist[s][t] > self.dist[s][u] + 1 + self.dist[v][t]:
                        ndist[(s, t)] = self.dist[s][u] + 1 + self.dist[v][t]
                        nsigma[(s, t)] = 0
                    if (s, t) not in nsigma:
                        nsigma[(s, t)] = self.sigma[s][t]
                    nsigma[(s, t)] += self.sigma[s][u] * self.sigma[v][t]
                    if t != v:
                        S[t].add(s)

            for s in S[t]:
                T[s].add(t)

            for w in self.g[t]:
                if not vis[w] and self.dist[u][w] >= 1 + self.dist[v][w]:
                    Q.append(w)
                    vis[w] = True
                    p[w] = t

        # print(ndist)
        # print(T)

        for s in S[v]:
            pqs = []
            for t in T[s]:
                pq.heappush(pqs, (-self.dist[s][t], t))

            deltas = self._betweenness_update(s, self.sigma[s], self.dist[s], pqs, T[s])
            for i in range(self.n):
                self.bc[i] -= deltas[i]

        self.g.add_edge(u, v)

        for s in S[v]:
            npqs = []
            for t in T[s]:
                if (s, t) in ndist:
                    pq.heappush(npqs, (-ndist[(s, t)], t))
                else:
                    pq.heappush(npqs, (-self.dist[s][t], t))

            nsigmas = [nsigma[(s, i)] if (s, i) in nsigma else self.sigma[s][i] for i in range(self.n)]
            ndists = [ndist[(s, i)] if (s, i) in ndist else self.dist[s][i] for i in range(self.n)]
            ndeltas = self._betweenness_update(s, nsigmas, ndists, npqs, T[s])
            for i in range(self.n):
                self.bc[i] += ndeltas[i]

        for s, t in ndist:
            self.dist[s][t] = ndist[(s, t)]
        for s, t in nsigma:
            self.sigma[s][t] = nsigma[(s, t)]

        return self.bc

    def _betweenness_update(self, s, sigma, dist, pqs, T):
        delta = [0 for _ in range(self.n)]
        vis = set()
        for _, v in pqs:
            vis.add(v)
        while len(pqs) > 0:
            _, w = pq.heappop(pqs)
            for y in self.g.predecessors(w):
                if y != s and dist[w] != float('inf') and dist[w] == dist[y] + 1:
                    if w in T:
                        c = sigma[y] / sigma[w] * (1 + delta[w])
                    else:
                        c = sigma[y] / sigma[w] * delta[w]
                    if y not in vis:
                        pq.heappush(pqs, (-dist[y], y))
                        vis.add(y)
                    delta[y] += c

        return delta


class algo():
    def __init__(self, dg: nx.DiGraph):
        self.obj = BC_incremental(dg)

    def update(self, edge):
        nbc = self.obj.betweenness_add_edge(edge)
        return nbc

    @staticmethod
    def directed():
        return True

if __name__ == '__main__':
    g = nx.DiGraph([(0, 2), (0, 3), (1, 0), (1, 2), (1, 3), (2, 0), (2, 1), (2, 3), (3, 1)])
    bc = nx.betweenness_centrality(g, normalized=False)
    print(bc)
    algo = BC_incremental(g.copy())
    nedge = (3, 0)
    nbc = algo.betweenness_add_edge(nedge)
    g.add_edge(nedge[0], nedge[1])
    nx.nx_agraph.view_pygraphviz(g)
    bc = nx.betweenness_centrality(g, normalized=False)
    print(bc, '\n', nbc)