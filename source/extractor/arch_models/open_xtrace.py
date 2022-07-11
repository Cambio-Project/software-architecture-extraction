import json
from distutils.util import strtobool
from tokenize import String
from xmlrpc.client import Boolean

from extractor.arch_models.circuit_breaker import CircuitBreaker
from extractor.arch_models.dependency import Dependency

from extractor.arch_models.model import IModel
from typing import OrderedDict, Tuple, Union, Any, Dict, List

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
            service_name = span.get('application', '')
            node = span.get("rootOfSubTrace", {})
            children = node.get("children", {})
            host = self.checkPort(span)

            if service_name not in self._services:
                service = Service(service_name)
                service.tags = { "servicename" : service_name, "ipv4" : host}
                service.add_host(host)
                self._services[service_name] = service
            
            tupel = self.calculateOperations(span, host)
            operation = tupel[0]
            operation_id = tupel[1]
            for child in children:
                dependency = self._parse_children(child)
                child_dependency = dependency[0] 
                child_id = dependency[1]
                #add retry
                operation.retry.add_call_history_entry(
                    operation_id,
                    {child_dependency.timestamp[child_id]: (child_dependency.name, child_dependency.error[child_id], child_dependency.starttime[child_id], child_dependency.endtime[child_id])})
                if not operation.contains_operation_as_dependency(child_dependency):
                    operation.add_dependency(Dependency(child_dependency))
                if not operation.get_dependency_with_operation(child_dependency).calling_spans.__contains__(
                        operation_id):
                    operation.get_dependency_with_operation(child_dependency).add_calling_span(operation_id)
                    operation.get_dependency_with_operation(child_dependency).add_call()
                    
        self.subsequent_calculations()
        return True

    def _parse_children(self, model: List[Dict[str, Any]]) -> Tuple[Operation, int]:
        child = model.get('targetSubTrace', {})
        service_name = child.get('application', '')
        node = child.get("rootOfSubTrace", {})
        children = node.get("children", {})

        host = self.checkPort(child)

        if service_name not in self._services:
            service = Service(service_name)
            service.tags = { "serviceName" : service_name, "ipv4" : host}
            service.add_host(host)
            self._services[service_name] = service
        elif not self._services[service_name].hosts.__contains__(host):
            self._services[service_name].add_host(host)

        tupel = self.calculateOperations(model, host)
        operation = tupel[0]
        operation_id = tupel[1]
        latency = operation.latency[operation_id]
        for child in children:        
            dependency = self._parse_children(child)
            child_dependency : Operation = dependency[0]
            child_id = dependency[1]
            child_latency = child_dependency.latency[child_id]
            #add retry
            operation.retry.add_call_history_entry(
                    operation_id,
                    {child_dependency.timestamp[child_id]: (child_dependency.name, child_dependency.error[child_id], child_dependency.starttime[child_id], child_dependency.endtime[child_id])})
            if not operation.contains_operation_as_dependency(child_dependency):
                tmp = Dependency(child_dependency)
                operation.add_dependency(tmp)
                if latency != None:
                    tmp.add_latency(child_latency)
            elif latency != None:
                operation.get_dependency_with_operation(child_dependency).add_latency(latency)
                    
            if not operation.get_dependency_with_operation(child_dependency).calling_spans.__contains__(
                        operation_id):
                operation.get_dependency_with_operation(child_dependency).add_calling_span(operation_id)
                operation.get_dependency_with_operation(child_dependency).add_call()
        return operation, operation_id

    # Checks if a circuitBreaker pattern exists and adds it to the operation
    def addCircuitBreaker(self, model: List[Dict[str, Any]], operation : Operation) :
        pattern = "additionalInformation.pattern.circuitBreaker"
        if pattern in model:
            circuitbreaker = model.get(pattern, '')
            boolean = strtobool(circuitbreaker)
            if bool(boolean) is True:
                operation.add_circuit_breaker(CircuitBreaker())

    # Looks up if a port is specified and adds it to the host
    def checkPort(self, model: List[Dict[str, Any]]) -> String:
        port = model.get('port', '')
        host = model.get('host', '')
        if port is not None:
            if port != -1 and not host.__contains__(port):
                host = str(host) + ':' + str(port)
        return host

    #
    def calculateOperations(self, model: List[Dict[str, Any]], host) -> Tuple[Operation, str]: 
        latency = None
        timestamp = None
        timestamp_start = None
        timestamp_end = None
        child = model.get('targetSubTrace', {})
        service_name = child.get('application', '')
        operation = child.get("businessTransaction", '')
        node = child.get("rootOfSubTrace", {})
        duration = int(child.get('responseTime', -1) / 1000)
        if "rootOfSubTrace" in model:
            operation = model.get("businessTransaction", '')
            node = model.get("rootOfSubTrace", {})
            service_name = model.get('application', '')
            duration = int(model.get('responseTime', -1) / 1000)
        else:
            timestamp = node.get('timeStamp', 0) * 1000
            timestamp_start = model.get('timeStamp', 0) * 1000
            timestamp_end = model.get('exitTime', 0) * 1000
            latency = int((timestamp - timestamp_start))
        identifier = node.get('identifier')
        httpmethod = node.get("requestMethod", "")
        httppath = node.get("uri", "")

        if operation in self.services[service_name].operations:
            operation = self.services[service_name].operations[operation]
        else:
            operation = Operation(operation)
            self.addCircuitBreaker(node, operation)
            self._services[service_name].add_operation(operation)

        # Track the amount times this operation gets called
        operation.add_span(identifier)

        # store the response time (duration) of the operation
        if duration != -1:
            if operation.response_times.keys().__contains__(host):
                operation.response_times[host].append((timestamp, duration))
            else:
                operation.response_times[host] = [(timestamp, duration)]
        if duration != None:
            operation.durations[identifier] = duration
        if latency != None:    
            operation.latency[identifier] = latency
        operation.error[identifier] = model.get("additionalInformation.error", False)

        if timestamp != None:    
            operation.timestamp[identifier] = timestamp

        if timestamp_start != None:
            operation.starttime[identifier] = timestamp_start

        if timestamp_end != None:
            operation.endtime[identifier] = timestamp_end

        tags = self.filterAdditionalInformation(model)
        tags.update(self.filterAdditionalInformation(node))
        if (not "http.method" in tags) and httpmethod != "":
            tags["http.method"] = httpmethod 
        if (not "http.path" in tags) and httppath != "":
            tags["http.path"]= httppath
        operation.tags[identifier] = OrderedDict(sorted(tags.items(), key=lambda t: t[0]))
        operation.logs[identifier] = {}

        return operation, identifier

    def filterAdditionalInformation(self, model: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        tags = dict()
        filtertags = dict(filter(lambda item: "additionalInformation" in item[0], model.items()))
        for key in filtertags:
            newKey = key.replace('additionalInformation.', '')
            tags[newKey] = filtertags.get(key)
        return tags

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
