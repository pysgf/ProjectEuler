#!/usr/bin/env python
"""
A collection of Project Euler solutions.

http://projecteuler.net/
"""
import math
import operator
import re
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
        n += 1
        isprime = True
        for j in range(2, int(math.sqrt(n)) + 1):
            if not n % j:
                isprime = False
                break
        if isprime:
            pcount += 1
            pval = n
        if pcount == 10001:
            break
    return pval

def p8():
    prod = 0
    fdex, tdex = 0, 5
    digits = """73167176531330624919225119674426574742355349194934
                96983520312774506326239578318016984801869478851843
                85861560789112949495459501737958331952853208805511
                12540698747158523863050715693290963295227443043557
                66896648950445244523161731856403098711121722383113
                62229893423380308135336276614282806444486645238749
                30358907296290491560440772390713810515859307960866
                70172427121883998797908792274921901699720888093776
                65727333001053367881220235421809751254540594752243
                52584907711670556013604839586446706324415722155397
                53697817977846174064955149290862569321978468622482
                83972241375657056057490261407972968652414535100474
                82166370484403199890008895243450658541227588666881
                16427171479924442928230863465674813919123162824586
                17866458359124566529476545682848912883142607690042
                24219022671055626321111109370544217506941658960408
                07198403850962455444362981230987879927244284909188
                84580156166097919133875499200524063689912560717606
                05886116467109405077541002256983155200055935729725
                71636269561882670428252483600823257530420752963450"""
    digits = re.sub('\s+', '', digits)
    while True:
        dints = [int(d) for d in digits[fdex:tdex]]
        if len(dints) < 5:
            break

        new_prod = reduce(operator.mul, dints)
        if new_prod > prod:
            prod = new_prod

        fdex += 1
        tdex += 1

    return prod


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
