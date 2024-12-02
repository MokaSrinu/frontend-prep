# if...elif...else

age = int(input('Please nter the age of the person...'))
if age < 5:
    print('Too Young')
elif age == 5:
    print('Kindergarden')
elif ((age > 5 ) and (age < 17)):
    grade = age - 5
    print('Go to {} grade'.format(grade))
else:
    print('Go To College')

    