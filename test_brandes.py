#! /usr/bin/env python3

import unittest

import data
import brandes
import networkx as nx


class brandesTest(unittest.TestCase):
    def _test_correct(self, n=20):
        g = data.gen_random_graph_connected(n, None)
        # print(g.edges())
        bc0 = brandes.brandes(g)
        bc1 = nx.betweenness_centrality(g, normalized=False)
        # print(bc0, bc1)
        for i in range(n):
            self.assertAlmostEqual(bc0[i], bc1[i])

    def test_correctness(self):
        for n in range(3, 25):
            for t in range(100):
                self._test_correct(n)


if __name__ == '__main__':
    unittest.main()
