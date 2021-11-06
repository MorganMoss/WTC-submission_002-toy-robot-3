import unittest
from io import StringIO
import math
from test_base import captured_io

class TestBaseRobot(unittest.TestCase):
    from base_robot import BaseRobot
    base_robby = BaseRobot()

    def test_say_message(self):
        pass


    def test_get_name(self):
        with captured_io(StringIO('ROBBY\n')) as (out, err):
            self.base_robby.robot_get_name()
        output = out.getvalue().strip()
        self.assertEqual("What do you want to name your robot?", output)
        self.assertEqual(self.base_robby.name, "ROBBY")


    def test_report_position(self):
        pass
    def test_valid_move(self):
        pass


    def test_robot_move(self):
        for angle in range(0, 271, 90):
            self.base_robby.rotation = angle
            angle = math.radians(angle)
            self.base_robby.robot_move(5)
            self.assertEqual(self.base_robby.position, 
                            (round(5*math.sin(angle)),round(5*math.cos(angle))))
            self.base_robby.position = (0,0)
            self.base_robby.rotation = 0
        

    def test_robot_rotate(self):
        with captured_io(StringIO()) as (out, err):
            self.base_robby.robot_rotate(-90)
            self.assertEqual(self.base_robby.rotation, 270)
            self.base_robby.rotation = 0
            self.base_robby.robot_rotate(90)
            self.assertEqual(self.base_robby.rotation, 90)
            for _ in range(3):
                self.base_robby.robot_rotate(90)
            self.assertEqual(self.base_robby.rotation, 0)
        output = out.getvalue()
        self.assertEqual(
""" > ROBBY turned left.
 > ROBBY now at position (0,0).
 > ROBBY turned right.
 > ROBBY now at position (0,0).
 > ROBBY turned right.
 > ROBBY now at position (0,0).
 > ROBBY turned right.
 > ROBBY now at position (0,0).
 > ROBBY turned right.
 > ROBBY now at position (0,0).
""", output)
        self.base_robby.rotation = 0

class TestCommandRobot(unittest.TestCase):
    from command_robot import CommandRobot
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
        self.assertEquals(
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


class TestCommandHandler(unittest.TestCase):
    from command_handling import CommandHandler
    handler_robby = CommandHandler()

    def test_command_word_valid(self):
        pass
    def test_convert_command_args(self):
        pass
    def test_organise_args(self):
        pass
    def test_organise_opt(self):
        pass
    def test_overflow_arg(self):
        pass
    def test_command_valid(self):
        pass
    def test_replay_valid_args(self):
        pass


    def test_get_command(self):
        for key in ["LEFT", "RIGHT", "HELP", "REPLAY", "OFF"]:
            # input_string = "Fail\n"
            input_string = f"{key}\n"
            input_string += f"{key.lower()}\n"
            input_string += f"{key[0]}{key[1:len(key)-1].lower()}{key[-1]}\n"
            input_string += f"{key[0].lower()}{key[1:len(key)-1]}{key[-1].lower()}\n"

            with captured_io(StringIO(input_string)) as (out, err):
                # self.assertRaises(self.handler_robby.get_command(), InputError)
                for _ in range(4):
                    self.assertEqual(self.handler_robby.get_command()[0].upper(), key)


class TestToyRobot(unittest.TestCase):
    from toy_robot import ToyRobot
    robby = ToyRobot()

    def test_cmd(self):
        pass
    def test_start(self):
        pass
    '''
    robby = ToyRobot()


    def test_create_robot(self):
        self.assertEqual(self.robby.name, "")
        self.assertEqual(self.robby.position, (0,0))
        self.assertEqual(self.robby.rotation, 0)


    def test_replay(self):
        self.robby.exec_cmd(["REPLAY"])
        
    '''


if __name__ == '__main__':
    unittest.main()
