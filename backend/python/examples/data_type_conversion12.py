# Implicit Type conversion
num_int = 123
num_float= 1.23
new_num = num_int + num_float

print('Interger Number:', num_int, 'Type:', type(num_int))
print('Float Number:', num_float, 'Type:', type(num_float))
print('Added New Number:', new_num, 'Type:', type(new_num))


# Addition of string(higher) data type and integer(lower) data type
num_int1 = 123
num_str1 = '123'
print('Integer data type:', num_int1, 'Type:', type(num_int1))
print('String data type:', num_str1, 'Type:', type(num_str1))

# Error: Implicit conversion will not work here
# print(num_int1 + num_str1)

# Explicit type conversion
num_str1 = int(num_str1) # converting string into integer
print('Data type of the string after Type casting', type(num_str1))
num_sum = num_int1 + num_str1
print('Sum of num_str1 & num_int1:', num_sum, 'Type:', type(num_sum))
