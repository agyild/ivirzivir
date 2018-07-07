#!/usr/bin/env python3

# Quick and dirty Caesar cipher bruteforcer

import sys

if len(sys.argv) > 1:
    ciphertext = sys.argv[1].upper()

    for x in range(26):
        t = ''
        for y in ciphertext:
            y = ord(y)
            if 64 < y < 91:
                y += x
            if y > 90:
                y -= 26
            t += chr(y)
        print(f'{x+1:2}. {t} [{x:+3} | {x-26:+3}]', '[ROT13]' if x==13 else '')
else:
    import os.path
    print('Usage:\n' + os.path.split(sys.argv[0])[-1], 'ciphertext')