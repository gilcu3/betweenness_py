import unittest
import data
import toy
import networkx as nx


class toyTest(unittest.TestCase):

    def _test_add_correct(self, n=20):
        g = data.gen_random_graph_directed(n, None)
        # if not nx.is_connected(g.to_undirected()):
        #     return
        edge = data.gen_new_edge(g)
        if edge is None: return
        bc = nx.betweenness_centrality(g, normalized=False)

        # print(g.edges(), edge)

        bc_toy = toy.icentral_directed(g.copy(), bc, edge, toy.ops.ADD)
        g.add_edge(edge[0], edge[1])
        # nx.nx_agraph.view_pygraphviz(g)
        bc_brandes = nx.betweenness_centrality(g, normalized=False)

        # print(bc_brandes, bc_toy)
        for i in range(n):
            self.assertAlmostEqual(bc_toy[i], bc_brandes[i])

    def test_add_correctness(self):
        for n in range(1, 25):
            for t in range(100):
                self._test_add_correct(n)


if __name__ == '__main__':
    unittest.main()
