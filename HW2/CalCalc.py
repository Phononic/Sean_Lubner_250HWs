def calculate(command_string, use_wolfram=False):
    """ Evaluates command_string and prints the result, if it is safe to do so"""
    
    def wolf_search(wolf_string):
        import urllib2
        query_address = 'http://api.wolframalpha.com/v2/query?input=' + \
        urllib2.quote(wolf_string).replace('/','%2F') + \
        '&appid=UAGAWR-3X6Y8W777Q'
        print 'talking to Wolfram Alpha...\n\t'
        search_data = urllib2.urlopen(query_address).read()
        search_start = search_data.find("<pod title='Input")
        search_start += search_data[search_start+1:].find("<pod title=") # next pod is the result
        result_start = search_data[search_start:].find("<plaintext>")+search_start+11
        result_end = search_data[search_start:].find("</plaintext>")+search_start
        print 'From Wolfram Alpha:', search_data[result_start:result_end]
        
            
    is_dangerous = ('os.' in command_string) or ('__' in command_string)
    
    if is_dangerous:
        print "OS or Built-In commands are not allowed!"
    else:
        if not use_wolfram:
            try:
                result = eval(str(command_string))
                print result
            except:
                wolf_search(str(command_string))
                
        else: # use the interwebz
            wolf_search(str(command_string))
            
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
