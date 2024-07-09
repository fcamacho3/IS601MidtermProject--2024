"""conftest.py: Automatic generation of test data for arithmetic operations."""

from decimal import Decimal
from faker import Faker
from app.calculator.operations import ArithmeticOperations as AO

fake = Faker()

DIVISOR_NOT_ZERO = 3  # Use a named constant to avoid "magic numbers".

def generate_test_data(num_records):
    """
    Generates test data for arithmetic operations.

    Parameters:
    - num_records (int): Number of records to generate.

    Yields:
    - tuple: Test data (num1, num2, operation_name, operation_func, expected result).
    """
    operation_mappings = {
        'add': AO.addition,
        'subtract': AO.subtraction,
        'multiply': AO.multiplication,
        'divide': AO.division
    }

    operation_names = list(operation_mappings.keys())  # Conversion to list done once.

    for _ in range(num_records):
        num1 = Decimal(fake.random_number(digits=2))
        num2 = Decimal(fake.random_number(digits=2)) if _ % DIVISOR_NOT_ZERO != 0 else Decimal(fake.random_number(digits=1))
        operation_name = fake.random_element(elements=operation_names)
        operation_func = operation_mappings[operation_name]

        if operation_func is AO.division and num2 == 0:
            num2 = Decimal(1)  # Simplified Decimal initialization.

        try:
            expected = operation_func(num1, num2)
        except ZeroDivisionError:
            expected = "ZeroDivisionError"

        yield num1, num2, operation_name, operation_func, expected

def pytest_addoption(parser):
    """
    Adds a custom command-line option to specify the number of test records.

    Parameters:
    - parser: The parser for command line arguments and ini-file values.
    """
    parser.addoption("--num_records", action="store", default=5, type=int,
                     help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    """
    Generates tests based on the specified number of records.

    Parameters:
    - metafunc: The Metafunc object for the test function.
    """
    if {"num1", "num2", "expected"}.intersection(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        parameters = list(generate_test_data(num_records))
        modified_parameters = [
            (num1, num2, op_name if 'operation_name' in metafunc.fixturenames else op_func, expected)
            for num1, num2, op_name, op_func, expected in parameters
        ]
        metafunc.parametrize("num1,num2,operation,expected", modified_parameters)
