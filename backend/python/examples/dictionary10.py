# Accessing elements from a dictionary
new_dict = { 1: 'Hello', 2: 'Hi', 3: 'Hola' }
print(new_dict)
print(new_dict[1])
print(new_dict.get(2))

# Updating value
new_dict[1] = 'Hey'
print(new_dict)

# Adding Value
new_dict[4] = 'Namste'
print(new_dict)

# Creating a new dictionary
squares = { 1: 1, 2: 4, 3: 9, 4: 16, 5: 25 }
print(squares)

# Remove a particular item
print(squares.pop(4))
print(squares)

# Remove an arbitrary item
print(squares.popitem())
print(squares)

# Delete a Particular item
del squares[1]
print(squares)

# remove all items
squares.clear()
print(squares)

# delete the dictionary itself
del squares
# print(squares) # NameError: name 'squares' is not defined

# Creating a new dictionary using Comprehension
squares1 = {x: x*x for x in range(6)}
print(squares1)

# Dictionary membership test
squares2 = { 1: 1, 3: 9, 5: 25, 7: 49, 9: 81 }
print(1 in squares2)
print(2 not in squares2)
print(49 in squares2) # membership tests for key but not for value

# Iterating through a dictionary
for i in squares2:
    print(squares2[i])

# Using built-in functions in a dictionary
print(len(squares2)) # prints the length of the dictionary
print(sorted(squares2)) # prints the dictionary in sorted order



