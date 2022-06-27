from curses.ascii import NUL
import json
from distutils.util import strtobool 
from pickle import TRUE
import re

from extractor.arch_models.circuit_breaker import CircuitBreaker
from extractor.arch_models.dependency import Dependency

from extractor.arch_models.model import IModel
from typing import Union, Any, Dict, List

from typing import IO

from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service


class OpenXTrace(IModel):

    def __init__(self, source: Union[str, IO, list] = None, multiple: bool = False, pattern: str = None):
        super().__init__(self.__class__.__name__, source, multiple, pattern)

    def _parse_multiple(self, model: List[List[Dict[str, Any]]]) -> bool:
        multiple = [trace for trace_list in model for trace in trace_list]
        return self._parse(multiple)



    def _parse(self, model: List[Dict[str, Any]]) -> bool:
        # Store all services
        for span in model:
            span = span.get("rootOfTrace", {})
            root_service = span.get('application', '')
            root_port = span.get('port', '')
            root_host = span.get('host', '')
            operation = span.get("businessTransaction", '')
            rootnode = span.get("rootOfSubTrace", {})
            children = rootnode.get("children", {})

            if root_port is not None:
                if root_port != -1 and not root_host.__contains__(root_port):
                    root_host = str(root_host) + ':' + str(root_port)

            if root_service not in self._services:
                service = Service(root_service)
                service.tags = {}
                service.add_host(root_host)
                self._services[root_service] = service
        
            
            if operation in self.services[root_service].operations:
                operation = self.services[root_service].operations[operation]
            else:
                operation = Operation(operation)
                self.addCircuitBreaker(rootnode, operation) 
                self._services[root_service].add_operation(operation)   

            for child in children:
                dependency = self._parse_children(child)

                if not operation.contains_operation_as_dependency(dependency):
                    operation.add_dependency(Dependency(dependency))

        return True

    def _parse_children(self, model: List[Dict[str, Any]]) -> Operation:
        model = model.get('targetSubTrace', {})
        service_name = model.get('application', '')
        port = model.get('port', '')
        host = model.get('host', '')
        operation = model.get("businessTransaction", '')
        rootnode = model.get("rootOfSubTrace", {})
        children = rootnode.get("children", {})

        if port is not None:
            if port != -1 and not host.__contains__(port):
                host = str(host) + ':' + str(port)

        if service_name not in self._services:
            service = Service(service_name)
            service.tags = {}
            service.add_host(host)
            self._services[service_name] = service

        if operation in self.services[service_name].operations:
            operation = self.services[service_name].operations[operation]
        else:
            operation = Operation(operation)
            self.addCircuitBreaker(rootnode, operation)
            self._services[service_name].add_operation(operation)

        for child in children:        
           dependency = self._parse_children(child)

           if not operation.contains_operation_as_dependency(dependency):
            operation.add_dependency(Dependency(dependency))

        return operation

    def addCircuitBreaker(self, model: List[Dict[str, Any]], operation : Operation) :
        pattern = "additionalInformation.pattern.circuitBreaker"
        if pattern in model:
            circuitbreaker = model.get(pattern, '')
            boolean = strtobool(circuitbreaker)
            if bool(boolean) is True:
                operation.add_circuit_breaker(CircuitBreaker())

    def read_multiple(self, source: Union[str, IO, list] = None) -> bool:
        if isinstance(source, str):
            return self._parse_multiple(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse_multiple(json.load(source))
        elif isinstance(source, list):
            return self._parse_multiple(source)
        return False

    def read(self, source: Union[str, IO, list] = None) -> bool:
        if isinstance(source, str):
            return self._parse(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse(json.load(source))
        elif isinstance(source, list):
            return self._parse(source)
        return False
