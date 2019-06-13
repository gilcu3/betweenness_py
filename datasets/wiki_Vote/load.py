#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import dill


def load():
    with open('datasets/wiki_Vote/Wiki-Vote.bin', 'rb') as fin:
        g = dill.load(fin)
        return g
    return None

def write():
    with open('Wiki-Vote.bin', 'rb') as fin:
        g = dill.load(fin)
    with open('Wiki-Vote.in', 'w') as fin:
        for edge in g.edges:
            print('%d %d' % (edge[0], edge[1]), file = fin)

def main(args):
    write()
    return
    data = open('Wiki-Vote.txt')
    g = nx.DiGraph()
    ids = 0
    str2id = {}
    for line in data.readlines():
        if line[0] == '#':
            continue
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
    cns = nx.connected_components(nx.to_undirected(g))
    mx, wmx = 0, None
    for cc in cns:
        if len(cc) > mx:
            mx = len(cc)
            wmx = cc
    g = nx.convert_node_labels_to_integers(nx.induced_subgraph(g, wmx))
    print(g.number_of_nodes(), g.number_of_edges())
    out = open('Wiki-Vote.bin', 'wb')
    dill.dump(g, out)
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
