"""app/plugins/history/__init__.py

"""
from unittest.mock import patch
from app.commands import Command
from app.calculator.calculations import CalculationHistory
import logging

class HistoryCommand(Command):
    """
    A command to manage calculation history. This class provides the logic to handle user input for
    actions such as retrieving the most recent calculation, clearing history, saving history to CSV,
    loading history from CSV, and deleting specific calculations.
    """
    def __init__(self):
        super().__init__()
        self.name = "history"
        self.description = "Manage calculation history (retrieve, clear, save, load, delete)."

    def execute(self, *args):
        """
        Display the history management menu and process user choices.
        """

        while True:  # Keep running until the user decides to exit
            print("\n--- History Menu ---")
            print("1. Retrieve the most recent calculation")
            print("2. Retrieve all calculations")
            print("3. Clear calculation history")
            print("4. Save calculation history to CSV")
            print("5. Load calculation history from CSV")
            print("6. Delete a calculation from history")
            print("\nType 'exit' to return to the main menu.")
            choice = input("\nEnter your choice: ")

            if choice.lower() == 'exit':
                break  # Exit the loop, ending the command

            self.process_choice(choice)

    def process_choice(self, choice):
        options = {
            '1': self._display_most_recent_calculation,
            '2': self._display_all_calculations,
            '3': self._clear_history,
            '4': self._save_calculation_history,
            '5': self._load_calculation_history,
            '6': self._delete_calculation_from_history,
        }
        action = options.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Select a valid option or type 'exit' to return to main menu.")

    def _display_most_recent_calculation(self):
        most_recent = CalculationHistory.get_latest_history()
        if most_recent:
            self.print_result(most_recent)
        else:
            print("No calculations in history.")

    def _display_all_calculations(self):
        all_calculations = CalculationHistory.get_history()
        if all_calculations:
            print("\nAll Calculations:")
            for idx, calculation in enumerate(all_calculations, start=1):
                try:
                    result = calculation.compute()
                    print(f"{idx}. {calculation} results in {result}")  # Format this based on how your calculations are stored/represented
                except ZeroDivisionError:
                    print(f"{idx}. {calculation} is undefined")
        else:
            print("No calculations in history.")

    def print_result(self, calculation):
        '''Print the result of a calculation, handling cases where the calculation is undefined'''
        try:
            result = calculation.compute()
            print(f"{calculation} results in {result}")
        except ZeroDivisionError:
            print(f"{calculation} is undefined.")
        except Exception as e: # pragma: no cover
            print(f"Error occured: {e}")

    def _clear_history(self):
        if CalculationHistory.get_history():  # Checks if there are any calculations in the history
            CalculationHistory.clear_history()
            print("Calculation history cleared.")
        else:
            print("History is already empty, no history to clear.")

    # CSV methods
    def _save_calculation_history(self):
        '''Save history of calculations to CSV'''
        CalculationHistory.save_history_to_csv()

    def _load_calculation_history(self):
        '''Load history of calculations from CSV'''
        try:
            CalculationHistory.load_history_from_csv()
            # Check if any calculations were loaded
        except Exception as e:
            print(f"\nError loading history: {e}")

    def _delete_calculation_from_history(self):
        if not CalculationHistory.get_history():
            print("No history available to delete.")
            return  # Return to the history menu
        
        self._display_all_calculations()  # Show all calculations with indexes for user reference
        
        try:
            index_to_delete = int(input("Enter the index of the calculation to delete: ")) - 1
            CalculationHistory.delete_calculation_by_index(index_to_delete)
            print(f"Calculation at index {index_to_delete + 1} has been deleted.")
        except ValueError:
            print("Invalid index. Enter a valid index or 'exit' to return to history menu.")
        except IndexError:
            print("No calculation found at the given index.")
