"""Tests for the ArithmeticOperations class in calculator/operations.py
This suite uses Faker and randomized test data to evaluate arithmetic operations (addition, subtraction,
multiplication, and division), ensuring functionality across a range of Decimal inputs.
"""
from decimal import Decimal
import pytest
from app.calculator.operations import ArithmeticOperations as AO

def test_operations(num1, num2, operation, expected):
    """Parameterized test for arithmetic operations with varied inputs and expected outputs."""
    assert operation(num1, num2) == expected, f"Failed {operation.__name__} with {num1} and {num2}"

def test_division_by_zero():
    """Test division by zero is handled as expected."""
    with pytest.raises(ZeroDivisionError):
        AO.division(Decimal('1'), Decimal('0'))
