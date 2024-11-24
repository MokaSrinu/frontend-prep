def func1():
    x = 20
    def func2():
        global x # global keyword is used to modify a global variable
        x = 25
    
    print('Before calling function2:', x)
    print('Calling func2 now...')
    func2()
    print('After calling func2:', x)

func1()
print('Global x', x)

