import unittest

from app.data.screader import SCReader


class TestReader(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reader(self):
        reader = SCReader()
        res = reader.read_file("data/KOSDAQ_2020.csv")
        assert res
        res = reader.read_file("data/KOSPI_2020.csv")
        assert res
