"""

Collection of helper functions for Project Euler solutions.

"""
import math
import operator
import itertools
import copy


def factors(n):
    xs = []
    for j in xrange(2, int(math.sqrt(n)) + 1):
        if not n % j:
            xs.extend([n, j])
            n /= j
    return xs


def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def prime_factors(n):
    
    p_factors = set()
    
    def __split_num_into_factors(num):
        if num > 3:
            for can_fact in xrange(2, int(math.sqrt(num)) + 1):
                if not num % can_fact:
                    return [__split_num_into_factors(can_fact), __split_num_into_factors(num / can_fact)]
    
        return [num]
     
    return list(set().union(flatten(__split_num_into_factors(n))))

def fib(n):
    a, b, = 1, 1
    for i in xrange(3, n + 1):
        a, b = b, a + b
    return b


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def is_prime(n):
    if n == 2:
        return True

    # We want to skip anything that is even.
    if n == 1 or not n % 2:
        return False

    for j in xrange(3, int(math.sqrt(n)) + 1, 2):
        if not n % j:
            return False

    return True


def lcm(a, b):
    return abs(a * b) / gcd(a, b)


def product(xs):
    return reduce(operator.mul, xs)


def pandigital(mynum):
    return all([str(x) in list(str(mynum)) for x in xrange(1, len(str(mynum)) + 1)])
