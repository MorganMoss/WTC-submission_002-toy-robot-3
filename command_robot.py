from base_robot import BaseRobot
from exceptions import InputError, ValidationError

class CommandRobot(BaseRobot):      
    """
    This class inherits from the base class and implements
    commands for the robot.
    """

    def exec_command(self, command:list):
        """
        Executes a specific command available to the robot.
        
        Not necessary to call this function outside of this class.

        Args:
            command (list): contains a valid uppercase command 
            and the necessary arguments in their correct types.
        """
        if  self.command_dict[command[0].upper()]["history"]:
            self.history.append(command)

        if  len(command) > 1:
            self.command_dict[command[0].upper()]["command"](*command[1:])   
        else:
            self.command_dict[command[0].upper()]["command"]()


    def command_forward(self, steps:int):
        """
        Moves robot forward and displays appropriate messages.

        Args:
            steps (int): The distance the robot moves. Ignores negatives
        """
        self.robot_move(abs(steps))
        self.robot_report_position()
        

    def command_back(self, steps:int):
        """
        Moves robot back and displays appropriate messages.

        Args:
            steps (int): The distance the robot moves. Ignores positives
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
        self.robot_rotate(degrees)


    def command_turn_left(self, degrees:int = -90):
        """
        Rotates robot 90° to the left
        and displays appropriate messages.

        Args:
            degrees (int): The amount the robot turns in degrees. 
            Defaults to -90.
        """
        self.robot_rotate(degrees)
        

    def command_sprint(self, steps:int):
        """
        Recursively moves the robot forward.

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
            spaces = "  " if key == "OFF" else " " if key == "HELP" else "\t"
            self.robot_say_message(f"{key}{spaces}- {value['description']}")


    def replay_valid_args(self, command_arguments:str):
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
            raise ValidationError

        if  len(command_arguments) == 1:
            command_arguments = command_arguments[0].strip().split('-')

            if  not all(map(lambda arg : arg.isdigit(), command_arguments)):
                raise ValidationError
            if  len(command_arguments) > 2:
                raise ValidationError

            
            if len(command_arguments) == 2:
                start = h_size - int(command_arguments[0])
                stop = h_size - int(command_arguments[1])
            else:
                start = h_size - int(command_arguments[0])
                stop = h_size
            
            if  0 > start or start > stop or stop > h_size:
                raise ValidationError
        
            processed_args["range"] = range(start, stop)
       

        return processed_args

    #tighten and complete this too
    def command_replay(self, command_arguments:str=""):
        try:
            processed_args = self.replay_valid_args(command_arguments)
        except ValidationError:
            raise InputError

        if  processed_args['silent']:
            self.messages_enabled = False

        if  processed_args['reversed']:
            self.history.reverse()
        
        for index in processed_args['range']:
            command = self.history[index]
            self.exec_command(command)
            self.history.pop()

        if  processed_args['reversed']:
            self.history.reverse()

        self.messages_enabled = True
        self.robot_say_message(
            ''.join([
                "replayed",
                f" {len(list(processed_args['range']))}",
                " commands",
                " in reverse" if processed_args['reversed'] else '',
                " silently" if processed_args['silent'] else '',
                '.'
            ]),
            f" > {self.name} "
        )
        self.robot_report_position()


    
    def __init__(self) -> None:
        super().__init__()
        self.history:list = list()

        
        """
        Rules for command_dict commands:
            * The key is the command word.
            * The item is a dictionary:
                * requires "description" with a relevant explanation.
                * requires "command" that equals the relevant method in CommandRobot.
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
        self.command_dict:dict = {
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
                        "command" :  self.command_turn_right, 
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
