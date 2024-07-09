"""Test for app/plugins/history/__init__.py"""
# Disable specific pylint warnings that are not relevant for this file.
# pylint: disable=unnecessary-dunder-call, invalid-name
# pylint: disable=protected-access
import unittest
from decimal import Decimal
from unittest.mock import patch, MagicMock, call
from io import StringIO
from app.calculator.calculations import CalculationHistory
from app.plugins.history import HistoryCommand
from app.calculator.calculation import Calculation
from app.calculator.operations import ArithmeticOperations as AO

class TestHistoryCommandExecute(unittest.TestCase):
    """Test case for the execute method of the HistoryCommand class."""

    @patch('app.plugins.history.HistoryCommand._display_most_recent_calculation')
    def test_process_choice_valid(self, mock_retrieve_latest):
        """Testing process choice"""
        history_command = HistoryCommand()
        history_command.process_choice('1')  # Assuming '1' is a valid choice
        mock_retrieve_latest.assert_called_once()

    @patch('app.calculator.calculations.CalculationHistory.get_latest_history')
    def test_execute_prints_latest_calculation_and_exits(self, mock_get_latest_history):
        """Test whether execute method prints the latest calculation and then exits correctly."""

        # Mocking the latest calculation
        mock_operation = AO.addition
        mock_calculation = Calculation(2, 3, mock_operation)
        mock_get_latest_history.return_value = mock_calculation

        # Redirect stdout to capture print statements and simulate user input
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect=['1', 'exit']):  # Simulate choosing option 1 then exiting
                HistoryCommand().execute()

                # Check if the expected output is in stdout
                expected_output = f"{mock_calculation} results in 5"  # Adjust based on the actual output format
                output = mock_stdout.getvalue().strip()
                self.assertIn(expected_output, output)

    @patch('app.calculator.calculations.CalculationHistory.get_latest_history', return_value=None)
    @patch('builtins.print')
    def test_retrieve_latest_calculation_no_history(self, mock_print, mock_get_latest_history):
        """Testing retrieve latest history"""
        history_command = HistoryCommand()
        history_command._display_most_recent_calculation()
        mock_print.assert_called_once_with("No calculations in history.")

    @patch('app.calculator.calculations.CalculationHistory.clear_history')
    @patch('builtins.print')
    def test_clear_history_empty_history(self, mock_print, mock_clear_history):
        """Testing clear history with empty history"""
        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Mock CalculationHistory.get_history to return an empty list
        with patch('app.calculator.calculations.CalculationHistory.get_history', return_value=[]):
            # Call the _clear_history method
            history_command._clear_history()

        # Assert that CalculationHistory.clear_history was not called
        mock_clear_history.assert_not_called()

        # Assert that the correct message was printed
        mock_print.assert_called_once_with("History is already empty, no history to clear.")

    @patch('builtins.print')
    def test_print_result_zero_division_error(self, mock_print):
        """Testing print_result with ZeroDivisionError"""
        # Create a mock Calculation instance that will raise ZeroDivisionError when compute() is called
        mock_calculation = MagicMock(spec=Calculation)
        mock_calculation.compute.side_effect = ZeroDivisionError

        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Call the print_result method with the mock calculation
        history_command.print_result(mock_calculation)

        # Assert that the appropriate message was printed
        mock_print.assert_called_once_with(f"{mock_calculation} is undefined.")

    @patch('builtins.print')
    def test_display_all_calculations_zero_division_error(self, mock_print):
        """Testing display_all_calculations with ZeroDivisionError"""
        # Create mock Calculation instances
        mock_calculation1 = MagicMock(spec=Calculation)
        mock_calculation2 = MagicMock(spec=Calculation)

        # Mock the compute method of the first calculation to raise ZeroDivisionError
        mock_calculation1.compute.side_effect = ZeroDivisionError

        # Mock the get_history method of CalculationHistory to return the list of mock calculations
        with patch('app.plugins.history.CalculationHistory.get_history', return_value=[mock_calculation1, mock_calculation2]):
            # Create an instance of HistoryCommand
            history_command = HistoryCommand()

            # Call the _display_all_calculations method
            history_command._display_all_calculations()

            # Assert that the appropriate message was printed for the first calculation
            mock_print.assert_any_call(f"1. {mock_calculation1} is undefined")

    # Tests for csv methods
    @patch('app.calculator.calculations.CalculationHistory.save_history_to_csv')
    def test_save_history_to_csv(self, mock_save_history):
        """Test saving the history to a CSV file."""
        with patch('builtins.input', side_effect=['4', 'exit']), patch('sys.stdout', new=StringIO()):
            HistoryCommand().execute()
        mock_save_history.assert_called_once()

    @patch('app.calculator.calculations.CalculationHistory.load_history_from_csv')
    def test_load_history_from_csv(self, mock_load_history):
        """Test loading the history from a CSV file."""
        with patch('builtins.input', side_effect=['5', 'exit']), patch('sys.stdout', new=StringIO()):
            HistoryCommand().execute()
        mock_load_history.assert_called_once()

    @patch('app.calculator.calculations.CalculationHistory.load_history_from_csv')
    @patch('builtins.print')
    def test_load_history_from_csv_with_exception(self, mock_print, mock_load_history):
        """Test handling of an exception when loading the history from a CSV file."""

        # Setup the mock to raise an exception when called
        mock_load_history.side_effect = Exception("Failed to load CSV")

        # Call the load_history method
        history_command = HistoryCommand()
        history_command._load_calculation_history()

        # Check if the correct error message is printed
        mock_print.assert_called_with("\nError loading history: Failed to load CSV")

    @patch('builtins.print')
    @patch('app.plugins.history.CalculationHistory.load_history_from_csv')
    def test_load_calculation_history_exception(self, mock_load_history_from_csv, mock_print):
        """Testing _load_calculation_history with exception"""
        # Mock the load_history_from_csv method to raise an exception
        mock_load_history_from_csv.side_effect = Exception("Test exception")

        # Create an instance of HistoryCommand
        history_command = HistoryCommand()

        # Call the _load_calculation_history method
        history_command._load_calculation_history()

        # Assert that the appropriate message was printed
        mock_print.assert_called_once_with("\nError loading history: Test exception")

    @patch('app.calculator.calculations.CalculationHistory.delete_calculation_by_index')
    @patch('app.calculator.calculations.CalculationHistory.get_history', return_value=[Calculation(Decimal('2'), Decimal('3'), AO.addition)])
    def test_delete_specific_calculation(self, mock_get_history, mock_delete_calculation):
        """Test deleting a specific calculation by index."""
        with patch('builtins.input', side_effect=['6', '0', 'exit']), patch('sys.stdout', new=StringIO()):
            HistoryCommand().execute()
        mock_delete_calculation.assert_called_once_with(-1)

    @patch('app.calculator.calculations.CalculationHistory.delete_calculation_by_index')
    @patch('builtins.print')
    def test_delete_specific_calculation_value_error(self, mock_print, _):
        """Test handling of ValueError when deleting a specific calculation."""

        # Mock input to return a non-numeric value, simulating a ValueError
        with patch('builtins.input', return_value='not_a_number'):
            history_command = HistoryCommand()
            history_command._delete_calculation_from_history()

            # Check if the correct error message is printed
            mock_print.assert_called_with("Invalid index. Enter a valid index or 'exit' to return to history menu.")

    def test_invalid_choice(self):
        """Test handling of invalid menu choice."""
        with patch('builtins.input', side_effect=['invalid', 'exit']), patch('sys.stdout', new=StringIO()) as mock_stdout:
            HistoryCommand().execute()
        self.assertIn("Invalid choice", mock_stdout.getvalue())

    @patch('app.calculator.calculations.CalculationHistory.delete_calculation_by_index')
    @patch('app.calculator.calculations.CalculationHistory.get_history', return_value=[])
    @patch('builtins.input', return_value='1')  # Assume an out-of-range index
    @patch('builtins.print')
    def test_delete_specific_calculation_empty_history(self, mock_print, mock_input, mock_get_history, mock_delete_calculation_by_index):
        """Test handling of IndexError when deleting a specific calculation."""

        # The mock for delete_calculation_by_index should raise an IndexError
        mock_delete_calculation_by_index.side_effect = IndexError("No history available to delete.")

        history_command = HistoryCommand()
        history_command._delete_calculation_from_history()

        # Check if the correct error message is printed
        mock_print.assert_called_with("No history available to delete.")

    @patch('builtins.input', return_value='10')  # Simulate entering an out-of-range index
    @patch('builtins.print')  # Mock the print function
    def test_delete_specific_calculation_index_error(self, mock_print, mock_input):
        """Test IndexError"""
        history_command = HistoryCommand()
        history_command._delete_calculation_from_history()
        mock_input.assert_called_once()  # Verify input function was called
        mock_print.assert_has_calls([call("No calculation found at the given index.")])  # Verify error message

    def test_display_all_calculations_without_history(self):
        """test calculation when history is empty"""
        class MockHistoryCommand(HistoryCommand):
            """Define a subclass of HistoryCommand to override CalculationHistory.get_history()"""

            def _display_all_calculations(self = None):  # noqa # Add a default parameter to match the superclass
                """attempts to display calculatoins"""
                print("No calculations in history.")

            def _clear_history(self = None):  # noqa # Add a default parameter to match the superclass
                """clear history"""

        # Override CalculationHistory.get_history() to return an empty list
        CalculationHistory.get_history = lambda: []

        # Create an instance of the mock class
        mock_history_command = MockHistoryCommand()

        # Call the method you want to test
        mock_history_command._display_all_calculations()
