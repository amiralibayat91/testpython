import random

k = 1
b = 99
hads = random.randint(k, b)
print(f'aya javab shoma in add ast? ', hads)
javab = input ('age dorost bego (d) age bozorg tare bego (b) agar ham kocheik tare bego (k)? ')

while javab != 'd':
    if javab == 'k':
        b = hads - 1
        hads = random.randint(k, hads)
        print(f'aya javab shoma in add ast? ', hads)
    elif javab == 'b':
        k = hads + 1
        hads = random.randint(hads, b)
        print(f'aya javab shoma in add ast? ', hads)
    else:
        print(f'age addet = {hads} bego (d) age addet > {hads} bego (b) agar addet < {hads} bego (k) :')

    javab = input ('age dorost bego (d) age bozorg tare bego (b) agar ham kocheik tare bego (k)? ')
    
print(f'wowwwwwwwwwowowwwwowowwowowowo my wiinnnnnnnn')