'''
THIS FILE IS CURRENTLY NOT IN USE.

This is a random card selector.
'''

import random

colours = ['R', 'B', 'G', 'Y']

def ask_ai(lower, upper, iswild=False):
    if iswild == True:
        return random.choice(colours)
    else:
        return random.randint(lower, upper)