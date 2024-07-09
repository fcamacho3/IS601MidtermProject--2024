"""app/plugins/subtract/__init__.py
This module defines the SubtractCommand class for performing subtraction operations. It extends the Command
base class, inheriting its interface for integration into the application's command structure.
"""
from app.commands import Command
from app.plugins import execute_operation
import logging

class SubtractCommand(Command):
    """
    A command for subtracting one number from another. This class provides the logic to execute the subtraction
    operation from user input.
    """
    def __init__(self):
        super().__init__()
        self.name = "subtract"
        self.description = "Subtract two numbers from one another."

    def execute(self, *args):
        """
        Executes the subtraction operation. Prompts the user for two numbers to subtract and displays the result.
        """
        logging.info("Executing subtraction command")
        user_input_prompt = "Operation: Subtraction\n"
        execute_operation(user_input_prompt, self.name)
