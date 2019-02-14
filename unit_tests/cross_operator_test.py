import unittest
from data_structers.cross_operators import create_cross_table, longest_common_num_seq
import numpy as np


class TestCross(unittest.TestCase):
    def test_one_subsequence(self):
        x = np.array([-1, 2, 3, -1, 11, 12, 13, -1, 6, 5])
        y = np.array([3, 2, -1, -1, 11, 12, 13, 6, 5, -1])
        z = longest_common_num_seq(np.copy(x), np.copy(y))
        self.assertEqual(z.size, 4)
        self.assertTrue(np.array_equal(z, np.array([-1, 11, 12, 13])))
