#!/usr/bin/python

# A quick one-off to solve the problem posed at http://hackerunderground.com/

import re
from math import sqrt, floor

p = re.compile('[a-z]+', re.IGNORECASE)

file = open('puzzle.txt')
prime_candidates = []

# Chuck letters and grab uniques
while 1:
    line = file.readline()
    if not line:
        break
    lines = line.split(' ')
    lines.sort()
    prev_line = 0
    for line in lines:
        if line == prev_line:
            if p.match(line) == None:
                prime_candidates.append(line)
        else:
            prev_line = line
    break

# find the prime number among the uniques   
for candidate in prime_candidates:
    # rough cut off
    limit = int(sqrt(float(candidate))) + 1
    candidate = int(candidate)
    is_prime = True
    
    for i in range (2, limit):
        if is_prime:
            if candidate % i == 0:
                is_prime = False
                break
        else:
            break
    
    if is_prime:
        print candidate
        break
