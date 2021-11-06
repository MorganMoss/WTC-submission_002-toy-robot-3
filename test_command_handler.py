import unittest
from io import StringIO
from test_base import captured_io
from robot_command_handling import CommandHandler


class TestCommandHandler(unittest.TestCase):
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
                    self.assertEquals(self.handler_robby.get_command()[0].upper(), key)


if __name__ == '__main__':
    unittest.main()