HW2
Sean Lubner
==================

**** Usage ****
At command line:
$ python CalCalc.py -s 'expression to be evaluated here'
#Include the -W flag to force use of Wolfram Alpha for your query

In Python environment:
from CalCalc import calculate
calculate('expression to be evaluated here', use_wolfram=False)
# set use_wolfram = True to force use of Wolfram Alpha for your query

Tests check:
* Ability to evaluate simple expressions
* Ability to defer to Wolfram Alpha for un-parseable queries
* Ability to specify a Wolfram Alpha search
* Ability to return strings
* Ability to return ints

Note:
It is a deliberate design decision to *not* parse out the numerical part of a Wolfram Alpha query such as "mass of moon in kg," in order to preserve access to the more interesting Wolfram Alpha queries, which should return strings.