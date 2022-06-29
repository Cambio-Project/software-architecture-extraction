import json
import re

from extractor.arch_models.circuit_breaker import CircuitBreaker
from extractor.arch_models.dependency import Dependency

from extractor.arch_models.model import IModel
from typing import Union, Any, Dict, List

from typing import IO

from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service


class ZipkinTrace(IModel):

    def __init__(self, source: Union[str, IO, list] = None, multiple: bool = False, pattern: str = None):
        super().__init__(self.__class__.__name__, source, multiple, pattern)

    def _parse_multiple(self, model: List[List[Dict[str, Any]]]) -> bool:
        multiple = [trace for trace_list in model for trace in trace_list]
        return self._parse(multiple)

    def _parse(self, model: List[Dict[str, Any]]) -> bool:
        # Store span_id: span
        span_ids = {}

        client_span_ids = {}

        # Set default value for the call string pattern
        if self._call_string == "" or self._call_string is None:
            self.set_call_string('^get$')

        # Store all services
        for span in model:
            if span.get('kind', None) != 'CLIENT':
                span_ids[span['id']] = span
            else:
                client_span_ids[span['id']] = span

            local = span.get('localEndpoint', {})
            remote = span.get('remoteEndpoint', {})

            local_endpoint = local.get('serviceName', '')
            remote_endpoint = remote.get('serviceName', '')

            local_host = local.get('ipv4') or local.get('ipv6')
            local_port = local.get('port', None)

            remote_host = remote.get('ipv4') or remote.get('ipv6')
            remote_port = remote.get('port', None)

            if local_port is not None:
                local_host = str(local_host) + ':' + str(local_port)
            if remote_port is not None:
                remote_host = str(remote_host) + ':' + str(remote_port)

            if local_endpoint not in self._services:
                service = Service(local_endpoint)
                service.tags = local
                service.add_host(local_host)
                self._services[local_endpoint] = service
            else:
                if not self._services[local_endpoint].hosts.__contains__(local_host):
                    self._services[local_endpoint].add_host(local_host)
            if len(remote_endpoint) > 0:
                if remote_endpoint not in self._services:
                    service = Service(remote_endpoint)
                    service.tags = remote
                    service.add_host(remote_host)
                    self._services[remote_endpoint] = service
                else:
                    if not self._services[remote_endpoint].hosts.__contains__(remote_host):
                        self._services[remote_endpoint].add_host(remote_host)

        # Add operations
        for span in model:
            local = span.get('localEndpoint', {})
            service_name = local.get('serviceName', '')
            span_id = span['id']

            # Unknown service
            if not service_name:
                return False

            operation_name = span['name']
            if re.search(self._call_string, operation_name):
                continue

            if operation_name in self.services[service_name].operations:
                operation = self.services[service_name].operations[operation_name]
            else:
                operation = Operation(operation_name)
                self._services[service_name].add_operation(operation)

            # Track the amount times this operation gets called
            operation.add_span(span_id)

            duration = span.get('duration', -1)

            # calculate host of operation
            local = span.get('localEndpoint', {})
            local_host = local.get('ipv4') or local.get('ipv6')
            local_port = local.get('port', None)
            if local_port is not None:
                local_host = str(local_host) + ':' + str(local_port)

            # store the response time (duration) of the operation
            if duration != -1:
                if operation.response_times.keys().__contains__(local_host):
                    operation.response_times[local_host].append((span['timestamp'], duration))
                else:
                    operation.response_times[local_host] = [(span['timestamp'], duration)]

            operation.durations[span_id] = duration
            operation.tags[span_id] = span.get('tags', {})
            operation.logs[span_id] = {a['timestamp']: {'log': a['value']} for a in span.get('annotations', {})}

            for s in operation.tags.items():
                for value in s[1]:
                    if value == 'pattern.circuitBreaker':
                        if bool(s[1][value]):
                            operation.add_circuit_breaker(CircuitBreaker())

        # Add dependencies
        for span in model:
            if span.get('parentId', 0) in span_ids:

                # Callee
                ID = span['id']
                local = span.get('localEndpoint', {})
                service_name = local.get('serviceName', '')
                operation_name = span['name']
                if re.search(self._call_string, operation_name):
                    continue

                operation = self._services[service_name].operations[operation_name]

                # Caller
                parent_id = span['parentId']
                parent_span = span_ids[parent_id]
                parent = parent_span.get('localEndpoint', {})
                parent_service_name = parent.get('serviceName', '')
                parent_operation_name = parent_span['name']
                if re.search(self._call_string, parent_operation_name):
                    continue

                parent_operation = self._services[parent_service_name].operations[parent_operation_name]

                if not parent_operation.contains_operation_as_dependency(operation):
                    parent_operation.add_dependency(Dependency(operation))

                # add a custom latency to the dependency if a client span is present for this span
                if client_span_ids.keys().__contains__(ID):
                    client_span = client_span_ids[ID]
                    latency = span['timestamp'] - client_span['timestamp']
                    parent_operation.get_dependency_with_operation(operation).add_latency(latency)

                # keep track of spans that call this operation in order to calculate probabilities later
                if not parent_operation.get_dependency_with_operation(operation).calling_spans.__contains__(parent_span):
                    parent_operation.get_dependency_with_operation(operation).add_calling_span(parent_span)
                    parent_operation.get_dependency_with_operation(operation).add_call()

                # add this call to the call history of the parent span in order to detect retries later
                parent_operation.retry.add_call_history_entry(
                    parent_span['id'], {span['timestamp']: (operation_name, span['tags'].get('error', False))})

        self.subsequent_calculations()

        return True

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
