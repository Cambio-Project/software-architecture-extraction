from typing import Dict, List, Union

from ..graph.edge import Edge
from ..graph.node import Node


class Graph:
    def __init__(self):
        self._nodes = {}
        self._edges = {}
        self._adjacency = {}

        self._node_id = 0
        self._edge_id = 0

    def __repr__(self) -> str:
        return '{} ({}, {})'.format(self.__class__.__name__, len(self._nodes), len(self._edges))

    def __str__(self) -> str:
        s = self.__repr__()
        s += '\n---'
        for _, n in self._nodes.items():
            s += '\n- {}'.format(n)
        s += '\n---'
        for e in self._edges:
            s += '\n - {}'.format(e)
        return s

    @property
    def nodes(self) -> Dict[int, Node]:
        return self._nodes

    @property
    def edges(self) -> Dict[int, Edge]:
        return self._edges

    def print(self):
        print(self)

    def node(self, node: Union[int, str]) -> Union[Node, None]:
        """
        Finds an node either by id or label.
        :return: Union[Node, None]      The node if the search was successful, None otherwise.
        """
        if isinstance(node, int):
            return self._nodes[node]
        elif isinstance(node, str):
            for _, n in self._nodes.items():
                if n.label == node:
                    return n
        return None

    def edge(self, edge: Union[int, str]) -> Union[Edge, None]:
        """
        Finds an edge either by id or label.
        :return: Union[Edge, None]      The edge if the search was successful, None otherwise.
        """
        if isinstance(edge, int):
            return self._edges[edge]
        elif isinstance(edge, str):
            for e in self._edges:
                if e.label == edge:
                    return e
        return None

    def node_priority(self, node: Node):
        """
        Give the node a priority based on the number of incoming/outgoing/self edges.
        @param node: Node
        @return: node priority
        """
        prio = 0
        for source in self._adjacency:
            # Outgoing edges
            if source == node.id:
                prio += len(self._adjacency[source]) * 2
        for target in self._adjacency:
            if node.id in self._adjacency[target]:
                if target == node.id:
                    prio -= 1
                else:
                    prio += 2
        return prio

    def edge_priority(self, edge: Edge):
        """
        Give the edge a priority based on the priority of the nodes it connects.
        @param edge: Edge
        @return: node priority
        """
        prio = 0
        for n in self._adjacency:
            # source
            if n == edge.source.id:
                prio += self.node_priority(edge.source)
            # target
            if n == edge.target.id:
                prio += self.node_priority(edge.target)
        return prio

    def neighbours(self, node: Node) -> List[Node]:
        return [self._nodes[n_id] for n_id in self._adjacency[node.id].keys()]

    def add_node(self, node: Node):
        if node.id in self._nodes:
            return

        self._nodes[node.id] = node

        self._adjacency[node.id] = {}

    def remove_node(self, node: Node):
        del self._nodes[node.id]

    def add_edge(self, edge: Edge):
        if edge.id in self._edges:
            return

        edge.id = self._edge_id
        self._edge_id += 1
        self._edges[edge.id] = edge

        if edge.source.id not in self._nodes:
            self.add_node(edge.source)
        if edge.target.id not in self._nodes:
            self.add_node(edge.target)

        self._adjacency[edge.source.id][edge.target.id] = edge.weight

    def remove_edge(self, edge: Edge):
        del self._edges[edge.id]

    @staticmethod
    def check_cycles(graph, check_all: bool = False) -> List[List[Node]]:
        """
        Tarjan's algorithm: https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
        Complexity: O(|E| + |V|)
        :param graph: Graph
        :param check_all: bool          If False, stop at first cycle, otherwise get all cycles.
        :return: List[List[Node]]       A list of list that contains all cycles in the graph.
        """
        cycles = []
        stack = []
        index = [-1 for _ in range(0, len(graph.nodes))]
        low_link = [-1 for _ in range(0, len(graph.nodes))]
        on_stack = [False for _ in range(0, len(graph.nodes))]

        def strongly_connected(_id: int, i: int):
            v = _id
            index[v] = i
            low_link[v] = i
            on_stack[v] = True
            stack.append(v)
            i += 1

            # Advance to all neighbours.
            for e in graph.neighbours(graph.nodes[v]):
                w = e.id
                if index[w] == -1:
                    strongly_connected(w, i)

                    # Exit condition for one cycle.
                    if len(cycles) == 1 and not check_all:
                        return

                    low_link[v] = min(low_link[v], low_link[w])
                elif on_stack[w]:
                    low_link[v] = min(low_link[v], index[w])

            if low_link[v] == index[v]:
                temp_stack = []
                w = stack.pop()
                on_stack[w] = False
                temp_stack.append(graph.nodes[w])
                while w != v:
                    w = stack.pop()
                    on_stack[w] = False
                    temp_stack.append(graph.nodes[w])

                # Add only strongly connected components that consist of at least 2 nodes.
                if len(temp_stack) > 1:
                    cycles.append(temp_stack)

                # Exit condition for one cycle.
                if len(cycles) == 1 and not check_all:
                    return

        # Check strongly connected components for evey node.
        for _, n in graph.nodes.items():
            if index[n.id] == -1:
                strongly_connected(n.id, 0)

                # Exit condition for one cycle.
                if len(cycles) == 1 and not check_all:
                    return cycles

        return cycles
