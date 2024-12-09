# Creating Class and Object in python

class myBird:
    def __init__(self):
        print('myBird class constructor is executing...')
    
    def whatType(self):
        print('I am a Bird...')

    def canSwim(self):
        print('I can Swim...')

class myParrot:
    # class attribute
    species = 'bird'

    # instance attribute
    def __init__(self, name, age):
        print('myParrot class constructor is executing...')
        self.name = name
        self.age = age

    def canSing(self, thisSong):
        return '{} can sing {}'.format(self.name, thisSong)
    
class myPenguin(myBird):
    def __init__(self):
        # call super() function
        super().__init__()
        print('Penguin is ready')

    def whoIsThis(self):
        print('I am Penguin.')

    def canRun(self):
        print('I can run faster.')

# instantiate the Parrot class
mp1 = myParrot('MyParrpt1', 10)
mp2 = myParrot('MyParrot2', 12)

# access the class attributes
print('mp1 is {}'.format(mp1.__class__.species))
print('mp2 is also a {}'.format(mp2.__class__.species))

# access the instance attributes
print('{} is {} years of age'.format(mp1.name, mp1.age))
print('{} is {} years of age'.format(mp2.name, mp2.age))
print(mp1.canSing('chirp'))

# accessing the child class's attributes (Inheritance)
pg1 = myPenguin()
pg1.whoIsThis()
pg1.canSwim()
pg1.canRun()

## Data encapsulation
class personalComputer:
    def __init__(self):
        self.maxComputerPrice = 20000

    def mySell(self):
        print('selling price: {}'.format(self.maxComputerPrice))

    def setMaxComputerPrice(self, price):
        self.maxComputerPrice = price
    
pc = personalComputer()
pc.mySell()

# change the price 
pc.maxComputerPrice = 30000
pc.mySell()

# using setter function
pc.setMaxComputerPrice(40000)
pc.mySell()
        