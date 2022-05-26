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

        services_of_model = sorted(self._model.services.items(), key=lambda x: x[0])
        for _, s in services_of_model:
            # variables of this microservice
            name = s.name
            instances = len(s.hosts)
            patterns = []
            capacity = 1000
            operations = []

            # get all operations of this microservice
            operations_of_microservice = sorted(s.operations.items(), key=lambda x: x[0])
            for _, o in operations_of_microservice:
                op_name = o.name
                demand = 100
                circuit_breaker = o.circuit_breaker
                dependencies = []

                # Get all dependencies of this operation
                dependencies_of_operation = sorted(o.dependencies, key=lambda x: x.name)
                for d in dependencies_of_operation:
                    service = d.service.name
                    operation = d.name
                    probability = 1.0

                    dependency = {'service': service,
                                  'operation': operation,
                                  'probability': probability}

                    # eliminate duplicate dependencies
                    if dependency not in dependencies:
                        dependencies.append(dependency)

                # if a circuit breaker is present, add the corresponding attributes
                if circuit_breaker is not None:
                    circuit_breaker_dict = {
                        "rollingWindow": circuit_breaker.rolling_window,
                        "requestVolumeThreshold": circuit_breaker.request_volume_threshold,
                        "errorThresholdPercentage": circuit_breaker.error_threshold_percentage,
                        "sleepWindow": circuit_breaker.sleep_window,
                        "timeout": circuit_breaker.timeout
                    }
                else:
                    circuit_breaker_dict = None

                operations.append({
                    'name': op_name,
                    'demand': demand,
                    'circuitBreaker': circuit_breaker_dict,
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
