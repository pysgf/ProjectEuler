#!/usr/bin/env python
"""
A collection of Project Euler solutions.

http://projecteuler.net/
"""
import sys
from functions import *

def p1(n=1000):
    return sum([d for d in xrange(n) if not (d % 3 and d % 5)])

def p2(n=4000000):
    i, total = 1, 0
    while True:
        ifib = fib(i)
        if ifib < n:
            total += ifib * (not ifib % 2)
        else:
            break
        i += 1
    return total

if __name__ == '__main__':
    print "Enter a function or type 'quit' to stop."
    while True:
        try:
            fxn = raw_input("Enter a function to run: ")
            if fxn == "quit":
                print "Goodbye."
                sys.exit()
            print eval('%s()' % fxn)
        except (EOFError, KeyboardInterrupt):
            print
            sys.exit()
