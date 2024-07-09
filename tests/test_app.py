"""tests/test_app.py"""
import logging
from unittest.mock import patch, MagicMock
import pytest
from app import App
from app import DynamicMenuCommand
from app.commands import CommandHandler

@pytest.fixture
def app_instance():
    '''Create an instance of the app'''
    return App()

# Tests for configure_logging
def test_configure_logging_with_logging_conf(app_instance): # This test does not contribute to coverage
    '''Tests configure_logging with logging configuration file.'''
    # Patch os.path.exists to return True and mock fileConfig
    with patch('os.path.exists', return_value=True), \
        patch('logging.config.fileConfig') as mock_file_config:

        # Call configure_logging method which should trigger fileConfig
        app_instance.configure_logging()

        # Assert that fileConfig is called once with the correct arguments
        mock_file_config.assert_called_once_with('logging.conf', disable_existing_loggers=False)

def test_configure_logging_without_logging_conf(app_instance, caplog):
    '''Test configure_logging when logging.conf file doesn't exist'''
    # Mock the absence of the logging.conf file
    with patch('os.path.exists', return_value=False):
        # Call the configure_logging method
        app_instance.configure_logging()

    # Check if the logging configuration is set to INFO level and if the message is logged
    assert logging.getLogger().getEffectiveLevel() == logging.INFO, \
       "Logging level is not set to INFO when logging.conf is missing"
    assert "Logging configured." in caplog.text, "Expected message 'Logging configured.' in log output"

# Tests for get_environment_variables
@pytest.mark.parametrize("env_var, expected_result", [
    ('ENVIRONMENT', 'TEST'),
    ('ANOTHER_ENV', 'DEFAULT')
])
def test_get_environment_variable(app_instance, env_var, expected_result):
    '''Test getting environment variables'''
    app_instance.settings = {'ENVIRONMENT': 'TEST'}
    result = app_instance.get_environment_variable(env_var, 'DEFAULT')
    assert result == expected_result, f"Expected result '{expected_result}' but got '{result}'"

# Tests for load_plugins method
@pytest.mark.parametrize("plugin_modules, expected_commands", [
    ([('add', 'add', True), ('subtract', 'subtract', True)], ['add', 'subtract']),
    ([], [])  # No plugin modules
])
def test_load_plugins_with_existing_plugins(app_instance, plugin_modules, expected_commands):
    '''Mock the plugin directory structure to simulate the presence of existing plugins'''
    with patch('os.path.exists', return_value=True):
        # Simulate the presence of existing plugin modules by providing their names
        with patch('pkgutil.iter_modules') as mock_iter_modules:
            mock_iter_modules.return_value = plugin_modules

            # Call the load_plugins method to load the existing plugins
            app_instance.load_plugins()

    # Assert that commands from the existing plugins are registered
    assert len(app_instance.command_handler.commands) == len(expected_commands), \
       f"Expected {len(expected_commands)} commands but found {len(app_instance.command_handler.commands)}"
    for command in expected_commands:
        assert command in app_instance.command_handler.commands, \
           f"Expected command '{command}' to be registered but it was not found."

def test_load_plugins_without_plugins_directory(app_instance, caplog):
    '''Test loading plugins when the plugins directory does not exist'''
    # Mock the absence of the plugins directory
    with patch('os.path.exists', return_value=False):
        # Call the load_plugins method
        app_instance.load_plugins()

    # Check if a warning message is logged
    assert "Plugins directory 'app/plugins' not found." in caplog.text, \
       "Expected warning message about missing plugins directory."

def test_load_plugins_with_import_error(app_instance, caplog):
    '''Test loading plugins when there is an ImportError'''
    # Mock the existence of the plugins directory
    with patch('os.path.exists', return_value=True):
        # Simulate an ImportError when importing a plugin module
        with patch('app.importlib.import_module') as mock_import_module:
            mock_import_module.side_effect = ImportError('Simulated ImportError')

            # Call the load_plugins method
            app_instance.load_plugins()

    # Check if an error message is logged
    assert "Error importing plugin" in caplog.text, "Expected 'Error importing plugin' message in logs"

def test_load_plugins_with_other_exception(app_instance, caplog):
    '''Test loading plugins when there is an exception other than ImportError'''
    # Mock the existence of the plugins directory
    with patch('os.path.exists', return_value=True): # pylint: disable=logging-fstring-interpolation
        # Simulate an exception other than ImportError when importing a plugin module
        with patch('app.importlib.import_module') as mock_import_module:
            mock_import_module.side_effect = Exception('Simulated Exception')

            # Call the load_plugins method
            app_instance.load_plugins()

    # Check if an error message is logged
    assert "Error loading plugin" in caplog.text, "Expected 'Error loading plugin' message in logs"

# Tests for start method
def test_start_application(app_instance, capsys):
    '''Test the behavior of starting the application'''
    # Simulate starting the application
    with patch('builtins.input', side_effect=['exit']):
        with pytest.raises(SystemExit) as ex:  # Expect SystemExit to be raised
            app_instance.start()

    # Assert the exit code
    assert ex.value.code == 0, f"Expected exit code 0 but got {ex.value.code}"

def test_keyboard_interrupt_graceful_shutdown(app_instance, caplog):
    '''Test graceful shutdown on keyboard interrupt'''
    with patch('builtins.input', side_effect=KeyboardInterrupt), \
         pytest.raises(SystemExit) as ex:
        app_instance.start()

    assert ex.value.code == 0, "Expected exit code 0 for graceful shutdown"
    assert "Application interrupted and exiting gracefully." in caplog.text, "Expected log message for keyboard interrupt"
    assert "Application shutdown." in caplog.text, "Expected log message for application shutdown"

def test_dynamic_menu_command_execute_prints_menu():
    """
    Test that DynamicMenuCommand execute method prints the menu correctly 
    and logs the appropriate message.
    """
    # Mocking the command handler
    command_handler_mock = MagicMock(spec=CommandHandler)
    command_handler_mock.get_commands.return_value = [("command1", "Description 1"), ("command2", "Description 2")]

    # Creating an instance of DynamicMenuCommand with the mocked command handler
    dynamic_menu_command = DynamicMenuCommand(command_handler_mock)

    # Capturing the printed menu
    with patch('builtins.print') as print_mock:
        dynamic_menu_command.execute()

    # Asserting the printed menu content
    expected_menu = "Application Menu:\n\tcommand1: Description 1\n\tcommand2: Description 2\n"
    print_mock.assert_called_once_with(expected_menu)

    # Asserting the logging call
    command_handler_mock.get_commands.assert_called_once()


def test_start_unknown_command_ok(app_instance, caplog):
    '''Test behavior when an unknown command is entered'''
    # Mocking command_handler to raise KeyError for unknown commands
    app_instance.command_handler.execute_command = MagicMock(side_effect=lambda cmd_name, *args: logging.error(f"Unknown command: {cmd_name}")) # pylint: disable=logging-fstring-interpolation

    # Simulate user input of an unknown command
    with patch('builtins.input', side_effect=['unknown_command', 'exit']):
        # Catch the SystemExit exception
        with pytest.raises(SystemExit) as ex: # pylint: disable=unused-variable
            app_instance.start()

    # Check if the KeyError is logged
    assert "Unknown command: unknown_command" in caplog.text, \
        "Expected log message for unknown command"
