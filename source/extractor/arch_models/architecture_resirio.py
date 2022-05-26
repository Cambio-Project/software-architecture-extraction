import json
import re
from typing import Tuple, List

from source.extractor.graph.graph import Graph, Node, Edge
from source.extractor.arch_models.model import IModel, UnknownOperation


class CyclicServiceOperations(BaseException):
    def __init__(self, nodes: List[Node]):
        super().__init__('Cyclic operations: {}'.format(' -> '.join(map(str, nodes))))


class Architecture:
    """
    Creates a architectural representation of a generic model from services, operations, and dependencies.
    """

    def __init__(self, model: IModel):
        self._model = model
        self._graph = Graph()

        self._build_graph()

    def _build_graph(self):
        temp = None

        # Add nodes
        for _, s in self._model.services.items():
            self._graph.add_node(Node(s.name, s.id))

        # Add edges
        for _, s in self._model.services.items():
            for _, o in s.operations.items():
                source = self._graph.node(s.id)

                # Self edge
                if not o.dependencies:
                    self._graph.add_edge(Edge(source, source, o.name))

                else:
                    for d in o.dependencies:
                        target = self._graph.node(d.service.id)

                        # Self edge (already handled)
                        if temp == target:
                            continue

                        temp = target
                        try:
                            self._graph.add_edge(Edge(source, target, o.name))
                        except UnknownOperation(d.service.name, d.name):
                            pass

    @property
    def model(self) -> IModel:
        return self._model

    @property
    def graph(self) -> Graph:
        return self._graph

    def validate(self, check_everything: bool = False) -> Tuple[bool, List[BaseException]]:
        valid = True
        stack = []

        cycle = Graph.check_cycles(self._graph, False)
        if cycle:
            stack.append(CyclicServiceOperations(cycle[0]))

        return valid, stack

    def export(self, pretty: bool = False, lightweight: bool = False) -> str:
        result = {'nodes': {}, 'edges': {}, 'analysis': {}}

        for _, n in self._graph.nodes.items():
            result['nodes'][n.id] = {
                'id':       n.id,
                'label':    n.label,
                'priority': self._graph.node_priority(n)
            }

            if not lightweight:
                result['nodes'][n.id]['data'] = {
                    'tags': self._model.services[n.label].tags
                }

        for _, e in self._graph.edges.items():
            operation = self._model.services[e.source.label].operations[e.label]
            result['edges'][e.id] = {
                'id':       e.id,
                'label':    e.label,
                'source':   e.source.id,
                'target':   e.target.id,
                'priority': result['nodes'][e.source.id]['priority'] + result['nodes'][e.target.id]['priority']
            }

            if not lightweight:
                result['edges'][e.id]['data'] = {
                    'duration': operation.durations,
                    'logs':     operation.logs,
                    'tags':     operation.tags
                }

        # Unused: would create existing hazards at the start of the elicitation.
        # for hazard in self._model.hazards:
        #     result['hazards'][hazard.id] = {
        #         'id':            hazard.id,
        #         'type':          hazard.type,
        #         'metric':        hazard.metric,
        #         'property_type': hazard.prop_type,
        #         'property_name': hazard.prop_name,
        #         'keyword':       hazard.keyword,
        #         'value':         hazard.value,
        #         'nodes':         hazard.nodes,
        #         'edges':         hazard.edges
        #     }

        for name, hazardlist in self._model.hazards.items():
            for hazard in hazardlist:
                if hazard.type not in result['analysis']:
                    result['analysis'][hazard.type] = {
                        'property_type': hazard.prop_type,
                        'property_name': hazard.prop_name,
                        'metric':        hazard.metric,
                        'keyword':       hazard.keyword,
                        'value':         hazard.value
                    }

        if pretty:
            return json.dumps(result, indent=2)
        return json.dumps(result)

    @staticmethod
    def normalize_operation_name(name: str):
        return re.sub(r'^.*(get|put|post)\s*', '', name, flags=re.IGNORECASE) or 'GET /'
