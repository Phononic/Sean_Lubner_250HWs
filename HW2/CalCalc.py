def calculate(command_string, use_wolfram=False):
    """ Evaluates command_string and prints the result, if it is safe to do so"""
    is_dangerous = ('os.' in command_string) or ('__' in command_string)
    
    if is_dangerous:
        print "OS or Built-In commands are not allowed!"
    else:
        if not use_wolfram:
            try:
                result = eval(str(command_string))
                print result
            except:
                print "Need to add WolframAlpha API here"
        else:
            print 'You wanted to search the interwebz'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='CalCalc Application')
    parser.add_argument('-s', action='store', dest='command_string',
                        help='This is the command string for your query.')
    parser.add_argument('-t', action='store_true', default=False,
                        dest='use_wolfram_online',
                        help='Apply this flag if you wish to search on Wolfram Alpha.')
    results = parser.parse_args()

    calculate(results.command_string, use_wolfram=results.use_wolfram_online)
