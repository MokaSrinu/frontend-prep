# Decorators

def make_decorated(func):
    def inner_func():
        print('I got decorated.')
        func()
    return inner_func

def simple_func():
    print('I am a simple function')

decor = make_decorated(simple_func)
decor()


# The above implementation can also be written in a simple way with '@'

def make_decorated(func):
    def inner_func():
        print('I got decorated.')
        func()
    return inner_func

@make_decorated
def simple_func():
    print('I am a simple function')

simple_func()

# Example2:
def my_smart_div(func):
    def inner_func(x, y):
        print('I am dividing x, and y')
        if y == 0:
            print('Oops! Division by Zero is illegal... !!!')
            return
        return func(x, y)
    return inner_func

@my_smart_div
def go_divide(a, b):  # generally, we decorate a function and reassign it as,
    return a/b        # go_divide = my_smart_div(go_divide)

print('20/2', go_divide(20, 2))