# Global and Local variable with different name
x = 'global'
def funct1():
    global x
    y = 'local'
    x = x * 2
    print(x)
    print(y)

print('Global x:', x)
funct1()
print('Global x after funct1 invocation:', x)

# global and local variable with same name
a = 5
def func2():
    a = 10
    print('Local variable a:', a) # local variables are accessed from the block where it is defined only
print('Global a:', a)
func2()
print('Global a:', a)

# Creating and using Non-local variable

def outer():
    b = 'local'
    def inner():
        nonlocal b # Non-local variable are used in nested functions
        b = 'nonlocal'
        print('Inner b:', b)
    print('Outer b:', b) 
    inner()
    print('Outer b:', b)
outer()


