import hashlib
import csv
import random

# with open('G:\python\hashes.csv') as f:
#     reader = csv.reader(f)
#     for i in reader:
#         name = i[0]
        
#     f = {i[1]}
#     print(f)

t = {}

target_hash = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
for num in range(10000):
    if hashlib.sha256(str(num).encode()).hexdigest() == target_hash:
        print(f"Password is: {num}")
        break