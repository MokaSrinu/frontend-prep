# Name (also called identifier) is simply a name given to objects

# We can get the adress (in RAM) of some object through built-in function, id().
# Note: You may get different value of id

a = 2
print('id(2)', id(2))
print('id(a)', id(a))

a = 2
print(id(a))

a = a + 1
print(id(a))
print(id(3))

b = 2
print(id(2))
print(id(b))

# Scope

def outer_func():
    global a
    a = 20
    def inner_func():
        global a
        a = 30
        print('a value:', a)
    inner_func()
    print('a value:', a)
a = 10
print(a)
outer_func()
print(a)



