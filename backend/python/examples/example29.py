# Declaring and defining a nested dictionary
people = {
    1: {'name': 'John', 'age': '24', 'sex': 'Male'},
    2: {'name': 'Marie', 'age': '25', 'sex': 'Female'},
}

print(people)

# Accessing elements of a dictionary
print(people[2]['name'])
print(people[1])
print(people[1]['name'])
print(people[1]['age'])
print(people[1]['sex'])

people[3] = {}
# Adding elements to a dictionary
people[3]['name'] = 'Luna'
people[3]['age'] = '24'
people[3]['sex'] = 'Female'
people[3]['married'] = 'No'

print('people', people)

# deleting elements from a dictionary
del people[3]['name']
print(people)

# deleting dictionary from nested dictionary
del people[3], people[1]
print(people)

# iterating through a nested dictionary
for p_id, p_info in people.items():
    print('\n Person ID:', p_id)

    for key in p_info:
        print(key + ':', p_info[key])
