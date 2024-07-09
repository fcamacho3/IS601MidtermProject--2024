"""tests/test_calculation.py
Test suite for the Calculation class in the calculator package.
Ensures that calculations are correctly created, computed, and represented.
"""
from decimal import Decimal
from app.calculator.calculation import Calculation
from app.calculator.operations import ArithmeticOperations as AO

def test_compute(num1, num2, operation, expected):
    """Verify that compute method returns correct result for basic arithmetic operations."""
    calculation = Calculation(num1, num2, operation)
    assert calculation.compute() == expected, f"Incorrect calculation result for {operation.__name__}."

def test_create_calculation():
    """Ensure the factory method creates a Calculation instance as expected."""
    num1, num2 = Decimal('10'), Decimal('5')
    operation = AO.addition
    calculation = Calculation.create_calculation(num1, num2, operation)
    assert isinstance(calculation, Calculation), "create_calculation did not produce a Calculation instance."
    assert calculation.compute() == AO.addition(num1, num2), "Factory method instance did not compute correctly."

def test_calculation_repr():
    """Check that the Calculation instance is represented as expected."""
    calculation = Calculation(Decimal('1'), Decimal('2'), AO.addition)
    expected_repr = "Calculation(1, 2, addition)"
    assert repr(calculation) == expected_repr, "Calculation __repr__ does not match expected format."
