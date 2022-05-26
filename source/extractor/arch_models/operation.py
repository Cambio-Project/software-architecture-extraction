from typing import Dict, List
from source.extractor.arch_models.circuit_breaker import CircuitBreaker


class Operation:
    ID = 0

    def __init__(self, name: str):
        self._id = Operation.ID
        self._name = name
        self._dependencies = []
        self._service = None
        self._circuit_breaker = None
        
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
    def durations(self) -> Dict:
        return self._durations
        
    @property
    def logs(self) -> Dict[str, Dict]:
        return self._logs

    @property
    def circuit_breaker(self) -> CircuitBreaker:
        return self._circuit_breaker

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

    def remove_dependency_with_duplicates(self, dependency):
        while self._dependencies.__contains__(dependency):
            self._dependencies.remove(dependency)

    def add_circuit_breaker(self, circuitBreaker: CircuitBreaker):
        self._circuit_breaker = circuitBreaker
