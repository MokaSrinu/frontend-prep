# This is a comment

# This is a long comment
# and multi-line comment
# can be written like this

'''
Multi-line comments
can also be written like this
'''

# Statement - Assignment statement
a = 1

# Multi-line statement
# Explicit line continuation - '\'
b = 1 + 2 + 3 + \
    4 + 5 + 6

# Implicit line continuation within brackets
c = (1 + 2 + 3 + 
    4 + 5 + 6)

# Multiple statements in one line using ';'
d = 2; e = 1; f = 0


# code block (body of a function, loop etc,.) starts with indentation
# and ends with first unintended line
for i in range(1, 10):
    print(i)
    if i == 5:
        break

print('End of the program...')

