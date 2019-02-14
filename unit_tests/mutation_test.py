import unittest
import numpy as np
from data_structers.mutation_operators import *


class TestIndividual(unittest.TestCase):
    def test_change_random_element(self):
        print('test_change_random_element')
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        y = change_one_element_permutation(np.copy(x))
        self.assertEqual(x.size, y.size)
        self.assertFalse(np.array_equal(x, y))

    def test_swap_random_element(self):
        print('test_swap_random_element')
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        y = swap_random_elements(np.copy(x))
        self.assertEqual(x.size, y.size)
        self.assertFalse(np.array_equal(x, y))

    def test_mutation_add_car(self):
        print('test_mutation_add_car')
        x = np.array([1, 2, -1, 3, 4, 5, 6, -1, 7, 8])
        input_table_markers = np.count_nonzero(x == -1)
        y = add_marker_in_random(np.copy(x), -1)
        z = add_marker_in_random(np.copy(x), -1, n_elements=2)
        self.assertEqual(input_table_markers + 1, np.count_nonzero(y == -1))
        self.assertEqual(x.size + 1, y.size)
        self.assertEqual(input_table_markers + 2, np.count_nonzero(z == -1))

    def test_shift_one_marker(self):
        print('test_shift_one_marker')
        x = np.array([1, 2, -1, 3, 4, 5, 6, -1, 7, 8])
        y = shift_one_marker(np.copy(x), -1)
        self.assertEqual(x.size, y.size)
        self.assertFalse(np.array_equal(x, y))

    def test_delete_random_comeback(self):
        print('test_delete_random_comeback')
        xx = np.array([0, 1, 0, 0, 0, 1, 0])
        zer_bef = np.count_nonzero(xx == 0)
        ind = Individual(array=np.copy(xx))
        delete_random_comeback(ind)
        self.assertEqual(zer_bef - 1, np.count_nonzero(ind.street_order == 0))

    def test_add_random_comeback(self):
        print('test_add_random_comeback')
        xx = np.array([0, 1, 0, 0, 0, 1, 0])
        zer_bef = np.count_nonzero(xx == 0)
        ind = Individual(array=np.copy(xx))
        add_random_comeback(ind)
        self.assertEqual(zer_bef + 1, np.count_nonzero(ind.street_order == 0))


if __name__ == '__main__':
    unittest.main()
