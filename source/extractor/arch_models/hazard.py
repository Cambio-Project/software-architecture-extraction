from typing import Union

from ..arch_models.operation import Operation
from ..arch_models.service import Service


class Keyword:
    NO = 'no'
    NOT = 'not'
    LESS = 'less than'
    MORE = 'more than'
    OTHER = 'other than'
    DIFFER = 'differ by'


class Metric:
    AVAILABILITY = 'availability'
    RESPONSE_TIME = 'response time'
    THROUGHPUT = 'throughput'


class Consequence:
    MINOR = 1, 'minor'
    SERIOUS = 2, 'serious'
    CRITICAL = 3, 'critical'


class Likelihood:
    UNLIKELY = 1, 'unlikely'
    POSSIBLE = 2, 'possible'
    PROBABLE = 3, 'probable'


class Property:
    SERVICE = 'service'
    OPERATION = 'operation'


class Hazard:
    ID = 0

    def __init__(self, prop: Union[Service, Operation]):
        self._id = Hazard.get_id()
        self._type = ''
        self._property = prop
        self._property_type = Property.SERVICE
        self._keyword = Keyword.NO
        self._metric = Metric.AVAILABILITY
        self._value = 0
        self._consequence = Consequence.MINOR
        self._likelihood = Likelihood.UNLIKELY
        self._severity = self._consequence[0] * self._likelihood[0]

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def get_id() -> int:
        _id = Hazard.ID
        Hazard.ID += 1
        return _id

    @property
    def id(self) -> int:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    @property
    def prop(self) -> Union[Operation, Service]:
        return self._property

    @property
    def prop_type(self) -> str:
        return self._property_type

    @property
    def prop_name(self) -> str:
        return self._property.name

    @property
    def keyword(self) -> str:
        return self._keyword

    @property
    def metric(self) -> str:
        return self._metric

    @property
    def value(self) -> float:
        return self._value

    @property
    def consequence(self) -> tuple:
        return self._consequence

    @property
    def likelihood(self) -> tuple:
        return self._likelihood

    @property
    def severity(self) -> int:
        return self._severity

    @property
    def nodes(self) -> list:
        return [self.prop.id] if isinstance(self, ServiceHazard) else []

    @property
    def edges(self) -> list:
        return [self.prop.id] if isinstance(self, OperationHazard) else []


class ServiceHazard(Hazard):
    def __init__(self, service: Service):
        super().__init__(service)

        self._property_type = Property.SERVICE


class ServiceFailure(ServiceHazard):
    def __init__(self, service: Service):
        super().__init__(service)

        self._type = 'Service Failure'
        self._metric = Metric.THROUGHPUT
        self._keyword = Keyword.NO


class DecreasedServicePerformance(ServiceHazard):
    def __init__(self, service: Service):
        super().__init__(service)

        self._type = 'Decreased Service Performance'
        self._metric = Metric.THROUGHPUT
        self._keyword = Keyword.LESS


class OperationHazard(Hazard):
    def __init__(self, operation: Operation):
        super().__init__(operation)

        self._property_type = Property.OPERATION


class ResponseTimeDeviation(OperationHazard):
    DEVIATION_INTERVAL = 0.5

    def __init__(self, operation: Operation, value: float):
        super().__init__(operation)

        self._type = 'Response Time Deviation'
        self._metric = Metric.RESPONSE_TIME
        self._keyword = Keyword.DIFFER
        self._value = value


class ResponseTimeSpike(OperationHazard):
    DEVIATION_FACTOR = 3

    def __init__(self, operation: Operation, value: float):
        super().__init__(operation)

        self._type = 'Response Time Spike'
        self._metric = Metric.RESPONSE_TIME
        self._keyword = Keyword.MORE
        self._value = value
