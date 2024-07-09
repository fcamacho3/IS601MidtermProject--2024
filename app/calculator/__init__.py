"""calculator/__init__.py
This module defines the Calculator class, centralizing arithmetic functionality with support
for addition, subtraction, multiplication, and division. It seamlessly records each calculation
in a shared history, enabling not just computation but also easy retrieval of past calculations.
Designed for simplicity and ease of use, the Calculator serves as the core component of the
basic calculator system, leveraging the ArithmeticOperations for mathematical operations and
CalculationHistory for maintaining a log of all calculations.
"""
from decimal import Decimal
from typing import Callable
from app.calculator.calculation import Calculation
from app.calculator.operations import ArithmeticOperations as ao
from app.calculator.calculations import CalculationHistory as ch

class Calculator:
    """
    Serves as a core component of a basic calculator system. Integrates components for performing
    arithmetic calculations and managing history.
    """

    @staticmethod
    def _calculate_and_record(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> Decimal:
        """Internal method to perform and record a calculation."""
        calculation = Calculation.create_calculation(a, b, operation)
        ch.add_calculation(calculation)
        return calculation.compute()

    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        '''Perform addition by delegating to the _calculate_and_record method'''
        return Calculator._calculate_and_record(a, b, ao.addition)

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        '''Perform subtraction by delegating to the _calculate_and_record method'''
        return Calculator._calculate_and_record(a, b, ao.subtraction)

    @staticmethod
    def multiply (a: Decimal, b: Decimal) -> Decimal:
        '''Perform multiplication by delegating to the _calculate_and_record method'''
        return Calculator._calculate_and_record(a, b, ao.multiplication)

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        '''Perform division by delegating to the _calculate_and_record method'''
        return Calculator._calculate_and_record(a, b, ao.division)
