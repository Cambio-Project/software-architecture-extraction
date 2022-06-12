class Dependency:
    """
    Class that represents a dependency of a specific Operation
    """

    def __init__(self, operation):
        self._operation = operation
        self._service = operation.service
        self._name = operation.name
        self._probability = 1.0
        self._latencies = []

    @property
    def operation(self):
        return self._operation

    @property
    def service(self):
        return self._service

    @property
    def name(self):
        return self._name

    @property
    def probability(self):
        return self._probability

    @property
    def latencies(self):
        return self._latencies

    def add_latency(self, latency):
        self._latencies.append(latency)
