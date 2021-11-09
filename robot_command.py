from robot_base import BaseRobot

class CommandRobot(BaseRobot):      
    """
    This class inherits from the base class and implements
    commands for the robot.
    """


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


    def command_replay(self, processed_args:dict):
        """
        Replays all previous movement and rotation commands in a range.

        Args:
            processed_args (dict): The processed string argument
                Contains:
                    * 'silent' (bool): Whether or not you want 
                    the robot to show output from replayed commands
                    * 'reversed (bool): If you want to go through the history
                    from first to last (False) or last to first (True)
                    * 'range' (range): The range of history that repaly will
                    call commands from.
        """
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
            
        getattr(
            self,
            self.command_dict[command[0].upper()]["command"]
        )(*command[1:])


    def __init__(self) -> None:
        """
        Contructor for CommandRobot, initializes a dictionary 
        containing all the commands above,
        with descriptions and arguments
        It also creates an empty history list 
        and calls the BaseRobot constructor.
        """
        super().__init__()
        self.history:list = list()
        """
        Rules for command_dict commands:
            * The key is the command word (in caps!).
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
        "OFF"       : { "description": "Shut down robot",
                        "command": "command_off" ,
                        "history": False},

        "HELP"      : { "description": "provide information about commands", 
                        "command": "command_help", 
                        "history": False},

        "FORWARD"   : { "description": "Move robot foward by [number] steps", 
                        "command": "command_forward", 
                        "args": [int],
                        "history": True},

        "BACK"      : { "description": "Move robot back by [number] steps", 
                        "command": "command_back", 
                        "args": [int],
                        "history": True},

        "RIGHT"     : { "description": "Rotate robot right", 
                        "command": "command_turn_right", 
                        "history": True},    

        "LEFT"      : { "description": "Rotate robot left", 
                        "command": "command_turn_left", 
                        "history": True},

        "SPRINT"    : { "description": "Move robot foward by [number] steps, "+
                        "then [number]-1 steps, and so on, until it hits 0.", 
                        "command": "command_sprint", 
                        "args": [int],
                        "history": True},       

        "REPLAY"    : { "description": "Replays previous movement commands.\n"+
                        "\t  It has optional arguments:"+
                        "\n\t\tSilent - Hides output from replayed commands"+
                        "\n\t\tReversed - Reverses the order to be last to first"+
                        "\n\t\t<int> - Starts from previous <int> commands"+
                        "\n\t\t<int>-<int> - Starts from previous <int> "+
                        "commands and ends at <int> previous commands", 
                        "command": "command_replay", 
                        "optional": [str],
                        "history": False},            
        }
