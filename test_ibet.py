import unittest
import data
import ibet
import networkx as nx


class ibetTest(unittest.TestCase):

    def _test_cur(self):
        g = nx.DiGraph([(0, 4), (1, 2), (2, 0), (2, 1), (2, 3), (3, 1), (3, 4), (4, 1)])
        n = g.number_of_nodes()
        bc = nx.betweenness_centrality(g, normalized=False)
        print(bc)
        algo = ibet.BC_incremental(g.copy())
        g.add_edge(4, 2)
        nx.nx_agraph.view_pygraphviz(g)
        nbc = algo.betweenness_add_edge((4, 2))

        bc = nx.betweenness_centrality(g, normalized=False)
        print(bc, '\n', nbc)
        for i in range(n):
            self.assertAlmostEqual(bc[i], nbc[i])

    def _test_add_correct(self, n=20):
        g = data.gen_random_graph_directed(n, None)

        edge = data.gen_new_edge(g)
        if edge is None: return

        algo = ibet.BC_incremental(g.copy())
        # print(g.edges(), edge)
        g.add_edge(edge[0], edge[1])
        bc_ibet = algo.betweenness_add_edge(edge)

        # nx.nx_agraph.view_pygraphviz(g)
        bc_brandes = nx.betweenness_centrality(g, normalized=False)

        # print(bc_brandes, bc_ibet)
        for i in range(n):
            self.assertAlmostEqual(bc_ibet[i], bc_brandes[i])

    def test_add_correctness(self):
        for n in range(1, 25):
            for t in range(100):
                self._test_add_correct(n)


if __name__ == '__main__':
    unittest.main()
