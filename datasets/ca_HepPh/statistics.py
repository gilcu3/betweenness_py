#!/usr/bin/env python3

import networkx as nx
import pickle

if __name__ == '__main__':
    with open('ca_HepPh.bin', 'rb') as fin:
        g = pickle.load(fin)
    filestr = '../../edges/ca_HepPh.bin'
    with open(filestr, 'rb') as edgefile:
        edges = pickle.load(edgefile)
    for edge in edges:
        g.add_edge(edge[0], edge[1])
        cc = nx.biconnected_components(g)
        mx = -1
        lcc = list(cc)
        bicg = nx.Graph()
        cur = [[] for v in g]
        for i, cci in enumerate(lcc):
            mx = max(mx, len(cci))
            for v in cci:
                for p in cur[v]:
                    bicg.add_edge(p, i)
                cur[v].append(i)
        print(sorted([len(cci) for cci in lcc])[-5:])
        g.remove_edge(edge[0], edge[1])
    cc = nx.biconnected_components(g)
    mx = -1
    lcc = list(cc)
    bicg = nx.Graph()
    cur = [[] for v in g]
    for i, cci in enumerate(lcc):
        mx = max(mx, len(cci))
        for v in cci:
            for p in cur[v]:
                bicg.add_edge(p, i)
            cur[v].append(i)
    print(sorted([len(cci) for cci in lcc])[-5:])
    print('Number of nodes:', g.number_of_nodes())
    print('Number of edges:', g.number_of_edges())
    print('Biggest biconnected component:', mx)
