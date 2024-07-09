"""calculator/calculations.py
Defines the CalculationHistory class for managing a shared history of calculations
performed within the calculator application. This class offers class methods to add
calculations to the history, retrieve the full history or the most recent calculation,
and clear the history. The history is maintained as a class-level list, allowing easy
access and modification across different parts of the application.
"""
import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Optional
from decimal import Decimal
from app.calculator.calculation import Calculation
from app.calculator.operations import ArithmeticOperations as AO
import logging

load_dotenv()

class CalculationHistory:
    """Manages the history of calculations performed by the calculator.
    
    This class offers class methods to add calculations to the history,
    retrieve the full history or the most recent calculation, and clear
    the history. The history is maintained as a class-level list, allowing
    easy access and modification across different parts of the application.
    """
    _history: List[Calculation] = []  # Class-level attribute to store instances of Calculation

    @classmethod
    def add_calculation(cls, calculation: Calculation):
        """Add a calculation to the history.
        
        Args:
            calculation (Calculation): The calculation to add to the history.
        """
        cls._history.append(calculation)
    
    @classmethod
    def get_history(cls) -> List[Calculation]:
        """Retrieve the entire calculation history.
        
        Returns:
            List[Calculation]: The list of calculations.
        """
        return cls._history

    @classmethod
    def clear_history(cls):
        """Clear the calculation history."""
        cls._history.clear()

    @classmethod
    def get_latest_history(cls) -> Optional[Calculation]:
        """Retrieves the most recent calculation & returns None if there are no calculations in history."""
        if cls._history:
            return cls._history[-1]
        else:
            return None

    @classmethod
    def delete_calculation_by_index(cls, index: int):
        """Delete a calculation from the history by its index.

        Args:
            index (int): The index of the calculation to delete.
        """
        if 0 <= index < len(cls._history):
            del cls._history[index]
            cls.save_history_to_csv()  # Optionally save the updated history to CSV
        else:
            raise IndexError("Calculation index out of range.")

    # CSV methods
    @classmethod
    def save_history_to_csv(cls):
        """Save the calculation history to a CSV file."""
        
        if not cls._history:
            print("No calculations in history to save.")
            return

        data_dir = os.getenv('DATA_DIR', './')
        file_name = os.getenv('CALC_HISTORY_FILE', 'calculator_history.csv')
        file_path = os.path.join(data_dir, file_name)

        # Ensure the directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Convert history to a DataFrame and save
        df = pd.DataFrame([{
            'fld_Operation': calc.operation.__name__,
            'fld_Operand1': calc.num1,
            'fld_Operand2': calc.num2
        } for calc in cls._history])
        df.to_csv(file_path, index=False)
        logging.info(f"History saved to {file_name}")

    @classmethod
    def load_history_from_csv(cls):
        """Load the calculation history from a CSV file."""
        data_dir = os.getenv('DATA_DIR', './')
        file_name = os.getenv('CALC_HISTORY_FILE', 'calculator_history.csv')
        file_path = os.path.join(data_dir, file_name)

        operation_mapping = {
            'addition': AO.addition,
            'subtraction': AO.subtraction,
            'multiplication': AO.multiplication,
            'division': AO.division,
        }

        try:
            df = pd.read_csv(file_path)
            # Ensure only valid operations are loaded
            cls._history = [
                Calculation(
                    Decimal(row['fld_Operand1']),
                    Decimal(row['fld_Operand2']),
                    operation_mapping.get(row['fld_Operation'], lambda x, y: None)
                ) for index, row in df.iterrows() if row['fld_Operation'] in operation_mapping
            ]
            logging.info("Calculation history loaded successfully.")
        except pd.errors.EmptyDataError:
            logging.info("The history CSV file is empty. No history to load.")
        except FileNotFoundError:
            logging.info("The history CSV file was not found.")
        except Exception as e:
            logging.error(f"An error occurred while loading history: {e}")
