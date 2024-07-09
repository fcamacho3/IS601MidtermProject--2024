"""calculator/calculation.py
Defines the Calculation class for handling individual arithmetic operations.
This module provides the Calculation class, which offers a flexible way to encapsulate a
single arithmetic operation, including operands and the operation itself, within an object.
This abstraction is designed to be used within a Calculator class for executing operations.
"""
from decimal import Decimal
from typing import Callable

class Calculation:
    """
    A class to encapsulate a single arithmetic calculation involving two operands. It provides a
    structured way to perform and represent individual calculations, with support for extending
    functionality through subclassing or custom operation functions.
    """

    def __init__(self, num1: Decimal, num2: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> None:
        """
        Initializes a new instance of Calculation with two operands and an operation.

        Parameters:
            num1 (Decimal): The first operand for the calculation.
            num2 (Decimal): The second operand for the calculation.
            operation (Callable[[Decimal, Decimal], Decimal]): The operation to be performed on the operands.
        """
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    @classmethod
    def create_calculation(cls, num1: Decimal, num2: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        """
        Factory method to create and return a new instance of Calculation.

        This method provides an alternative way to instantiate the Calculation class,
        encapsulating the instantiation logic and potentially allowing for future enhancements
        like object pooling or instance caching.

        Parameters:
            num1 (Decimal): The first operand for the calculation.
            num2 (Decimal): The second operand for the calculation.
            operation (Callable[[Decimal, Decimal], Decimal]): The operation to be performed on the operands.

        Returns:
            Calculation: A new instance of the Calculation class.
        """
        return cls(num1, num2, operation)

    def compute(self) -> Decimal:
        """
        Executes the stored arithmetic operation with the stored operands.

        This method calls the operation provided at instantiation with the operands,
        returning the result of the operation. It abstracts the execution of the operation,
        allowing the operation logic to be defined externally.

        Returns:
            Decimal: The result of performing the operation on the operands.
        """
        return self.operation(self.num1, self.num2)

    def __repr__(self) -> str:
        """
        This method provides a string that represents the Calculation instance, including
        the operands and the name of the operation. It is intended for debugging and logging
        purposes, offering a clear description of the instance state.

        Returns:
            str: A string representation of the Calculation instance, including class name,
                 operands, and operation.
        """
        return f"Calculation({self.num1}, {self.num2}, {self.operation.__name__})"
