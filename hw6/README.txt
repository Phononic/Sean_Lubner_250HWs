AY250 Homework 6
Sean Lubner

Sad story time...

After spending a few days combatting Murphy's Law in my lab, I started this homework set irresponsibly late.  I consequently managed to spend 4.5 hours (sidenote: how does that even happen? 4.5 hours?? I think coding creates a black hole of time-dilating curved space-time in the immediate vicinity -- must be all the caffeine) just trying to correctly import the data and push it to an SQL table.  I tried various combinations of numpy's loadtxt, pandas' read_csv, different dtypes, sqlite3, sqlalchemy, etc. before finally finding the successful implementation you see before you, in the first cell of hw6.ipynb.

Given that, at this point, it was already silly-late, and it was rather important that I get some sleep that night for presentations and other research stuff the next day, I called it quits and decided to take the hit on my grade.  

For what it's worth, below is an outline of algorithmically how I would finish the problem set, if I could magically conjure time-bubbles in which to continue working:

----- Problem 1 -----
Done.  First cell of notebook.  Well, almost done.  I'd still need to do a loop to re-insert the query results into a new table (see snipets of frustrated rage-code in the bottom cells of the ipython notebook for examples of how I would do this)

----- Problem 2 -----
Done.  First cell of notebook.

----- Problem 3 -----
* I would loop through each airport code (from querying the table), and for each airport code I would loop through every year until now, and within each year I would loop through every month (for 2013, stopping on the present month). "Now" would be defined by a datetime.datetime() call.
* For each nested loop, I would construct a URL and import the data, parse out the values I care about (hooray for nice tab delimited outputs), and save each element to a growing list.  For example, I would have a separate list for max_temps, and for min_temps, and for cloud_cover, etc.
* I would then use "zip" to create a list of tuples, where each tuple contained a min_temp, max_temp, cloud_cover, etc. as well as the city, for a given date.
* I would then sort this list based on the city name in each tuple for convenience, something like .sort(key = lambda x: x[3]) if the city were the 4th item in each tuple.
* This list of tuples would then be in a convenient format to load into my "weather" table by iterating over each tuple in the list (see code cells near bottom of notebook for example).

----- Problem 4 -----
* I would do a query of the form:
SELECT city, date, max_temp from weather
and store the result, probably as a numpy array.  Similarly for cloud_cover
* I would convert the date to a number of days, and create copies of the numpy array but shifted forward by 1, 3, and 7 days.
* I would then caculate the cross correlation of all combos of these numpy arrays (note: the numpy arrays used for the cross correlations have the max_temp or cloud_cover as their actual data.  The date was only used to calculate how much to shift each one to generate the shifted arrays, and the city is just used to create a key afterward to correlate the nth item to a given city)

----- Problem 5 -----
* With these cross correlations calculated, I'd pick the top 10 as instructed, and use my key as mentioned before to find the city corresponding to each cross-correlation.  I'd then use a database query to match each city to its relevant longitude and lattitude, from which an absolute distance can also be calculated (neglecting local curvature of the surface of the Earth).  
* If memory serves me correctly, the weather tends to travel from West to East, on the order of a few days to cross the whole country?  So if that's right, I'd expect to see trends that reflected that model.

P.S. What's the policy for late homework submissions?
