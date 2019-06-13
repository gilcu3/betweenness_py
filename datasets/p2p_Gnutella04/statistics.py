#!/usr/bin/env python3

import networkx as nx
import dill

if __name__ == '__main__':
    with open('p2p-Gnutella04.bin', 'rb') as fin:
        g = dill.load(fin)
    cc = nx.biconnected_components(nx.to_undirected(g))
    mx = -1
    for cci in cc:
        mx = max(mx, len(cci))
    print('Number of nodes:', g.number_of_nodes())
    print('Number of edges:', g.number_of_edges())
    print('Biggest biconnected component:', mx)
    # print('Diameter:', nx.diameter(nx.to_undirected(g)))

    mx = -1
    scc = nx.strongly_connected_components(g)
    for cci in scc:
        mx = max(mx, len(cci))

    print('Biggest strongly connected component:', mx)
