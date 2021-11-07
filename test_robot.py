import unittest
from test_base import run_unittests

class TestRobot(unittest.TestCase):

    def test_base_robot(self):
        import test_base_robot
        test_result = run_unittests("test_base_robot")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_command_robot(self):
        import test_command_robot
        test_result = run_unittests("test_command_robot")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_command_handler(self):
        import test_command_handler
        test_result = run_unittests("test_command_handler")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

    def test_toy_robot(self):
        import test_toy_robot
        test_result = run_unittests("test_toy_robot")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")

if __name__ == '__main__':
    unittest.main()