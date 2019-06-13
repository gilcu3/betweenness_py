#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import dill


def load(fname):
    with open('datasets/rmat_generator/%s.bin' % fname, 'rb') as fin:
        g = dill.load(fin)
        return g
    return None


def main(args):
    for n in range(1024, 16385, 1024):
        fname = 'RMAT_%d' % n
        data = open('%s.in' % fname)
        g = nx.DiGraph()
        for line in data.readlines():
            if line[0] == '%':
                continue
            u, v = map(int, line.split())
            g.add_edge(u, v)
        cns = nx.connected_components(nx.to_undirected(g))
        mx, wmx = 0, None
        for cc in cns:
            if len(cc) > mx:
                mx = len(cc)
                wmx = cc
        g = nx.convert_node_labels_to_integers(nx.induced_subgraph(g, wmx))
        print(g.number_of_nodes(), g.number_of_edges(), mx)
        out = open('%s.bin' % fname, 'wb')
        dill.dump(g, out)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
