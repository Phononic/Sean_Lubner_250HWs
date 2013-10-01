# Command line calculator -- by Sean Lubner

#==============================================================================
# Main Functions
#==============================================================================

def calculate(command_string, use_wolfram=False):
    """ Evaluates command_string and prints the result, if it is safe to do so"""
    
    def wolf_search(wolf_string):
        import urllib2
        query_address = 'http://api.wolframalpha.com/v2/query?input=' + \
        urllib2.quote(wolf_string).replace('/','%2F') + \
        '&appid=RLER5L-8TJ6Q3T6KJ'
        print '\tTalking to Wolfram Alpha, please wait...\n'
        search_data = urllib2.urlopen(query_address).read()
        if "<queryresult success='true'" in search_data: # search was successful
            search_start = search_data.find("<pod title='Input")
            search_start += search_data[search_start+1:].find("<pod title=") # next pod is the result
            result_start = search_data[search_start:].find("<plaintext>")+search_start+11
            result_end = search_data[search_start:].find("</plaintext>")+search_start
            print 'From Wolfram Alpha:', search_data[result_start:result_end]
            return search_data[result_start:result_end]
        else:
            print "Wolfram Alpha did not understand your question."
        
            
    is_dangerous = ('os.' in command_string) or ('__' in command_string)
    
    if is_dangerous:
        print "OS or Built-In commands are not allowed!"
    else:
        if not use_wolfram:
            try:
                result = eval(str(command_string))
                print result
                return result
            except:
                print "I don't know the answer to this question, so let's ask Wolfram Alpha."
                return wolf_search(str(command_string))
                
        else: # use the interwebz
            return wolf_search(str(command_string))

#==============================================================================
# Tests
#==============================================================================
def test_1():
    assert abs(64.0 - calculate('8**2')) < .001

def test_2():
    assert abs(10 - int(calculate('five plus five', use_wolfram=True))) < .001

def test_3():
    assert abs(15 - int(calculate('five plus ten'))) < .001
    
def test_4():
    answer = 'A woodchuck would chuck all the wood he could chuck if a woodchuck could chuck wood.'
    check = calculate('How much wood would a woodchuck chuck, if a woodchuck could chuck wood?', use_wolfram=True).split('\n')[0]
    assert answer.lower().strip() == check.lower().strip()

def test_5():
    assert calculate('min([5,4,3,4,5])') == 3

#==============================================================================
# Command Line Parsing
#==============================================================================
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='CalCalc Application')
    parser.add_argument('-s', action='store', dest='command_string',
                        help='This is the command string for your query.')
    parser.add_argument('-W', action='store_true', default=False,
                        dest='use_wolfram_online',
                        help='Apply this flag if you wish to search on Wolfram Alpha.')
    results = parser.parse_args()

    calculate(results.command_string, use_wolfram=results.use_wolfram_online)
