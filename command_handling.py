from exceptions import InputError
from command_robot import CommandRobot

class CommandHandler(CommandRobot):
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
            raise InputError(command)


    def convert_command_args(self, arg_type:type, command_iter:iter):
        """
        Tries to convert the next or all the following
        command words into their the required type.

        Args:
            arg_type (type): The type the command needs to be converted to.
            command_iter (iter): Iterable containing the command, word by word

        Returns:
            arg_type: next command_iter(s) converted

        Raises:
            InputError: Argument of the wrong type was entered.
        """
        if arg_type is str:
            return arg_type(" ".join([*command_iter]))

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
        Organises compulsory arguments needed for given command word.

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
                    "".join([
                        f"Sorry, '{command_word}' needs ",
                        f"{len(command_args)} arguments."
                    ])
                )
        return args


    def organise_opt(self, command_word:str, command_iter:iter):
        """
        Organises optional arguments needed for given command word.

        Args:
            command_word (str): The command word.
            command_iter (iter): The iterable arguments from the input.

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
        Checks if there's too many arguments in the given input.

        Args:
            command_iter (iter): The supposedly empty iterator.

        Raises:
            InputError: Raised if command_iter isn't empty.
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


    def replay_valid_args(self, command_arguments:str):
        """
        Special case of data processing used for 'REPLAY'.

        Args:
            command_arguments (str): the input string after the command word.

        Raises: (Respectively)
            InputError: Too many arguments.
            InputError: Range has non digits.
            InputError: Too many numbers in range arg.
            InputError: Range is too big, small or in the incorrect order.

        Returns:
            dict: The dictionary 'REPLAY' needs as an argument.
        """
        h_size = len(self.history)
        processed_args = {
            'silent'    : False,
            'reversed'  : False,
            'range'     : range(0, h_size)
        }
        
        command_arguments = command_arguments.lower().strip().split()
        for key in ['silent', 'reversed']:
            try: 
                command_arguments.remove(key)
            except ValueError:
                continue
            processed_args[key] = True
        if len(command_arguments) > 1:
            raise InputError

        if  len(command_arguments) == 1:
            command_arguments = command_arguments[0].strip().split('-')

            if  not all(map(lambda arg : arg.isdigit(), command_arguments)):
                raise InputError
            if  len(command_arguments) > 2:
                raise InputError

            
            if len(command_arguments) == 2:
                start = h_size - int(command_arguments[0])
                stop = h_size - int(command_arguments[1])
            else:
                start = h_size - int(command_arguments[0])
                stop = h_size
            
            if  0 > start or start > stop or stop > h_size:
                raise InputError
        
            processed_args["range"] = range(start, stop)

        return processed_args


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
        
        #REPLAY is a special case
        if command[0].upper() == 'REPLAY':
            try:
                command[1] = self.replay_valid_args(command[1])
            except InputError:
                raise InputError(command)
        
        return [command[0], *command[1:]] \
                if len(command) > 1 else command
    
    
    def __init__(self) -> None:
        """
        Constructor for CommandHandling. 
        Calls the CommandRobot Constructor.
        """
        super().__init__()
