class Retry:

    def __init__(self):
        self._has_retry = False
        self._call_history = {}  # maps {spanID: {timestamp: (Operation, hasError)}}

    def has_retry(self):
        return self._has_retry

    def add_call_history_entry(self, span, entry):
        if self._call_history.keys().__contains__(span):
            self._call_history[span].update(entry)
        else:
            self._call_history[span] = entry

    def detect_retry(self):
        for entry in self._call_history.values():
            error_occurred = False
            last_operation = None

            timestamps = list(entry.keys())
            timestamps.sort()

            for timestamp in timestamps:
                current_call = entry[timestamp]
                if last_operation == current_call[0] and error_occurred:
                    self._has_retry = True

                last_operation = current_call[0]
                error_occurred = current_call[1]
