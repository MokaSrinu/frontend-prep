# 1. Creating Sets
# Set of Integers
my_set1 = {11, 33, 66, 55, 44, 22}
print(my_set1)

# Set of Mixed DataTypes
my_set2 = {101, 'agnibha', (21, 2, 1994)}
print(my_set2)

# Duplicate values are not allowed
my_set3 = {11, 22, 44, 33, 11, 33, 22, 22, 23}
print(my_set3)

# # Set cannot have a Mutable Items
# my_set4 = {1, 2, [3, 4]} # TypeError: unhashable type: 'list'

# We can make a Set from a List
my_set5 = set([1, 2, 3, 2])
print(my_set5)
print(type(my_set5))

# We can make a List from a set
my_list1 = list({11, 22, 33, 44})
print(my_list1)
print(type(my_list1))

# 2. Operations on Sets
my_set6 = {11, 33, 44, 66, 55}

# # 'set object does not support indexing
# print(my_set6[1]) # TypeError: 'set' object is not subscriptable

# add an element
my_set6.add(77)
print(my_set6)

# Add Multiple Elements
my_set6.update([23, 36, 6])
print(my_set6)

# Add List and Set
my_set6.update([100, 200], {103, 104, 105})
print(my_set6)

# remove and discard
# discard an element which is not present, no error
my_set6.discard(4)
print(my_set6)

# # remove an element which is not present, error raised
# my_set6.remove(4) # KeyError: 4

# discard an element
my_set6.discard(100)
print(my_set6)

# remove an element
my_set6.remove(200)
print(my_set6)

# using pop()
# pop an element
print(my_set6.pop())
print(my_set6.pop())

# clear my set
my_set6.clear()
print(my_set6)

# set Operations -- Union, Intersection, Set difference, symmetric-difference
myset1 = {0, 1, 2, 3, 4, 5}
myset2 = {4, 5, 6, 7, 8, 9}

# use "|" operator for union
print(myset1 | myset2)
print(myset2 | myset1)
print(myset1.union(myset2))
print(myset2.union(myset1))

# use "&" operator for intersection
print(myset1 & myset2)
print(myset2 & myset1)
print(myset1.intersection(myset2))
print(myset2.intersection(myset1))

# use "-" operator for set difference
print(myset1 - myset2)
print(myset2 - myset1)
print(myset1.difference(myset2))
print(myset2.difference(myset1))

# use "^" operator for symmetric difference
print(myset1 ^ myset2)
print(myset2 ^ myset1)
print(myset1.symmetric_difference(myset2))
print(myset2.symmetric_difference(myset1))

# set membership
myset3 = {0, 1, 2, 3, 4, 5}
print(2 in myset3)
print(6 in myset3)
print(2 not in myset3)
print(6 not in myset3)


# Iterating through a set
for letter in set('welcome'):
    print(letter)

# built-in functions with sets
print(len(myset3))
print(max(myset3))
print(min(myset3))
print(sorted(myset3))


# python frozenset
# Frozenset is a new class that has the characteristics of a set, but its elements cannot be changed once assigned.
# while tuples are immutable lists, frozensets are immutable sets
myset4 = frozenset([1, 2, 3, 4])
myset5 = frozenset([3, 4, 5, 6])
print(myset4)
print(myset5)
print(myset4.difference(myset5))
print(myset4.union(myset5))
print(myset4.intersection(myset5))
print(myset4.symmetric_difference(myset5))
# myset5.add(4) # AttributeError: 'frozenset' object has no attribute 'add'

