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
        self._spans = set()

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
    def spans(self):
        return self._spans

    def add_latency(self, latency):
        self._latencies.append(latency)

    # returns the mean of all network latencies of this dependency in ms
    def get_latency_mean(self):
        latencies = [x / 1000 for x in self._latencies]
        return str(np.mean(latencies))

    def get_latency_mean_with_std(self):
        latencies = [x / 1000 for x in self._latencies]
        return str(np.mean(latencies)) + '+-' + str(np.std(latencies))

    def add_span(self, span):
        self._spans.add(span)

    def calculate_probability(self, parent_executions):
        # Probability of a dependency is defined as the total amount executions of the operation of this dependency
        # divided by the amount of executions of the parent.
        # Example:
        # If the parent operation is executed 2 times but this dependency only occurs once, the probability is 0.5
        self._probability = len(self._spans) / parent_executions