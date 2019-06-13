#!/usr/bin/env python3

import networkx as nx
import pickle

if __name__ == '__main__':
    with open('eva.bin', 'rb') as fin:
        g = pickle.load(fin)
    cc = nx.biconnected_components(g)
    mx = -1
    for cci in cc:
        mx = max(mx, len(cci))
    print('Number of nodes:', g.number_of_nodes())
    print('Number of edges:', g.number_of_edges())
    print('Biggest biconnected component:', mx)
