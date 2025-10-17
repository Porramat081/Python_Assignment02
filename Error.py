class TypeException(Exception):
    def __init__(self, variable , *type):
        condition = ""
        if len(type) > 1:
            condition = " or ".join(type)
        elif len(type) == 1:
            condition = type[0]
        super().__init__('\n'+variable + " must be "+condition+'\n')

class OptionException(Exception):
    def __init__(self, *option_list):
        super().__init__('\nInvalid option, please choose only: ' + ", ".join(option_list) + '\n')

class InvalidNumber(Exception):
    def __init__(self, variable ,type_constraint):
        condition = ""
        if type_constraint == '+':
            condition = "positive number (>= 0)"
        elif type_constraint == '>0':
            condition = "greater than zero (> 0)"
        message = f'\n{variable} must be {condition}\n'
        super().__init__(message) 

class ExtrabedException(Exception):
    def __init__(self, option , exist_bed=0):
        message = ""
        if option == 'max':
            message = "Extra bed can be ordered only 2 beds at maximum"
        if exist_bed > 0:
            message += f'\n You ordered {exist_bed} extra-bed already'
        super().__init__(f'\n{message}\n')

class CarParkException(Exception):
    def __init__(self, stay_length):
        message = 'Car Park must be ordered at least ' + stay_length
        super().__init__(message)