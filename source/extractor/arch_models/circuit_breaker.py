class CircuitBreaker:
    """
    Class that represents a circuit breaker with default values
    """

    def __init__(self):
        # set all attributes to default values
        self.rolling_window = 10
        self.request_volume_threshold = 20
        self.error_threshold_percentage = 0.5
        self.threshold = 0.5
        self.timeout = 1
        self.sleep_window = 5
