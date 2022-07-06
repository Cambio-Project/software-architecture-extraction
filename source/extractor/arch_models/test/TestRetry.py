import unittest

from extractor.arch_models import architecture_misim
from extractor.arch_models.retry import Retry, RetrySequence


class TestRetry(unittest.TestCase):
    def test_retry1(self):
        retry = Retry()
        # Two operation calls on "a": first error second try no error
        retry.add_call_history_entry(1, {1: ("a", "400", 0.1, 0.2), 2: ("a", False, 0.4, 0.5)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)
        self.assertEqual(1, len(retry.retry_sequences))
        self.assertListEqual(retry.retry_sequences[0].sequence, [(0.1, 0.2, "400"), (0.4, 0.5, False)])

    def test_retry2(self):
        retry = Retry()
        # Two operation calls on "a": first error second try no error, but order of timestamps is mixed up
        retry.add_call_history_entry(1, {2: ("a", False, 0.4, 0.5), 1: ("a", "400", 0.1, 0.2)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)
        self.assertEqual(1, len(retry.retry_sequences))
        self.assertListEqual(retry.retry_sequences[0].sequence, [(0.1, 0.2, "400"), (0.4, 0.5, False)])

    def test_retry3(self):
        retry = Retry()
        # Two operation calls on "a": first error second try no error, but first one successful call on "b"
        retry.add_call_history_entry(1,
                                     {2: ("a", "400", 0.4, 0.5), 3: ("a", False, 0.7, 0.9), 1: ("b", False, 0.1, 0.2)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)
        self.assertEqual(1, len(retry.retry_sequences))
        self.assertListEqual(retry.retry_sequences[0].sequence, [(0.4, 0.5, "400"), (0.7, 0.9, False)])

    def test_retry4(self):
        retry = Retry()
        # First span: Successful calls on "a" and "b"
        # Second span: Two operation calls on "a": first error second try no error, but first one successful call on "b"
        retry.add_call_history_entry(2, {2: ("a", False, 0.7, 0.9), 1: ("b", False, 0.1, 0.2)})
        retry.add_call_history_entry(1,
                                     {2: ("a", "400", 0.4, 0.5), 3: ("a", False, 0.7, 0.95), 1: ("b", False, 0.1, 0.2)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)
        self.assertEqual(1, len(retry.retry_sequences))
        self.assertListEqual(retry.retry_sequences[0].sequence, [(0.4, 0.5, "400"), (0.7, 0.95, False)])

    def test_retry5(self):
        retry = Retry()
        # Two operation calls on "a": first error second try also error
        retry.add_call_history_entry(1, {1: ("a", "400", 0.1, 0.2), 3: ("a", "400", 0.4, 0.5)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)
        self.assertEqual(1, len(retry.retry_sequences))
        self.assertListEqual(retry.retry_sequences[0].sequence, [(0.1, 0.2, "400"), (0.4, 0.5, "400")])

    def test_retry6(self):
        retry = Retry()
        # Two operation calls on "a": first error second try also error, after that call on "b"
        retry.add_call_history_entry(1,
                                     {4: ("b", False, 0.7, 0.9), 1: ("a", "400", 0.1, 0.2), 3: ("a", "400", 0.4, 0.5)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)
        self.assertEqual(1, len(retry.retry_sequences))
        self.assertListEqual(retry.retry_sequences[0].sequence, [(0.1, 0.2, "400"), (0.4, 0.5, "400")])

    def test_retry7(self):
        retry = Retry()
        # Three operation calls on "a": first error second try also error third time success, after that call on "b"
        retry.add_call_history_entry(1,
                                     {4: ("b", False, 0.7, 0.9), 1: ("a", "400", 0.1, 0.2), 3: ("a", False, 0.55, 0.6),
                                      2: ("a", True, 0.4, 0.5)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)
        self.assertEqual(1, len(retry.retry_sequences))
        self.assertListEqual(retry.retry_sequences[0].sequence,
                             [(0.1, 0.2, "400"), (0.4, 0.5, True), (0.55, 0.6, False)])

    def test_retry8(self):
        retry = Retry()
        # Two operation calls on "a": first error second try also error, after that same situation with  "b"
        retry.add_call_history_entry(1, {4: ("b", True, 0.7, 0.9), 1: ("a", "400", 0.1, 0.2), 3: ("a", "400", 0.4, 0.5),
                                         5: ("b", True, 1.1, 1.2)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)
        self.assertEqual(2, len(retry.retry_sequences))
        self.assertListEqual(retry.retry_sequences[0].sequence, [(0.1, 0.2, "400"), (0.4, 0.5, "400")])
        self.assertListEqual(retry.retry_sequences[1].sequence, [(0.7, 0.9, True), (1.1, 1.2, True)])

    def test_retry9(self):
        retry = Retry()
        # Two operation calls on "a": first error second try also error
        # Second span: Two operation calls on "a": first error second try no error, but first one successful call on "b"
        retry.add_call_history_entry(2, {2: ("a", "400", 0.1, 0.2), 3: ("a", "400", 0.4, 0.5)})
        retry.add_call_history_entry(1,
                                     {2: ("a", "400", 0.4, 0.5), 3: ("a", False, 0.7, 0.95), 1: ("b", False, 0.1, 0.2)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)
        self.assertEqual(2, len(retry.retry_sequences))
        self.assertListEqual(retry.retry_sequences[0].sequence, [(0.1, 0.2, "400"), (0.4, 0.5, "400")])
        self.assertListEqual(retry.retry_sequences[1].sequence, [(0.4, 0.5, "400"), (0.7, 0.95, False)])

    def test_no_retry1(self):
        retry = Retry()
        # One operation call on "a": first error and no retry
        retry.add_call_history_entry(1, {1: ("a", "400", 0.1, 0.2)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)
        self.assertListEqual(retry.retry_sequences, [])

    def test_no_retry2(self):
        retry = Retry()
        # One operation call on "a": first error and second call on different operation
        retry.add_call_history_entry(1, {1: ("a", "400", 0.1, 0.2), 2: ("b", False, 0.4, 0.5)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)
        self.assertListEqual(retry.retry_sequences, [])

    def test_no_retry3(self):
        retry = Retry()
        # One operation call on "a": first error and second call on different operation,
        # but order of timestamps is mixed up
        retry.add_call_history_entry(1, {2: ("b", False, 0.4, 0.5), 1: ("a", "400", 0.1, 0.2)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)
        self.assertListEqual(retry.retry_sequences, [])

    def test_no_retry4(self):
        retry = Retry()
        # Two operation calls on "a": first error second try no error, but between the two calls on call on "b"
        retry.add_call_history_entry(1,
                                     {1: ("a", "400", 0.1, 0.2), 3: ("a", False, 0.7, 0.9), 2: ("b", False, 0.4, 0.5)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)
        self.assertListEqual(retry.retry_sequences, [])

    def test_no_retry5(self):
        retry = Retry()
        # Two operation calls on "a": first error second try also error, between them call on "b"
        retry.add_call_history_entry(1,
                                     {2: ("b", False, 0.4, 0.5), 1: ("a", "400", 0.1, 0.2), 3: ("a", "400", 0.7, 0.9)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)
        self.assertListEqual(retry.retry_sequences, [])

    def test_timings1(self):
        sequence = RetrySequence("name")
        sequence.add_call_entry((1656349746228000, 1656349746343243, True))
        sequence.add_call_entry((1656349751353000, 1656349751359823, True))
        sequence.add_call_entry((1656349756361000, 1656349756365687, False))
        sequence.estimate_parameters()
        print(sequence.get_timings_from_sequence())
        print("Strategy: " + str(sequence._strategy))
        print("Base: " + str(sequence._base))
        print("Base backoff: " + str(sequence._baseBackoff))
        print("Max Backoff: " + str(sequence._maxBackoff))
        print("Error: " + str(sequence._error))

    def test_result_merging1(self):
        # Two similar, non-conflicting sequences
        sequence1 = RetrySequence("1")
        sequence1._strategy = "exponential"
        sequence1._maxTries = 5
        sequence1._base = 2
        sequence1._baseBackoff = 1
        sequence1._maxBackoff = 4
        sequence1._error = 0.1

        sequence2 = RetrySequence("1")
        sequence2._strategy = "exponential"
        sequence2._maxTries = 5
        sequence2._base = 2.2
        sequence2._baseBackoff = 1.2
        sequence2._maxBackoff = 4.2
        sequence2._error = 0.3

        retry = Retry()
        retry._retry_sequences.append(sequence1)
        retry._retry_sequences.append(sequence2)
        retry.set_results()

        # expected results are the averaged values of both sequences
        self.assertEqual("exponential", retry.strategy)
        self.assertEqual(5, retry.maxTries)
        self.assertEqual(2.1, retry.base)
        self.assertEqual(1.1, retry.baseBackoff)
        self.assertEqual(4.1, retry.maxBackoff)
        self.assertEqual(0.2, retry.error)

    def test_result_merging2(self):
        # Two different, conflicting sequences.
        sequence1 = RetrySequence("1")
        sequence1._strategy = "exponential"
        sequence1._maxTries = 5
        sequence1._base = 2
        sequence1._baseBackoff = 1
        sequence1._maxBackoff = 4
        sequence1._error = 0.1

        sequence2 = RetrySequence("1")
        sequence2._strategy = "linear"
        sequence2._maxTries = 3
        sequence2._base = 7
        sequence2._baseBackoff = 2
        sequence2._maxBackoff = 4
        sequence2._error = 0.4

        retry = Retry()
        retry._retry_sequences.append(sequence1)
        retry._retry_sequences.append(sequence2)
        retry.set_results()

        # expected results are the values of the sequence with lower error
        self.assertEqual("exponential", retry.strategy)
        self.assertEqual(5, retry.maxTries)
        self.assertEqual(2, retry.base)
        self.assertEqual(1, retry.baseBackoff)
        self.assertEqual(4, retry.maxBackoff)
        self.assertEqual(0.1, retry.error)

    def test_result_merging3(self):
        # only one sequence
        sequence1 = RetrySequence("1")
        sequence1._strategy = "exponential"
        sequence1._maxTries = 5
        sequence1._base = 2
        sequence1._baseBackoff = 1
        sequence1._maxBackoff = 4
        sequence1._error = 0.1

        retry = Retry()
        retry._retry_sequences.append(sequence1)
        retry.set_results()

        # expected results are the values of sequence1
        self.assertEqual("exponential", retry.strategy)
        self.assertEqual(5, retry.maxTries)
        self.assertEqual(2, retry.base)
        self.assertEqual(1, retry.baseBackoff)
        self.assertEqual(4, retry.maxBackoff)
        self.assertEqual(0.1, retry.error)

    def test_result_merging4(self):
        # Two similar, non-conflicting sequences with different amounts of estimated parameters
        sequence1 = RetrySequence("1")
        sequence1._strategy = "exponential"
        sequence1._maxTries = 5
        sequence1._base = 2
        sequence1._baseBackoff = 1
        sequence1._maxBackoff = 4
        sequence1._error = 0.1

        sequence2 = RetrySequence("1")
        sequence2._strategy = "exponential"
        sequence2._maxTries = None
        sequence2._base = 2.2
        sequence2._baseBackoff = 1.2
        sequence2._maxBackoff = None
        sequence2._error = 0.3

        retry = Retry()
        retry._retry_sequences.append(sequence1)
        retry._retry_sequences.append(sequence2)
        retry.set_results()

        # expected results are the averaged values of both sequences and the values of sequence1 where sequence2 has
        # no estimation
        self.assertEqual("exponential", retry.strategy)
        self.assertEqual(5, retry.maxTries)
        self.assertEqual(2.1, retry.base)
        self.assertEqual(1.1, retry.baseBackoff)
        self.assertEqual(4, retry.maxBackoff)
        self.assertEqual(0.2, retry.error)

    def test_result_merging5(self):
        # Two similar, non-conflicting sequences with different amounts of estimated parameters and one sequence with
        # a different strategy and a hight error
        sequence1 = RetrySequence("1")
        sequence1._strategy = "exponential"
        sequence1._maxTries = 5
        sequence1._base = 2
        sequence1._baseBackoff = 1
        sequence1._maxBackoff = 4
        sequence1._error = 0.1

        sequence2 = RetrySequence("1")
        sequence2._strategy = "exponential"
        sequence2._maxTries = None
        sequence2._base = 2.2
        sequence2._baseBackoff = 1.2
        sequence2._maxBackoff = None
        sequence2._error = 0.3

        sequence3 = RetrySequence("2")
        sequence3._strategy = "linear"
        sequence3._maxTries = 6
        sequence3._base = 5
        sequence3._baseBackoff = 7
        sequence3._maxBackoff = 10
        sequence3._error = 0.8

        retry = Retry()
        retry._retry_sequences.append(sequence1)
        retry._retry_sequences.append(sequence2)
        retry._retry_sequences.append(sequence3)
        retry.set_results()

        # expected results are the averaged values of both sequences and the values of sequence1 where sequence2 has
        # no estimation. The values of the third sequence should be ignored
        self.assertEqual("exponential", retry.strategy)
        self.assertEqual(5, retry.maxTries)
        self.assertEqual(2.1, retry.base)
        self.assertEqual(1.1, retry.baseBackoff)
        self.assertEqual(4, retry.maxBackoff)
        self.assertEqual(0.2, retry.error)

    def test_retry_description1(self):
        # one retry, description is expected to contain the same values
        retry1 = Retry()
        retry1._strategy = "exponential"
        retry1._maxTries = 5
        retry1._base = 2
        retry1._baseBackoff = 1
        retry1._maxBackoff = 4
        retry1._error = 0.1

        self.assertEqual(
            {'type': 'retry', 'config': {'maxTries': 5},
             'strategy': {'type': 'exponential', 'config': {'baseBackoff': 1, 'maxBackoff': 4, 'base': 2}}}
            , architecture_misim.build_retry_description([retry1]))

    def test_retry_description2(self):
        # 3 retries, description is expected to contain values of the retry with the lower error
        retry1 = Retry()
        retry1._strategy = "exponential"
        retry1._maxTries = 5
        retry1._base = 2
        retry1._baseBackoff = 1
        retry1._maxBackoff = 4
        retry1._error = 0.1

        retry2 = Retry()
        retry2._strategy = "exponential"
        retry2._maxTries = 8
        retry2._base = 4
        retry2._baseBackoff = 2
        retry2._maxBackoff = 7
        retry2._error = 0.5

        retry3 = Retry()
        retry3._strategy = "linear"
        retry3._maxTries = 2
        retry3._base = 1
        retry3._baseBackoff = 3
        retry3._maxBackoff = 6
        retry3._error = 0.6

        self.assertEqual(
            {'type': 'retry', 'config': {'maxTries': 5},
             'strategy': {'type': 'exponential', 'config': {'baseBackoff': 1, 'maxBackoff': 4, 'base': 2}}}
            , architecture_misim.build_retry_description([retry1, retry2, retry3]))
