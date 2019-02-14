import unittest
import numpy as np


class MyTestCase(unittest.TestCase):
    def setUp(cls):
        cls.matrix = np.load('../data/distance_matrix.npy')

    def test_non_zeros(self):
        for i in range(0, self.matrix.shape[0]):
            for j in range(0, self.matrix.shape[1]):
                self.assertGreaterEqual(self.matrix[i, j], 0)

    def test_far_localisation(self):
        for i in range(0, self.matrix.shape[0]):
            for j in range(0, self.matrix.shape[1]):
                self.assertLessEqual(self.matrix[i, j], 40)


if __name__ == '__main__':
    for i in range(100):
        unittest.main()
