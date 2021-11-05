from exceptions import InputError



class CommandHandler:
    """
    Handles the process of getting user input
    and processing it into commands
    """

    def command_word_valid(self, command:list):
        """
        Checks if the command word at the beginning
        of the given input exists in the command dictionary

        Args:
            command (list): The user's input, split.

        Raises:
            InputError: If the command does not exist.
        """
        if  command[0].upper() not in self.command_dict:
            raise InputError(
                f"Sorry, I did not understand '{' '.join(command)}'."
            )


    def convert_command_args(self, arg_type:type, command_iter:iter):
        """
        Tries to convert the next or all the following
        command words into their the required type.

        Args:
            arg_type (type): The type the command needs to be converted to.
            command_iter (iter): Iterable containing the command, word by word

        Returns:
            arg_type: next command_iter(s) converted
        """
        #str case
        if arg_type is str:
            return arg_type(" ".join([*command_iter]))
        #non-subscriptable case
        next_arg = next(command_iter)
        try:
            return arg_type(next_arg)
        except TypeError and ValueError:
            raise InputError(
                " ".join([
                    f"Sorry, '{next_arg}' needs to be of type",
                    f"'{arg_type().__class__.__name__}'",
                ])
            ) 


    def organise_args(self, command_word:str, command_iter:iter):
        """
        Organises optional arguments needed for given command word.

        Args:
            command_word (str): The command word
            command_iter (iter): The iterable arguments from the input

        Raises:
            InputError: Raised if insufficient arguments are given

        Returns:
            list: The arguments, 
            formatted so to be used in command functions.
        """
        args = list()
        try:
            command_args = self.command_dict[command_word]["args"]
        except KeyError:
            command_args = []
        for arg_type in command_args:
            try:
                new_arg = self.convert_command_args(arg_type, command_iter)
                args.append(new_arg)
            except StopIteration:
                raise InputError(
                    " ".join([
                        f"Sorry, '{command_word}' needs",
                        f"{len(command_args)} arguments."
                    ])
                )
        return args


    def organise_opt(self, command_word:str, command_iter:iter):
        """AI is creating summary for organise_opt

        Args:
            command_word (str): The command word
            command_iter (iter): The iterable arguments from the input

        Returns:
            list: The optional arguments, 
            formatted so to be used in command functions.
        """
        args = list()
        try:
            command_opt = self.command_dict[command_word]["optional"]
        except KeyError:
            command_opt = []
        for arg_type in command_opt:
            try:
                new_arg = self.convert_command_args(arg_type, command_iter)
                args.append(new_arg)
            except StopIteration and InputError:
                ... 
        return args


    def overflow_arg(self, command_iter:iter):
        """
        Checks if there's too many arguments in the given input

        Args:
            command_iter (iter): The supposedly empty iterator

        Raises:
            InputError: Raised if command_iter isn't empty
        """
        try:
            next(command_iter) 
        except StopIteration:
            return
        raise InputError(f"Sorry, You have too many arguments.")


    def command_valid(self, command:list):
        """
        Checks if the input is valid and has the correct arguments.

        Args:
            command (list): contains a command then arguments as strings.

        Raises:
            InputError: If command is invalid

        Returns:
            list: contains a valid uppercase command 
            and the necessary arguments in their correct types
            if the input was valid.
        """
        self.command_word_valid(command)

        command_iter = iter(command[1:])

        args = self.organise_args(command[0].upper(), command_iter)\
             + self.organise_opt(command[0].upper(), command_iter)

        self.overflow_arg(command_iter)
        return [command[0]] + args


    def get_command(self):
        """
        Asks for a valid command.

        Raises:
            InputError: Raised if command is invalid.

        Returns:
            list: contains a valid uppercase command 
            and the necessary arguments in their correct types.
        """
        command = self.command_valid(input().strip().split(" "))

        return [command[0], *command[1:]] \
                if len(command) > 1 else command
    
