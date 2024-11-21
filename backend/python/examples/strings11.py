# different ways to define a string in python
mystr1 = 'welcome'
print(mystr1)

mystr2 = "welcome"
print(mystr2)

mystr3 = '''welcome'''
print(mystr3)

mystr4 = """welcome"""
print(mystr4)

# Triple Quotes string can extend multiple line
mystr5 = '''welcome
to the world of 
python programming'''
print(mystr5)

# accessing characters in a string
my_str = 'language'
print('my_str', my_str)

print('my_str[0] = ', my_str[0])
print('my_str[-1] = ', my_str[-1])
print('my_str[1:5] = ', my_str[1:5])
print('my_str[5:-2] = ', my_str[5:-2])
# print('my_str[10] = ', my_str[10]) # IndexError: string index out of range


# strings are immutable but different strings can be assigned
my_str1 = 'language'
print(my_str1)

my_str1 = 'programming'
print(my_str1)

# my_str1[3] = 'x' # TypeError: 'str' object does not support item assignment

# concatenation of strings
print(my_str1 + my_str)
print(my_str1 * 3)

# Iterating through a string
letter_count = 0
for letter in my_str1:
    if letter == 'm':
        letter_count += 1
print('Count of letter m in my_str1 is:', letter_count)

# string membership
print('l' in 'hello')
print('l' not in 'hello')
print('b' in 'hello')
print('b' not in 'hello')

# built-in functions
my_str2 = 'university'

my_list_enumerate = list(enumerate(my_str2))
print('list(enumerate(my_str2)):', my_list_enumerate)

# using character count
print('length of my_str2 is:', len(my_str2))

# string formatting using escape sequence
# print("tell me "what is your name ? "") # SyntaxError: invalid syntax. Perhaps you forgot a comma?

# using triple quotes
print('''tell me "what's your name?"''')

# escaping single quotes
print('tell me "what\'s your name?"')

# escaping single quotes
print("tell me 'what\'s your name?'")

# escaping double quotes
print("tell me \"what's your name?\"")

print("C:\\User\\user\\mydata.txt")
print("This line is having a new line \ncharacter")
print("This line is having a tab \tcharacter")
print("ABC written in \x41\x42\x43 (Hex) Representation")

# format() method
# default (implicit) order
default_order = '{} {} {}'.format('Today', 'is', 'sunday')
print(default_order)

# order using positional argument
positional_order = '{1} {0} {2}'.format('is', 'Today', 'sunday')
print(positional_order)

# order usinhg keyword argument
keyword_order = '{t} {i} {s}'.format( i='is', t='Today', s='sunday' )
print(keyword_order)

# formatting numbers
print('Required binary represntation of {0}is {0:b}'.format(20))

# formatting floats
print('Exponent representation : {0:e}'.format(1566.345))

# round off
print('One third is: {0:3f}'.format(1/3))

# string methods

