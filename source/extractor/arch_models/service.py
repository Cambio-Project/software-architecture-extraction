from typing import Dict, List

from extractor.arch_models.operation import Operation


class Service:
    ID = 0

    def __init__(self, name: str):
        self._id = Service.ID
        self._name = name
        self._operations = {}
        self._hosts = []
        self._capacity = 1000

        # Runtime
        self._tags = {}

        Service.ID += 1

    def __repr__(self) -> str:
        return '{} {} ({})'.format(self.__class__.__name__, self._id, self._name)

    def __str__(self) -> str:
        s = self.__repr__()
        for _, operation in self._operations.items():
            s += '\n  - {}'.format(operation)
        return s

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def operations(self) -> Dict[str, Operation]:
        return self._operations

    @property
    def tags(self) -> Dict[str, str]:
        return self._tags

    @property
    def hosts(self):
        return self._hosts

    @property
    def capacity(self):
        return self._capacity

    def set_capacity(self, capacity):
        self._capacity = capacity

    @tags.setter
    def tags(self, tags: Dict[str, str]):
        self._tags = tags

    def print(self):
        print(self)

    def add_operation(self, operation: Operation):
        self._operations[operation.name] = operation
        operation.service = self

    def add_operations(self, operations: List[Operation]):
        for operation in operations:
            self._operations[operation.name] = operation
            operation.service = self

    def remove_operation(self, operation: Operation):
        del self._operations[operation.name]
        operation.service = None

    def remove_operations(self, operations: List[Operation]):
        for operation in operations:
            del self._operations[operation.name]
            operation.service = self

    def add_host(self, host):
        if host not in self._hosts:
            self._hosts.append(host)
