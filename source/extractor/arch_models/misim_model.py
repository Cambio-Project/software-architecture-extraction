import json

from typing import IO, Union, Dict, Any

from extractor.arch_models.dependency import Dependency
from extractor.arch_models.model import IModel, UnknownOperation, WrongFormatException
from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service


class MiSimModel(IModel):
    def __init__(self, source: Union[str, IO, dict] = None):
        super().__init__(self.__class__.__name__, source)

    # Private

    def _parse(self, model: Dict[str, Any]) -> bool:
        try:
            microservices = model['microservices'] or []

            # Iterate over all services.
            for ms in microservices:
                ms_name = ms['name']
                ms_instances = ms['instances']
                ms_capacity = ms['capacity']
                ms_operations = ms['operations'] or []
                service = Service(ms_name)

                for i in range(0, ms_instances):
                    # add default instances
                    service.add_host(str(i))

                service.set_capacity(ms_capacity)

                # Iterate over all operations.
                for ms_operation in ms_operations:
                    ms_operation_name = ms_operation['name']
                    ms_operation_demand = ms_operation['demand']
                    operation = Operation(ms_operation_name)
                    operation.set_demand(ms_operation_demand)

                    service.add_operation(operation)

                self._services[service.name] = service

            # Assign all dependencies
            for ms in microservices:
                ms_name = ms['name']
                ms_operations = ms['operations'] or []

                for ms_operation in ms_operations:
                    ms_operation_name = ms_operation['name']
                    ms_operation_dependencies = ms_operation['dependencies'] or []

                    for dependency in ms_operation_dependencies:
                        dependency_service = dependency['service']
                        dependency_operation = dependency['operation']
                        dependency_probability = dependency['probability']
                        dependency_latency: str = dependency['custom_delay'] or None

                        try:
                            operation = self._services[dependency_service].operations[dependency_operation]
                            if not self._services[ms_name].operations[ms_operation_name].contains_operation_as_dependency(operation):
                                dependency_of_op = Dependency(operation)

                                if dependency_latency.__contains__('+-'):
                                    mean_std = dependency_latency.split('+-')
                                    mean = mean_std[0]
                                    std = mean_std[1]
                                    dependency_of_op.add_latency(float(mean) * 1000000)
                                    dependency_of_op.add_latency((float(mean) - float(std)) * 1000000)
                                    dependency_of_op.add_latency((float(mean) + float(std)) * 1000000)
                                elif dependency_latency is not None:
                                    dependency_of_op.add_latency(int(dependency_latency) * 1000000)

                                if dependency_probability is not None:
                                    dependency_of_op.set_probability(dependency_probability)
                                else:
                                    dependency_of_op.set_probability(1.0)

                                self._services[ms_name].operations[ms_operation_name].add_dependency(dependency_of_op)

                        except KeyError:
                            raise UnknownOperation(dependency_service, dependency_operation)
            return True

        except WrongFormatException as e:
            print(e)
            return False

        except UnknownOperation as e:
            print(e)
            return False

    # Public

    def read(self, source: Union[str, IO, dict]) -> bool:
        if isinstance(source, str):
            return self._parse(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse(json.load(source))
        elif isinstance(source, dict):
            return self._parse(source)
        return False
