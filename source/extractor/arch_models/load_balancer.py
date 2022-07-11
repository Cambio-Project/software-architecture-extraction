class LoadBalancer:

    def __init__(self):
        self._strategy = "random"  # default strategy is random

        # List with currently supported strategies
        self._valid_strategies = ["random", "round_robin", "round_robin_fast", "utilization"]

    def set_strategy_with_tag(self, tag: str):
        if self._valid_strategies.__contains__(tag):
            self._strategy = tag

    @property
    def strategy(self):
        return self._strategy
