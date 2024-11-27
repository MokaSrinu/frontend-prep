# A simple generator function
def my_generator():
    n = 1
    print('This is printed first')
    # Generator function contains yield statements
    yield n

    n += 1
    print('This is printed second')
    yield n

    n += 1
    print('This is printed third')
    yield n

a = my_generator()
# iterating using next()
next(a)
next(a)
next(a)

print('Using for loop...')
# Iterating using for loop
for item in my_generator():
    print(item)


# Generators with loop
def reverse_string(my_string):
    length = len(my_string)
    for i in range(length-1, -1, -1):
        yield my_string[i]
    
# for loop to reverse the string

for char in reverse_string('World'):
    print(char)
