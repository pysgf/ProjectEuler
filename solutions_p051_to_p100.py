#!/usr/bin/env python
"""PySGF solutons to Project Euler Problems 51-100.

http://projecteuler.net/
Solutions presume Python 2.7.

"""

import re
import sys
import time
import urllib
import csv
from contextlib import closing

from data import *
from functions import *


def p51():
    """Project Euler Problem 51 solution.
    
    By replacing the 1st digit of *3, it turns out that six of the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.
    By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first example having seven primes among the ten generated numbers, yielding the family:
        56003, 56113, 56333, 56443, 56663, 56773, and 56993. Consequently 56003, being the first member of this family, is the smallest prime with this property.
    Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is part of an eight prime value family.
    
    """
    prime_set = set([2, 3])
    max_check = [3]


    def __memoized_is_prime(num):
        while max_check[0] < num:
            max_check[0] += 2
            if is_prime(max_check[0]):
                prime_set.add(max_check[0])
        return num in prime_set
   
    
    def __get_replacement_nums(num):
        snum = str(num)
        return [[rval for rval in sorted(set().union([int(snum.replace(dig, new_dig)) for new_dig in '0123456789'])) if rval >= num and __memoized_is_prime(rval)] for dig in str(num)]


    num = 1
    while True:
        num += 2
        if __memoized_is_prime(num):
            for rep_list in __get_replacement_nums(num):
                if len(rep_list) == 8:
                        return rep_list[0]


def p100():
    """Project Euler Problem 100 solution.
    
    If a box contains twenty-one coloured discs, composed of fifteen blue discs and six red discs, and two discs were taken at random, it can be seen that the probability
    of taking two blue discs, P(BB) = (15/21) x (14/20) = 1/2.
    The next such arrangement, for which there is exactly 50% chance of taking two blue discs at random, is a box containing eighty-five blue discs and thirty-five red discs.
    By finding the first arrangement to contain over 10**12 = 1,000,000,000,000 discs in total, determine the number of blue discs that the box would contain.
    
    """
    # 2x(x-1) = y(y-1)
    # By quadratic formula,
    # x = (1+sqrt(1+2(y^2-y)))/2
    #   = (1+z)/2
    # where z^2 = y^2 + (y-1)^2
    # So y, y-1, and z form a twin primitive pythagorean triple which can be generated by Euclid's method:
    # y = max(A,B) where A = p(i)^2 - p(i-1)^2 and B = 2p(i)p(i-1) and C = p(i)^2 + p(i-1)^2
    # where p(i) is the ith  Pell number given by
    # p(0) = 1, p(1), = 2, and p(i) = 2p(i-1)+p(i-2).
    
    pells = [1,2]
    
    def __pell_next():
        pells[1], pells[0] = 2 * pells[1] + pells[0], pells[1]
        
    def __y_and_z_next():
        __pell_next()
        aval = pells[1] ** 2 - pells[0] ** 2
        bval = 2 * pells[1] * pells[0]
        zval = pells[1] ** 2 + pells[0] ** 2
        return max(aval, bval), zval
        
    ymin = 10 ** 12 + 1
    while True:
        yval, zval = __y_and_z_next()
        if yval >= ymin:
            xval = (1 + zval) / 2
            return xval

