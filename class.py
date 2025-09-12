class Person:
    count = 0
    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.count += 1
    def get_name(self):
        print("name is : %s" % self.name)
    def get_age(self):
        print("age is : %s" % self.age)
    def get_info(self):
        print("name is : (%s)  age is : (%i)" % (self.name, self.age))
    def tavalod(self):
        self.age += 1
        print ("tavalodt mobarak %s" % self.name)
    def return_count(self):
        return (Person.count)
jadi = Person('jadi', 40)

jadi.get_name()
jadi.get_age()
jadi.get_info()
jadi.tavalod()
jadi.get_age()

print ("adad : %i" % jadi.return_count())