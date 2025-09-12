import hashlib
import itertools
import string

# کاراکترها: حروف کوچک، حروف بزرگ و اعداد
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits

target_hash = "fe2592b42a727e977f055947385b709cc82b16b9a87f88c6abf3900d65d0cdc3"
length = 4  # طول پسورد

for combo in itertools.product(chars, repeat=length):
    candidate = "".join(combo)
    if hashlib.sha256(candidate.encode()).hexdigest() == target_hash:
        print("Password is:", candidate)
        break
