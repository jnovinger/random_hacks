#!/usr/bin/env python

''' Inspired by http://www.blog.republicofmath.com/archives/4727 '''

''' This short little script test all integers below <i>limit</i> for the Munchausen identity.'''

limit = 10000
exp_values = {}

# we only have ten digits, so precompute values
for digit in range(0,10):
    if digit == 0:
        exp_values[str(digit)] = 1
    else:
        exp_values[str(digit)] = digit ** digit

# for our range check for Munchausen numbers
for number in range(1, limit):

    sum = 0
    digits = []

    #explode number into list
    for digit in str(number):
        digits.append(digit)

    # find sum for number
    for digit in digits:
        sum += exp_values[digit]

    # check for Munchausen identity
    if number == sum:
        print "Number: ", number, "Sum:", sum, "Fits:", number == sum
    