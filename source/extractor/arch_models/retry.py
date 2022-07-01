class RetrySequence:

    def __init__(self, operation_name):
        self._operation_name = operation_name
        self._sequence = []  # stores (startTimeOfCall, EndTimeOfCall, Error)

    def add_call_entry(self, entry):
        self._sequence.append(entry)

    @property
    def sequence(self):
        return self._sequence


class Retry:

    def __init__(self):
        self._call_history = {}  # maps {spanID: {timestamp: (Operation, hasError, startTime, endTime)}}
        self._retry_sequences = []

    @property
    def retry_sequences(self) -> list[RetrySequence]:
        return self._retry_sequences

    def has_retry(self):
        return len(self._retry_sequences) > 0

    def add_call_history_entry(self, span, entry):
        if self._call_history.keys().__contains__(span):
            self._call_history[span].update(entry)
        else:
            self._call_history[span] = entry

    def detect_retry(self):
        for entry in self._call_history.values():
            last_call = (None, None, None)

            timestamps = list(entry.keys())
            timestamps.sort()

            retry_sequence = None

            for timestamp in timestamps:
                current_call = entry[timestamp]

                # If last call was same operation as current call and last call had an error continue or start a new
                # retry sequence
                if (last_call[0] == current_call[0]) and last_call[1]:

                    # If there is no retry sequence yet, start a new one and add the last call to it.
                    if retry_sequence is None:
                        retry_sequence = RetrySequence(current_call[0])
                        retry_sequence.add_call_entry((last_call[2], last_call[3], last_call[1]))
                        self._retry_sequences.append(retry_sequence)

                    # add the current call the current retry sequence
                    retry_sequence.add_call_entry((current_call[2], current_call[3], current_call[1]))

                # End-conditions for a retry sequence: Current call was successful (hasError is False) or the Service
                # is continuing with calling another operation.
                if not current_call[1] or (last_call[0] != current_call[0]):
                    retry_sequence = None

                last_call = current_call

        pass
