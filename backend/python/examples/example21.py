# Function taking arguments and returning a value

def findMax(a, b):
    if a > b:
        return a
    else:
        return b
    
print('Max of 10 and 20 is:', findMax(10, 20))

# Function with default parameter
def hello(name, msg = ", how are you?"):
    print("Hello", name, msg)

hello('srinu', ", What's up?")
hello('stranger')

# function with arbitrary arguments

def sumAll(*args):
    sum = 0
    for i in args:
        sum += i
    return sum

print('Sum of all Integers between 1 and 5 is:', sumAll(1, 2, 3, 4, 5))

def defaultArg(a = 0, b = 0, c = 0):
    print('a = {}, b = {}, c = {}...'.format(a,b,c))
defaultArg(10, 20, 30)
defaultArg(10, 20)
defaultArg(10)
defaultArg()
defaultArg(b=222, c=333, a=111)
