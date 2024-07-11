# Advanced Python Calculator for Software Engineering Graduate Course
[__IS_601 Midterm__]

---

## 1. Design Patterns

- __Facade Pattern__

I used the [__Facade Pattern__](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/__init__.py#L14-L155) to simplify the interaction with the application's complex subsystems, providing a unified interface for starting the application, loading plugins, and handling commands.
> The `App` class serves as the facade, encapsulating the complexities of loading plugins and handling commands. Clients interact with the `App` facade without needing to understand the internal workings of these subsystems. By encapsulating the initialization process, loading of plugins, and registration of commands, the App facade shields clients from the implementation details of these subsystems. Clients only need to know how to interact with the App class, making the application more maintainable and easier to use.
```python
class App:
    def __init__(self):
        # Encapsulate the initialization process
        self.command_handler = CommandHandler()

    def load_plugins(self):
        # Encapsulate the process of loading plugins
        # ...

    def register_plugin_commands(self, plugin_module):
        # Encapsulate the process of registering commands from plugins
        # ...
    
    ...
```
> The `App` facade provides a unified interface for starting the application and interacting with its features. Clients interact with the `App` class to start the application and execute commands, abstracting away the complexity of the underlying subsystems.
```python
if __name__ == "__main__":
    # Initialize and start the application
    App().start()
```
> In summary, the Facade Pattern in this context simplifies the usage of the application by providing a clear and unified interface while encapsulating the complexities of its subsystems.
<br>

- __Command Pattern__

I use the [__Command Pattern__](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/commands/__init__.py#L8-L33) to enhance modularity and flexibility.
> Each concrete command class, like `AddCommand`, `DivideCommand`, `MultiplyCommand`, and `SubtractCommand`, encapsulates a specific operation within its execute method. (Along with `HistoryCommand`) 
```python
class AddCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "add"
        self.description = "Add two numbers together."

    def execute(self, *args):
        logging.info("Executing addition command")
        user_input_prompt = "Operation: Addition\n"
        execute_operation(user_input_prompt, self.name)

class DivideCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "divide"
        self.description = "Divide two numbers from one another."

    def execute(self, *args):
        logging.info("Executing division command")
        user_input_prompt = "Operation: Division\n"
        execute_operation(user_input_prompt, self.name)

class MultiplyCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "multiply"
        self.description = "Multiply two numbers together."

    def execute(self, *args):
        logging.info("Executing multiplication command")
        user_input_prompt = "Operation: Multiplication\n"
        execute_operation(user_input_prompt, self.name)

class SubtractCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "subtract"
        self.description = "Subtract two numbers from one another."

    def execute(self, *args):
        logging.info("Executing subtraction command")
        user_input_prompt = "Operation: Subtraction\n"
        execute_operation(user_input_prompt, self.name)
```
> This encapsulation allows for uniform invocation of diverse operations through a common interface defined by the `Command` superclass. 
```python
class Command:
    def __init__(self):
        """Constructor for command class"""
        self.name = ""  # Command name for menu display
        self.description = ""  # Command description for menu display

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Command execution not implemented.")
```
> The `CommandHandler` class serves as the invoker, maintaining a dictionary of registered commands and facilitating their dynamic execution based on user input or other triggers. 
```python
class CommandHandler:
    def __init__(self):
        self.commands = {} # A dictionary to store command instances keyed by their names.

    def register_command(self, command):
        if command.name in self.commands:
            logging.warning(f"Command '{command.name}' is already registered. Overwriting.")
        self.commands[command.name] = command
        logging.info(f"Command '{command.name}' registered successfully.")

    def get_commands(self):
        return [(cmd.name, cmd.description) for cmd in self.commands.values()]

    def execute_command(self, name, *args):
        command = self.commands.get(name)
        if not command:
            logging.error(f"Command '{name}' not found.")
            raise KeyError
        try:
            command.execute(*args)
        except Exception as e:
            logging.error(f"Error executing command '{name}': {e}")
```
> By interacting with commands solely through the Command interface, the `CommandHandler` remains decoupled from the specific implementations of individual commands. This decoupling promotes flexibility, as new commands can be added or existing ones modified without necessitating changes to the `CommandHandler` or other components of the system.
<br>

- __Factory Method__, __Singleton__, & __Strategy Patterns__

I use the [__Factory Method Pattern__](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/calculator/calculation.py#L30-L48) to encapsulate and delegate the instantiation of Calculation objects within the Calculation class itself. This pattern allows for greater flexibility and decoupling by delegating the creation logic to a separate method, `create_calculation`, facilitating easy modifications to the instantiation process without affecting the client code.
> The `create_calculation` class method acts as a factory that takes operands and an operation as its arguments. It then returns a new instance of the Calculation class configured with these inputs. This method abstracts the instantiation logic from the client, promoting a loose coupling between the object creation and its usage.
```python
class Calculation:
    def __init__(self, num1: Decimal, num2: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> None:
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    @classmethod
    def create_calculation(cls, num1: Decimal, num2: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        return cls(num1, num2, operation)
```
> Employing the Factory Method Pattern in this way encapsulates object creation, enhancing the `Calculation` class's adaptability. It centralizes changes—such as more complex initialization or new calculation types—within the `create_calculation` method, minimizing impact on the broader application. This approach streamlines creation, boosting code maintainability and scalability by isolating creation logic.
<br>

I use the [__Singleton Pattern__](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/calculator/calculations.py#L27-L58) to ensure that there is only one, globally accessible history of calculations within the application, managed through the CalculationHistory class.
> The `_history` attribute is a class-level attribute. This means it is shared across all instances of the CalculationHistory class. Any modification to _history through any instance (or directly via the class) will be reflected across the entire application, maintaining a single state of the calculation history.
```python
class CalculationHistory:
    _history: List[Calculation] = []  # Class-level attribute to store instances of Calculation
```
> All methods within `CalculationHistory` are class methods (@classmethod). These methods operate on the class level rather than the instance level. This further enforces the Singleton pattern, as these methods ensure that the operations on the calculation history are performed on a global state (_history) rather than any instance-specific state.
```python
    @classmethod
    def add_calculation(cls, calculation: Calculation):
        cls._history.append(calculation)
    
    @classmethod
    def get_history(cls) -> List[Calculation]:
        return cls._history

    @classmethod
    def clear_history(cls):
        cls._history.clear()

    @classmethod
    def get_latest_history(cls) -> Optional[Calculation]:
        if cls._history:
            return cls._history[-1]
        else:
            return None
```
<br>

I used the [__Strategy Pattern__](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/calculator/operations.py#L9-L77) to decouple the implementation of various arithmetic operations from the main application logic, allowing for flexibility and extensibility in handling different operations.
> Each static method encapsulates a specific arithmetic operation, providing a common interface for performing calculations. This design allows the caller to choose and switch between different strategies (operations) dynamically.
```python
class ArithmeticOperations:
    @staticmethod
    def addition(num1: Decimal, num2: Decimal) -> Decimal:
        return num1 + num2

    @staticmethod
    def subtraction(num1: Decimal, num2: Decimal) -> Decimal:
        return num1 - num2

    @staticmethod
    def multiplication(num1: Decimal, num2: Decimal) -> Decimal:
        return num1 * num2

    @staticmethod
    def division(num1: Decimal, num2: Decimal) -> Decimal:
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        else:
            return num1 / num2

```
> In my [*calculator/calc_utils.py*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/calculator/calc_utils.py#L9-L36) module, I utilize these strategies by invoking the corresponding static methods from the `ArithmeticOperations` class based on user input. For example:
```python
def perform_operation(num1: Decimal, num2: Decimal, operation_name: str) -> str:
    operation_callable = getattr(ArithmeticOperations, operation_name, None)
    if operation_callable is None:
        return f"Unknown operation: {operation_name}"
    else:
        result = operation_callable(num1, num2)
        return f"The result of {num1} {operation_name} {num2} is equal to {result}"
```
> Here, the `perform_operation` function dynamically selects the appropriate strategy (operation) based on the operation_name provided by the user. This demonstrates the dynamic nature of the Strategy Pattern, where the choice of strategy can vary at runtime.

---

## 2. Description of Environment Variables
Loading Environment Variables at Application Startup
> In [*app/__init__.py*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/__init__.py#L14-L25), environment variables are loaded from the `.env` file into the application's environment:
```python
from dotenv import load_dotenv
...
class App:
    def __init__(self):
        ...
        load_dotenv()  # This line loads environment variables from the .env file
        self.settings = self.load_environment_variables()
        ...
```
Accessing Environment Variables to Configure Application Settings
> After loading the environment variables, [`load_environment_variables()`](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/__init__.py#L47-L61) method in *app/__init__.py* is used to store them in a dictionary for easy access:
```python
import os
...
class App:
    ...
    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}  # Access environment variables
        logging.info("Environment variables loaded.")
        return settings
```
Utilizing Environment Variables for Dynamic Configuration
> Environment variables are specifically utilized within [*calculator/calculations.py*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/calculator/calculations.py#L74-L87) for determining file paths and names related to calculation history management:
```python
import os
from dotenv import load_dotenv
...
class CalculationHistory:
    ...
    @classmethod
    def save_history_to_csv(cls):
        ...
        data_dir = os.getenv('DATA_DIR', './')  # Gets the DATA_DIR environment variable or defaults to './'
        file_name = os.getenv('CALC_HISTORY_FILE', 'calculator_history.csv')  # Defaults to 'calculator_history.csv' if not set
        file_path = os.path.join(data_dir, file_name)
        ...
```
And similarly, for [loading calculation history from a CSV](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/calculator/calculations.py#L99-L103) file:
```python
    @classmethod
    def load_history_from_csv(cls):
        ...
        data_dir = os.getenv('DATA_DIR', './')
        file_name = os.getenv('CALC_HISTORY_FILE', 'calculator_history.csv')
        file_path = os.path.join(data_dir, file_name)
        ...
```

---

## 3. Utilizing Logging

I tried to integrate logging extensively to facilite both debugging and runtime monitoring.
Configuration of logging
> I used use a [*logging.conf*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/logging.conf#L1-L28) file to define loggers, handlers, formatters, and their configurations. This file is read at the start of my application to configure the logging system. This snippet from [*app/__init__.py*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/__init__.py#L27-L45) shows how I checked for the existence of *logging.conf* and use it to configure logging. If the file is not found, it falls back to a basic configuration.
```python
import logging.config
...
class App:
    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")
```
<br>

Logging is used throughout the code to record everything from information about the application's state to warnings and errors. Here are specific examples demonstrating its effective use:
> __Logging Application Events and States:__ In [*app/__init__.py*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/__init__.py#L121-L155), logging is used to mark significant application events, such as the start and termination of the application, as well as the loading of environment variables.
```python
logging.info("Environment variables loaded.")
...
logging.info("Application started. Type 'show_menu' to see the menu or 'exit' to exit.\n")
...
logging.info("Application shutdown.")
```
> __Logging in Plugin Operations:__ In the plugins directory, such as [*app/plugins/add/__init__.py*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/plugins/add/__init__.py#L24), logging is utilized to trace the execution of specific operations, aiding in debugging and providing runtime insights.
```python
import logging
...
class AddCommand(Command):
    ...
    def execute(self, *args):
        logging.info("Executing addition command")
        ...
```
> __Error Logging:__ I also log errors and exceptions, providing a trail that can be used to troubleshoot issues. For example, in [*app/plugins/__init__.py*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/plugins/__init__.py#L36-L42):
```python
except Exception as e:
    logging.warning(f"Invalid input in {operation_name} operation: {e}\n")
    ...
```
> __Critical Errors and Exceptions:__ In addition to regular logging, I also tried captures and log critical errors, ensuring that these high-severity issues are flagged for immediate attention. For example in [*app/calculator/calc_utlis.py*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/calculator/calc_utils.py#L48-L50):
```python
except Exception as e:
    logging.critical(f"Unexpected error in operation.\n", exc_info=True)
    ...
```
In summary, I utilized the logging library to capture a wide range of information, from operational data and event tracing to error and critical condition reporting. 

---

## 4. LBYP vs EAFP
- __Look Before You Leap ([*if/else*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/plugins/__init__.py#L44-L61))__:
The __LBYL__ approach involves checking for conditions before performing an operation. This preventive method is about ensuring that operations are safe to perform by checking preconditions or constraints ahead of time.
> In *app/plugins/__init__.py*, the parse_input function illustrates LBYL by checking the input format before proceeding with the operation:
```python
def parse_input(user_input):
    parts = user_input.split()
    if len(parts) != 2:  # Pre-check for the expected number of inputs
        raise ValueError("Invalid input format. Please use: <operand1> <operand2>")
    
    return parts[0], parts[1]
```
> Here, I explicitly check if the user input splits into exactly two parts, which is the expected format, before proceeding to return the operands. This is a clear example of LBYL, as I am ensuring the preconditions are met before moving forward with the operation.
<br>

- __Easier to Ask for Forgivness than Permission ([*try/except*](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/calculator/calc_utils.py#L52-L73))__:
__EAFP__ is about trying to perform the operation directly and handling the fallout if it fails. This method is often preferred in environments where exceptions are cheap to catch or when the error condition is expected to be rare.
> In *app/calculator/calc_utils.py*, the `calculate_and_print` function demonstrates the EAFP philosophy by attempting to perform operations and catching exceptions if they occur:
```python
def calculate_and_print(num1_str, num2_str, operation_name):
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
```
> This code attempts to convert the string inputs to Decimal, which might raise an __InvalidOperation__ exception if the strings cannot be converted. Instead of checking beforehand if the strings are valid representations of numbers, the code just tries to convert them and catches the exception if it fails. This is a textbook example of EAFP, where the operation is attempted directly with exceptions used to handle cases where the operation is not possible.
<br>

Another example:
> The [`perform_operation`](https://github.com/fcamacho3/IS601MidtermProject--2024/blob/master/app/calculator/calc_utils.py#L9-L50) function within *app/calculator/calc_utils.py* is another prime example of employing the "Easier to Ask for Forgiveness than Permission" (EAFP) coding style. This approach is particularly effective in Python due to the language's robust exception handling mechanisms and the philosophy that it's better to attempt an operation and catch exceptions if it fails rather than pre-checking for conditions that might lead to failure. Here's how EAFP is applied in perform_operation:
```python
def perform_operation(num1: Decimal, num2: Decimal, operation_name: str) -> str:
    operation_mapping = {
        'add': Calculator.add,
        'subtract': Calculator.subtract,
        'multiply': Calculator.multiply,
        'divide': Calculator.divide,
    }

    logging.info(f"Attempting to perform operation: {operation_name} with operands {num1} and {num2}")

    try:
        operation_callable = operation_mapping.get(operation_name)
        if operation_callable is None:
            logging.error(f"Unknown operation: {operation_name}")
            return f"Unknown operation: {operation_name}"

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
```
> __Attempt Direct Operation:__ The function tries to perform the requested operation directly without checking if the operation is valid or if the operation will succeed. This is seen where it maps `operation_name` to a callable and attempts to invoke it with the provided operands.
> __Handling Exceptions as a Control Flow Mechanism:__ Instead of pre-validating the inputs or the operation's viability (for example, checking if num2 is zero before division), `perform_operation` proceeds with the operation and catches exceptions to handle various error scenarios: __ZeroDivisionError__, __ValueError__, and __General Exception__.

---

## 5. Video
[Calculator Demo Video](https://youtu.be/yBn5uVixzNs)
