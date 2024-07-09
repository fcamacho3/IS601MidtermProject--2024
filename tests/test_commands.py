"""tests/test_commands.py
Test suite for the Command and CommandHandler classes in the app.commands module.

These tests validate the functionality related to command registration, execution,
and error handling within a dynamic command-driven application architecture.
"""
from unittest.mock import patch
import logging
import pytest
from app.commands import Command, CommandHandler

# Mock command class for testing
class MockCommand(Command):
    """
    A mock command class for testing, inheriting from the Command base class.
    Allows setting of name and description upon instantiation and provides a basic
    execute method.
    """
    def __init__(self, name, description=""):
        """constructor"""
        super().__init__()
        self.name = name
        self.description = description

    def execute(self, *args, **kwargs):
        """necessary for MockCommand"""
        return f"Executed {self.name}" # pragma: no cover

@pytest.fixture
def command_handler():
    """Fixture to provide a fresh instance of CommandHandler for each test."""
    return CommandHandler()

def test_register_command(command_handler):
    """
    Test that a command can be successfully registered within the CommandHandler.
    """
    command1 = MockCommand("test1", "Test Command 1")
    command_handler.register_command(command1)
    assert "test1" in command_handler.commands
    assert command_handler.commands["test1"].description == "Test Command 1"

def test_register_duplicate_command(caplog, command_handler):
    """
    Verify that registering a command with a duplicate name logs a warning.
    """
    command1 = MockCommand("test1")
    command2 = MockCommand("test1")
    command_handler.register_command(command1)
    with caplog.at_level(logging.WARNING):
        command_handler.register_command(command2)
    assert "overwriting" in caplog.text.lower()

def test_get_commands(command_handler):
    """
    Ensure that the get_commands method returns a correct list of registered commands.
    """
    command1 = MockCommand("test1", "Test Command 1")
    command2 = MockCommand("test2", "Test Command 2")
    command_handler.register_command(command1)
    command_handler.register_command(command2)
    commands = command_handler.get_commands()
    assert ("test1", "Test Command 1") in commands
    assert ("test2", "Test Command 2") in commands

def test_execute_command(command_handler):
    """
    Test the execution of a registered command through CommandHandler.
    """
    command1 = MockCommand("test1")
    command_handler.register_command(command1)
    with patch.object(MockCommand, "execute", return_value="Executed test1") as mock_execute:
        command_handler.execute_command("test1")
        mock_execute.assert_called_once()

def test_execute_nonexistent_command(caplog, command_handler):
    """
    Verify that attempting to execute a non-existent command logs an appropriate error.
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(KeyError):  # Expecting KeyError to be raised
            command_handler.execute_command("nonexistent")
    assert "not found" in caplog.text.lower()

def test_execute_command_error(caplog, command_handler):
    """
    Test that an error during command execution is logged correctly.
    """
    def mock_execute(*args, **kwargs):
        raise Exception("Test error")  # pylint: disable=broad-exception-raised

    command1 = MockCommand("test1")
    command1.execute = mock_execute
    command_handler.register_command(command1)

    with caplog.at_level(logging.ERROR):
        command_handler.execute_command("test1")
    assert "test error" in caplog.text.lower()

def test_command_execute_not_implemented():
    """
    Test that the execute method of the Command class raises a NotImplementedError
    if it has not been overridden in a subclass.
    """
    # Instantiate the base Command class directly
    cmd = Command()

    # Use pytest.raises to verify that NotImplementedError is raised when execute is called
    with pytest.raises(NotImplementedError) as exc_info:
        cmd.execute()

    # Optionally, assert on the message of the error, if specificity is needed
    assert "Command execution not implemented." in str(exc_info.value)
