# error handling in python
try:
    '''
    The code which can give raise to an exception is written here.
    '''
    a = 'hi'
    b = int(a)
    print('Value of b:', b)
except:
    print('Exception Caught!')


# Catch Specific exception
try:
    x = 5
    y = 0
    z = x/y
except ZeroDivisionError:
    print('Division by Zero is not possible.')

# Exceptions can also be raised.
try:
    raise TypeError
except TypeError:
    print('Type Exception Caught!')

# try...except...finally
try:
    print('Im in Try block')
    raise TypeError
except:
    print('Im in Except block')
finally:
    print('Im in finally block')
