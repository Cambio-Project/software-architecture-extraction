from typing import Union, Dict, Tuple, List, Any
from typing import IO
import pandas as pd

from extractor.arch_models.hazard import *
from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service
from util.log import tb


class NoDependenciesException(BaseException):
    def __init__(self):
        super().__init__('No dependencies found')


class WrongFormatException(BaseException):
    def __init__(self):
        super().__init__('Wrong format')


class UnknownOperation(BaseException):
    def __init__(self, service: str, operation: str):
        super().__init__('Unknown Operation: {}/{}'.format(service, operation))


class OperationSelfDependency(BaseException):
    def __init__(self, operation: Operation):
        if operation.service:
            operation = '{}/{}'.format(operation.service.name, operation.name)
        super().__init__('Self Dependency: {}'.format(operation))


class CyclicOperationDependency(BaseException):
    def __init__(self, operation1: Operation, operation2: Operation):
        if operation1.service:
            operation1 = '{}/{}'.format(operation1.service.name, operation1.name)
        if operation2.service:
            operation2 = '{}/{}'.format(operation2.service.name, operation2.name)
        super().__init__('Circular Dependency: {} <-> {}'.format(operation1, operation2))


class IModel:
    """
    Interface for all models.
    All derived classes must implement the read method.
    The read method is responsible to check the syntax of the model.

    IModel provides a validation method that checks for validity of the model.
    This validation checks the semantic of the model.
    """
    def __init__(self, model_type: str, source: Union[str, IO] = None, multiple: bool = False, pattern: str = None):
        self._model_type = model_type
        self._services = {}
        self._valid = False
        self._hazards = {}
        self._stimuli = []
        self._call_string = pattern

        if source:
            try:
                if multiple:
                    success = self.read_multiple(source)
                else:
                    success = self.read(source)

                if not success:
                    print('Model was not read successful')
            except BaseException as e:
                print(tb(e))
                print('Something went wrong')

    def __iter__(self):
        return iter(self._services)

    @property
    def type(self) -> str:
        return self._model_type

    @property
    def services(self) -> Dict[str, Service]:
        return self._services

    @property
    def valid(self) -> bool:
        return self._valid

    @property
    def hazards(self) -> Dict[str, List[Hazard]]:
        return self._hazards

    @property
    def call_string(self):
        return self._call_string

    def set_call_string(self, call_pattern):
        self._call_string = call_pattern

    @hazards.setter
    def hazards(self, hazards: Dict[str, List[Hazard]]):
        self._hazards = hazards

    # Private

    def _parse_multiple(self, model: Dict[str, Any]) -> bool:
        raise NotImplementedError('_parse_multiple() method must be implemented!')

    def _parse(self, model: Dict[str, Any]) -> bool:
        raise NotImplementedError('_parse() method must be implemented!')

    # Public

    def calculate_dependency_probabilities(self):
        # iterate through all dependencies and call the method for calculating the probability
        for service in self.services.values():
            for operation in service.operations.values():
                for dependency in operation.dependencies:
                    dependency.calculate_probability(len(operation.spans))

    def validate(self, check_everything=False) -> Tuple[bool, List[BaseException]]:
        valid = True
        stack = []

        try:
            for _, service in self._services.items():
                for _, operation in service.operations.items():

                    # Check self dependency
                    if operation in operation.dependencies:
                        stack.append(OperationSelfDependency(operation))

                    for dependency in operation.dependencies:
                        # Check circular dependencies
                        if operation in dependency.dependencies:
                            stack.append(CyclicOperationDependency(operation, dependency))
                            continue

                        try:
                            _ = self._services[dependency.service.name].operations[dependency.name]

                        # Service or operation is not known.
                        except AttributeError:
                            print(service)
                            if not check_everything:
                                return False, [UnknownOperation(service.name, operation.name)]
                            else:
                                valid = False
                                stack.append(UnknownOperation(service.name, operation.name))

        # Unknown exception has occurred.
        except BaseException as e:
            stack.append(e)
            return False,  stack

        self._valid = valid
        return valid, stack

    def analyze(self) -> Dict[str, List[Hazard]]:
        stack = {}

        try:
            for _, service in self._services.items():
                for _, operation in service.operations.items():
                    series = pd.Series(operation.durations.values())
                    stack[operation.name] = []

                    # Filter outliers by 3 times standard deviation
                    filtered = series[~((series-series.mean()).abs() > series.std() * ResponseTimeSpike.DEVIATION_FACTOR)]
                    diff = 1 - filtered.min() / filtered.max()

                    # Min and Max response times differ by at least 50%
                    if diff > ResponseTimeDeviation.DEVIATION_INTERVAL:
                        stack[operation.name].append(ResponseTimeDeviation(operation, diff))

                    # At least one outlier detected
                    if len(filtered) < len(series):
                        # Spike workload
                        deviation = filtered.max() - series.max()
                        if deviation > 0:
                            stack[operation.name].append(ResponseTimeSpike(operation, deviation))

            for _, service in self._services.items():
                for _, operation in service.operations.items():
                    if operation.name in stack:
                        if len(stack[operation.name]) > 0:
                            for hazard in stack[operation.name]:
                                if isinstance(hazard, ResponseTimeSpike):
                                    stack[service.name].append(ServiceFailure(service))
                                elif isinstance(hazard, ResponseTimeDeviation):
                                    stack[service.name].append(DecreasedServicePerformance(service))

            return stack
        except BaseException as e:
            tb(e)
            return stack

    def print(self):
        for _, service in self._services.items():
            service.print()

    def read_multiple(self, source: Union[str, IO]) -> bool:
        raise NotImplementedError('read_multiple() method must be implemented!')

    def read(self, source: Union[str, IO]) -> bool:
        raise NotImplementedError('read() method must be implemented!')
