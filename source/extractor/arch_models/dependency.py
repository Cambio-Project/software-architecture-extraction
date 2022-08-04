import numpy as np


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
        self._calling_spans = []
        self._calls = 0

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

    @property
    def calling_spans(self):
        return self._calling_spans

    def add_latency(self, latency):
        self._latencies.append(latency)

    # returns the mean of all network latencies of this dependency in ms
    def get_latency_mean(self):
        latencies = [x / 1000000 for x in self._latencies]
        return str(np.mean(latencies))

    def get_latency_mean_with_std(self):
        latencies = [x / 1000000 for x in self._latencies]
        return str(np.mean(latencies)) + '+-' + str(np.std(latencies))

    def add_calling_span(self, span):
        self._calling_spans.append(span)

    def add_call(self):
        self._calls = self._calls + 1

    def calculate_probability(self, parent_executions):
        # Probability of a dependency is defined as the total amount executions of the operation of this dependency
        # divided by the amount of executions of the parent.
        # Example:
        # If the parent operation is executed 2 times but this dependency only occurs once, the probability is 0.5
        self._probability = min(1.0, self._calls / parent_executions)

    def set_probability(self, probability):
        self._probability = probability
