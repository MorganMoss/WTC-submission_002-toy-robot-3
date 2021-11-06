import unittest
from io import StringIO
from test_base import captured_io
from robot_command import CommandRobot


class TestCommandRobot(unittest.TestCase):
    command_robby = CommandRobot()
    command_robby.name = "ROBBY"

    def test_exec_command(self):
        pass


    def test_forward(self):
        pass


    def test_back(self):
        pass


    def test_right(self):
        with captured_io(StringIO()) as (out, err):
            self.command_robby.exec_command(["RIGHT"])
        self.assertEqual(self.command_robby.rotation, 90)
        output = out.getvalue().strip()
        self.assertIn("> ROBBY turned right.", output)


    def turn_left(self):
        with captured_io(StringIO()) as (out, err):
            self.command_robby.exec_command(["LEFT"])
        self.assertEqual(self.command_robby.rotation, 270)
        output = out.getvalue().strip()
        self.assertIn("> ROBBY turned left.", output)


    def test_sprint(self):
        pass

    
    def test_off(self):
        with captured_io(StringIO()) as (out, err):
            try:
                self.command_robby.exec_command(["OFF"])
            except SystemExit:
                ...
        output = out.getvalue().strip()
        self.assertEqual("ROBBY: Shutting down..", output)


    def test_help(self):
        with captured_io(StringIO()) as (out, err):
            self.command_robby.exec_command(["HELP"])
        output = out.getvalue()
        self.assertEqual(
"""I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD\t- Move robot foward by [number] steps
BACK\t- Move robot back by [number] steps
RIGHT\t- Rotate robot right
LEFT\t- Rotate robot left
SPRINT\t- Move robot foward by [number] steps
REPLAY\t- Replays previous movement commands.
\t  It has optional arguments:
\t\tSilent - Hides output from replayed commands
\t\tReversed - Reverses the order to be last to first
\t\t<int> - Starts from previous <int> commands
\t\t<int>-<int> - Starts from previous <int> commands and ends at <int> previous commands
""", output)


    def test_replay(self):
        pass


if __name__ == '__main__':
    unittest.main()
