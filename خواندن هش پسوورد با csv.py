import hashlib
import csv
import itertools
import string

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
length = 4

def find_password(target_hash):
    for combo in itertools.product(chars, repeat=length):
        candidate = ''.join(combo)
        if hashlib.sha256(candidate.encode()).hexdigest() == target_hash:
            return candidate
    return None

input_file = 'hashes.csv'   # فایل ورودی که شامل دو ستون هست
output_file = 'results.csv' # فایل خروجی

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    writer.writerow(['label', 'hash', 'password'])
    
    for row in reader:
        label = row[0].strip()       # ستون اول: حروف a, b, c,...
        target_hash = row[1].strip() # ستون دوم: هش
        password = find_password(target_hash)
        writer.writerow([label, target_hash, password])
        print(f"Processed: {label} -> {password}")
