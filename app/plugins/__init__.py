"""app/plugins/__init__.py: Utility functions for operation command plugins.
This module provides shared utility functions used by arithmetic operation command plugins.
It includes functionality for executing operations based on user input and parsing that input.
These utilities support a consistent user experience across different arithmetic operations,
such as addition, subtraction, multiplication, and division, by standardizing input handling
and execution feedback.
"""
from app.calculator.calc_utils import calculate_and_print
import logging

def execute_operation(user_input_prompt, operation_name):
    """
    Executes an arithmetic operation based on user input and the specified operation name.

    Parameters:
    - user_input_prompt (str): The prompt to display to the user for input.
    - operation_name (str): The name of the operation to perform ('add', 'subtract', 'multiply', 'divide').

    The function leverages a while loop to continuously prompt the user for input, allowing
    multiple operations to be performed in sequence. The loop can be exited by typing 'exit',
    providing a user-friendly way to return to the main menu.
    """
    logging.info(f"Starting {operation_name} operation.")
    print(user_input_prompt)
    print("\tEnter your two numbers separated by space")
    print("\tType 'exit' at any time to return to the main menu.")
    print("\t\t[Example]: 2 3")

    while True:
        user_input = input(f"[{operation_name.capitalize()}]:   ")

        if user_input.lower() == 'exit':
            logging.info(f"Exiting {operation_name} operation.\n")
            break

        try:
            num1_str, num2_str = parse_input(user_input)
            calculate_and_print(num1_str, num2_str, operation_name)
            print(f"Continue to {operation_name} or type 'exit' to return to the main menu.\n")
        except Exception as e:
            logging.warning(f"Invalid input in {operation_name} operation: {e}\n")
            print(f"Error: {e}\nPlease try again or type 'exit' to exit.\n")

def parse_input(user_input):
    """
    Parses the user input into two operands.

    Parameters:
    - user_input (str): A string input by the user.

    Returns:
    A tuple containing the two operands as strings.

    Raises:
    ValueError: If the input format is incorrect.
    """
    parts = user_input.split()
    if len(parts) != 2:
        raise ValueError("Invalid input format. Please use: <operand1> <operand2>")
    
    return parts[0], parts[1]
