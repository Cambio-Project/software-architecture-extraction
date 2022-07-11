import sys
import warnings
from copy import copy
import numpy as np
import scipy.optimize
from scipy.optimize import OptimizeWarning

# Threshold that is used to detect if the retry sequence has reached the maximum backoff value
MAX_BACKOFF_DETECTION_THRESHOLD = 0.01


# Function for estimating the backoff strategy based on a linear function
def assume_linear(xi, base, baseBackoff):
    return base * xi + baseBackoff


# Function for estimating the backoff strategy based on an exponential function
def assume_exponential(xi, base, baseBackoff):
    return baseBackoff * (base ** xi)


# This method calculated the difference between two consecutive time intervals. If the difference is lower than the
# MAX_BACKOFF_DETECTION_THRESHOLD, the index where the thresholding begins is returned.
def detect_max_backoff_index(timings):
    last_interval = None
    current_interval_index = 0
    for interval in timings:
        if last_interval is not None:
            if (interval - last_interval) < MAX_BACKOFF_DETECTION_THRESHOLD:
                # if the difference between the two intervals is very small, we have reached the threshold
                return current_interval_index - 1
        last_interval = interval
        current_interval_index += 1
    return None


class RetrySequence:
    """
    This class represents a Retry Sequence: Such a sequence consists of all (times of) calls made during retrying a
    failing Operation
    The class offers methods that can be used to estimate the parameters of the function used for the timings of the
    retry.
    """

    def __init__(self, operation_name):
        self._sequence = []  # stores (startTimeOfCall, EndTimeOfCall, Error)
        self._operation_name = operation_name
        self._strategy = None
        self._maxTries = None
        self._base = None
        self._baseBackoff = None
        self._maxBackoff = None
        self._error = None

    @property
    def error(self):
        return self._error

    @property
    def sequence(self):
        return self._sequence

    @property
    def strategy(self):
        return self._strategy

    @property
    def maxTries(self):
        return self._maxTries

    @property
    def base(self):
        return self._base

    @property
    def baseBackoff(self):
        return self._baseBackoff

    @property
    def maxBackoff(self):
        return self._maxBackoff

    def add_call_entry(self, entry):
        self._sequence.append(entry)

    # Tries to estimate all parameters of the function that was used to for the time intervals between the retries
    def estimate_parameters(self):
        warnings.simplefilter("ignore", OptimizeWarning)

        y = self.get_timings_from_sequence()
        y = [y_i / 1000000 for y_i in y]
        old_y = copy(y)

        # Check if we have reached the maximum backoff during the retry sequence:
        maxBackoff_index = detect_max_backoff_index(y)

        if maxBackoff_index is not None:
            # If we have reached the maximum backoff, all data points after the threshold is reached get eliminated
            # in order to get a better estimation for the parameters later.
            maxBackoff_values = y[maxBackoff_index:len(y)]
            self._maxBackoff = np.mean(maxBackoff_values)

            y = y[0:maxBackoff_index]

        # handle edge cases
        if len(y) < 2:
            if len(y) == 0:
                if self._maxBackoff is not None:
                    # The backoff Strategy is constant
                    self._strategy = "linear"
                    self._base = 0
                    self._baseBackoff = self._maxBackoff

                    error_lin = np.square(old_y - self._maxBackoff)
                    mse_lin = np.mean(error_lin)
                    self._error = mse_lin
                    return
                else:
                    return
            elif len(y) == 1:
                if self._maxBackoff is None:
                    # Only one data point available, assuming a constant backoff strategy
                    self._strategy = "linear"
                    self._base = 0
                    self._baseBackoff = y[0]
                    self._error = sys.maxsize  # maximum uncertainty
                    return
                else:
                    # One data point and a max backoff available, continue with estimation with those two points.
                    # This will, however lead to an uncertain result
                    y.append(self._maxBackoff)

        x = [i for i in range(0, len(y))]

        # try to fit a linear and an exponential function to the data points
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

        # Use the estimation that has the smaller error
        if mse_exp < mse_lin:
            self._strategy = "exponential"
            self._base = result_exponential[0]
            self._baseBackoff = result_exponential[1]
            self._error = mse_exp
        else:
            self._strategy = "linear"
            self._base = result_linear[0]
            self._baseBackoff = result_linear[1]
            self._error = mse_lin

        if self._sequence[len(self._sequence) - 1][2]:
            # if the sequence ends with an error, the maximum amount of retry attempts has been reached
            self._maxTries = len(self._sequence) - 1

    # extracts the time intervals between all calls from a sequence of calls with start and end time
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
    """
    Class that represents the retry pattern of an operation in the generic model. It stores all retry sequences that
    have been detected int the traces with the corresponding estimated function parameters
    """

    def __init__(self):
        self._call_history = {}  # maps {spanID: {timestamp: (Operation, hasError, startTime, endTime)}}
        self._retry_sequences = []
        self._strategy = None
        self._maxTries = None
        self._base = None
        self._baseBackoff = None
        self._maxBackoff = None
        self._error = None

    @property
    def strategy(self):
        return self._strategy

    @property
    def maxTries(self):
        return self._maxTries

    @property
    def base(self):
        return self._base

    @property
    def baseBackoff(self):
        return self._baseBackoff

    @property
    def maxBackoff(self):
        return self._maxBackoff

    @property
    def error(self):
        return self._error

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

    # This Method tries to detect a retry. If it finds one, the whole Retry Sequence is extracted.
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

        for sequence in self.retry_sequences:
            sequence.estimate_parameters()

        if self.has_retry():
            self.set_results()

    # If there are multiple retry sequences, the results get merged. In case of conflicting strategies, the strategy
    # with the lowest error from the estimation is taken and all the values of the all sequences that follow the same
    # strategy are averaged.
    # It is assumed that the calling operation uses the same Retry configuration for all operations that it calls.
    def set_results(self):
        if len(self._retry_sequences) > 1:
            maxTryValues = []
            baseValues = []
            baseBackoffValues = []
            maxBackoffValues = []
            errors = []

            bestStrategy = None
            currentError = None
            # search for strategy with the lowest error
            for sequence in self.retry_sequences:
                if (currentError is None) or sequence.error < currentError:
                    bestStrategy = sequence.strategy
                    currentError = sequence.error

            for sequence in self.retry_sequences:
                if sequence.strategy == bestStrategy:
                    if sequence.maxTries is not None:
                        maxTryValues.append(sequence.maxTries)
                    if sequence.base is not None:
                        baseValues.append(sequence.base)
                    if sequence.baseBackoff is not None:
                        baseBackoffValues.append(sequence.baseBackoff)
                    if sequence.maxBackoff is not None:
                        maxBackoffValues.append(sequence.maxBackoff)
                    if sequence.error is not None:
                        errors.append(sequence.error)

            self._strategy = bestStrategy
            if len(maxTryValues) > 0:
                self._maxTries = max(maxTryValues)
            if len(baseValues) > 0:
                self._base = np.mean(baseValues)
            if len(baseBackoffValues) > 0:
                self._baseBackoff = np.mean(baseBackoffValues)
            if len(maxBackoffValues) > 0:
                self._maxBackoff = np.mean(maxBackoffValues)
            if len(errors) > 0:
                self._error = np.mean(errors)
        else:
            sequence = self._retry_sequences[0]
            self._strategy = sequence.strategy
            self._maxTries = sequence.maxTries
            self._base = sequence.base
            self._baseBackoff = sequence.baseBackoff
            self._maxBackoff = sequence.maxBackoff
            self._error = sequence.error
