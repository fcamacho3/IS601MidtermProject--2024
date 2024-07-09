"""tests/test_calculations.py
Test suite for the CalculationHistory class in the calculator package.
This module tests the functionality of the CalculationHistory class, including
adding calculations to the history, retrieving the history and the most recent
calculation, and clearing the history.
"""
from decimal import Decimal
from unittest.mock import patch
import pandas as pd
import pytest
from app.calculator.calculation import Calculation
from app.calculator.operations import ArithmeticOperations as AO
from app.calculator.calculations import CalculationHistory as CH

def setup_function(function):
    """Setup for tests clears the calculation history before each test function is run."""
    CH.clear_history()

def test_add_calculation():
    """Test adding a single calculation to the history."""
    calc = Calculation(Decimal('1'), Decimal('2'), AO.addition)
    CH.add_calculation(calc)
    assert calc in CH.get_history(), "Calculation should be in history after addition."

def test_get_history():
    """Test retrieving the entire calculation history."""
    calc1 = Calculation(Decimal('1'), Decimal('2'), AO.addition)
    calc2 = Calculation(Decimal('3'), Decimal('4'), AO.subtraction)
    CH.add_calculation(calc1)
    CH.add_calculation(calc2)
    history = CH.get_history()
    assert history == [calc1, calc2], "The history should contain all added calculations."

def test_clear_history():
    """Test clearing the calculation history."""
    calc = Calculation(Decimal('1'), Decimal('2'), AO.addition)
    CH.add_calculation(calc)
    CH.clear_history()
    assert not CH.get_history(), "The history should be empty after clearing."

def test_get_latest_history():
    """Test retrieving the most recent calculation from the history."""
    calc1 = Calculation(Decimal('1'), Decimal('2'), AO.addition)
    calc2 = Calculation(Decimal('3'), Decimal('4'), AO.subtraction)
    CH.add_calculation(calc1)
    CH.add_calculation(calc2)
    latest_calc = CH.get_latest_history()
    assert latest_calc == calc2, "The latest calculation should be the most recently added."

def test_get_latest_history_empty():
    """Test that get_latest_history returns None when the history is empty."""
    CH.clear_history()  # Ensure the history is empty
    latest_calc = CH.get_latest_history()
    assert latest_calc is None, "get_latest_history should return None when the history is empty."

# New Tests w/ CSV
def test_delete_calculation_by_index_valid_index():
    """Test deleting a calculation by a valid index."""
    # Add some calculations to the history
    calc1 = Calculation(Decimal('1'), Decimal('2'), AO.addition)
    calc2 = Calculation(Decimal('3'), Decimal('4'), AO.subtraction)
    CH.add_calculation(calc1)
    CH.add_calculation(calc2)

    # Delete the calculation at index 0
    CH.delete_calculation_by_index(0)

    # Check that the calculation at index 0 is deleted
    assert len(CH.get_history()) == 1, "History should contain only one calculation after deletion"
    assert CH.get_history()[0] == calc2, "Second calculation should be at index 0 after deletion"

def test_delete_calculation_by_index_invalid_index():
    """Test deleting a calculation by an invalid index."""
    # Add some calculations to the history
    calc1 = Calculation(Decimal('1'), Decimal('2'), AO.addition)
    calc2 = Calculation(Decimal('3'), Decimal('4'), AO.subtraction)
    CH.add_calculation(calc1)
    CH.add_calculation(calc2)

    # Try to delete a calculation with an out-of-range index
    with pytest.raises(IndexError):
        CH.delete_calculation_by_index(2)

def test_save_history_to_csv():
    """Test saving history to CSV."""
    # Add some calculations to the history
    calc1 = Calculation(Decimal('1'), Decimal('2'), AO.addition)
    calc2 = Calculation(Decimal('3'), Decimal('4'), AO.subtraction)
    CH.add_calculation(calc1)
    CH.add_calculation(calc2)

    # Call the class method to save the history to CSV
    CH.save_history_to_csv()

    # You can add assertions here to verify that the CSV file was created successfully

def test_load_history_from_csv():
    """Test loading history from CSV."""
    # Add some calculations to the history
    calc1 = Calculation(Decimal('1'), Decimal('2'), AO.addition)
    calc2 = Calculation(Decimal('3'), Decimal('4'), AO.subtraction)
    CH.add_calculation(calc1)
    CH.add_calculation(calc2)

    # Call the class method to load history from CSV
    CH.load_history_from_csv()

    # You can add assertions here to verify that the history was loaded successfully

def test_load_history_from_csv_empty_file():
    """Test loading history from an empty CSV file."""
    with patch('app.calculator.calculations.pd.read_csv', side_effect=pd.errors.EmptyDataError):
        # Since the file is empty, it should log the appropriate message
        with patch('app.calculator.calculations.logging.info') as mock_logging:
            CH.load_history_from_csv()
            mock_logging.assert_called_once_with("The history CSV file is empty. No history to load.")

def test_load_history_from_csv_file_not_found():
    """Test loading history when the CSV file is not found."""
    with patch('app.calculator.calculations.pd.read_csv', side_effect=FileNotFoundError):
        # Since the file is not found, it should log the appropriate message
        with patch('app.calculator.calculations.logging.info') as mock_logging:
            CH.load_history_from_csv()
            mock_logging.assert_called_once_with("The history CSV file was not found.")

def test_load_history_from_csv_other_error():
    """Test loading history when an unexpected error occurs."""
    with patch('app.calculator.calculations.pd.read_csv', side_effect=Exception("An unexpected error")):
        # Since an unexpected error occurs, it should log the error message
        with patch('app.calculator.calculations.logging.error') as mock_logging:
            CH.load_history_from_csv()
            mock_logging.assert_called_once_with("An error occurred while loading history: An unexpected error")

@patch('app.calculator.calculations.CalculationHistory.get_history', return_value=[])
def test_save_history_to_csv_no_history(mock_get_history):
    """Test saving history to CSV when there are no calculations in history."""
    with patch('builtins.print') as mock_print:
        CH.save_history_to_csv()
        mock_print.assert_called_once_with("No calculations in history to save.")
