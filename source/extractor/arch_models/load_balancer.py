class LoadBalancer:
    """
    Class that represents a load balancer for the incoming requests of a service. It stores the strategy, that can be
    set via tags in the traces.
    It also offers a method for detecting a round-robin load-balancing strategy.
    """

    def __init__(self):
        self._strategy = None  # default strategy is None
        self._instance_history = {}  # maps {timestamp: instance}

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

    # This method tries to detect a round-robin load balancing strategy. In a first stage it analyzes the beginning
    # of the sequence. If the beginning could be a round-robin pattern, it is checked if the remaining part of the
    # sequence matches this pattern. If yes, the load-balancing strategy is set to 'round_robin'.
    def detect_round_robin_pattern(self):
        timestamps = sorted(self._instance_history.keys())

        instances_in_order = []

        for timestamp in timestamps:
            instances_in_order.append(self._instance_history[timestamp])

        distinct_instances = set(instances_in_order)
        instance_count = len(distinct_instances)

        counter = 0
        current_pattern_index = 0
        round_robin_pattern = []

        if not len(instances_in_order) > instance_count:
            # The amount of history entries is not large enough for an estimation
            return False

        if instance_count < 2:
            # if there are less than two instances the load balancing strategy can not be determined
            return False

        for current_instance in instances_in_order:
            if counter < instance_count:
                # if counter < instance_count, the algorithm is still detecting the possible round-robin pattern
                if not round_robin_pattern.__contains__(current_instance):
                    round_robin_pattern.append(current_instance)
                else:
                    # Not all instances have occurred yet in the history, but one instance occurred already
                    # twice, this can not be a round-robin load balancing strategy
                    return False
                counter += 1
            else:
                # Every instance occurred exactly once now, in the second step we check if the current instance
                # matches the expected instance when a round-robin load balancing strategy is assumed.
                if not round_robin_pattern[current_pattern_index % instance_count] == current_instance:
                    return False
                current_pattern_index += 1

        self._strategy = 'round_robin'
        return True
