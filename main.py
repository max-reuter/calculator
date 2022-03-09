import sys
import calculator

calc = calculator.Calculator()
while True:
    input = sys.stdin.readline()
    result = calc(input)
    if result == 'exit':
        break
    else:
        print(result)
