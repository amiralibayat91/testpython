# crack_fast.py
import hashlib
import csv
import argparse
from pathlib import Path

def load_hashes(path):
    d = {}
    with open(hash.csv, 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            user = row[0].strip()
            h = row[1].strip().lower()
            d[user] = h
    return d

def build_hash_dict(wordlist_path):
    h2p = {}
    with open(wordlist_path, encoding='utf-8', errors='ignore') as f:
        for line in f:
            pw = line.rstrip('\n')
            if not pw: continue
            h = hashlib.sha256(pw.encode('utf-8')).hexdigest()
            # فقط اولین متناظر را ذخیره می‌کنیم (در صورت وجود collision انسانی نادر است)
            if h not in h2p:
                h2p[h] = pw
    return h2p

def main(hashes_file, wordlist_file, out_file=None):
    hashes = load_hashes(hashes_file)
    print(f"Loaded {len(hashes)} target hashes.")
    h2p = build_hash_dict(wordlist_file)
    print(f"Built dictionary of {len(h2p)} password hashes.")
    results = {}
    for user, target in hashes.items():
        pw = h2p.get(target)
        if pw:
            results[user] = pw
            print(f"[+] {user} -> {pw}")
        else:
            print(f"[-] {user} -> NOT FOUND")

    if out_file:
        with open(out_file, 'w', encoding='utf-8') as f:
            for user, pw in results.items():
                f.write(f"{user},{pw}\n")
        print(f"Results saved to {out_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crack SHA-256 hashes with a wordlist.")
    parser.add_argument('--hashes', default='hashes.csv', help='CSV file username,hash')
    parser.add_argument('--wordlist', default='passwords.txt', help='wordlist (one password per line)')
    parser.add_argument('--out', default='cracked.txt', help='output file for found passwords (optional)')
    args = parser.parse_args()
    main(args.hashes, args.wordlist, args.out)
