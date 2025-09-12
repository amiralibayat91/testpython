import random
javab = random.randint(1, 99)
name = input ('What is your name? ')
hads = input ('What is your hads? ')
hads = int(hads)

while hads != javab:
    if hads > javab:
        print (f'adad man kochik tare az {hads}!')
    else:
        print (f'adad man boozoorg tare az {hads}!')

    hads = input ('What is your hads? ')
    hads = int(hads)
print('aaaaafaaaaarrrrrriiiiinnnnn!!!!!!', name, 'dorost bod !!')