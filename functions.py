#!/usr/bin/env python
"""
A collection of Project Euler solutions.

http://projecteuler.net/
"""

def p1(n=1000):
    return sum([d for d in xrange(n) if not (d % 3 and d % 5)])
