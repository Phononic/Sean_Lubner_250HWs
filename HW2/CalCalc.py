#!/usr/bin/python

import argparse
parser = argparse.ArgumentParser(description='CalCalc Application')
parser.add_argument('command_string', help='This is the (required) command string')
#parser.add_argument('required_arg_2', help='This positional argument is also required')
#parser.add_argument('-s', action='store', dest='simple_value',
#                    help='Store a simple value')
#parser.add_argument('-c', action='store_const', dest='constant_value',
#                    const='value-to-store',
#                    help='Store a constant value')
#parser.add_argument('-t', action='store_true', default=False,
#                    dest='boolean_switch',
#                    help='Set a switch to true')
#parser.add_argument('-a', action='append', dest='collection',
#                    default=[],
#                    help='Add repeated values to a list',
#                    )
#parser.add_argument('-A', action='append_const', dest='const_collection',
#                    const='value-1-to-append',
#                    default=[],
#                    help='Add different values to list')
#parser.add_argument('-B', action='append_const', dest='const_collection',
#                    const='value-2-to-append',
#                    help='Add different values to list')
#parser.add_argument('--version', action='version', version='%(prog)s 1.0')

results = parser.parse_args()
#print 'required_args    =', results.required_arg_1, results.required_arg_2
#print 'simple_value     =', results.simple_value
#print 'constant_value   =', results.constant_value
#print 'boolean_switch   =', results.boolean_switch
#print 'collection       =', results.collection
#print 'const_collection =', results.const_collection
is_dangerous = ('os.' in results.command_string) or ('__' in results.command_string)

#if is_dangerous:
#    print "OS or Built-In commands are not allowed!"
#else:
#    print 'Your command was (via program direct):', results.command_string



def calculate(command_string):
    if is_dangerous:
        print "OS or Built-In commands are not allowed!"
    else:
        try:
            result = eval(command_string)
            print result
        except:
            print "Need to add WolframAlpha API here"

if __name__ == '__main__':
    calculate(results.command_string)
