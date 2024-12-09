# 1. Creating an empty tuple
tuple1 = ()
print(tuple1)

# 2. Creating tuple with integer elements
tuple2 = (1, 2, 3)
print(tuple2)

# 3. Tuple with mixed Data Types
tuple3 = ('Srinu', 24, 200.00, True)
print(tuple3)

# 4. Creation of Nested Tuples
tuple4 = ('points', [1, 4, 3], (7, 8, 6))
print(tuple4)

# 5. Tuple can be created with out paranthesis
# also called Tuple Packing
tuple5 = 101, 'srinu', 2000.00, 'Tech'
print(tuple5)

# 6. Tuple unpacking is also possible
empid, empname, empsal, empdept = tuple5
print(empid)
print(empname)
print(empsal)
print(empdept)

# 7. Accessing elements in a Tuple
tuple6 = ('w', 'e', 'l', 'c', 'o', 'm', 'e')
print(tuple6)
print(tuple6[1])
print(tuple6[3])
print(tuple6[5])

# 8. Accessing Nested Tuple
nested_tuple = ('point', [1, 3, 5], (8, 7, 9))
print('Nested tuple', nested_tuple)
print(nested_tuple[0])
print(nested_tuple[1][0])
print(nested_tuple[2][2])

# 9. Slicing Tuple Contents
slicing_tuple = ('w', 'e', 'l', 'c', 'o', 'm', 'e')
print(slicing_tuple[1:3])
print(slicing_tuple[:-3])
print(slicing_tuple[3:])
print(slicing_tuple[:])

# 10. Tuple elements are immutable
tuple7 = ('w', 'e', 'l', 'c', 'o', 'm', 'e')
print(tuple7)
# tuple7[1] = 'x' # TypeError: 'tuple' object does not support item assignment

# 11. Tuples can be reassigned
tuple7 = ('g', 'o', 'o', 'd', 'b', 'y', 'e')
print(tuple7)

# 12. concatenation of Tuples
tuple8 = ('w', 'e', 'l')
tuple9 = ('c', 'o', 'm', 'e')
print(tuple8 + tuple9)
print(('again', ) * 4) # Tuple duplicating 4 times

# 13. deletion operation on Tuple
tuple_to_delete = ('d', 'e', 'l', 'e', 't', 'e', 'm', 'e')

# # as Tuple is immutable elements cannot be deleted
# del tuple_to_delete[2] #TypeError: 'tuple' object doesn't support item deletion

# # but can delete the entire tuple
# del tuple_to_delete
# print(tuple_to_delete) # NameError: name 'tuple_to_delete' is not defined

# 14. Tuple Methods
tuple10 = ('w', 'e', 'l', 'c', 'o', 'm', 'e', 'c')
print(tuple10.count('e'))
print(tuple10.index('c'))

# 15. Tuple Operations
# membership
print('c' in tuple10)
print('c' not in tuple10)
print('a' in tuple10)
print('a' not in tuple10)

# 16. Iteration through Tuple Elements
for letters in tuple10:
    print('Letter is:', letters)

# 17. Built-in functions with Tuple
tuple11 = (22, 33, 55, 44, 77, 66, 11)
print(max(tuple11))
print(min(tuple11))
print(sorted(tuple11))
print(len(tuple11))
