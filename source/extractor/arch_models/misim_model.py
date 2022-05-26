import json

from typing import IO, Union, Dict, Any

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
                ms_operations = ms['operations'] or []
                service = Service(ms_name)

                # Iterate over all operations.
                for ms_operation in ms_operations:
                    ms_operation_name = ms_operation['name']
                    operation = Operation(ms_operation_name)

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

                        try:
                            operation = self._services[dependency_service].operations[dependency_operation]
                            self._services[ms_name].operations[ms_operation_name].add_dependency(operation)
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
