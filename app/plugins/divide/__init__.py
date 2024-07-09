"""app/plugins/divide/__init__.py
This module defines the DivideCommand class for performing division operations. It extends the Command
base class, inheriting its interface for integration into the application's command structure.
"""
from app.commands import Command
from app.plugins import execute_operation
import logging

class DivideCommand(Command):
    """
    A command for dividing one number by another. This class provides the logic to execute the division
    operation from user input.
    """
    def __init__(self):
        super().__init__()
        self.name = "divide"
        self.description = "Divide two numbers from one another."

    def execute(self, *args):
        """
        Executes the division operation. Prompts the user for two numbers to divide and displays the result.
        """
        logging.info("Executing division command")
        user_input_prompt = "Operation: Division\n"
        execute_operation(user_input_prompt, self.name)
