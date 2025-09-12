class Cumputer:
    count = 0
    def __init__(self, ram, hard, cpu):
        Cumputer.count += 1
        self.ram = ram
        self.hard = hard
        self.cpu = cpu

    def value(self):
        return self.ram+self.hard+self.cpu
    def __del__(self):
        Cumputer.count -= 1


class Laptop(Cumputer):
    def value(self):
        return self.ram + self.hard + self.cpu + self.size


pc1 = Cumputer(12, 2, 4)
print(pc1.value())
del pc1
pc2 = Cumputer(8, 4, 4)
print(pc2.value())
LP = Laptop(16, 2, 4)
LP.size = 13
print(LP.value())