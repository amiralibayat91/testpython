import hashlib
import csv

chars = '0123456789'
length = 4

def find_password(target_hash):
    for num in range(10**length):
        candidate = f"{num:0{length}d}"  # عدد 4 رقمی با صفر پر شده مثل 0001 یا 0234
        if hashlib.sha256(candidate.encode()).hexdigest() == target_hash:
            return candidate
    return None

input_file = 'hashes.csv'   # فایل ورودی که شامل دو ستون: label, hash
output_file = 'results.csv' # فایل خروجی

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    writer.writerow(['label', 'hash', 'password'])
    
    for row in reader:
        label = row[0].strip()
        target_hash = row[1].strip()
        password = find_password(target_hash)
        writer.writerow([label, target_hash, password])
        print(f"Processed: {label} -> {password}")
