"""

Collection of helper functions for Project Euler solutions.

"""


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


def lcm(a, b):
    return abs(a * b) / gcd(a, b)
