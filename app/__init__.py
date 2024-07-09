"""app/__init__.py
This module provides an interactive command-line interface (CLI) for performing arithmetic operations
and other actions through a plug-and-play command system. The App class orchestrates the loading of
command plugins, registering them for use, and handling user input to execute commands dynamically.
"""
import os
import pkgutil
import importlib
import sys
from dotenv import load_dotenv
import logging.config
from app.commands import Command, CommandHandler

class App:
    """
    The main application class for the CLI tool. It handles the initialization of the command environment,
    loading of plugins, and the main application REPL for processing user input.
    """

    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.command_handler = CommandHandler()

    def configure_logging(self):
        """
        Configures application logging based on an external configuration (logging.conf) file or 
        fallback defaults.

        This method attempts to configure logging settings by reading a 'logging.conf' file. If the
        configuration file does not exist, it sets up a basic logging configuration with a default
        logging level of INFO and a simple message format. This ensures that logging is available
        for capturing runtime information and errors, enhancing the application's observability.

        The method creates a log entry once logging is configured, signifying that the application
        is ready to log further events.
        """
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        """
        Loads all environment variables into the application's settings.

        This method utilizes the os.environ dictionary to fetch all available environment
        variables and stores them in the `self.settings` dictionary. It's called during
        the initialization phase of the application to ensure that all settings are loaded
        and accessible throughout the application lifecycle.

        Returns:
            dict: A dictionary containing all environment variables as key-value pairs.
        """
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings
    
    def get_environment_variable(self, env_var: str = 'ENVIRONMENT', default_value = None):
        """
        Retrieves the value of a specified environment variable from the application's settings.

        If the environment variable is not found within the application's settings, this method
        returns a default value if one is specified. This functionality is crucial for accessing
        configuration values that may vary between development, testing, and production environments.

        Args:
            env_var (str): The name of the environment variable to retrieve. Defaults to 'ENVIRONMENT'.
            default_value (Optional[Any]): The default value to return if the environment variable
                                        is not found. Defaults to None.

        Returns:
            The value of the environment variable if it exists, otherwise the specified default value.
        """
        return self.settings.get(env_var, default_value)

    def load_plugins(self):
        """
        Loads command plugins from the designated plugins directory, registering each discovered command
        with the command handler.
        """
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found.")
            return
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")
                except Exception as e:
                    logging.error(f"Error loading plugin {plugin_name}: {e}")

    def register_plugin_commands(self, plugin_module):
        """
        Registers commands found within a plugin module with the command handler.

        Args:
            plugin_module: The module object representing a plugin, from which commands will be extracted
                           and registered.

        Notes:
            This method looks for classes within the module that are subclasses of the Command base class
            (but not Command itself) and instantiates and registers each as a command with the CommandHandler.
            It prints a message upon successful registration of each command.
        """
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                command_instance = item()
                self.command_handler.register_command(command_instance)
                logging.info(f"Command '{command_instance.name}' from plugin '{command_instance.name}' registered.")

    def start(self):
        """
        Starts the application's REPL loop, dynamically loading plugins and awaiting user commands.

        This method first loads available command plugins, then enters a loop to process user input,
        invoking commands based on the input provided. Special commands include 'exit' to terminate the application
        and 'show_menu' to display available commands.
        """
        self.load_plugins()
        # Dynamically generate and register the menu command
        dynamic_menu_command = DynamicMenuCommand(self.command_handler)
        self.command_handler.register_command(dynamic_menu_command)

        logging.info("Application started. Type 'show_menu' to see the menu or 'exit' to exit.\n")
        try:
            while True:
                cmd_input = input(">>> ")
                if cmd_input.lower() == "exit":
                    logging.info("Application exit.")
                    sys.exit(0)
                elif cmd_input == '':
                    # If the input is empty, show the dynamic menu of commands
                    self.command_handler.execute_command("show_menu") # Execute the show_menu command
                else:
                    try:
                        cmd_name, *args = cmd_input.split()
                        self.command_handler.execute_command(cmd_name, *args)
                    except KeyError:
                        logging.error(f"Unknown command: {cmd_input}")
                        self.command_handler.execute_command("show_menu") # Show menu if unknown command
        except KeyboardInterrupt:
            logging.info("Application interrupted and exiting gracefully.")
            sys.exit(0) # Assuming a KeyboardInterrupt should also result in a clean exit.
        finally:
            logging.info("Application shutdown.")

class DynamicMenuCommand(Command):
    """
    A special command for displaying a dynamic menu of all registered commands, providing users with
    information about available operations and their descriptions.
    """
    def __init__(self, command_handler):
        super().__init__()
        self.name = "show_menu"
        self.description = "Show the dynamic menu of all commands."
        self.command_handler = command_handler

    def execute(self, *args, **kwargs):
        """
        Executes the command to display a dynamic menu listing all registered commands and their descriptions.

        Args:
            *args: Ignored for this command.
            **kwargs: Ignored for this command.

        Outputs:
            Prints a formatted list of command names and their descriptions to the console.
        """
        commands = self.command_handler.get_commands()
        menu = "Application Menu:\n"
        for name, description in commands:
            menu += f"\t{name}: {description}\n"
        print(menu)
        logging.info("Displayed the dynamic menu of commands to the user.")
