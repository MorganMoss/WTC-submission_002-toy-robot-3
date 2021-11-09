import math

class BaseRobot():
    """
    An instance of this class is a robot that can be 
    controlled via commands and sends messages to the console.
        * Only robot_... methods should be called
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
    
    
    def robot_get_name(self):
        """
        Sets robots name to a given input.
        """
        self.robot_say_message("What do you want to name your robot? ", end="")
        self.name = input()


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
        Moves the robot and then the robot
        sends a message saying it has done so.

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
        
    
    def robot_rotate(self, angle:int):
        """
        Rotates robot by <angle> degrees.

        Args:
            angle (int): degrees to be rotated.
        """
        direction =  'right' if angle > 0 else 'left'

        self.rotation = (self.rotation + angle)%360


        self.robot_say_message(
            f"turned {direction}.",
            f" > {self.name} "
        )

        self.robot_report_position()


    def __init__(self) -> None:
        """
        Constructor that sets the default values for the robot
        when a new instance of it is created.

        Args:
            name (str, optional): Robot's name. Defaults to "".
            position (tuple, optional): Starting position. Defaults to (0,0).
            rotation (int, optional): Starting direction. Defaults to 0.
        """
        self.bounds:tuple = ((-100, 100), (-200, 200))
        self.position:tuple = (0,0)
        self.rotation:int = 0
        self.name:str = ''
        self.messages_enabled:bool = True
