import json

from extractor.arch_models.model import IModel
from typing import Union, Any, Dict

from typing.io import IO

from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service


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
        return False

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

                if operation_name in self._services[service_name].operations:
                    operation = self._services[service_name].operations[operation_name]
                else:
                    operation = Operation(operation_name)
                    self._services[service_name].add_operation(operation)

                operation.durations[span_id] = span.get('duration', -1)
                operation.tags[span_id] = {tag['key']: tag['value'] for tag in span.get('tags', {})}
                operation.logs[span_id] = JaegerTrace._parse_logs(span.get('logs', {}))

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
