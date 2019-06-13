#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import pickle


def load():
    with open('datasets/ca_HepTh/ca_HepTh.bin', 'rb') as fin:
        g = pickle.load(fin)
        return g
    return None


def main(args):
    data = open('CA-HepTh.txt')
    g = nx.Graph()

    ids = 0
    str2id = {}

    for line in data.readlines():
        if line[0] == '#' or len(line) == 0: continue
        u, v = line.split()
        if u not in str2id:
            str2id[u] = ids
            ids += 1
        if v not in str2id:
            str2id[v] = ids
            ids += 1

        u, v = str2id[u], str2id[v]
        if u != v:
            g.add_edge(u, v)
    cns = nx.connected_components(g)
    mx, wmx = 0, None
    for cc in cns:
        if len(cc) > mx:
            mx = len(cc)
            wmx = cc
    g = nx.convert_node_labels_to_integers(nx.induced_subgraph(g, wmx))
    print(g.number_of_nodes(), g.number_of_edges())
    out = open('ca_HepTh.bin', 'wb')
    pickle.dump(g, out)
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
