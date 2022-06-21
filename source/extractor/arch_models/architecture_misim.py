import json
from extractor.arch_models.model import IModel


class ArchitectureMiSim:
    """
    Creates an architectural representation of a generic model from services, operations, and dependencies with
    the format of a MiSim model.
    """

    def __init__(self, model: IModel, network_latency, custom_latency_format):
        self._model = model
        self._network_latency = network_latency
        self._custom_latency_format = custom_latency_format

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
            capacity = s.capacity
            operations = []

            operation_has_CB = False

            # get all operations of this microservice
            operations_of_microservice = sorted(s.operations.items(), key=lambda x: x[0])
            for _, o in operations_of_microservice:
                op_name = o.name
                demand = o.demand
                circuit_breaker = o.circuit_breaker
                dependencies = []

                # Get all dependencies of this operation
                dependencies_of_operation = sorted(o.dependencies, key=lambda x: x.name)
                for d in dependencies_of_operation:
                    service = d.service.name
                    operation = d.name
                    probability = d.probability

                    dependency = {'service': service,
                                  'operation': operation,
                                  'probability': probability}

                    # add a custom latency if the model contains latencies for this dependency
                    if len(d.latencies) > 0:
                        if self._custom_latency_format == 'm':
                            custom_latency = d.get_latency_mean()
                            dependency['custom_delay'] = custom_latency
                        elif self._custom_latency_format == 'mstd':
                            custom_latency = d.get_latency_mean_with_std()
                            dependency['custom_delay'] = custom_latency

                    dependencies.append(dependency)

                # if a circuit breaker is present, set the flag to add the CB later into the patterns array
                if circuit_breaker is not None:
                    operation_has_CB = True

                operations.append({
                    'name': op_name,
                    'demand': demand,
                    'dependencies': dependencies
                })

                # If at least one Operation implements a circuit breaker, add a default CB to the patterns array
                if operation_has_CB:
                    circuit_breaker_dict = {
                        "type": "circuitbreaker",
                        "config": {
                            "requestVolumeThreshold": circuit_breaker.request_volume_threshold,
                            "threshold": circuit_breaker.threshold,
                            "rollingWindow": circuit_breaker.rolling_window,
                            "sleepWindow": circuit_breaker.sleep_window,
                        }
                    }
                    patterns.append(circuit_breaker_dict)

            microservices.append({
                'name': name,
                'instances': instances,
                'patterns': patterns,
                'capacity': capacity,
                'operations': operations
            })
        result = {}
        if self._network_latency != "":
            result['network_latency'] = self._network_latency
        result['microservices'] = microservices
        return json.dumps(result, indent=2)
