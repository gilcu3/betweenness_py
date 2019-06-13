#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import pickle


def main(args):
    data = open('out.munmun_twitter_social')
    g = nx.Graph()
    for line in data.readlines():
        if line[0] == '%': continue
        u, v = map(int, line.split())
        g.add_edge(u, v)
    cns = nx.connected_components(g)
    mx, wmx = 0, None
    for cc in cns:
        if len(cc) > mx:
            mx = len(cc)
            wmx = cc
    g = nx.convert_node_labels_to_integers(nx.induced_subgraph(g, wmx))
    print(g.number_of_nodes(), g.number_of_edges())
    out = open('twitter-munmun.bin', 'wb')
    pickle.dump(g, out)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
