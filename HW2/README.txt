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