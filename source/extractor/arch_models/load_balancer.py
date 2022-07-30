class LoadBalancer:
    """
    Class that represents a load balancer for the incoming requests of a service. It stores the strategy, that can be
    set via tags in the traces.
    It also offers a method for detecting a round-robin load-balancing strategy.
    """

    def __init__(self):
        self._strategy = None  # default strategy is None
        self._instance_history = {}  # maps {timestamp: instance}
        self._allowed_error_percentage = 0.1

        # List with currently supported strategies
        self._valid_strategies = ["random", "round_robin", "round_robin_fast", "utilization"]

    @property
    def strategy(self):
        return self._strategy

    @property
    def instance_history(self):
        return self._instance_history

    def set_strategy_with_tag(self, tag: str):
        if self._valid_strategies.__contains__(tag):
            self._strategy = tag

    def add_instance_history_entry(self, timestamp, entry):
        self._instance_history[timestamp] = entry

    def set_allowed_error_percentage(self, percentage):
        self._allowed_error_percentage = percentage

    # This method tries to detect a round-robin load balancing strategy.
    # The algorithm has two states: One for detecting a possible pattern and another state for validating a pattern
    # The algorithm starts in the first state, and adds all instances to the pattern it can find until one instance
    # occurs, that is already in the pattern.
    # In this case the state is switched, and it is checked if the next instances come in the same order as the pattern
    # would suggest.
    # If a new instance occurred, that is not part of the pattern yet, the pattern gets reset and the state switches.
    # This situation can happen during autoscaling, so it does not count as an error in the pattern.
    # If the instance is in the pattern, but occurred in the wrong order, the state is reset, and the error counter
    # is increased.
    # This implementation allows for a less strict detection of a round-robin load balancing strategy, because it can
    # allow a certain amount of errors
    def detect_round_robin_pattern(self):
        timestamps = sorted(self._instance_history.keys())

        instances_in_order = []

        last_occurrence = {}

        for timestamp in timestamps:
            instances_in_order.append(self._instance_history[timestamp])

        index = 0
        for instance in instances_in_order:
            last_occurrence[instance] = index
            index += 1

        distinct_instances = set(instances_in_order)
        instance_count = len(distinct_instances)

        current_pattern_index = 0
        round_robin_pattern = []
        known_instances = []

        if not len(instances_in_order) > instance_count:
            # The amount of history entries is not large enough for an estimation
            return False

        if instance_count < 2:
            # if there are less than two instances the load balancing strategy can not be determined
            return False

        PATTERN_BUILD_UP = True
        PATTERN_VALIDATION = False

        error_count = 0

        index = 0
        for current_instance in instances_in_order:
            if PATTERN_BUILD_UP:
                # add instances to the pattern, as long as new instances occur in the history
                if not round_robin_pattern.__contains__(current_instance):
                    round_robin_pattern.append(current_instance)
                else:
                    PATTERN_BUILD_UP = False
                    PATTERN_VALIDATION = True

            if PATTERN_VALIDATION:
                # validate the current pattern
                expected_instance = round_robin_pattern[current_pattern_index % len(round_robin_pattern)]
                if expected_instance == current_instance:
                    # expected instance occurred
                    current_pattern_index += 1
                else:
                    # an unexpected instance occurred, the state gets reset to PATTERN_BUILD_UP
                    PATTERN_BUILD_UP = True
                    PATTERN_VALIDATION = False

                    if known_instances.__contains__(current_instance) and last_occurrence[expected_instance] > index:
                        # the unexpected instance is already known and the expected instance is still alive, so
                        # it appeared at the wrong place and an error has to get tracked.
                        # If this is not true, it is either the first appearance of this instance (up-scaling) or the
                        # last occurrence of the instance already happened (down-scaling). In both cases we do not want
                        # to track errors because those Situations do not violate a round-robin pattern
                        error_count += 1

                    round_robin_pattern = []
                    current_pattern_index = 0

            if not known_instances.__contains__(current_instance):
                known_instances.append(current_instance)

            index += 1

        error_percentage = error_count / len(instances_in_order)
        if error_percentage <= self._allowed_error_percentage:
            self._strategy = 'round_robin'
            return True
        else:
            return False
