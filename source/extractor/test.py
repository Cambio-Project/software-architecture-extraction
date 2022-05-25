import unittest

from .graph.graph import Graph, Node, Edge


class TestGraph(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_node(self):
        node1 = Node()
        node2 = Node('test')

        self.assertEqual(node1.label, '')

        self.assertEqual(node2.label, 'test')

    def test_edge(self):
        node1 = Node(_id=0)
        node2 = Node('test', 1)
        edge1 = Edge(node1, node2)
        edge2 = Edge(node1, node1, 'operation')

        self.assertEqual(edge1.label, '')
        self.assertEqual(edge1.source, node1)
        self.assertEqual(edge1.target, node2)

        self.assertEqual(edge2.label, 'operation')
        self.assertEqual(edge2.source, edge2.target)

    def test_graph(self):
        node1 = Node('A', 0)
        node2 = Node('B', 1)
        edge1 = Edge(node1, node2)

        graph = Graph()
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(edge1)

        self.assertEqual(len(graph.nodes), 2)
        self.assertEqual(graph.nodes, {node1.id: node1, node2.id: node2})
        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(graph.edges, {edge1.id: edge1})

    def test_check_cycles(self):
        G = Graph()
        a, b, c, d, e, f, g = \
            Node('A', 0), Node('B', 1), Node('C', 2), Node('D', 3), Node('E', 4), Node('F', 5), Node('G', 6)

        N = [a, b, c, d, e, f, g]

        for node in N:
            G.add_node(node)

        E = [
            Edge(a, b),
            Edge(b, c),
            Edge(c, d),
            Edge(a, d),
            Edge(d, e),
            Edge(e, a),
            Edge(e, f),
            Edge(f, g),
            Edge(g, f),
        ]

        for edge in E:
            G.add_edge(edge)

        self.assertEqual(Graph.check_cycles(G, True), [[g, f], [e, d, c, b, a]])
        self.assertEqual(Graph.check_cycles(G, False), [[g, f]])
