"""app/commands/__init__.py
This module defines the core command pattern implementations including the base Command class
and the CommandHandler for managing and executing commands. It enables the application to
extend its functionality dynamically through commands, facilitating a plugin architecture.
"""
import logging

class Command:
    """
    A base class for all command plugins, providing essential metadata for dynamic command 
    registration and display in menus or help documentation.

    Attributes:
        name (str): The command's unique name, used for invocation and identification.
        description (str): A brief description of what the command does, used for help documentation.
    """
    def __init__(self):
        """Constructor for command class"""
        self.name = ""  # Command name for menu display
        self.description = ""  # Command description for menu display

    def execute(self, *args, **kwargs):
        """
        The method to execute the command's logic. This method should be overridden in subclasses.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Command execution not implemented.")

class CommandHandler:
    """
    Manages registration and execution of commands within the application. It acts as a central 
    repository of commands, facilitating command lookup and execution based on user input.
    """
    def __init__(self):
        self.commands = {} # A dictionary to store command instances keyed by their names.

    def register_command(self, command):
        """
        Registers a command instance with the command handler.

        Args:
            command (Command): The command instance to register.

        Notes:
            If a command with the same name is already registered, it will be overwritten,
            and a warning message will be printed.
        """
        if command.name in self.commands:
            logging.warning(f"Command '{command.name}' is already registered. Overwriting.")
        self.commands[command.name] = command
        logging.info(f"Command '{command.name}' registered successfully.")

    def get_commands(self):
        """
        Returns a list of tuples containing the command names and descriptions for all registered commands.

        Returns:
            List[Tuple[str, str]]: A list of command metadata.
        """
        return [(cmd.name, cmd.description) for cmd in self.commands.values()]

    def execute_command(self, name, *args):
        """
        Executes a command by name, passing along any arguments to the command's execute method.

        Args:
            name (str): The name of the command to execute.
            *args: Arguments to pass to the command's execute method.

        Notes:
            If the command is not found, a not found message will be printed. Exceptions raised
            during command execution are caught and printed as error messages.
        """
        command = self.commands.get(name)
        if not command:
            logging.error(f"Command '{name}' not found.")
            raise KeyError
        try:
            command.execute(*args)
        except Exception as e:
            logging.error(f"Error executing command '{name}': {e}")
