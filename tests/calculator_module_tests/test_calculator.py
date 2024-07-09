"""tests/test_calculator.py
Test suite for the Calculator class in the calculator package. Tests the Calculator's ability
to correctly perform arithmetic operations (addition, subtraction, multiplication, division)
and records each operation in the calculation history.
"""
import pytest
from app.calculator import Calculator
from app.calculator.calculations import CalculationHistory as ch

@pytest.fixture(autouse=True)
def clear_history_before_tests():
    """Ensure a clean history for each test"""
    ch.clear_history()
    yield

def test_addition():
    '''Test that calculator add function works '''    
    assert Calculator.add(2,2) == 4

def test_subtraction():
    '''Test that calculator subtract function works '''    
    assert Calculator.subtract(2,2) == 0

def test_multiply():
    '''Test that calculator multiply function works '''    
    assert Calculator.multiply(2,2) == 4

def test_divide():
    '''Test that calculator divide function works '''    
    assert Calculator.divide(2,2) == 1
