import unittest
from unittest import mock
from io import StringIO
from test_base import captured_io
from robot_toy import ToyRobot


class TestToyRobot(unittest.TestCase):
    robby = ToyRobot()

    @mock.patch.object(ToyRobot, "robot_get_name")
    @mock.patch.object(ToyRobot, "robot_say_message")
    def test_start(self, mock1, mock2):
        with captured_io(StringIO("ROBBY")) as (out, err):
            self.robby.start()
            mock1.assert_called()
            mock2.assert_called()

    @mock.patch.object(ToyRobot, "exec_command")
    def test_cmd(self, mock):
        with captured_io(StringIO("oFf")) as (out, err):
            self.robby.cmd()
            mock.assert_called()
            

if __name__ == '__main__':
    unittest.main()
