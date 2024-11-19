# Defining and declaring an array
arr = [10, 20, 30, 40, 50]
print(arr)

# Accessing Array Elements
print(arr[0], arr[1], arr[2], arr[-1], arr[-2])



brands = ['Coke', 'Apple', 'Google', 'Microsoft', 'Toyota']
# finding the length of the array
brands_length = len(brands)
print(brands_length)

# adding an element to an array using append
brands.append('Intel')
print(brands)


# removing elements from an array
del brands[0]
print(brands)
brands.remove('Intel')
print(brands)
brands.pop(3)
print(brands)


# modifying elements of an array using indexing
brands[0] = 'banana'
brands[-1] = 'mango'
print(brands)

# concatinating 2 array using +
concat = [1, 2, 3]
concat+= [4, 5, 6]
print(concat)

# Repeating element in array
repeat = ['a']
repeat = repeat * 5
print(repeat)

# Slicing an array
fruits = ['Apple', 'Banana', 'Mango', 'Grapes', 'Orange']
print(fruits[1:4])
print(fruits[ : 3])
print(fruits[-4: ])
print(fruits[-3 : -1])

# declaring and defining multi-dimensional array
multd = [[1, 2], [3, 4], [5, 6], [7, 8]]
print(multd)
print(multd[0])
print(multd[3])
print(multd[3][1])
print(multd[2][0])

