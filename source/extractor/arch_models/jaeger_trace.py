import json

from ..arch_models.model import IModel
from typing import Union, Any, Dict

from typing.io import IO

from ..arch_models.operation import Operation
from ..arch_models.service import Service
from ..arch_models.circuit_breaker import CircuitBreaker


class JaegerTrace(IModel):
    def __init__(self, source: Union[str, IO, dict] = None, multiple: bool = False):
        super().__init__(self.__class__.__name__, source, multiple)

    @staticmethod
    def _parse_logs(logs) -> Dict[int, Dict[str, str]]:
        operation_logs = {}
        for log in logs:
            operation_logs[log['timestamp']] = {f['key']: f['value'] for f in log['fields']}

        return operation_logs

    def _parse_multiple(self, model: Dict[str, Any]) -> bool:
        return self._parse(model)

    def _parse(self, model: Dict[str, Any]) -> bool:
        # Store process_id: service_name
        process_ids = {}
        # Store span_id: span
        span_ids = {}
        traces = model['data']

        for trace in traces:
            # Identify all services (processes)
            for process_id, process in trace['processes'].items():
                service_name = process['serviceName']

                service = Service(service_name)
                service.tags = {tag['key']: tag['value'] for tag in process['tags']}
                service.tags['serviceName'] = service_name

                # check if service already exists
                if service_name not in self.services:
                    self._services[service_name] = service
                process_ids[process_id] = service_name

            # Add operations to the corresponding services.
            for span in trace['spans']:
                pid = span['processID']

                # Unknown process
                if pid not in process_ids:
                    return False

                span_id = span['spanID']
                span_ids[span_id] = span
                operation_name = span['operationName']

                service_name = process_ids[pid]

                host = trace['processes'][pid]['tags'][0].get('value')
                if not self.services[service_name].hosts.__contains__(host):
                    self.services[service_name].add_host(host)

                if operation_name in self._services[service_name].operations:
                    operation = self._services[service_name].operations[operation_name]
                else:
                    operation = Operation(operation_name)
                    self._services[service_name].add_operation(operation)

                operation.durations[span_id] = span.get('duration', -1)
                operation.tags[span_id] = {tag['key']: tag['value'] for tag in span.get('tags', {})}
                operation.logs[span_id] = JaegerTrace._parse_logs(span.get('logs', {}))

                for s in operation.tags.items():
                    for value in s[1]:
                        if value == 'pattern.circuitBreaker':
                            if bool(s[1][value]):
                                operation.add_circuit_breaker(CircuitBreaker())

            # Add dependencies
            for span in trace['spans']:
                for reference in span['references']:
                    if reference['refType'] == 'CHILD_OF':
                        # Callee
                        pid = span['processID']
                        service_name = process_ids[pid]
                        operation_name = span['operationName']

                        operation = self._services[service_name].operations[operation_name]

                        # Caller
                        parent_id = reference['spanID']
                        parent_span = span_ids[parent_id]
                        parent_pid = parent_span['processID']
                        parent_service_name = process_ids[parent_pid]
                        parent_operation_name = parent_span['operationName']

                        parent_operation = self._services[parent_service_name].operations[parent_operation_name]
                        parent_operation.add_dependency(operation)

            # A GET-request-dependency gets replaced with all the dependencies of this GET-request.
            for _, s in self.services.items():
                for _, op in s.operations.items():
                    for dependency in op.dependencies:
                        if dependency.name == 'GET':
                            for new_dep in self.services[dependency.service.name].operations.get('GET').dependencies:
                                op.add_dependency(new_dep)
                            op.remove_dependency_with_duplicates(dependency)

            # Delete all GET-operations from the model
            for _, s in self.services.items():
                get_operations = []
                for _, op in s.operations.items():
                    if op.name == 'GET':
                        get_operations.append(op)
                s.remove_operations(get_operations)

        return True

    def read_multiple(self, source: Union[str, IO, dict] = None) -> bool:
        if isinstance(source, str):
            return self._parse_multiple(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse_multiple(json.load(source))
        elif isinstance(source, dict):
            return self._parse_multiple(source)
        return False

    def read(self, source: Union[str, IO, dict] = None) -> bool:
        if isinstance(source, str):
            return self._parse(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse(json.load(source))
        elif isinstance(source, dict):
            return self._parse(source)
        return False
