"""

Collection of helper functions for Project Euler solutions.

"""
import math
import operator


def factors(n):
    xs = []
    for j in xrange(2, int(math.sqrt(n)) + 1):
        if not n % j:
            xs.extend([n, j])
            n /= j
    return xs


def fib(n):
    memo_dict = {0: 1, 1: 1}

    def __aux(n):
        if n not in memo_dict:
            memo_dict[n] = __aux(n - 1) + __aux(n - 2)
        return memo_dict[n]

    return __aux(n)


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
