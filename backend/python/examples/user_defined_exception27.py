class VotersEligibility(Exception):
    def __init__(self):
        super()
    
try:
    age = '18'
    print('Age is', str(age))
    if age < 18:
        raise VotersEligibility
except VotersEligibility:
    print('Age is less than 18.')
except TypeError:
    print('Age is not Numeric')
else:
    print('Age is greater than or equal to 18.')
finally:
    print('End of the program.')
