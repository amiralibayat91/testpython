a = input('chand saeat kar kardi: ')
b = input('dar saeat che qader pol migiry?: ')
a = int(a)
b = int(b)
def hogoogh(saeat, pol):
    if saeat > 24:
        return 'Error! saeat ziad'
    elif pol > 20:
        return 'Error! pol ziad'
    else:
        dramd = saeat * pol
        return dramd
print('shoma in qader pol gerftid! :')
print(hogoogh(a, b))