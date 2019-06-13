#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import dill


def load():
    with open('datasets/wiki_RfA/wiki_Rfa.bin', 'rb') as fin:
        g = dill.load(fin)
        return g
    return None


def main(args):
    data = open('wiki-RfA.txt')
    g = nx.DiGraph()
    ids = 0
    str2id = {}
    src = -1
    for line in data.readlines():
        if len(line) < 4:
            continue
        if line[:4] == 'SRC:':
            src = line[4:].strip()
        elif line[:4] == 'TGT:':
            tgt = line[4:].strip()
            u, v = src, tgt
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
    out = open('wiki_Rfa.bin', 'wb')
    dill.dump(g, out)
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
