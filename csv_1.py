import csv
from statistics import mean

with open('G:/python/1234.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print (row)
        name = row[0]
        this_grade = list()
        for grade in row[1:]:
            this_grade.append(int(grade))
            print(this_grade)
        
        print("average %s is: %2.3f" % (name, mean(this_grade)))