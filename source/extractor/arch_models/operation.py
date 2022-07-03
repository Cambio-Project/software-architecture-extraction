from typing import Dict, List
from extractor.arch_models.circuit_breaker import CircuitBreaker
from extractor.arch_models.dependency import Dependency
from extractor.arch_models.retry import Retry


class Operation:
    ID = 0

    def __init__(self, name: str):
        self._id = Operation.ID
        self._name = name
        self._dependencies: [Dependency] = []
        self._service = None
        self._circuit_breaker = None
        self._demand = 100
        self._spans = set()
        self._retry = Retry()

        # stores {host1 :  [(timestamp1, response time 1), (timestamp2, response time 2), ...], host2: [(..),..], ...}
        self._response_times = {}

        # Runtime 
        self._durations = {}
        self._tags = {}
        self._logs = {}

        Operation.ID += 1

    def __repr__(self) -> str:
        if self._service:
            return '{} {} ({}/{})'.format(self.__class__.__name__, self._id, self._service.name, self._name)
        else:
            return '{} {} ({})'.format(self.__class__.__name__, self._id, self._name)

    def __str__(self) -> str:
        s = self.__repr__()
        for dependency in self._dependencies:
            s += ' -> {}'.format(dependency)
        return s

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def service(self) -> object:
        return self._service

    @service.setter
    def service(self, service: object):
        self._service = service

    @property
    def dependencies(self) -> List:
        return self._dependencies

    @property
    def response_times(self) -> Dict:
        return self._response_times

    @property
    def demand(self):
        return self._demand

    @property
    def durations(self) -> Dict:
        return self._durations

    @property
    def logs(self) -> Dict[str, Dict]:
        return self._logs

    @property
    def circuit_breaker(self) -> CircuitBreaker:
        return self._circuit_breaker

    @property
    def spans(self):
        return self._spans

    @property
    def retry(self):
        return self._retry

    @logs.setter
    def logs(self, logs: Dict[str, Dict]):
        self._logs = logs

    @property
    def tags(self) -> Dict[str, Dict]:
        return self._tags

    @tags.setter
    def tags(self, tags: Dict[str, Dict]):
        self._tags = tags

    def print(self):
        print(self)

    def add_dependency(self, dependency):
        self._dependencies.append(dependency)

    def add_dependencies(self, dependencies: List):
        self._dependencies.extend(dependencies)

    def remove_dependency(self, dependency):
        self._dependencies.remove(dependency)

    def remove_dependencies(self, dependencies: List):
        for dependency in dependencies:
            self._dependencies.remove(dependency)

    def contains_operation_as_dependency(self, operation):
        for dependency in self._dependencies:
            if dependency.name == operation.name and dependency.service == operation.service:
                return True
        return False

    def get_dependency_with_operation(self, operation):
        for dependency in self._dependencies:
            if dependency.name == operation.name and dependency.service == operation.service:
                return dependency
        return None

    def remove_dependency_with_duplicates(self, dependency):
        while self._dependencies.__contains__(dependency):
            self._dependencies.remove(dependency)

    def add_circuit_breaker(self, circuitBreaker: CircuitBreaker):
        self._circuit_breaker = circuitBreaker

    def set_demand(self, demand):
        self._demand = demand

    def add_span(self, span):
        self._spans.add(span)
