#!/usr/bin/env python3

import networkx as nx
import dill

if __name__ == '__main__':
    for n in range(1024, 16385, 1024):
        fname = 'RMAT_%d' % n
        print(fname)
        with open('%s.bin' % fname, 'rb') as fin:
            g = dill.load(fin)

        print('Number of nodes:', g.number_of_nodes())
        print('Number of edges:', g.number_of_edges())

        mxg = 0
        for i in g.nodes():
            mxg = max(g.degree(i), mxg)
        print('Max degree:', mxg)
        print('Diameter:', nx.diameter(nx.to_undirected(g)))
        cc = nx.biconnected_components(nx.to_undirected(g))
        mx = -1

        for cci in cc:
            mx = max(mx, len(cci))
        print('Biggest biconnected component:', mx)

        mx = -1
        scc = nx.strongly_connected_components(g)
        for cci in scc:
            mx = max(mx, len(cci))

        print('Biggest strongly connected component:', mx)


