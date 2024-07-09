"""app/plugins/multiply/__init__.py
This module defines the MultiplyCommand class for performing multiplication operations. It extends the Command
base class, inheriting its interface for integration into the application's command structure.
"""
from app.commands import Command
from app.plugins import execute_operation
import logging

class MultiplyCommand(Command):
    """
    A command for multiplying two numbers. This class provides the logic to execute the multiplication
    operation from user input.
    """
    def __init__(self):
        super().__init__()
        self.name = "multiply"
        self.description = "Multiply two numbers together."

    def execute(self, *args):
        """
        Executes the multiplication operation. Prompts the user for two numbers to multiply together
        and displays the result.
        """
        logging.info("Executing multiplication command")
        user_input_prompt = "Operation: Multiplication\n"
        execute_operation(user_input_prompt, self.name)
