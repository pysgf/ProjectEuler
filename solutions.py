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
    return max([f for f in factors(n) if is_prime(f)])


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
    """We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.
    The product 7254 is unusual, as the identity, 39 x 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.
    Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.
    HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum."""
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
    """The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.
    We shall consider fractions like, 30/50 = 3/5, to be trivial examples.
    There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.
    If the product of these four fractions is given in its lowest common terms, find the value of the denominator."""
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
    """145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.
    Find the sum of all numbers which are equal to the sum of the factorial of their digits.
    Note: as 1! = 1 and 2! = 2 are not sums they are not included.""" 
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
    """The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.
    There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.
    How many circular primes are there below one million?"""
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
    """The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.
    Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.
    (Please note that the palindromic number, in either base, may not include leading zeros.)"""
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
    """The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.
    Find the sum of the only eleven primes that are both truncatable from left to right and right to left.
    NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes."""
    
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
    """Take the number 192 and multiply it by each of 1, 2, and 3:
        192 x 1 = 192
        192 x 2 = 384
        192 x 3 = 576
    By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)
    The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).
    What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?"""
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
    """If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.
    {20,48,52}, {24,45,51}, {30,40,50}
    For which value of p <= 1000, is the number of solutions maximised?"""
        
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
    """An irrational decimal fraction is created by concatenating the positive integers:
    0.123456789101112131415161718192021...
    It can be seen that the 12th digit of the fractional part is 1.
    If dn represents the nth digit of the fractional part, find the value of the following expression.
    d1 x d10 x d100 x d1000 x d10000 x d100000 x d1000000"""
    
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
    """We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.
    What is the largest n-digit pandigital prime that exists?"""
    
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
    """The nth term of the sequence of triangle numbers is given by, tn = (1/2)n(n+1); so the first ten triangle numbers are:
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

    word_reader = csv.reader(open('words.txt', 'rb'), delimiter = ',', quotechar = '"')
    for word_list in word_reader:
        for word in word_list:
            __check_word_for_triangle(word)      
         
    return triangle_word_count[0]

def p43():
    """The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.
    Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:
    d2d3d4=406 is divisible by 2
    d3d4d5=063 is divisible by 3
    d4d5d6=635 is divisible by 5
    d5d6d7=357 is divisible by 7
    d6d7d8=572 is divisible by 11
    d7d8d9=728 is divisible by 13
    d8d9d10=289 is divisible by 17
    Find the sum of all 0 to 9 pandigital numbers with this property."""

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

def p48():
    """Find the last ten digits of the number 1^1 ....1000^1000"""
    return str(sum(x**x for x in xrange(1, 1001)))[-10:]


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
    default_pnum = 357
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
        
    presence_determined, problem_present = IsProjectEulerProblemPresent(guess_pnum)
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
