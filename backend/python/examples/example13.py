value1 = 100
print(type(value1))
print(isinstance(value1, int))
print(isinstance(value1, float))
print(isinstance(value1, complex))

value2 = 100.24
print(type(value2))
print(isinstance(value2, int))
print(isinstance(value2, float))
print(isinstance(value2, complex))

value3 = 50 + 6j
print(type(value3))
print(isinstance(value3, int))
print(isinstance(value3, float))
print(isinstance(value3, complex))

print(0b1101, 0B1101) # binary representation. 2^3*1+2^2*1+2^1*0+2^0*1 = 8+4+0+1 = 13
print(0xab, 0Xab) # hexa-decimal representation 16^1*10 + 16^0*11 = 160 + 11 = 171
print(0o23, 0O23) # octal 8^1*2 + 8^0*3 = 16 + 3 = 19

# Type conversion
print(int(10.5)) # 10
print(int(-20.99)) # -20
print(float(5)) # 5.0

# python decimal
data1 = 0.1 + 0.2
print(data1)
data1 = 1.20 * 2.50
print(data1)
from decimal import Decimal as D
print(D('0.1') + D('0.2'))
print(D('1.2') * D('2.5'))

# python fractions
from fractions import Fraction as F
print(F(1.5))
print(F(5))
print(F(1,5))

# python math module
import math
print(math.pi)
print(math.cos(10))
print(math.log(10))
print(math.log10(10))
print(math.exp(10))
print(math.factorial(5))
print(math.sinh(10))
print(abs(-12.34))

# python random module
import random
print('Random Number -->', random.randrange(5,15))
print('Random Number -->', random.randrange(5,15))

day = ['sun', 'mon', 'tue', 'wed', 'thurs', 'fri', 'sat']
print(random.choice(day))

print(day)
random.shuffle(day)
print(day)

# print random element
print(random.random())

