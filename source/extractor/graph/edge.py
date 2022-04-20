from ..graph.node import Node


class Edge:
    def __init__(self, source: Node, target: Node, label: str = '', weight: int = 1):
        self._label = label
        self._weight = weight
        self._id = -1
        self._source = source
        self._target = target

    def __repr__(self) -> str:
        return '{} {} ({} -> {}) [{}]'.format(self.__class__.__name__, self._id, self._source, self._target, self._label)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, edge_id: int):
        self._id = edge_id

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def source(self) -> Node:
        return self._source

    @source.setter
    def source(self, source: Node):
        self._source = source

    @property
    def target(self) -> Node:
        return self._target

    @target.setter
    def target(self, target: Node):
        self._target = target

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, weight: int):
        self._weight = weight
