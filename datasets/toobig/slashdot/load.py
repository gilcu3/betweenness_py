#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import dill


def load():
    with open('datasets/slashdot/slashdot.bin', 'rb') as fin:
        g = dill.load(fin)
        return g
    return None


def main(args):
    data = open('out.slashdot-threads')
    g = nx.DiGraph()
    for line in data.readlines():
        if line[0] == '%':
            continue
        u, v, _, tt = map(int, line.split())
        g.add_edge(u, v, time=tt)
    cns = nx.connected_components(nx.to_undirected(g))
    mx, wmx = 0, None
    for cc in cns:
        if len(cc) > mx:
            mx = len(cc)
            wmx = cc
    g = nx.convert_node_labels_to_integers(nx.induced_subgraph(g, wmx))
    print(g.number_of_nodes(), g.number_of_edges())
    out = open('slashdot.bin', 'wb')
    dill.dump(g, out)
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
