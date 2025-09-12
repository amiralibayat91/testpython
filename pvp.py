string = 'salam. jadi is here and testing python for fun'

counter = dict()

for letter in string:

        counter[letter] = counter.get(letter, 0) + 1

for this_one in (counter.keys()):
    print('%s item %s  wjod dare' % (this_one, counter[this_one]))