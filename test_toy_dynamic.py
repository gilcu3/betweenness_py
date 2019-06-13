import unittest

import data
import networkx as nx
import toy_dynamic


class toy_dynamicTest(unittest.TestCase):
    def _test_add_correct(self, n = 20):
        g = data.gen_random_graph_directed_connected(n, None)

        edge = data.gen_new_edge(g)
        if edge is None: return

        bc0 = nx.betweenness_centrality(g, normalized=False)

        bc_toy_dynamic = toy_dynamic.icentral_directed(g, bc0, edge, toy_dynamic.ops.ADD)
        # print(g.edges(), edge)
        g.add_edge(edge[0], edge[1])
        bc_brandes = nx.betweenness_centrality(g, normalized=False)

        for i in range(n):
            self.assertAlmostEqual(bc_toy_dynamic[i], bc_brandes[i])

    def _test_delete_correct(self, n = 20):
        g = data.gen_random_graph_directed_connected(n, None)

        edge = data.gen_new_edge(g)
        if edge is None: return

        bc_brandes = nx.betweenness_centrality(g, normalized=False)

        g.add_edge(edge[0], edge[1])
        bc0 = nx.betweenness_centrality(g, normalized=False)

        bc_toy_dynamic = toy_dynamic.icentral_directed(g, bc0, edge, toy_dynamic.ops.DELETE)
        # print(g.edges(), edge)

        for i in range(n):
            self.assertAlmostEqual(bc_toy_dynamic[i], bc_brandes[i])


    def test_add_correctness(self):
        for n in range(1, 25):
            for t in range(100):
                self._test_add_correct(n)

    def test_delete_correctness(self):
        for n in range(1, 25):
            for t in range(100):
                self._test_delete_correct(n)


if __name__ == '__main__':
    unittest.main()
