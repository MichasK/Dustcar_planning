import unittest
import pandas as pd


class TestFinderDistance(unittest.TestCase):
    def setUp(cls):
        cls.df = pd.read_csv("../data/parsed.csv", header=0)

    def test_longitude(self):

        for index, row in self.df.iterrows():
            self.assertAlmostEqual(row.longitude, 18.5, delta=1)

    def test_latitude(self):

        for index, row in self.df.iterrows():
            self.assertAlmostEqual(row.latitude, 50, delta=1)


if __name__ == '__main__':
    unittest.main()
