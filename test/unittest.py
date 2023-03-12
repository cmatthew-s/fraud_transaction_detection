 import unittest
import sys

sys.path.insert(0, '..')

from system import Data

dt = Data.Data()

class TestFunction(unittest.TestCase):
    def setUp(self):
        pass

    def test_file(self):
        self.assertEqual(dt.check_file('./history_data'), False)

if __name__ == '__main__':
    unittest.main()
