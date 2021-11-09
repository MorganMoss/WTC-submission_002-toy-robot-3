import unittest
from io import StringIO
from unittest import mock
from test_base import captured_io
from robot_command_handling import CommandHandler
from exceptions import InputError


class TestCommandHandler(unittest.TestCase):
    handler_robby = CommandHandler()

    def test_command_word_valid(self):
        #shouldn't raise error
        for key in self.handler_robby.command_dict:
            self.handler_robby.command_word_valid(
                [f"{key}"])
            self.handler_robby.command_word_valid(
                [f"{key[0].lower()}{key[1:len(key)-1]}{key[-1].lower()}"])
            self.handler_robby.command_word_valid(
                [f"{key[0]}{key[1:len(key)-1].lower()}{key[-1]}"])
            self.handler_robby.command_word_valid(
                [f"{key.lower()}"])
        #should raise error
        try:
            self.handler_robby.command_word_valid(["Fail"])
        except InputError as e:
            self.assertEqual("Sorry, I did not understand 'Fail'.", str(e))


    def test_convert_command_args(self):
        for key in self.handler_robby.command_dict:
            input_args = list().copy()
            try:
                args = self.handler_robby.command_dict[key]['args']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str,input_args))
            #shouldn't give an error
            if args != []:
                for i in range(len(input_args)):
                    self.assertEqual(
                        input_args[i],
                        self.handler_robby.convert_command_args(args[i], input_args_iter))
        #now with type error
        for key in self.handler_robby.command_dict:
            input_args = list().copy()
            try:
                args = self.handler_robby.command_dict[key]['args']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(float())
            input_args_iter = iter(map(str,input_args))
            #shouldn't give an error
            if args != []:
                for i in range(len(input_args)):
                    try:
                        self.assertEqual(
                            input_args[i],
                            self.handler_robby.convert_command_args(args[i], input_args_iter))
                    except InputError as e:
                        #caught an error
                        self.assertTrue(True)
                    else:
                        self.assertTrue(False)


    def test_organise_args(self):
        for key in self.handler_robby.command_dict:
            input_args = list().copy()
            try:
                args = self.handler_robby.command_dict[key]['args']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str, input_args))
            #shouldn't give an error
            self.assertEqual(
                self.handler_robby.organise_args(key, input_args_iter),
                input_args
            )
        for key in self.handler_robby.command_dict:
            input_args = list().copy()
            try:
                args = self.handler_robby.command_dict[key]['args']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str, input_args))
            #should give an error
            if args != []:
                next(input_args_iter)
                try:
                    self.handler_robby.organise_args(key, input_args_iter)
                except InputError as e:
                    #caught an error
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)


    def test_organise_opt(self):
        for key in self.handler_robby.command_dict:
            input_args = list().copy()
            try:
                args = self.handler_robby.command_dict[key]['opt']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str, input_args))
            #shouldn't give an error
            self.assertEqual(
                self.handler_robby.organise_opt(key, input_args_iter),
                input_args
            )
        for key in self.handler_robby.command_dict:
            input_args = list().copy()
            try:
                args = self.handler_robby.command_dict[key]['opt']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args_iter = iter(map(str, input_args))
            #shouldnt give an error
            if args != []:
                next(input_args_iter)
                self.handler_robby.organise_opt(key, input_args_iter)
        for key in self.handler_robby.command_dict:
            input_args = list().copy()
            try:
                args = self.handler_robby.command_dict[key]['opt']
            except KeyError:
                args = list().copy()
            for arg in args:
                input_args.append(arg())
            input_args.append("Extra")
            input_args_iter = iter(map(str, input_args))
            #should give an error
            if args != []:
                try:
                    self.handler_robby.organise_opt(key, input_args_iter)
                except InputError as e:
                    #caught an error
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)           


    def test_overflow_arg(self):
        try:
            self.handler_robby.overflow_arg(iter([1]))
        except InputError as e:
            self.assertEqual(str(e), "Sorry, You have too many arguments.")
        self.handler_robby.overflow_arg(iter([]))


    @mock.patch.object(CommandHandler, "command_word_valid")
    @mock.patch.object(CommandHandler, "convert_command_args")
    @mock.patch.object(CommandHandler, "organise_args")
    @mock.patch.object(CommandHandler, "organise_opt")
    @mock.patch.object(CommandHandler, "overflow_arg")
    def test_command_valid(self, *mock):
        self.handler_robby.command_valid(["OfF"])
        for m in mock:
            m.assert_called()


    def test_replay_valid_args(self):
        history  = [1,2,3]
        base_dict = {
            'silent'    : False,
            'reversed'  : False,
            'range'     : range(0, 3)
        }
        self.assertEqual(
            self.handler_robby.replay_valid_args([]),
            base_dict
        )
        silent = base_dict.copy()
        silent['silent'] = True
        self.assertEqual(
            self.handler_robby.replay_valid_args(["silent"]),
            silent
        )
        reversed = base_dict.copy()
        silent['reversed'] = True
        self.assertEqual(
            self.handler_robby.replay_valid_args(["reversed"]),
            silent
        )
        both_silent_and_reverse = base_dict.copy()
        both_silent_and_reverse['reversed'] = True
        both_silent_and_reverse['silent'] = True
        self.assertEqual(
            self.handler_robby.replay_valid_args(["reversed", "silent"]),
            both_silent_and_reverse
        )
        self.assertEqual(
            self.handler_robby.replay_valid_args(["silent", "reversed"]),
            both_silent_and_reverse
        )




    def test_get_command(self):
        for key in ["LEFT", "RIGHT", "HELP", "REPLAY", "OFF"]:
            input_string = "Fail\n"
            input_string += f"{key}\n"
            input_string += f"{key.lower()}\n"
            input_string += f"{key[0]}{key[1:len(key)-1].lower()}{key[-1]}\n"
            input_string += f"{key[0].lower()}{key[1:len(key)-1]}{key[-1].lower()}\n"

            with captured_io(StringIO(input_string)) as (out, err):
                try:
                    self.handler_robby.get_command()
                except InputError as e:
                    self.assertEqual("Sorry, I did not understand 'Fail'.", str(e))
                for _ in range(4):
                    self.assertEquals(self.handler_robby.get_command()[0].upper(), key)


if __name__ == '__main__':
    unittest.main()