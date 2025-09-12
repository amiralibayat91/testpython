import hashlib
import itertools
import string
import csv

# کاراکترهای ممکن: حروف کوچک و بزرگ و اعداد
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
length = 6  # طول پسورد
output_file = 'all_hashes_length4.csv'

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['password', 'sha256_hash'])  # سرستون‌ها

    count = 0
    for combo in itertools.product(chars, repeat=length):
        password = ''.join(combo)
        hash_value = hashlib.sha256(password.encode()).hexdigest()
        writer.writerow([password, hash_value])
        count += 1
        
        # نمایش پیشرفت هر 100000 ردیف
        if count % 100000 == 0:
            print(f"{count} hashes generated...")

print(f"تمام هش‌ها تولید شدند و در فایل '{output_file}' ذخیره شدند.")
