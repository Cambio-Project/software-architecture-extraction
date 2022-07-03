import warnings

import numpy as np
import scipy.optimize
from scipy.optimize import OptimizeWarning


def assume_linear(xi, base, backoff):
    return base * xi + backoff


def assume_exponential(xi, base, backoff):
    return backoff * (base ** xi)


class RetrySequence:

    def __init__(self, operation_name):
        self._operation_name = operation_name
        self._sequence = []  # stores (startTimeOfCall, EndTimeOfCall, Error)
        self._strategy = None
        self._base = None
        self._baseBackoff = None

    def add_call_entry(self, entry):
        self._sequence.append(entry)

    @property
    def sequence(self):
        return self._sequence

    def estimate_parameters(self):
        warnings.simplefilter("ignore", OptimizeWarning)

        y = self.get_timings_from_sequence()
        y = [y_i / 1000000 for y_i in y]
        x = [i for i in range(0, len(y))]

        # try to estimate fit a linear and an exponential function to the data points
        result_linear, _ = scipy.optimize.curve_fit(assume_linear, x, y, p0=(0, y[0]))
        result_exponential, _ = scipy.optimize.curve_fit(assume_exponential, x, y, p0=(0, y[0]))

        # calculate the estimated values at the corresponding time steps
        estimates_exponential = np.array(
            [assume_exponential(xi, result_exponential[0], result_exponential[1]) for xi in x])
        estimates_linear = np.array([assume_linear(xi, result_linear[0], result_linear[1]) for xi in x])

        # calculate the mean squared error for both estimations
        error_exp = np.square(y - estimates_exponential)
        error_lin = np.square(y - estimates_linear)
        mse_exp = np.mean(error_exp)
        mse_lin = np.mean(error_lin)

        if mse_exp < mse_lin:
            self._strategy = "exponential"
            self._base = round(result_exponential[0], 5)
            self._baseBackoff = round(result_exponential[1], 5)
        else:
            self._strategy = "linear"
            self._base = round(result_linear[0], 1)
            self._baseBackoff = round(result_linear[1], 1)

        # print("Operation:" + self._operation_name)
        # print("Strategy: " + self._strategy)
        # print("Base: " + str(self._base))
        # print("Base backoff: " + str(self._baseBackoff))

    def get_timings_from_sequence(self):
        timings = []

        end_of_last_call = self._sequence[0][1]  # save end of first call in sequence

        # iterate over remaining entries and calculate the time between all calls
        for i in range(1, len(self._sequence)):
            current_call = self._sequence[i]
            start_of_current_call = current_call[0]

            timings.append(start_of_current_call - end_of_last_call)

            end_of_last_call = current_call[1]

        return timings


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

        for entry in self.retry_sequences:
            entry.estimate_parameters()
