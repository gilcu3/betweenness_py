#!/usr/bin/env python3

import networkx as nx
import pickle

if __name__ == '__main__':
    with open('as_caida.bin', 'rb') as fin:
        g = pickle.load(fin)

    print('Number of nodes:', g.number_of_nodes())
    print('Number of edges:', g.number_of_edges())


    mxg = 0
    for i in g.nodes():
        mxg = max(g.degree(i), mxg)
    print('Max degree:', mxg)
    cc = nx.biconnected_components(g)
    mx = -1

    for cci in cc:
        mx = max(mx, len(cci))

    print('Biggest biconnected component:', mx)
    # print('Diameter:', nx.diameter(g))


