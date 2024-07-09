"""test plugins"""
from unittest.mock import patch
import unittest
import pytest
from app.commands import CommandHandler
from app.plugins.add import AddCommand
from app.plugins.subtract import SubtractCommand
from app.plugins.divide import DivideCommand
from app.plugins.multiply import MultiplyCommand
from app.plugins import execute_operation, parse_input

class TestPluginCommands(unittest.TestCase):
    """Tests for plugins/__init__.py"""

    def _test_command_registration_and_execution(self, command_cls, input_value, expected_result):
        """Helper function for testing command registration and execution."""
        command_handler = CommandHandler()
        command = command_cls()
        command_handler.register_command(command)

        # Check command registration
        self.assertIn(command.name, command_handler.commands)

        with patch('builtins.input', side_effect=[input_value, 'exit']), patch('builtins.print') as mock_print:
            command.execute()
            # Verify interaction
            result_found = any(expected_result in call_args[0][0] for call_args in mock_print.call_args_list)
            self.assertTrue(result_found, f"Expected result printout not found in any print call for {command.name} command.")

    def test_add_command_registration_and_execution(self):
        """
        Test that the AddCommand is correctly registered and executed.
        """
        self._test_command_registration_and_execution(AddCommand, '5 3', "The result of 5 add 3 is equal to 8")

    def test_subtract_command_registration_and_execution(self):
        """
        Test that the SubtractCommand is correctly registered and executed.
        """
        self._test_command_registration_and_execution(SubtractCommand, '5 3', "The result of 5 subtract 3 is equal to 2")

    def test_divide_command_registration_and_execution(self):
        """
        Test that the DivideCommand is correctly registered and executed.
        """
        self._test_command_registration_and_execution(DivideCommand, '4 2', "The result of 4 divide 2 is equal to 2")

    def test_multiply_command_registration_and_execution(self):
        """
        Test that the MultiplyCommand is correctly registered and executed.
        """
        self._test_command_registration_and_execution(MultiplyCommand, '2 2', "The result of 2 multiply 2 is equal to 4")

    @patch('builtins.input', side_effect=['1 2 3', 'exit'])
    @patch('builtins.print')
    def test_execute_operation_with_invalid_input(self, mock_print, mock_input):
        """
        Test `execute_operation` with more than two operands to ensure it handles
        the exception raised by `parse_input` and provides the correct user feedback.
        """
        execute_operation("Performing a test operation.", "test")

        # Extract all print calls into a list of strings.
        printed_messages = [call_args[0][0] for call_args in mock_print.call_args_list]

        # Check if the error message is in any of the printed messages.
        self.assertTrue(any("Invalid input format. Please use: <operand1> <operand2>" in message for message in printed_messages), "Expected error message not found in any print call.")

# Parsing tests
def test_parse_input_valid():
    """Test parsing valid input."""
    user_input = "2 3"
    expected_result = ("2", "3")
    assert parse_input(user_input) == expected_result

def test_parse_input_invalid_format():
    """Test parsing input with invalid format."""
    user_input = "2 3 4"
    with pytest.raises(ValueError):
        parse_input(user_input)

def test_parse_input_empty():
    """Test parsing empty input."""
    user_input = ""
    with pytest.raises(ValueError):
        parse_input(user_input)
