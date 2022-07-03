import unittest

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

    def test_timings(self):
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

