import json
import re

from extractor.arch_models.dependency import Dependency
from extractor.arch_models.model import IModel
from typing import Union, Any, Dict

from typing import IO

from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service
from extractor.arch_models.circuit_breaker import CircuitBreaker


class JaegerTrace(IModel):
    def __init__(self, source: Union[str, IO, dict] = None, multiple: bool = False, pattern: str = None):
        super().__init__(self.__class__.__name__, source, multiple, pattern)

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

        # Set default value for the call string pattern
        if self._call_string == "" or self._call_string is None:
            self.set_call_string('^GET$')

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

                host = '0.0.0.0'
                for tag in trace['processes'][pid]['tags']:
                    if tag['key'] == 'ip':
                        host = tag['value']
                if not self.services[service_name].hosts.__contains__(host):
                    self.services[service_name].add_host(host)

                # Ignore GET-Requests or similar
                if re.search(self._call_string, operation_name):
                    continue

                if operation_name in self._services[service_name].operations:
                    operation = self._services[service_name].operations[operation_name]
                else:
                    operation = Operation(operation_name)
                    self._services[service_name].add_operation(operation)

                # Track the amount times this operation gets called
                operation.add_span(span_id)

                duration = span.get('duration', -1)

                # store the response time (duration) of the operation
                if duration != -1:
                    if operation.response_times.keys().__contains__(host):
                        operation.response_times[host].append((span['startTime'], duration))
                    else:
                        operation.response_times[host] = [(span['startTime'], duration)]

                operation.durations[span_id] = duration
                operation.tags[span_id] = {tag['key']: tag['value'] for tag in span.get('tags', {})}
                operation.logs[span_id] = JaegerTrace._parse_logs(span.get('logs', {}))

                for s in operation.tags.items():
                    for value in s[1]:
                        if value == 'pattern.circuitBreaker':
                            if bool(s[1][value]):
                                operation.add_circuit_breaker(CircuitBreaker())

                        if value == 'loadbalancer.strategy':
                            self.services[service_name].load_balancer.set_strategy_with_tag(str(s[1][value]))

            # Add dependencies
            for span in trace['spans']:
                for reference in span['references']:
                    if reference['refType'] == 'CHILD_OF':
                        # Callee
                        pid = span['processID']
                        service_name = process_ids[pid]
                        operation_name = span['operationName']

                        # Ignore GET-Requests or similar
                        if re.search(self._call_string, operation_name):
                            continue

                        operation = self._services[service_name].operations[operation_name]

                        # Caller
                        parent_id = reference['spanID']
                        parent_span = span_ids[parent_id]
                        parent_pid = parent_span['processID']
                        parent_service_name = process_ids[parent_pid]
                        parent_operation_name = parent_span['operationName']

                        latency = span['startTime'] - parent_span['startTime']
                        add_latency = False

                        # save start time and end time (needed for retry detection)
                        start_time = span['startTime']
                        end_time = start_time + span['duration']

                        parent_operation = None

                        # Handling of GET-Requests or similar.
                        # What kind of spans are ignored is specified with the call_string pattern.
                        # If the parent operation matches the pattern the true parent operation (the calling operation)
                        # has to be the grandparent operation of the current operation.
                        if re.search(self._call_string, parent_operation_name):
                            for ref in parent_span['references']:
                                if ref['refType'] == 'CHILD_OF':
                                    grandparent_id = ref['spanID']
                                    grandparent_span = span_ids[grandparent_id]
                                    grandparent_pid = grandparent_span['processID']
                                    grandparent_service_name = process_ids[grandparent_pid]
                                    grandparent_operation_name = grandparent_span['operationName']
                                    parent_operation = self._services[grandparent_service_name].operations[
                                        grandparent_operation_name]
                                    add_latency = True

                                    # update start- and end time
                                    start_time = parent_span['startTime']
                                    end_time = start_time + parent_span['duration']

                                    parent_span = grandparent_span
                        else:
                            parent_operation = self._services[parent_service_name].operations[parent_operation_name]

                        if not parent_operation.contains_operation_as_dependency(operation):
                            parent_operation.add_dependency(Dependency(operation))

                        # add a custom latency to the dependency if the calling span is a GET-Request or similar
                        if add_latency:
                            parent_operation.get_dependency_with_operation(operation).add_latency(latency)

                        # keep track of spans that call this operation in order to calculate probabilities later
                        if not parent_operation.get_dependency_with_operation(operation).calling_spans.__contains__(
                                parent_span):
                            parent_operation.get_dependency_with_operation(operation).add_calling_span(parent_span)
                            parent_operation.get_dependency_with_operation(operation).add_call()

                        # add this call to the call history of the parent span in order to detect retries later
                        tags = {tag['key']: tag['value'] for tag in span['tags']}
                        parent_operation.retry.add_call_history_entry(
                            parent_span['spanID'],
                            {span['startTime']: (operation_name, tags.get('error', False), start_time, end_time)})

        self.subsequent_calculations()

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
