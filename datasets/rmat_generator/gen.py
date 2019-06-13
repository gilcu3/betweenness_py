#! /usr/bin/env python2
from __future__ import print_function
import snap


import networkx as nx
import sys, os, time


if __name__ == '__main__':

    for n in range(1024, 16385, 1024):
        while True:
            if os.path.exists('RMAT_%d.in' % n):
                break
            m = 8 * n - 10
            Rnd = snap.TRnd()
            
            g = snap.GenRMat(n, m, .75, .1, .1)
            
            edges = [(int(edge.GetSrcNId()), edge.GetDstNId()) for edge in g.Edges()]
            g = nx.from_edgelist(edges)
            # cc = nx.is_connected(g)
            
            bb = max(len(b) for b in nx.biconnected_components(g))
            
            if bb * 1.0 / g.number_of_nodes() > 0.8:
                print(bb * 1.0 / g.number_of_nodes())
                # time.sleep(1)
                continue
            # print g.number_of_nodes(), g.number_of_edges()
            # print cc, bb * 1.0 / g.number_of_nodes()
            with open('RMAT_%d.in' % n, 'w') as fout:
                print('\n'.join(['%d %d' % (u, v) for u, v in edges]), file=fout)
            break
