#!/usr/bin/env python
"""
A collection of Project Euler solutions.

http://projecteuler.net/
"""
import operator
import re
import sys
import time
import urllib
from contextlib import closing
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

    while dex < len(digits):
        new_prod = reduce(operator.mul, [int(d) for d in digits[dex - 5:dex]])
        if new_prod > prod:
            prod = new_prod
        dex += 1

    return prod

def p32():
    """We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.
    The product 7254 is unusual, as the identity, 39 x 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.
    Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.
    HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum. 
    """
    pan_found = set([0])
    digits_avail_1 = set(['1','2','3','4','5','6','7','8','9'])  
    for d1 in digits_avail_1:
        digits_avail_2 = digits_avail_1 - set([d1])
        for d2 in digits_avail_2:
            digits_avail_3 = digits_avail_2 - set([d2])               
            for d3 in digits_avail_3:
                digits_avail_4 = digits_avail_3 - set([d3])               
                for d4 in digits_avail_4:
                    digits_avail_5 = digits_avail_4 - set([d4])                   
                    for d5 in digits_avail_5:
                        digits_avail_6 = digits_avail_5 - set([d5])
                        #Pandigital only possible there are 5 total digits
                        #   in the multiplicands.
                        #Only check for 1 digit X 4 digit and 2 digit * 3 digit
                        #   since commutative property makes others redundant.
                        m1, m2 = int(d1),int(d2+d3+d4+d5)
                        product = m1 * m2
                        if product < 10000 and set(str(product)) == digits_avail_6:
                            pan_found = pan_found.union(set([product]))
                        m1, m2 = int(d1+d2) , int(d3+d4+d5)
                        product = m1 * m2
                        if product < 10000 and set(str(product)) == digits_avail_6:
                            pan_found = pan_found.union(set([product]))
    return sum(pan_found)
                                        

def GetAnswerAndTime(pnum):
    solved = True
    start_time = time.time()
    try:
        ans =eval('p%i()' % pnum)
    except:
        solved = False
        ans = 0
        ctime = 0.0
    ctime = time.time() - start_time
    return solved, ans, ctime

def IsProjectEulerProblemPresent(pnum):
    problem_present = True
    with closing(urllib.urlopen('http://projecteuler.net/problem={0}'.format(pnum))) as page: 
        try:
            for lines in page.readlines():
                # If a problem is not present project euler reverts to problems page
                # which contains text 'Go to Problem'
                if re.search('go to problem', lines, re.IGNORECASE):
                    problem_present = False
                    break
                else:
                    #problem pages have the text confirmation code
                    if re.search('confirmation_code:', lines, re.IGNORECASE):
                        break;
        except:
            problem_present = False
    return problem_present
 
def GetNumberOfProjectEulerProblems():
    guess_pnum = 2**14
    guess_inc = 2**13
    present_pnum = 0
    #Do simple binary search for problems
    while guess_inc >= 1:
        if IsProjectEulerProblemPresent(guess_pnum):
            present_pnum = guess_pnum
            guess_pnum += guess_inc
        else:
            guess_pnum -= guess_inc
        guess_inc /= 2
    if IsProjectEulerProblemPresent(guess_pnum):
        present_pnum = guess_pnum
    return present_pnum

def pall(determine_problem_count=False):
    """Calculates solutions to all problems and prints stataistics.
    """
    print '-----------------------------------------------------------------\n' \
        'Calculation of the pySGF solutions to the Project Euler problems:\n'
    if determine_problem_count:
        #This should take around 20 seconds or less on a broadband connection.
        print '\n    Determining problem count...'
        start_time = time.time()
        num_problems = GetNumberOfProjectEulerProblems()
        print '    ...determination took {0:.2f} seconds.\n'.format(time.time() - start_time)
    else:
        num_problems = 356
        
    solved_problems = 0
    total_calc_time = 0.0
    max_calc_time = 0.0
    max_calc_problem = 0
    lowest_unsolved_problem = 0
    in_unsolved_block = False
    for pnum in xrange(1,num_problems + 1):
        solved, ans, ctime = GetAnswerAndTime(pnum)
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
    print '\nTotal calculation time: {0:>.5f} sec (average: {1:>.5f} sec).'.format(total_calc_time, total_calc_time/solved_problems)
    print 'It turns out that problem {0} took the longest time to calculate ({1:>.5f} sec).'.format(max_calc_problem, max_calc_time)
    if lowest_unsolved_problem > 0:
        print 'The lowest numbered unsolved problem is problem {0}.'.format(lowest_unsolved_problem)
    print '\nHappily, {0} of {1} problems have been solved ({2:>.3} %). {3} problems remain unsolved.'.format(solved_problems, num_problems, 100*float(solved_problems)/num_problems, num_problems-solved_problems)
    print '\n-----------------------------------------------------------------'
    return ''

def pallc(): return pall(True)

if __name__ == '__main__':
    if len(sys.argv) > 1:
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
