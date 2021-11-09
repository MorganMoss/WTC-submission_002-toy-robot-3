
class InputError(Exception):
    """
    Raised if the user enters a bad command
    """
    def __init__(self, command:list=[], *args: object) -> None:
        """
        Creates a default message for the error using the users command.
        
        Args:
            command (list, optional): The user command. Defaults to [].
        """
        if isinstance(command, list):
            super().__init__(
                f"Sorry, I did not understand '{' '.join(command)}'.",
                *args
            )
        else:
            super().__init__(command)