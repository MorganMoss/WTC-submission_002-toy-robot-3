import unittest
from unittest import mock
from io import StringIO
from test_base import captured_io
from robot_command import CommandRobot


class TestCommandRobot(unittest.TestCase):
    command_robby = CommandRobot()
    command_robby.name = "ROBBY"
    
    
    def test_exrc_command(self):
        command_robby = self.command_robby
        for command_name, command in self.command_robby.command_dict.items():
            def test_this_command(self, mock):
                l = [command_name]
                if command_name == "OFF":
                    try:
                        command_robby.exec_command(l)
                    except SystemExit: ...
                elif command_name == "REPLAY":
                    l += [{'silent': True, 'reverse': False, 'range': range(0)}]
                    command_robby.exec_command(l)
                else:
                    if 'args' in command.keys():
                        for arg in  command['args']:
                            l += [arg()]
                    if 'optional' in command.keys():
                        for arg in  command['optional']:
                            l += [arg()]
                    command_robby.exec_command(l)        
                mock.assert_called()
            with mock.patch.object(CommandRobot, command['command']) as m:
                test_this_command(self, m)


    @mock.patch.object(
        CommandRobot, 'robot_move', side_effect = command_robby.robot_move)
    def test_forward(self, mock):
        with captured_io(StringIO()) as (out, err):
            self.command_robby.command_forward(1)
            mock.assert_called()
            self.assertEqual(self.command_robby.position, (0, 1))
            self.command_robby.command_forward(-1)
            mock.assert_called()
            self.assertEqual(self.command_robby.position, (0, 2))
            self.command_robby.position = (0, 0)


    @mock.patch.object(
        CommandRobot, 'robot_move', side_effect = command_robby.robot_move)
    def test_back(self, mock):
        with captured_io(StringIO()) as (out, err):
            self.command_robby.command_back(1)
            mock.assert_called()
            self.assertEqual(self.command_robby.position, (0, -1))
            self.command_robby.command_back(-1)
            mock.assert_called()
            self.assertEqual(self.command_robby.position, (0, -2))
            self.command_robby.position = (0, 0)


    @mock.patch.object(
        CommandRobot, 'robot_rotate', side_effect = command_robby.robot_rotate)
    def test_right(self, mock):
        with captured_io(StringIO()) as (out, err):
            self.command_robby.exec_command(["RIGHT"])
        self.assertEqual(self.command_robby.rotation, 90)
        output = out.getvalue().strip()
        self.assertIn("> ROBBY turned right.", output)
        mock.assert_called()
        self.command_robby.rotation = 0


    @mock.patch.object(
        CommandRobot, 'robot_rotate', side_effect = command_robby.robot_rotate)
    def turn_left(self, mock):
        with captured_io(StringIO()) as (out, err):
            self.command_robby.exec_command(["LEFT"])
        self.assertEqual(self.command_robby.rotation, 270)
        output = out.getvalue().strip()
        self.assertIn("> ROBBY turned left.", output)
        mock.assert_called()
        self.command_robby.rotation = 0


    @mock.patch.object(
        CommandRobot, 'robot_move', side_effect = command_robby.robot_move)
    def test_sprint(self, mock):
        with captured_io(StringIO()) as (out, err):
            self.command_robby.command_sprint(2)
            mock.assert_called()
            mock.assert_called()
            self.assertEqual(self.command_robby.position, (0,3))
            self.command_robby.position = (0, 0)            
            self.command_robby.command_sprint(-2)
            mock.assert_called()
            mock.assert_called()
            self.assertEqual(self.command_robby.position, (0,-3))
            self.command_robby.position = (0, 0)
    

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
        ...


if __name__ == '__main__':
    unittest.main()
