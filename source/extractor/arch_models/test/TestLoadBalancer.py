import unittest

from extractor.arch_models.load_balancer import LoadBalancer


class MyTestCase(unittest.TestCase):
    def test_round_robin_detection1(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "a", 5: "b", 6: "c"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection2(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {4: "a", 5: "b", 6: "c", 1: "a", 2: "b", 3: "c"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection3(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {4: "a", 5: "b", 6: "c", 1: "a", 2: "b", 3: "c", 7: "a", 8: "b"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection4(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "a", 5: "b", 6: "c", 7: "a", 8: "b", 9: "c",
                                           10: "a", 11: "b", 12: "c"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection5(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "a", 5: "b", 6: "c", 7: "a", 8: "b", 9: "c",
                                           10: "a", 11: "b", 12: "c", 13: "a"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection6(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "a"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection7(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "d", 2: "b", 3: "c", 4: "d", 5: "b", 6: "c"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection8(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "a", 9: "b",
                                           10: "c", 11: "d", 12: "e", 13: "f"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection9(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "a", 5: "b", 6: "c", 7: "a", 8: "b", 9: "c",
                                           10: "a", 11: "b", 12: "c", 13: "a", 14: "b", 15: "c", 16: "a", 17: "b",
                                           18: "c", 19: "a", 20: "b"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection_fail_1(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "a", 5: "c", 6: "b"}
        self.assertEqual(False, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection_fail_2(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c"}
        self.assertEqual(False, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection_fail_3(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "c", 3: "c", 4: "a"}
        self.assertEqual(False, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection_fail_4(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "a", 5: "b", 6: "c", 7: "c"}
        self.assertEqual(False, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection_fail_5(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "a", 3: "a", 4: "a", 5: "a", 6: "a"}
        self.assertEqual(False, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection_fail_7(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "c", 3: "b", 4: "a", 5: "b", 6: "c"}
        self.assertEqual(False, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection_new_instance(self):
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "a", 5: "d", 6: "c"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())

    def test_round_robin_detection_not_so_strict(self):
        # only one error at the end -> inside the tolerance
        load_balancer = LoadBalancer()
        load_balancer.set_allowed_error_percentage(0.1)
        load_balancer._instance_history = {1: "a", 2: "b", 3: "c", 4: "a", 5: "b", 6: "c", 7: "a", 8: "b", 9: "c",
                                           10: "a", 11: "b", 12: "c", 13: "a", 14: "b", 15: "c", 16: "a", 17: "b",
                                           18: "c", 19: "a", 20: "b", 21: "b"}
        self.assertEqual(True, load_balancer.detect_round_robin_pattern())
