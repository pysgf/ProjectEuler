#!/usr/bin/env python
"""
A collection of Project Euler solutions.

http://projecteuler.net/
Solutions presume Python 2.7.

"""
import re
import sys
import time
import datetime
import urllib
from contextlib import closing

from solutions_p001_to_p050 import *
from solutions_p051_to_p100 import *
from solutions_p101_to_p150 import *
from solutions_p151_to_p200 import *
from solutions_p201_to_p250 import *
from solutions_p251_to_p300 import *
from solutions_p301_to_p350 import *
from solutions_p351_to_p400 import *


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
    
    default_pnum = 363
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


def get_estimated_completion(solved_problems, total_problems):
    """Estimates time to completion and completion date."""   
    
    start_date_str = '10/25/2011'  
    month_start, day_start, year_start = (int(x) for x in start_date_str.split('/'))
    start_date = datetime.date(year_start, month_start, day_start)
    now = datetime.datetime.now()
    now_date = datetime.date(now.year, now.month, now.day)
    time_since_start = now_date - start_date  
    
    fraction_solved = float(solved_problems)/total_problems
    days_to_go_mod = math.modf(float(total_problems - solved_problems) * time_since_start.days / solved_problems)
    days_to_go = int(days_to_go_mod[1] + (1 if days_to_go_mod[0] > 0 else 0))
    estimated_completion_date = now_date + datetime.timedelta(days = days_to_go)
    return time_since_start.days, days_to_go, estimated_completion_date


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
         
    average_calc_time = total_calc_time/solved_problems if solved_problems else 0.0
    days_since_start, days_to_finish, finish_date = get_estimated_completion(solved_problems, num_problems)
    print '\nTotal calculation time: {0:>.5f} sec (average: {1:>.5f} sec).'.format(total_calc_time, average_calc_time)
    print 'It turns out that problem {0} took the longest time to calculate ({1:>.5f} sec).'.format(max_calc_problem, max_calc_time)
    if lowest_unsolved_problem > 0:
        print 'The lowest numbered unsolved problem is problem {0}.'.format(lowest_unsolved_problem)
    print '\nHappily, {0} of {1} problems have been solved ({2:>.3} %). {3} problems remain unsolved.'.format(solved_problems, num_problems, 100*float(solved_problems)/num_problems, num_problems-solved_problems)
    print '\nPySGF has been solving Project Euler problems for {0} days and is expected to continue for {1} more days.\nEstimated completion date: {2}.'.format(days_since_start, days_to_finish, finish_date.strftime('%h %d, %Y'))
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
