import hashlib
import itertools
import string

# کاراکترهایی که پسورد می‌تواند شامل شود
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
length = 4  # طول پسورد

def find_password(target_hash):
    for combo in itertools.product(chars, repeat=length):
        candidate = ''.join(combo)
        if hashlib.sha256(candidate.encode()).hexdigest() == target_hash:
            return candidate
    return None

# گرفتن هش از کاربر
target_hash = input ("hash password sha256 ro ward knid : ").strip()

# پیدا کردن پسورد
password = find_password(target_hash)

if password:
    print(f"password ro pey da kardam : {password}")
else:
    print("password ro pey da nakardam !")
