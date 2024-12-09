import random as r
random_num = r.randrange(1, 10) # Generating a random number between 1 and 9
i = 1
while True:
    if(i == random_num):
        print('Random Number guesses correctly', random_num, i)
        break
    i += 1

