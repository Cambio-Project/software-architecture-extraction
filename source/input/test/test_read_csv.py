import unittest

from input.input_utils import read_csv


class TestReadCSV(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_read_capacity_csv(self):
        capacities = read_csv("test_capacities.csv")
        self.assertTrue(capacities[0][0], "A")
        self.assertTrue(capacities[1][0], "B")
        self.assertTrue(capacities[2][0], "C")
        self.assertTrue(capacities[3][0], "D")

        self.assertTrue(capacities[0][1], "1779")
        self.assertTrue(capacities[1][1], "189")
        self.assertTrue(capacities[2][1], "2211")
        self.assertTrue(capacities[3][1], "9450")
