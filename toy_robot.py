from command_handling import CommandHandler
from exceptions import InputError


class ToyRobot(CommandHandler):
    """
    This class uses the Command Handler class
    to be able to execute commands on the robot via user input.
    """


    def cmd(self):
        """
        Receives and executes a user input command.
        """
        self.robot_say_message(
            "What must I do next? ",
            f"{self.name}: ",
            end=""
        )
        try:
            command = CommandHandler.get_command(self)
            self.exec_command(command)
        except InputError as e:
                self.robot_say_message(str(e), f"{self.name}: ")
                

    def start(self):
        """ 
        Gets the robot to ask for a name and say hello.
        """
        self.robot_get_name()
        self.robot_say_message(
            "Hello kiddo!", 
            f"{self.name}: "
        )   


    def __init__(self) -> None:
        """
        Constructor for ToyRobot, calls CommandHandler's constructor.
        """
        super().__init__()
        

