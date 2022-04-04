import json
from source.extractor.arch_models.model import IModel


class ArchitectureMiSim:
    """
    Creates an architectural representation of a generic model from services, operations, and dependencies with
    the format of a MiSim model.
    """

    def __init__(self, model: IModel):
        self._model = model

    def export(self) -> str:
        """
        For each microservice it retrieves the relevant variables from the generic model and converts them
        into a json representation.
        """

        microservices = []

        for _, s in self._model.services.items():
            # variables of this microservice
            name = s.name
            instances = 1
            patterns = []
            capacity = 1000

            operations = []

            # retrieve all operations of this microservice
            for _, o in s.operations.items():
                op_name = o.name
                demand = 100
                dependencies = []

                # Get all dependencies of this operation
                for d in o.dependencies:
                    service = d.service.name
                    operation = d.name
                    probability = 1.0

                    dependency = {'service': service,
                                  'operation': operation,
                                  'probability': probability}

                    # eliminate duplicate dependencies
                    if dependency not in dependencies:
                        dependencies.append(dependency)

                operations.append({
                    'name': op_name,
                    'demand': demand,
                    'dependencies': dependencies
                })

            microservices.append({
                'name': name,
                'instances': instances,
                'patterns': patterns,
                'capacity': capacity,
                'operations': operations
            })

        result = {'microservices': microservices}
        return json.dumps(result, indent=2)
