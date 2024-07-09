"""calculator/operations.py
This module defines the `ArithmeticOperations` class, which provides staticmethods for basic arithmetic
operations including addition, subtraction, multiplication, and division. These methods are implemented
with Decimal numbers to ensure precision, suitable for financial calculations or any scenario where
floating-point arithmetic may lead to inaccuracies.
"""
from decimal import Decimal

class ArithmeticOperations:
    """
    Class to perform basic arithmetic operations.

    Operations include addition, subtraction, multiplication, and division
    with support for Decimal numbers to maintain precision.
    """

    @staticmethod
    def addition(num1: Decimal, num2: Decimal) -> Decimal:
        """
        Perform addition of two Decimal numbers.

        Parameters:
        - num1 (Decimal): The first operand.
        - num2 (Decimal): The second operand.

        Returns:
        - Decimal: The sum of `num1` and `num2`.
        """
        return num1 + num2

    @staticmethod
    def subtraction(num1: Decimal, num2: Decimal) -> Decimal:
        """
        Perform subtraction between two Decimal numbers.

        Parameters:
        - num1 (Decimal): The minuend.
        - num2 (Decimal): The subtrahend.

        Returns:
        - Decimal: The difference of `num1` and num2`.
        """
        return num1 - num2

    @staticmethod
    def multiplication(num1: Decimal, num2: Decimal) -> Decimal:
        """
        Perform multiplication of two Decimal numbers.

        Parameters:
        - num1 (Decimal): The first factor.
        - num2 (Decimal): The second factor.

        Returns:
        - Decimal: The product of `num1` and `num2`.
        """
        return num1 * num2

    @staticmethod
    def division(num1: Decimal, num2: Decimal) -> Decimal:
        """
        Perform division between two Decimal numbers.

        Parameters:
        - num1 (Decimal): The dividend.
        - num2 (Decimal): The divisor.

        Raises:
        - ZeroDivisionError: If `num2` is zero, as division by zero is undefined.    

        Returns:
        - Decimal: The quotient of `num1` divided by `num2`.
        """
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        else:
            return num1 / num2
