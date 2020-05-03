import unittest

from app.data.screader import SCReader


class TestReader(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reader(self):
        reader = SCReader()
        res = reader.read_file("data/KOSDAQ.csv")
        assert res
        res = reader.read_file("data/KOSPI.csv")
        assert res
