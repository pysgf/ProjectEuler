#!/usr/bin/env python
"""
A collection of Project Euler solutions.

http://projecteuler.net/
"""
import re
import sys
import time
import urllib
import csv
from contextlib import closing

from data import *
from functions import *


def p1(n=1000):
    return sum(d for d in xrange(n) if not (d % 3 and d % 5))


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


def p3(n=600851475143):
    return max([f for f in prime_factors(n) if is_prime(f)])


def p4():
    big_pal = 0
    for m1 in xrange(100,1000):
        for m2 in xrange(m1, 1000):
            val = m1 * m2
            if val == int((str(val)[::-1])):
                if val > big_pal:
                    big_pal = val
    return big_pal


def p5(n=20):
    return reduce(lcm, xrange(1, 20))


def p6():
    return (sum(i for i in xrange(1, 101)) ** 2
            - sum(i ** 2 for i in xrange(1, 101)))


def p7():
    n, prime_count = 3, 2
    while True:
        if is_prime(n):
            if prime_count == 10001:
                return n
            else:
                prime_count += 1
        n += 2


def p8():
    prod, dex = 0, 5
    digits = re.sub('\s+', '', p8_digits)

    while dex < len(digits):
        new_prod = product([int(d) for d in digits[dex - 5:dex]])
        if new_prod > prod:
            prod = new_prod
        dex += 1

    return prod


def p9():
    for n in xrange(999):
        for m in xrange(999):
            a = (m ** 2) - (n ** 2)
            b = 2 * m * n
            c = (m ** 2) + (n ** 2)
            if a + b + c == 1000:
                return a * b * c


def p10(n=2000000):
    return sum([p for p in xrange(0, n) if is_prime(p)])

def p18(triangle=None):
        #triangle = [[3],
        #            [7, 4],
        #            [2, 4, 6],
        #            [8, 5, 9, 3]]
        if not triangle:
            triangle = p18_triangle

        for i in range(len(triangle) - 2, -1, -1):
            for j in range(0, len(triangle[i])):
                triangle[i][j] += max([triangle[i + 1][j], triangle[i + 1][j + 1]])

        return triangle[0][0]

def p67():
    return p18(triangle=p67_triangle)


def p16():
    """Find the sum of the digits in the number 2^1000"""
    return sum(int(x) for x in list(str(2**1000)))


def p20():
    """Find the sum of the digits in 100!"""
    return sum(int(x) for x in list(str(math.factorial(100))))

def p25():
    n = 1
    while True:
        if len(str(fib(n))) >= 1000:
            return n
        n += 1

def p11():
    # Calculate Horizontal product
    xs = []
    for i in xrange(20):
        for j in xrange(20):
            xs.append(product(p11_matrix[i][j:j+4]))
    horiz = max(xs)


    # Calculate Vertical product
    xs = []
    for i in xrange(20):
        for j in xrange(17):
            ys = []
            for k in xrange(4):
                ys.append(p11_matrix[j+k][i])
            xs.append(product(ys))
    vert = max(xs)

    # Calculate First Diagonal product
    xs = []
    for i in xrange(17):
        for j in xrange(17):
            ys = []
            for k in xrange(4):
                ys.append(p11_matrix[j+k][i+k])
            xs.append(product(ys))
    diag1 = max(xs)

    # Calculate Second Diagonal product
    xs = []
    for i in xrange(19, 2, -1):
        for j in xrange(17):
            ys = []
            for k in xrange(4):
                ys.append(p11_matrix[j+k][i-k])
            xs.append(product(ys))
    diag2 = max(xs)

    return max([horiz, vert, diag1, diag2])


def p32():
    """Project Euler Problem 32 solution.
    
    We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.
    The product 7254 is unusual, as the identity, 39 x 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.
    Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.
    HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
    
    """
    pan_found = set([0])
    
    def __check_pandig(product,dig_avail):
        if product < 10 ** 5 and set(str(product)) == dig_avail:
            pan_found.add(product)
            
    def __check_pandigset(dg1,dg2,dg3,dg4,dg5, dig_avail):
        #Only check for 1-digit times 4-digit and 2-digit times 3-digit since commutative property makes others redundant.
        __check_pandig(int(dg1) * int(dg2+dg3+dg4+dg5), dig_avail)
        __check_pandig(int(dg1+dg2) * int(dg3+dg4+dg5), dig_avail)     
              
    digits_avail = set('123456789')        
    for d1 in digits_avail:
        for d2 in  digits_avail - set(d1):             
            for d3 in digits_avail - set(d1 + d2):            
                for d4 in digits_avail - set(d1 + d2 + d3):                 
                    for d5 in digits_avail - set(d1 + d2 + d3 + d4):
                        #Pandigital only possible there are 5 total digits in the multiplicand and multiplier.
                        __check_pandigset(d1,d2,d3,d4,d5,digits_avail - set(d1 + d2 + d3 + d4 + d5))
                        
    return sum(pan_found)
    
    
def p33():
    """Project Euler Problem 33 solution.
    
    The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.
    We shall consider fractions like, 30/50 = 3/5, to be trivial examples.
    There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.
    If the product of these four fractions is given in its lowest common terms, find the value of the denominator.
    
    """
    def __do_unorthodox_cancelation(num,den, pnum, pden):
        snum, sden = str(num), str(den)
        digint = set(snum).intersection(sden)
        if len(digint) == 1:
            sdig=digint.pop()
            snum1, sden1= snum.replace(sdig, ''),sden.replace(sdig, '')
            if len(snum1) == 1 and len(sden1) == 1:
                cnum, cden = int(snum1), int(sden1)
                if num != 10 * cnum and num * cden == den * cnum:
                    return pnum * cnum, pden * cden
                
        return pnum, pden

    pnum, pden = 1, 1
    for numerator in xrange(10, 99):
        for denominator in xrange(numerator + 1, 100):
            pnum, pden = __do_unorthodox_cancelation(numerator, denominator, pnum, pden)
            
    return pden / gcd(pnum, pden)


def p34():
    """Project Euler Problem 34 solution.
    
    145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.
    Find the sum of all numbers which are equal to the sum of the factorial of their digits.
    Note: as 1! = 1 and 2! = 2 are not sums they are not included.
    
    """ 
    fsum = [0]
    fkeys = list('0123456789')
    fvalues = [math.factorial(x) for x in xrange(0, 10)]
    facts = {x:y for x, y in zip(fkeys, fvalues)}

    def __search_for_curious_nums(digs):
        nmax = min(facts['9'] * digs, 10 ** digs - 1)
        for tnum in xrange(10 ** (digs - 1), nmax + 1):
            if sum(facts[s] for s in str(tnum)) == tnum:
                fsum[0] += tnum            
  
    dig_cnt = 2
    # Loop number of digits in number up until even 99....999 gives a sum-of-factorial-digits that is too small
    while 10 ** dig_cnt - 1 <= dig_cnt * facts['9']:
        __search_for_curious_nums(dig_cnt)
        dig_cnt += 1
        
    return fsum[0]


def p35():
    """Project Euler Problem 35 solution.
    
    The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.
    There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.
    How many circular primes are there below one million?
    
    """
    primes = set([2])
    ccount = 0
    
    def __dig_rots(num):
        snum, dig_rots = str(num),[]
        for i in xrange(1, len(snum)):
            snum = snum[1::1] + snum[0]
            dig_rots.append(int(snum))
        return dig_rots
    
    def __is_circular_prime(num):
        for nval in __dig_rots(num):
            if nval not in primes: return False
        return True
    
    for n in xrange(3, 10 ** 6):
        if n % 2 and is_prime(n):
            primes.add(n)
            
    for pnum in primes:
        if __is_circular_prime(pnum): ccount += 1
        
    return ccount


def p36():
    """Project Euler Problem 36 solution.
    
    The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.
    Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.
    (Please note that the palindromic number, in either base, may not include leading zeros.)
    
    """
    pal_sum = 0
    
    def __is_base_2_pal(num):
        snum = '{0:b}'.format(num)
        return snum == snum[::-1]
    
    def __is_base_10_pal(num):
        snum = '{0:d}'.format(num)
        return snum == snum[::-1]
    
    for num in xrange(1, 10 ** 6):
        if __is_base_2_pal(num):
            if __is_base_10_pal(num):
                pal_sum += num
  
    return pal_sum

 
def p37():
    """Project Euler Problem 37 solution.
    
    The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.
    Find the sum of the only eleven primes that are both truncatable from left to right and right to left.
    NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
    
    """
    tcount = 0
    tsum = 0
    
    def __next_longer_r_tprimes(cur_r_tprimes):
        next_tprimes = set()
        for tprime in cur_r_tprimes:
            next_tprimes.update([tprime + s for s in '1379' if is_prime(int(tprime + s))])
        return next_tprimes
        
    def __next_longer_l_tprimes(cur_l_tprimes):
        next_tprimes = set()
        for tprime in cur_l_tprimes:
            next_tprimes.update([s + tprime for s in '123456789' if is_prime(int(s + tprime))])
        return next_tprimes
    
    l_tprimes = set('2357')
    r_tprimes = l_tprimes
    #Starting with the single digit left truncatable primes and right truncatable primes,
    #determine the next longer left and right truncatable primes and then the 'left-right' ones.
    #Keep going until there are no more left- or no more right- truncatable primes to build on.
    while len(l_tprimes) * len(r_tprimes) > 0:
        l_tprimes = __next_longer_l_tprimes(l_tprimes)
        r_tprimes = __next_longer_r_tprimes(r_tprimes)
        lr_tprimes = l_tprimes.intersection(r_tprimes)
        if len(lr_tprimes) > 0:
            tcount += len(lr_tprimes)
            tsum += reduce(lambda x,y: int(x) + int(y),lr_tprimes, '0')
        
    return tsum

def p38():
    """Project Euler Problem 38 solution.
    
    Take the number 192 and multiply it by each of 1, 2, and 3:
        192 x 1 = 192
        192 x 2 = 384
        192 x 3 = 576
    By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)
    The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).
    What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?
    
    """
    pan_max = 0
    all_digs = set('123456789')
    
    def __calc_concat_prod_str_list(num, seq_list):
        prods = [str(num * x) for x in seq_list]
        return ''.join(prods)
        
    def __prod_len_and_is_pandig_set(pstr):
        if len(pstr) == 9:
            return 9, len(all_digs - set(pstr)) == 0
        return len(pstr), False

    #Clearly, when using concat prod with (1,2,.., n) then  n must be 9 or less
    for n in xrange(2,10):
        seq_list = xrange(1,n+1)
        prod_len = 0
        #Start with a large number that will yet result in less than a 9 digit product, so we cover all numbers with low waste.
        mult = max(1, 10 ** (5 - n))
        while prod_len <= 9:
            pstr = __calc_concat_prod_str_list(mult, seq_list)
            prod_len, is_pan_dig = __prod_len_and_is_pandig_set(pstr)
            if is_pan_dig:
                pnum = int(pstr)
                if pnum > pan_max:
                    pan_max = pnum
            mult += 1

    return pan_max


def p39():
    """Project Euler Problem 39 solution.
    
    If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.
    {20,48,52}, {24,45,51}, {30,40,50}
    For which value of p <= 1000, is the number of solutions maximised?
    
    """
    def _get_b_for_perim_p(p, a):
        # Calc b based on solving equation a + b + sqrt(a ** 2 + b ** 2) = p
        # Also return whether number is integral
        num, den = p * (p - 2 * a), 2 * (p - a)
        is_int = not num % den
        return is_int, num / den
    
    max_sols = 0
    max_p = 0
    
    for p in xrange(1, 1001):
        num_sols = 0
        for a in xrange(1, p):
            is_int, b = _get_b_for_perim_p(p, a)
            if is_int:
                num_sols += 1
        
        if num_sols > max_sols:
            max_sols = num_sols
            max_p = p
    
    return max_p


def p40():
    """Project Euler Problem 40 solution.
    
    An irrational decimal fraction is created by concatenating the positive integers:
    0.123456789101112131415161718192021...
    It can be seen that the 12th digit of the fractional part is 1.
    If dn represents the nth digit of the fractional part, find the value of the following expression.
    d1 x d10 x d100 x d1000 x d10000 x d100000 x d1000000
    
    """
    dvals = [0, 0, 0, 0, 0, 0, 0]
    def __appended_num_len(num, cur_len):
        snum = str(num)
        new_len = cur_len + len(snum)
        for dnum in xrange(0, 7):
            if cur_len < 10 ** dnum <= new_len:
                dvals[dnum] = int(snum[10 ** dnum - cur_len - 1])
        return new_len
        
    clen = 0
    for num in xrange(1, 10 ** 6):
        clen = __appended_num_len(num, clen)
        
    return reduce(operator.mul, dvals)
       

def p41():
    """Project Euler Problem 41 solution.
    
    We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.
    What is the largest n-digit pandigital prime that exists?
    
    """
    overall_max_pandig = [0]
    
    def __for_digs(chosen_digs, digits_avail):
        for d1 in digits_avail:
            if len(digits_avail) == 1 and  d1 not in '24568':
                tnum = int(chosen_digs + d1)
                if is_prime(tnum):
                    if tnum >overall_max_pandig[0]:
                        overall_max_pandig[0] = tnum
            else:
                __for_digs(chosen_digs + d1, digits_avail - set(d1))
            
    for n in xrange(9, 0, -1):
        __for_digs('',set(''.join([str(i) for i in xrange(1, n+1)])))
        if overall_max_pandig[0] > 0:
            break;

    return overall_max_pandig[0]


def p42():
    """Project Euler Problem 42 solution.
    
    The nth term of the sequence of triangle numbers is given by, tn = (1/2)n(n+1); so the first ten triangle numbers are:
    1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...
    By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word a triangle word.
    Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?
    
    """
    let_keys = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    let_vals = range(1, 27)
    let_dict = {x:y for x, y in zip(let_keys, let_vals)}
    tnumbers = set([n * (n + 1) / 2 for n in xrange(1, 100)])
    triangle_word_count = [0]
    
    def __check_word_for_triangle(word):
        if sum(let_dict[let] for let in word) in tnumbers:
            triangle_word_count[0] = triangle_word_count[0] + 1

    word_reader = csv.reader(open('p42_words.txt', 'rb'), delimiter = ',', quotechar = '"')
    for word_list in word_reader:
        for word in word_list:
            __check_word_for_triangle(word)      
         
    return triangle_word_count[0]


def p43():
    """Project Euler Problem 43 solution.
    
    The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.
    Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:
    d2d3d4=406 is divisible by 2
    d3d4d5=063 is divisible by 3
    d4d5d6=635 is divisible by 5
    d5d6d7=357 is divisible by 7
    d6d7d8=572 is divisible by 11
    d7d8d9=728 is divisible by 13
    d8d9d10=289 is divisible by 17
    Find the sum of all 0 to 9 pandigital numbers with this property.
    
    """
    pandig_sum = [0]
    
    def __build_pandigs(chosen_digs, digits_avail):
        for d1 in digits_avail:
            snum = chosen_digs + d1
            if snum == '0':
                continue
            if len(snum) == 4 and int(snum[1:4]) % 2:
                continue
            if len(snum) == 5 and int(snum[2:5]) % 3:
                continue
            if len(snum) == 6 and int(snum[3:6]) % 5:
                continue
            if len(snum) == 7 and int(snum[4:7]) % 7:
                continue
            if len(snum) == 8 and int(snum[5:8]) % 11:
                continue
            if len(snum) == 9 and int(snum[6:9]) % 13:
                continue
            if len(snum) >= 10:
                if int(snum[7:10]) %17:
                    continue
                pandig_sum[0] += int(snum)
                continue
            else:
                __build_pandigs(snum, digits_avail - set(d1))
    
    __build_pandigs('',set('0123456789'))
    
    return pandig_sum[0]


def p44():
    """Project Euler Problem 44 solution.
    
    Pentagonal numbers are generated by the formula, Pn=n(3n-1)/2. The first ten pentagonal numbers are:
    1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...
    It can be seen that P4 + P7 = 22 + 70 = 92 = P8. However, their difference, 70 - 22 = 48, is not pentagonal.
    Find the pair of pentagonal numbers, Pj and Pk, for which their sum and difference is pentagonal and D = |Pk - Pj| is minimised; what is the value of D?
    
    """  
    pent_nums = set([1])
    pent_n_max = [1]
    pent_num_max = [1]
    
    def __is_pent_num(num):
        while pent_num_max[0] < num:
            pent_n_max[0] += 1
            pent_num_max[0] = pent_n_max[0] * (3 * pent_n_max[0] - 1) / 2
            pent_nums.add(pent_num_max[0]);
        return num in pent_nums
     
    # P<n+d> = P<n> + d * (6*n + 3*d - 1) / 2
    # Thus n = (2 * (P<n+d> - P<n>) - 3 * d ** 2 + d) / (6 * d)
    # So loop pentagonal differences, then loop d values looking for all positive integral n values. Then test to see if P<n> + P<n+d> is pentagonal.
    pdiffn = 1
    pent_set_found = False
    while not pent_set_found:
        pdiff = pdiffn * (3 * pdiffn - 1) / 2
        d_guess = 1
        n_num = (2 * pdiff - 3 * d_guess ** 2 + d_guess)
        while n_num > 0:
            if not n_num % (6 * d_guess):
                n_guess = n_num / (6 * d_guess)
                psum = pdiff + n_guess * (3 * n_guess - 1)
                if __is_pent_num(psum):
                    pent_set_found = True
                    break
            d_guess += 1
            n_num = (2 * pdiff - 3 * d_guess ** 2 + d_guess)
        pdiffn += 1
    
    return pdiff


def p45():
    """Project Euler Problem 45 solution.
    
    Triangle, pentagonal, and hexagonal numbers are generated by the following formulae:
    Triangle 	  	Tn=n(n+1)/2 	  	1, 3, 6, 10, 15, ...
    Pentagonal 	  	Pn=n(3n-1)/2 	  	1, 5, 12, 22, 35, ...
    Hexagonal 	  	Hn=n(2n-1) 	  	1, 6, 15, 28, 45, ...
    It can be verified that T285 = P165 = H143 = 40755.
    Find the next triangle number that is also pentagonal and hexagonal.
    
    """
    pent_nums = set([1])
    pent_n_max = [1]
    pent_num_max = [1]
    hex_nums = set([1])
    hex_n_max = [1]
    hex_num_max = [1]
    
    def __is_pent_num(num):
        while pent_num_max[0] < num:
            pent_n_max[0] += 1
            pent_num_max[0] = pent_n_max[0] * (3 * pent_n_max[0] - 1) / 2
            pent_nums.add(pent_num_max[0]);
        return num in pent_nums
    
    def __is_hex_num(num):
        while hex_num_max[0] < num:
            hex_n_max[0] += 1
            hex_num_max[0] = hex_n_max[0] * (2 * hex_n_max[0] - 1)
            hex_nums.add(hex_num_max[0]);
        return num in hex_nums

    t_index = 286
    while True:
        tnum = t_index * (t_index + 1) / 2
        if __is_hex_num(tnum) and __is_pent_num(tnum):
            return tnum
        t_index += 1


def p46():
    """Project Euler Problem 46 solution.
    
    It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.
    9 = 7 + 2*1**2
    15 = 7 + 2*2**2
    21 = 3 + 2*3**2
    25 = 7 + 2*3**2
    27 = 19 + 2*2**2
    33 = 31 + 2*1**2
    It turns out that the conjecture was false.
    What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
    
    """

    def __is_prime_plus_2square(num):
        root_num = 1
        while True:
            t_square_dif = num - 2 * root_num ** 2
            if (t_square_dif < 2):
                return False
            if is_prime(t_square_dif):
                return True
            root_num += 1

    odd_num = 3
    while True:
        if not is_prime(odd_num):
            if not __is_prime_plus_2square(odd_num):
                return odd_num
        odd_num += 2
        
def p47():
    """Project Euler Problem 47 solution.
    
    The first two consecutive numbers to have two distinct prime factors are:
    14 = 2 x 7
    15 = 3 x 5
    The first three consecutive numbers to have three distinct prime factors are:
    644 = 2 x 7 x 23
    645 = 3 x 5 x 43
    646 = 2 x 17 x 19.
    Find the first four consecutive integers to have four distinct primes factors. What is the first of these numbers?
    
    """
    first_num = 2
    while True:
        factors = prime_factors(first_num)
        if len(factors) == 4:
            factors = prime_factors(first_num + 1)
            if len(factors) == 4:
                factors = prime_factors(first_num + 2)
                if len(factors) == 4:
                    factors= prime_factors(first_num + 3)
                    if len(factors) == 4:
                        return first_num
                    else:
                        first_num += 4
                else:
                    first_num += 3
            else:
                first_num += 2
        else:
            first_num += 1


def p48():
    """Project Euler Problem 48 solution.
    
    Find the last ten digits of the number 1^1 ....1000^1000
    
    """
    return str(sum(x**x for x in xrange(1, 1001)))[-10:]
   
    
def p49():
    """Project Euler Problem 49 solution.
    
    The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.
    There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.
    What 12-digit number do you form by concatenating the three terms in this sequence?
    
    """     
    def __is_list_equal_diff(num_list):
        diffs = [num_list[vindex + 1] - num_list[vindex] for vindex in range(len(num_list) - 1)]
        return all(dval == diffs[0] for dval in diffs)   

    def __get_other_special_sequence(num):
        unique_num_perms = set().union(list(int(''.join(x)) for x in itertools.permutations(str(num),len(str(num)))))
        sorted_bigger_prime_unique_num_perms = sorted(vp for vp in unique_num_perms if vp >= num and is_prime(vp))
        if (len(sorted_bigger_prime_unique_num_perms) >= 3):
            combos = list(itertools.combinations(sorted_bigger_prime_unique_num_perms, 3))
            valid_combos = [com for com in combos if __is_list_equal_diff(com)]
            if (len(valid_combos) > 0 and valid_combos[0][0] != 1487):
                return valid_combos[0]
        return None
    
    for num in xrange(1000, 10000):
        seq = __get_other_special_sequence(num)
        if seq != None:
            return str(reduce(lambda x,y: int(str(x) + str(y)), seq))


def p50():
    """Project Euler Problem 50 solution.
    
    The prime 41, can be written as the sum of six consecutive primes:
    41 = 2 + 3 + 5 + 7 + 11 + 13
    This is the longest sum of consecutive primes that adds to a prime below one-hundred.
    The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.
    Which prime, below one-million, can be written as the sum of the most consecutive primes?
    
    """
    prime_set = set([2])
    prime_list = None
    max_consec = [1]
    max_start_index = [1]
    max_prime_sum = [2]
    
    def __record_if_prime(num):
        if is_prime(num):
            prime_set.add(num)
            
            
    def __find_prime_sum(start_index):
        consec_len = 1
        cur_sum = prime_list[start_index]
        while cur_sum < 10 ** 6 and start_index + consec_len < len(prime_list):
            consec_len += 1
            cur_sum += prime_list[start_index + consec_len - 1]
            if cur_sum in prime_set and consec_len > max_consec[0]:
                max_start_index[0] = start_index
                max_consec[0] = consec_len
                max_prime_sum[0] = cur_sum

    
    for num in xrange(3, 10 ** 6, 2):
        __record_if_prime(num)     
    prime_list = sorted(list(prime_set))
    for pindex in range(len(prime_list)):
        __find_prime_sum(pindex)
    return max_prime_sum[0]


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


def p101():
    """Project Euler Problem 101 solution.
    
    If we are presented with the first k terms of a sequence it is impossible to say with certainty the value of the next term,
    as there are infinitely many polynomial functions that can model the sequence.

    As an example, let us consider the sequence of cube numbers. This is defined by the generating function,
    u(n) = n^3: 1, 8, 27, 64, 125, 216, ...

    Suppose we were only given the first two terms of this sequence.
    Working on the principle that "simple is best" we should assume a linear relationship and predict the next term to be 15
    (common difference 7). Even if we were presented with the first three terms, by the same principle of simplicity,
    a quadratic relationship should be assumed.

    We shall define OP(k, n) to be the nth term of the optimum polynomial generating function for the first k terms of a sequence.
    It should be clear that OP(k, n) will accurately generate the terms of the sequence for n <= k,
    and potentially the first incorrect term (FIT) will be OP(k, k+1); in which case we shall call it a bad OP (BOP).

    As a basis, if we were only given the first term of sequence, it would be most sensible to assume constancy; that is, for n >= 2, OP(1, n) = u1.

    Hence we obtain the following OPs for the cubic sequence:
    OP(1, n) = 1 	    1, 1, 1, 1, ...
    OP(2, n) = 7n-6 	    1, 8, 15, ...
    OP(3, n) = 6n^2-11n+6   1, 8, 27, 58, ...
    OP(4, n) = n3 	    1, 8, 27, 64, 125, ...

    Clearly no BOPs exist for k >= 4.
    By considering the sum of FITs generated by the BOPs, we obtain 1 + 15 + 58 = 74.
    Consider the following tenth degree polynomial generating function:
    un = 1 - n + n^2 - n^3 + n^4 - n^5 + n^6 - n^7 + n^8 - n^9 + n^10
    Find the sum of FITs for the BOPs.
    
    """
    
    def __poly_eval(poly_coefs, xval):
        return sum(coef * xval ** index for (index, coef) in enumerate(poly_coefs))
        
    def __row_reduce(ini_op_vals, ini_sfun_vals, coef_index):
        op_vals = ini_op_vals
        sfun_vals = ini_sfun_vals
        row_index = 0
        for i in xrange(len(op_vals)):
            if i != coef_index:
                row_factor = op_vals[coef_index][coef_index]
                coef_factor = op_vals[i][coef_index]
                op_vals[i] = [x * row_factor - op_vals[coef_index][col_index] * coef_factor  for (col_index, x) in  enumerate(op_vals[i])]
                sfun_vals[i] =  sfun_vals[i] * row_factor - sfun_vals[coef_index] *  coef_factor
                del op_vals[i][coef_index]
                row_index += 1
        del op_vals[coef_index]
        del sfun_vals[coef_index]
        return op_vals, sfun_vals
    
    def _get_coef(op_vals, sfun_vals, coef_num):
        op_vals_red, sfun_vals_red = copy.deepcopy(op_vals), copy.deepcopy(sfun_vals)
        coef_index = coef_num
        while len(op_vals_red) > 1:
            if coef_index != 0:
                coef_to_eliminate = 0
                coef_index -= 1
            else:
                coef_to_eliminate = 1
            op_vals_red, sfun_vals_red = __row_reduce(op_vals_red, sfun_vals_red, coef_to_eliminate)
        coef_val = sfun_vals_red[0] / op_vals_red[0][0]
        return coef_val

    def __get_optimum_polynomial_coefficients(sfun_coefs, nval):
        op_vals = [[x ** n for n in xrange(nval)] for x in xrange(1, nval + 1)]
        sfun_vals = [__poly_eval(sfun_coefs, x) for x in  xrange(1, nval + 1)]
        op_coefs = [_get_coef(op_vals,  sfun_vals, n) for n in xrange(nval)]
        return op_coefs
    
    def __get_fip_value(sfun_coefs, nval):
        op_coefs = __get_optimum_polynomial_coefficients(sfun_coefs, nval)
        fip_val = __poly_eval(op_coefs, len(op_coefs) + 1)
        return fip_val

    sfun_coefs = [(-1) ** n for n in xrange(11)]
    fip_sum = sum(__get_fip_value(sfun_coefs, n) for n in xrange(1, len(sfun_coefs)))
    return fip_sum


def get_answer_and_time(pnum):
    """Call a problem function and time its execution."""
    
    solved = True
    start_time = time.time()   
    try:
        ans =eval('p%i()' % pnum)
    except StandardError:
        solved = False
        ans = 0
        ctime = 0.0
        
    ctime = time.time() - start_time
    return solved, ans, ctime


def is_project_euler_problem_present(pnum):
    """Determine whether the given Project Euler problem number exists."""
    
    problem_present = True
    presence_determined = False
    try:
        with closing(urllib.urlopen('http://projecteuler.net/problem={0}'.format(pnum))) as page: 
            for lines in page.readlines():
                # If a problem is not present project euler reverts to problems page
                # which contains text 'Go to Problem'
                if re.search('go to problem', lines, re.IGNORECASE):
                    problem_present = False
                    presence_determined = True
                    break
                else:
                    #problem pages have the problem name in their title
                    if re.search('<title>Problem ' + str(pnum), lines, re.IGNORECASE):
                        problem_present = True
                        presence_determined = True
                        break;
    
    except StandardError:
       presence_determined = False
       
    if not presence_determined:
        print '        ** Presence not determined for problem {0}'.format(pnum)

    return presence_determined, problem_present


def get_number_of_project_euler_problems(use_default_problem_count):
    """Determine the current number of Project Euler problems."""
    
    default_pnum = 360
    if use_default_problem_count:
        return default_pnum
    presumed_present_pnum = default_pnum
    guess_inc = 1
    max_guess_inc = 2 ** 14
    
    #Note: This approach presumes that the number of problems never decreases.
    #If it does decrease then the function will return the wrong value (the default value)
    #until the number of problems increases to the former number which would hopefully be the case.
    #Taking a decreasing number into account would double the expense of the most common case from 1 page requests to 2 page requests.
    #Do an increasing binary search for a problem that is not present
    while guess_inc <= max_guess_inc:
        guess_pnum = presumed_present_pnum + guess_inc
        presence_determined, problem_present = is_project_euler_problem_present(guess_pnum)
        if not presence_determined:
            return default_pnum       
        if not problem_present:
            break
        guess_inc *= 2
        
    if guess_inc > max_guess_inc:
        #we have gone very high and still haven't found the end so give up and use default (something is wrong)
        return default_pnum
    if guess_inc == 1:
        #first try was a miss so return what was presumed to exist
        return presumed_present_pnum
    missing_pnum = guess_pnum
    #retreat half way back to last existing problem
    guess_pnum -= guess_inc / 2
    #only need to use 1/4 inc to reach lowest nonexisting problem
    guess_inc /= 4
    
    #Do binary search for lowest problem that doesn't exist
    while guess_inc >= 1:
        presence_determined, problem_present = is_project_euler_problem_present(guess_pnum)
        if not presence_determined:
            return default_pnum
        if problem_present:
            guess_pnum += guess_inc
        else:
            missing_pnum = guess_pnum
            guess_pnum -= guess_inc
        guess_inc /= 2
        
    presence_determined, problem_present = is_project_euler_problem_present(guess_pnum)
    if not presence_determined:
        return default_pnum   
    if not problem_present:
        missing_pnum = guess_pnum
    guess_pnum = missing_pnum - 1
    if guess_pnum > default_pnum:
        print '        ** Problem count ({0}) greater than default problem count ({1}).'.format(guess_pnum, default_pnum)
        
    return guess_pnum


def pall(determine_problem_count = True):
    """Calculates solutions to all problems and prints stataistics."""
    
    print '-----------------------------------------------------------------\n' \
        'Calculation of the pySGF solutions to the Project Euler problems:\n'
    if determine_problem_count:
        #This should take less than 2 seconds or less on a broadband connection.
        print '\n    Determining problem count...'
        start_time = time.time()
        num_problems = get_number_of_project_euler_problems(False)
        print '    ...determination took {0:.2f} seconds.\n'.format(time.time() - start_time)
    else:
        num_problems = get_number_of_project_euler_problems(True)
        
    solved_problems = 0
    total_calc_time = 0.0
    max_calc_time = 0.0
    max_calc_problem = 0
    lowest_unsolved_problem = 0
    in_unsolved_block = False
    
    for pnum in xrange(1, num_problems + 1):
        solved, ans, ctime = get_answer_and_time(pnum)
        if solved:
            solved_problems += 1
            total_calc_time += ctime
            if ctime > max_calc_time:
                max_calc_time = ctime
                max_calc_problem = pnum     
            if in_unsolved_block:
                 print '*** unsolved problem(s) ****'
            in_unsolved_block = False
            print 'Problem {0:>4g}  Answer: {1:>20}        (calc time: {2:>7.5f} sec)'.format(pnum, str(ans), ctime)
        else:
            in_unsolved_block = True
            if lowest_unsolved_problem == 0:
                lowest_unsolved_problem = pnum
                
    if in_unsolved_block:
         print '*** unsolved problem(s) ****'
    print '\nTotal calculation time: {0:>.5f} sec (average: {1:>.5f} sec).'.format(total_calc_time, total_calc_time/solved_problems)
    print 'It turns out that problem {0} took the longest time to calculate ({1:>.5f} sec).'.format(max_calc_problem, max_calc_time)
    if lowest_unsolved_problem > 0:
        print 'The lowest numbered unsolved problem is problem {0}.'.format(lowest_unsolved_problem)
    print '\nHappily, {0} of {1} problems have been solved ({2:>.3} %). {3} problems remain unsolved.'.format(solved_problems, num_problems, 100*float(solved_problems)/num_problems, num_problems-solved_problems)
    print '\n-----------------------------------------------------------------'

    return ''


def pallc():
    """Calculates solutions to all problems, determining the number of Project Euler problems beforehand."""
    return pall(True)
    
def palld():
    """Calculates solutions to all problems, using the default number of Project Euler problems beforehand."""
    return pall(False)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if '(' in sys.argv[1]:
            print eval(sys.argv[1])
        else:
            print eval('p{0}()'.format(sys.argv[1]))
    else:
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
