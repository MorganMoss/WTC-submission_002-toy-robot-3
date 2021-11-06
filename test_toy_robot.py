import unittest
from io import StringIO
from test_base import captured_io
from toy_robot import ToyRobot

class TestToyRobot(unittest.TestCase):
    robby = ToyRobot()

    def test_cmd(self):
        pass
    def test_start(self):
        pass



if __name__ == '__main__':
    unittest.main()
