## 5.Python KeyWords and Identifiers

# 1.True False
print(5==5)
print(5>5)

# 2.None
print(None==0)
print(None==[])
print(None==False)
print(None==None)

# 3.A void function returns 'None'
def a_void_function():
    a=1
    b=2
    c=a+b
x=a_void_function()
print(x)

# 4.and, or, not
print(True and False)
print(True or False)
print(not True)

# 5.as
import math as myMath
print(myMath.cos(myMath.pi))

# 6.assert
assert 5 > 5 # Assertion Error
assert 5 == 5

# 7.break
for i in range(1,11):
    if i ==5:
        break
    print(i)

# 8.continue
for i in range(1,11):
    if i == 5:
        continue
    print(i)

# 9.class
class ExampleClass:
    def function1(parameters):
        print('Invoking function1 with params...', parameters)
    def function2(parameters):
        print('Invoking function2 with params...', parameters)

obj1 = ExampleClass
obj1.function1(1)
obj1.function2(2)

# 10.def and pass
def function_name(parameter):
    print('hi')
    pass
function_name(1)

# 11.del
a=10
print(a)
del a
print(a) # NameError: name 'a' is not defined

# 12.if..elif..else
num=2
if num == 1:
    print('One')
elif num == 2:
    print('Two')
else:
    print('Something Else')

# 13.try..raise..catch..finally
try:
    x=9
    raise ZeroDivisionError
except ZeroDivisionError:
    print('Division Cannot be performed')
finally:
    print('Execution success')

# 14.for
for i in range(1,10):
    print(i)

# 15.from..import
import math
from math import cos
print(cos(10))

# 16.global
globalVar = 10
def read1():
    print(globalVar)
def write1():
    global globalVar
    globalVar = 5
def write2():
    globalVar = 15
read1()
write1()
read1()
write2()
read1()

# 17.in, not in
a = [1, 2, 3, 4]
print(4 in a)
print(5 not in a)

# 18.is
print(True is True)
print(1 is 2)

# 19.lambda --> for anonymous functions. def for defined functions.
a = lambda x: x * 2
for i in range(1,5):
    print(a(i))

# 20.nonlocal --> here inner functions nonlocal 'a' --> assigns value to nonlocal variable 'a' which is outer functions 'a'.
def outer_func():
    a = 5
    def inner_func():
        nonlocal a
        a = 10
        print('inner function', a)
    inner_func()
    print('outer function', a)
outer_func()

# 21.pass --> pass is nothing but one placeholder later for new code insertion, we can replace pass with new set of codes.
def function1():
    pass

# 22.return
def functionWithReturnValue():
    a = 10
    return a
print(functionWithReturnValue())

# 23.while
i = 5
while(i>0):
    print(i)
    i-=1

# 24.with
with open('example.txt', 'w') as my_file:
    my_file.write('Hello World!!')

# 25.yield
def generator():
    for i in range(6):
        yield i*i
g = generator()
for i in g:
    print(i)


