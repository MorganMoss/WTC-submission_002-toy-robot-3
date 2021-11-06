import unittest
from io import StringIO
from test_base import captured_io
import math
from base_robot import BaseRobot

class TestBaseRobot(unittest.TestCase):
    base_robby = BaseRobot()

    def test_say_message(self):
        with captured_io(StringIO()) as (out, err): 
            self.base_robby.robot_say_message("Message", "Start", "End")
        output = out.getvalue()
        self.assertEqual(output, "StartMessageEnd")


    def test_get_name(self):
        with captured_io(StringIO('ROBBY\n')) as (out, err):
            self.base_robby.robot_get_name()
        output = out.getvalue().strip()
        self.assertEqual("What do you want to name your robot?", output)
        self.assertEqual(self.base_robby.name, "ROBBY")


    def test_report_position(self):
        with captured_io(StringIO()) as (out, err): 
            self.base_robby.robot_report_position()
        output = out.getvalue()
        self.assertEqual(output, " > ROBBY now at position (0,0).\n")


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


    def test_valid_move(self):
        with captured_io(StringIO()) as (out, err):
            self.assertFalse(self.base_robby.valid_move(201))
            self.assertFalse(self.base_robby.valid_move(-201))
            self.base_robby.robot_rotate(90)
            self.assertFalse(self.base_robby.valid_move(101))
            self.assertFalse(self.base_robby.valid_move(-101))
            self.base_robby.robot_rotate(-90)
            self.assertEqual(self.base_robby.valid_move(200), (0, 200))
            self.assertEqual(self.base_robby.valid_move(-200), (0, -200))
            self.base_robby.robot_rotate(90)
            self.assertEqual(self.base_robby.valid_move(100), (100, 0))
            self.assertEqual(self.base_robby.valid_move(-100), (-100, 0))


    def test_robot_move(self):
        with captured_io(StringIO()) as (out, err):
            for angle in range(0, 271, 90):
                self.base_robby.rotation = angle
                angle = math.radians(angle)
                self.base_robby.robot_move(5)
                self.assertEqual(self.base_robby.position, 
                                (round(5*math.sin(angle)),round(5*math.cos(angle))))
                self.base_robby.position = (0,0)
                self.base_robby.rotation = 0


if __name__ == '__main__':
    unittest.main()
