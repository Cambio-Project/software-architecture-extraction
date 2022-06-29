import unittest

from extractor.arch_models.retry import Retry


class TestRetry(unittest.TestCase):
    def test_retry1(self):
        retry = Retry()
        # Two operation calls on "a": first error second try no error
        retry.add_call_history_entry(1, {1: ("a", "400"), 2: ("a", False)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)

    def test_retry2(self):
        retry = Retry()
        # Two operation calls on "a": first error second try no error, but order of timestamps is mixed up
        retry.add_call_history_entry(1, {2: ("a", False), 1: ("a", "400")})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)

    def test_retry3(self):
        retry = Retry()
        # Two operation calls on "a": first error second try no error, but first one successful call on "b"
        retry.add_call_history_entry(1, {2: ("a", "400"), 3: ("a", False), 1: ("b", False)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)

    def test_retry4(self):
        retry = Retry()
        # First span: Successful calls on "a" and "b"
        # Second span: Two operation calls on "a": first error second try no error, but first one successful call on "b"
        retry.add_call_history_entry(1, {2: ("a", False), 1: ("b", False)})
        retry.add_call_history_entry(1, {2: ("a", "400"), 3: ("a", False), 1: ("b", False)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)

    def test_retry5(self):
        retry = Retry()
        # Two operation calls on "a": first error second try also error
        retry.add_call_history_entry(1, {1: ("a", "400"), 3: ("a", "400")})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)

    def test_retry6(self):
        retry = Retry()
        # Two operation calls on "a": first error second try also error, after that call on "b"
        retry.add_call_history_entry(1, {4: ("b", False), 1: ("a", "400"), 3: ("a", "400")})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)

    def test_retry7(self):
        retry = Retry()
        # Three operation calls on "a": first error second try also error third time success, after that call on "b"
        retry.add_call_history_entry(1, {4: ("b", False), 1: ("a", "400"), 3: ("a", True), 2: ("a", False)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), True)

    def test_no_retry1(self):
        retry = Retry()
        # One operation call on "a": first error and no retry
        retry.add_call_history_entry(1, {1: ("a", "400")})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)

    def test_no_retry2(self):
        retry = Retry()
        # One operation call on "a": first error and second call on different operation
        retry.add_call_history_entry(1, {1: ("a", "400"), 2: ("b", False)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)

    def test_no_retry3(self):
        retry = Retry()
        # One operation call on "a": first error and second call on different operation,
        # but order of timestamps is mixed up
        retry.add_call_history_entry(1, {2: ("b", False), 1: ("a", "400")})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)

    def test_no_retry4(self):
        retry = Retry()
        # Two operation calls on "a": first error second try no error, but between the two calls on call on "b"
        retry.add_call_history_entry(1, {1: ("a", "400"), 3: ("a", False), 2: ("b", False)})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)

    def test_no_retry5(self):
        retry = Retry()
        # Two operation calls on "a": first error second try also error, between them call on "b"
        retry.add_call_history_entry(1, {2: ("b", False), 1: ("a", "400"), 3: ("a", "400")})

        retry.detect_retry()
        self.assertEqual(retry.has_retry(), False)
