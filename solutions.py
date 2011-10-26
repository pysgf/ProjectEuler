#!/usr/bin/env python
"""
A collection of Project Euler solutions.

http://projecteuler.net/
"""
import math
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


def p4():
    big_pal = 0
    for m1 in xrange(100, 999):
        for m2 in xrange(100, 999):
            val = m1 * m2
            if val == int((str(val)[::-1])):
                if val > big_pal:
                    big_pal = val
    return big_pal


def p5(n=20):
    return reduce(lcm, xrange(1, 20))

def p7():
    n = 1
    pcount = 0
    pval = 0
    while True:
        n+=1
        isprime = True
        for j in range(2, int(math.sqrt(n))+1):
            if not n % j:
                isprime = False
                break
        if isprime:
            pcount += 1
            pval = n
        if pcount == 10001:
            break
    return str(pval)

if __name__ == '__main__':
    print "Enter a function (like 'p1()') or type 'quit' to stop."
    while True:
        try:
            fxn = raw_input("Enter a function to run: ")
            if fxn == "quit":
                print "Goodbye."
                sys.exit()
            print eval(fxn)
        except (EOFError, KeyboardInterrupt):
            print
            sys.exit()
