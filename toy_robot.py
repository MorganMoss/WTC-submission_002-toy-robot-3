import math
from typing import Iterable

class ToyRobot:
    """
    An instance of this class is a robot that can be 
    controlled via commands and sends messages to the console.
        * Only robot_... methods should be called outside the class
    """
    def robot_say_message(self, message:str, start:str = "", end:str = "\n"):
        """
        Robot Sends message to console.

        Args:
            message (str): The text the robot sends to the console.
            start (str, optional): print something before message. 
            Defaults to empty string.
            end (str, optional): string appended after the last value. 
            Defaults to newline.
        """
        if self.messages_enabled:
            print(f"{start}{message}" , end = end) 


    def robot_report_position(self):
        """
        Makes robot send a message displaying its current position.
        """
        self.robot_say_message(
            f"now at position {str(self.position).replace(' ', '')}.",
            f" > {self.name} "
        )


    def valid_move(self, steps:int): 
        """
        Checks if the move ends in a valid area.

        Args:
            steps (int): The distance the robot moves.

        Returns:
            bool: False if invalid move.
            tuple: The new position if valid move.
        """
        new_position = (
                (self.position[0] \
                + steps*round(math.sin(math.radians(self.rotation)))),
                (self.position[1] \
                + steps*round(math.cos(math.radians(self.rotation)))))
        if  (self.bounds[0][0] <= new_position[0] <= self.bounds[0][1]) \
        and (self.bounds[1][0] <= new_position[1] <= self.bounds[1][1]):
            return new_position
        self.robot_say_message(
            "Sorry, I cannot go outside my safe zone.",
            f"{self.name}: "
        )
        return False


    def robot_move(self, steps:int):
        """
        Moves the robot and then the robot sends a message saying it has done so.

        Args:
            steps (int): The distance the robot moves.
                * Positive int moves forward.
                * Negative int moves back.

        Returns:
            bool: True if move was successful.
        """
        new_position = self.valid_move(steps)

        if  new_position:
            self.position = new_position
            direction = "forward" if steps >= 0 else "back"
            self.robot_say_message(
                f"moved {direction} by {abs(steps)} steps.",
                f" > {self.name} "
            )
            return True
        return False
            

    def robot_get_name(self):
        """
        Sets robots name to a given input.
        """
        self.robot_say_message("What do you want to name your robot? ", end="")
        self.name = input()


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
        except TypeError:
            self.robot_say_message(
                " ".join([
                    f"Sorry, '{next_arg}'",
                    "needs to be of type",
                    f"'{arg_type().__class__.__name__}'",
                ]),
                f"{self.name}: "
            ) 
                
        
    def command_valid(self, command:list):
        """
        Checks if the input is valid and has the correct arguments.
            * If the input has more than the required arguments,
            the remainder is ignored.

            * Converts the command list into desired types in 
            the process of checking.

            * Robot sends appropriate error messages.

        Args:
            command (list): contains a command then arguments as strings.

        Returns:
            list: contains a valid uppercase command 
            and the necessary arguments in their correct types
            if the input was valid.
            bool: False when the command or arguments are invalid
        """
        #check if valid command
        if  command[0].upper() not in self.command_dict:
            self.robot_say_message(
                f"Sorry, I did not understand '{' '.join(command)}'.", 
                f"{self.name}: "
            )
            return False

        #initializing variables
        command[0] = command[0].upper()
        command_iter = iter(command[1:])
        args = list()
        try:
            command_args = self.command_dict[command[0]]["args"]
        except KeyError:
            command_args = []
        try:
            command_opt = self.command_dict[command[0]]["optional"]
        except KeyError:
            command_opt = []

        #organsing compulsory args
        for arg_type in command_args:
            try:
                new_arg = self.convert_command_args(arg_type, command_iter)
                if new_arg == None:
                    return False
                args.append(new_arg)
            except StopIteration:
                    self.robot_say_message(
                    " ".join([
                        f"Sorry, '{command[0]}'",
                        f"needs {len(command_args)}",
                        "arguments"
                    ]),
                    f"{self.name}: "
                )
        #organising optional args
        for arg_type in command_opt:
            try:
                new_arg = self.convert_command_args(arg_type, command_iter)
                if new_arg != None:
                    args.append(new_arg)
            except StopIteration:
                ... 
        #checking if theres an arg overflow
        try:
            next(command_iter)  
        except StopIteration:
            return [command[0]] + args
        self.robot_say_message(
                        " ".join([
                            f"Sorry, '{command[0]}'",
                            f"needs {len(command_args)}",
                            "arguments and, optionally, another",
                            f"{len(command_opt)} arguments.",
                            "You have too many arguments."
                        ]),
                        f"{self.name}: "
                    )
        return False   


    def robot_get_command(self):
        """
        Continuosly asks for a valid command until one is given.

        Returns:
            list: contains a valid uppercase command 
            and the necessary arguments in their correct types.
        """
        self.robot_say_message(
                "What must I do next? ",
                f"{self.name}: ",
                end=""
            )
        command = self.command_valid(input().strip().split(" "))
        if  not command:
            return self.robot_get_command()
        return [command[0].upper(), *command[1:]] \
                if len(command) > 1 else command


    def command_forward(self, steps:int):
        """
        Moves robot forward and displays appropriate messages.

        Args:
            steps (int): The distance the robot moves.
        """
        self.robot_move(abs(steps))
        self.robot_report_position()
        

    def command_back(self, steps:int):
        """
        Moves robot back and displays appropriate messages.

        Args:
            steps (int): The distance the robot moves.
        """
        self.robot_move(-abs(steps))
        self.robot_report_position()


    def command_turn_right(self, degrees:int = 90):
        """
        Rotates robot 90° to the right
        and displays appropriate messages.

        Args:
            degrees (int): The amount the robot turns in degrees. 
            Defaults to 90.
        """
        self.rotation += degrees
        while self.rotation >= 360:  
            self.rotation -= 360

        self.robot_say_message(
            "turned right.",
            f" > {self.name} " 
        )
        self.robot_report_position()


    def command_turn_left(self, degrees:int = 90):
        """
        Rotates robot 90° to the left
        and displays appropriate messages.

        Args:
            degrees (int): The amount the robot turns in degrees. 
            Defaults to 90.
        """
        self.rotation -= degrees
        while self.rotation < 0:  
            self.rotation += 360

        self.robot_say_message(
            "turned left.",
            f" > {self.name} "
        )
        self.robot_report_position()


    def command_sprint(self, steps:int):
        """
        Recursively moves the robot.

        Args:
            steps (int): The ditance the robot moves.
        """
        if  steps != 0 and self.robot_move(steps):
            self.command_sprint(steps + (-1 if steps > 0 else 1))
        else:
            self.robot_report_position()


    def command_off(self):
        """
        Exits and displays appropriate message.
        """
        self.robot_say_message(
            "Shutting down..",
            f"{self.name}: "
        )
        raise SystemExit
        

    def command_help(self):
        """
        Robot displays a detailed list of all the commands available.
        """
        self.robot_say_message("I can understand these commands:")
        for key, value in self.command_dict.items():
            #test_main is stupid
            spaces = "  " if key == "OFF" else " " if key == "HELP" else "\t"
            self.robot_say_message(f"{key}{spaces}- {value['description']}")


    def replay_valid_args(self, command_arguments:str):
        processed_args = {
            'silent'    : False,
            'reversed'  : True if 'reversed' in command_arguments else False,
            'range'     : [0, len(self.history)]
        }
        #I need to tighten this up tmoro
        command_arguments = command_arguments.lower()

        for key in processed_args.keys():
            if  key in command_arguments:
                processed_args[key] = True
                command_arguments = command_arguments.replace(key, '').strip()

        flag = False
        if command_arguments != '':
            for char in command_arguments:
                if  not (char.isnumeric()):          
                    return False
                if  flag and char == '-':
                    return False
                if  char == '-':
                    flag = True
                    continue
            if  command_arguments[0] == '-' or command_arguments[-1] == '-':
                return False

            if  '-' in command_arguments:
                processed_args["range"][0] = int(
                    command_arguments[:command_arguments.find('-')]
                )
                processed_args["range"][1] = int(
                    command_arguments[command_arguments.find('-')+1:]
                )
            else:
                processed_args["range"][1] = int(
                    command_arguments
                )
            if  not (0 < processed_args['range'][0] < processed_args['range'][1]\
                and 0 < processed_args['range'][1] <= len(self.history)):
                return False
        
        return processed_args


    def command_replay(self, command_arguments:str=""):
        processed_args = self.replay_valid_args(command_arguments)
        if not processed_args:
            raise TypeError("Arguments for 'REPLAY' are invalid")
        if processed_args['silent']:
            self.messages_enabled = False
        if processed_args['reversed']:
            ...
        for command in self.history[
                processed_args['range'][0]:processed_args['range'][1]
            ]:
            if  len(command) > 1:
                self.command_dict[command[0]]["command"](*command[1:])   
            else:
                self.command_dict[command[0]]["command"]() 

        self.messages_enabled = True
        self.robot_say_message(
            ''.join([
                "replayed",
                f" {processed_args['range'][1]-processed_args['range'][0]}",
                " commands",
                " in reverse" if processed_args['reversed'] else '',
                " silently" if processed_args['silent'] else '',
                '.'
            ]),
            f" > {self.name} "
        )
        self.robot_report_position()


    def robot_execute_command(self, command:list):
        """
        Executes a specific command available to the robot

        Args:
            command (list): contains a valid uppercase command 
            and the necessary arguments in their correct types.
        """
        if  self.command_dict[command[0]]["history"]:
            self.history.append(command)

        if  len(command) > 1:
            self.command_dict[command[0]]["command"](*command[1:])   
        else:
            self.command_dict[command[0]]["command"]() 

    
    def __init__(self, name:str = "", position:tuple = (0,0),
                 rotation:int = 0) -> None:
        """
        Constructor that sets the default values for the robot
        when a new instance of it is created.

        Args:
            name (str, optional): Robot's name. Defaults to "".
            position (tuple, optional): Starting position. Defaults to (0,0).
            rotation (int, optional): Starting direction. Defaults to 0.
        """
        self.history = list()
        self.bounds = ((-100, 100), (-200, 200))
        self.position = position
        self.rotation = rotation
        self.name = name
        self.messages_enabled = True

        """
        Rules for command_dict commands:
            * The key is the command word.
            * The item is a dictionary:
                * requires "description" with a relevant explanation.
                * requires "command" that equals the relevant method.
                * requires "history" for if it will be stored in robot history.
                * optional "args" if it needs any arguments, a list of types.
                    * if an str type is needed:
                        * have it at the end.
                        * have no optional arguments.
                        * have only one str argument.
                * optional "opt" if it has any optional arguments.
                    * if an str type is needed:
                        * have it at the end.
                        * have only one str argument.
        """
        self.command_dict = {
        "OFF"       : { "description" : "Shut down robot",
                        "command" : self.command_off ,
                        "history" : False},

        "HELP"      : { "description" : "provide information about commands", 
                        "command" : self.command_help, 
                        "history" : False},

        "FORWARD"   : { "description" : "Move robot foward by [number] steps", 
                        "command" : self.command_forward, 
                        "args" : [int],
                        "history" : True},

        "BACK"      : { "description" : "Move robot back by [number] steps", 
                        "command" : self.command_back, 
                        "args" : [int],
                        "history" : True},

        "RIGHT"     : { "description" : "Rotate robot right", 
                        "command" : self.command_turn_right, 
                        "history" : True},    

        "LEFT"      : { "description" : "Rotate robot left", 
                        "command" : self.command_turn_left, 
                        "history" : True},

        "SPRINT"    : { "description" : "Move robot foward by [number] steps", 
                        "command" : self.command_sprint, 
                        "args" : [int],
                        "history" : True},       

        "REPLAY"    : { "description" : "Redoes all previous movement commands", 
                        "command" : self.command_replay, 
                        "optional" : [str],
                        "history" : False},            
        }