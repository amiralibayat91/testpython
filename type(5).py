def hogog(hour, per_hour):
    if hour > 12:
        return 'Error! '
    else:
        kol = hour * per_hour
        return kol

print(hogog(5, 2))
