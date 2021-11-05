import unittest
from command_handling import InputError
from toy_robot import ToyRobot
from io import StringIO
import math
from test_base import captured_io


class TestRobot(unittest.TestCase):
    pass
    '''
    robby = ToyRobot()


    def test_create_robot(self):
        self.assertEqual(self.robby.name, "")
        self.assertEqual(self.robby.position, (0,0))
        self.assertEqual(self.robby.rotation, 0)


    def test_robot_get_name(self):
        with captured_io(StringIO('ROBBY\n')) as (out, err):
            self.robby.robot_get_name()
        output = out.getvalue().strip()
        self.assertEqual("What do you want to name your robot?", output)
        self.assertEqual(self.robby.name, "ROBBY")
    

    def test_get_command_and_valid_command_no_args(self):
        for key, command in filter(
            lambda item :
                'args' not in item.keys(),
                 self.robby.command_dict.items()
        ):
            input_string = "Fail\n"
            input_string += f"{key}\n"
            input_string += f"{key.lower()}\n"
            input_string += f"{key[0]}{key[1:len(key)-1].lower()}{key[-1]}\n"
            input_string += f"{key[0].lower()}{key[1:len(key)-1]}{key[-1].lower()}\n"

            with captured_io(StringIO(input_string)) as (out, err):
                self.assertRaises(self.robby.get_command(), InputError)
                for _ in range(4):
                    self.assertEqual(self.robby.get_command()[0], key)


    def test_command_help(self):
        with captured_io(StringIO()) as (out, err):
            self.robby.exec_cmd(["HELP"])
        output = out.getvalue().strip()

        self.assertIn(
"""I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD\t- Move robot foward by [number] steps
BACK\t- Move robot back by [number] steps
RIGHT\t- Rotate robot right
LEFT\t- Rotate robot left
SPRINT\t- Move robot foward by [number] steps
REPLAY\t- Redoes all previous movement commands""", output)
    

    def test_move(self):
        for angle in range(0, 271, 90):
            self.robby.rotation = angle
            angle = math.radians(angle)
            self.robby.robot_move(5)
            self.assertEqual(self.robby.position, 
                            (round(5*math.sin(angle)),round(5*math.cos(angle))))
            self.robby.position = (0,0)


    def test_turn(self):
        self.robby.rotation = 0
        self.robby.exec_cmd(["LEFT"])
        self.assertEqual(self.robby.rotation, 270)
        self.robby.rotation = 0
        self.robby.exec_cmd(["RIGHT"])
        self.assertEqual(self.robby.rotation, 90)

        for _ in range(3):
            self.robby.exec_cmd(["RIGHT"])
        self.assertEqual(self.robby.rotation, 0)


    def test_command_off(self):
        with captured_io(StringIO()) as (out, err):
            try:
                self.robby.exec_cmd(["OFF"])
            except SystemExit:
                ...
        output = out.getvalue().strip()
        self.assertEqual("ROBBY: Shutting down..", output)
    

    def test_replay(self):
        self.robby.exec_cmd(["REPLAY"])
        
    '''
if __name__ == '__main__':
    unittest.main()
