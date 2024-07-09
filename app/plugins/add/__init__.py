"""app/plugins/add/__init__.py
This module defines the AddCommand class for performing addition operations. It extends the Command
base class, inheriting its interface for integration into the application's command structure.
"""
from app.commands import Command
from app.plugins import execute_operation
import logging

class AddCommand(Command):
    """
    A command for adding two numbers. This class provides the logic to execute the addition
    operation from user input.
    """
    def __init__(self):
        super().__init__()
        self.name = "add"
        self.description = "Add two numbers together."

    def execute(self, *args):
        """
        Executes the addition operation. Prompts the user for two numbers to add together
        and displays the result.
        """
        logging.info("Executing addition command")
        user_input_prompt = "Operation: Addition\n"
        execute_operation(user_input_prompt, self.name)
