# Creating Class and Object in python

class myBird:
    def __init__(self):
        print('myBird class constructor is executing...')
    
    def whatType(self):
        print('I am a Bird...')

    def canSwim(self):
        print('I can Swim...')
    
# myPenguin class inheriting the attributes from the myBird class
class myPenguin(myBird):
    def __init__(self):
        # class super() function
        super().__init__()
        print('myPenguin class constructor is executing...')

    def whoisThis(self):
        print('I am Penguin...')

    def canRun(self):
        print('I can run faster...')

# Accessing the child class's attributes
pg1 = myPenguin()
pg1.canRun() # defined in myPenguin class
pg1.canSwim() # defined in myBird class
pg1.whatType() # defined in myBird class
pg1.whoisThis() # defined in myPenguin class
    

# Ploymorphism

class MyParrot:
    def canFly(self):
        print('Parrot can fly...')
    def canSwim(self):
        print('Parrot Cannot Swim...')

class MyPenguin:
    def canFly(self):
        print('Penguin cannot fly...')
    def canSwim(self):
        print('Penguin can swim...')

# Common Interface
def flying_bird_test(bird):
    bird.canFly()
    bird.canSwim()

# Instantiate objects
bird_parrot = MyParrot()
bird_penguin = MyPenguin()

flying_bird_test(bird_parrot)
flying_bird_test(bird_penguin)