
class InputError(Exception):
    """
    Raised if the user enters a bad command
    """
    ...

class ValidationError(Exception):
    """
    Raised if a validation step fails
    """
    ...