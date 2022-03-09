import math

# Possible extensions:
# * more calculation functions:
#       - cubed root, or any arbitrary root
#       - logarithm (base 10, base 2, etc.), natural logarithm
#       - trigonometry (sin, cos, tan, arcsin, etc.)
# * QOL
#       - allow for input of negative and multiples of constants, e.g. "-2pi"
#       - "undo" functionality

class Calculator:
    valid_operations = ['add', 'sub', 'mult', 'div', 'sqrt', 'pow']
    current_value = 0
    previous_calculation = (None, None, None) # operation, operand1, operand2

    def __init__(self):
        self.print_usage() # print usage details
        print(self.current_value) # print the current value, 0

    def __call__(self, input):
        return self.process_input(input)

    def print_usage(self):
        print('Usage:')
        print('       Operations: (add), (sub)tract, (mult)iply, (div)ide, (sqrt), (pow)er')
        print('       Constants: pi, e')
        print('       (1) "operation operand1 operand2"')
        print('       (2) "operation operand2" (takes current value as operand1)')
        print('       (3) "operation" (applies the operation to the current value, if applicable)')
        print('       (4) "<enter key>" (repeats the previous calculation on the current value)')
        print('       (5) "clear", "help", "exit"')
        print('       Example 1: "add 2 2"  --> 4.0')
        print('       Example 2: "sqrt 81"  --> 9.0')
        print('                  "sqrt"     --> 3.0')
        print('       Example 3: "pow e pi" --> 23.140692632779263')
    
    def void_command(self):
        self.previous_calculation = (None, None, None)
        return self.current_value # return the value as it was

    def process_input(self, input):
        parsed_args = input.split()
        
        if len(parsed_args) == 0:                                   # no input, return previous operation applied to current value
            return self.calculate(self.previous_calculation)
        elif parsed_args[0] == 'exit':                              # exit, return 'exit'
            return self.exit()
        elif parsed_args[0] == 'help':                              # help, print usage and return current value
            self.print_usage()
            return self.current_value
        elif parsed_args[0] == 'clear':                             # clear, return the new ("clear") value of 0
            return self.clear()
        elif parsed_args[0] == 'sqrt':                              # check syntax for sqrt, return calculation if appropriate
            if len(parsed_args) == 1:
                return self.calculate(['sqrt', None, None])
            elif len(parsed_args) > 2:
                print('invalid syntax: sqrt takes at most one operand.')
                return self.void_command()
        
        # ensure (1) a valid operation was given and (2) either 1 or 2 operands were given
        elif len(parsed_args) not in [2, 3] or parsed_args[0] not in self.valid_operations:
            print('invalid syntax: must provide 1 valid operation and the appropriate number of operands.')
            return self.void_command()
        operation = parsed_args[0]
        
        # ensure operand(s) are numbers or special constants
        try:
            def convert_operand(operand):
                if operand == 'pi':
                    return math.pi
                elif operand == 'e':
                    return math.e
                else:
                    return float(operand)
            operand1 = convert_operand(parsed_args[1])
            operand2 = None if len(parsed_args) < 3 else convert_operand(parsed_args[2])
        except ValueError:
            print('invalid syntax: input operands must be numbers or supported constants.')
            return self.void_command()

        # valid input syntax, proceed with calculation
        calculation = (operation, operand1, operand2)
        result = self.calculate(calculation)
        return result


    def calculate(self, calculation):
        operation, operand1, operand2 = calculation
        if operation == 'add':                      # add
            self.add(operand1, operand2)
        elif operation == 'sub':                    # subtract
            self.subtract(operand1, operand2)
        elif operation == 'mult':                   # multiply
            self.multiply(operand1, operand2)
        elif operation == 'div':                    # divide
            self.divide(operand1, operand2)
        elif operation == 'sqrt':                   # sqrt
            self.sqrt(operand1)
        elif operation == 'pow':                    # pow
            self.power(operand1, operand2)

        # store the formulation of this calculation to later reference as the previous calculation
        if operation == 'sqrt':
            self.previous_calculation = ('sqrt', None, None)
        else:
            self.previous_calculation = (operation, operand1 if operand2 is None else operand2, None)
        
        return self.current_value

    def add(self, operand1, operand2):
        self.current_value = self.current_value + operand1 if operand2 is None else operand1 + operand2

    def subtract(self, operand1, operand2):
        self.current_value = self.current_value - operand1 if operand2 is None else operand1 - operand2

    def multiply(self, operand1, operand2):
        self.current_value = self.current_value * operand1 if operand2 is None else operand1 * operand2

    def divide(self, operand1, operand2):
        if (operand2 is None and operand1 == 0) or (operand2 == 0):
            print('invalid calculation: attempted to divide by zero!')
        else:
            self.current_value = self.current_value / operand1 if operand2 is None else operand1 / operand2

    def sqrt(self, operand1=None):
        try:
            if operand1 is None:
                self.current_value = math.sqrt(self.current_value)
            else:
                self.current_value = math.sqrt(operand1)
        except ValueError:
            print('invalid calculation: attempted to take sqaure root of negative number!')

    def power(self, operand1, operand2):
        try:
            if operand2 is None:
                self.current_value = math.pow(self.current_value, operand1)
            else:
                self.current_value = math.pow(operand1, operand2)
        except OverflowError:
            # Catch any overflow error and set the current value to infinity.
            # This keeps this operation consistent with the behavior of the rest of the class,
            # namely setting the current value to -inf or inf instead of throwing overflow errors.
            self.current_value *= float('inf') # multiply by current value to preserve sign
        except ValueError:
            print('invalid calculation: attempted to divide by zero!')


    def clear(self):
        self.current_value = 0
        self.previous_calculation = (None, None, None)
        return self.current_value

    def exit(self):
        return 'exit'
