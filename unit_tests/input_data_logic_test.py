from data_structers.inputdata import InputData
import unittest


class TestIndividual(unittest.TestCase):
    def setUp(self):
        self.trivial = InputData("../data/trivial")

    def test_example_car_length(self):
        self.assertEqual(3, self.trivial.cars.shape[0])

