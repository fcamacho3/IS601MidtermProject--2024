"""app/calculator/calc_utils.py:
This module captures user input from the command line, performs arithmetic operations
using the Calculator class, and handles invalid inputs and exceptions.
"""
from decimal import Decimal, InvalidOperation
from app.calculator import Calculator
import logging

def perform_operation(num1: Decimal, num2: Decimal, operation_name: str) -> str:
    """
    Attempts to perform the specified arithmetic operation on two operands.
    
    Args:
        num1 (Decimal): The first operand.
        num2 (Decimal): The second operand.
        operation_name (str): The operation to perform.
        
    Returns:
        str: A message with the result of the operation or an error.
    """
    # Mapping of operation names to Calculator class methods
    operation_mapping = {
        'add': Calculator.add,
        'subtract': Calculator.subtract,
        'multiply': Calculator.multiply,
        'divide': Calculator.divide,
    }

    logging.info(f"Attempting to perform operation: {operation_name} with operands {num1} and {num2}")

    try:
        # Retrieve the corresponding method from the mapping
        operation_callable = operation_mapping.get(operation_name)
        if operation_callable is None:
            logging.error(f"Unknown operation: {operation_name}")
            return f"Unknown operation: {operation_name}"

        # Execute the operation
        result = operation_callable(num1, num2)
        logging.info(f"Operation {operation_name} completed successfully. Result: {result}")
        return f"The result of {num1} {operation_name} {num2} is equal to {result}"
    except ZeroDivisionError:
        logging.warning(f"Division by zero attempt.")
        return "An error occurred: Cannot divide by zero"
    except ValueError as e:
        logging.error(f"Value error in operation.\n")
        return str(e)
    except Exception as e:
        logging.critical(f"Unexpected error in operation.\n", exc_info=True)
        return f"An unexpected error occurred: {e}"

def calculate_and_print(num1_str, num2_str, operation_name):
    """
    Validates the input, performs the operation, and prints the result or an error message.
    
    Args:
        num1_str (str): The first operand as a string.
        num2_str (str): The second operand as a string.
        operation_name (str): The name of the operation to perform.
    """
    logging.info(f"Calculating {operation_name} for inputs '{num1_str}' and '{num2_str}'")

    try:
        num1_decimal = Decimal(num1_str)
        num2_decimal = Decimal(num2_str)
    except InvalidOperation:
        logging.warning(f"Invalid number input: '{num1_str}' or '{num2_str}' is not a valid number.\n")
        print(f"Invalid number input: {num1_str} or {num2_str} is not a valid number.")
        return
    
    result_message = perform_operation(num1_decimal, num2_decimal, operation_name)
    logging.info(f"Result of {operation_name}: {result_message}\n")
    print(result_message)
