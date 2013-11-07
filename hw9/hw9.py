
# Homework 9
# ------
# Sean Lubner

# In[9]:

print_outputs = False # mostly used for code development

from time import time
import numpy as np

# IPython multiprocessing:
from IPython.parallel import Client
rc = Client() # start a client
dview = rc.direct_view() # direct view of all engines
dview.block=True # wait until all engines are done executing a command

# Multiprocessing module:
from multiprocessing import Pool
pool = Pool(processes=2)

def throw_darts3(number_of_darts):
    """ throw number_of_darts darts and count how many of them hit the circle """
    from random import random # faster than random.uniform
    num_darts = int(number_of_darts) # number of darts to throw
    hits = 0 # number of darts falling within the circle
    for n in xrange(num_darts): # loop + xrange => don't store in memory
        x, y = random(), random()
        if x*x + y*y <= 1:
            hits += 1
    return hits
    
def serial_pi(n):
    """ Simple Monte Carlo serial estimation of pi, using n darts """
    tic = time() # start time
    hits = throw_darts3(n)
    toc = time() # end time
    pi_est = 4.0*(hits/float(n))
    run_time = toc-tic
    #print "\t\tFinished serial calculation for", num_darts, "darts, in", run_time, "seconds"
    
    if print_outputs:
        print '-------------- Serial Outpt --------------'
        print 'Apprixmate Pi:', pi_est
        print 'Number of darts thrown:', n
        print 'Execution time:', run_time, 'seconds'
        print 'Darts thrown per second:', n/run_time
        print '------------------------------------------\n\n'
        
    return run_time

def IPcluster_pi(n):
    """ Parallel processed Monte Carlo estimation of pi using IPython's cluster, using n darts """
    nnod = len(dview)
    tic = time() # start time
    hits = sum(dview.map_sync(throw_darts3, nnod*[int(n/nnod)]))
    toc = time() # end time
    pi_est = 4.0*(hits/float(n))
    run_time = toc-tic

    if print_outputs:
        print '-------------- IPcluster Outpt --------------'
        print 'Apprixmate Pi:', pi_est
        print 'Number of darts thrown:', n
        print 'Execution time:', run_time, 'seconds'
        print 'Darts thrown per second:', n/run_time   
        print '---------------------------------------------\n\n'
        
    return run_time

def multiprocessing_pi(n):
    """ Parallel processed Monte Carlo estimation of pi using multiprocessing module, using n darts """
    tic = time() # start time
    result = pool.map(throw_darts3, [n])
    hits = result[0]#.get()#[0]
    toc = time() # end time
    pi_est = 4.0*(hits/float(n))
    run_time = toc-tic
    
    if print_outputs:
        print '-------------- Multiprocessing Outpt --------------'
        print 'Apprixmate Pi:', pi_est
        print 'Number of darts thrown:', n
        print 'Execution time:', run_time, 'seconds'
        print 'Darts thrown per second:', n/run_time   
        print '---------------------------------------------------\n\n'
        
    return run_time
    
def darts_grid_search(dart_trials, repeats):
    """ Estimates pi using all 3 methods for each number of darts listed in the 'dart_trials' list.
        Returns a np array with columns: [# darts thrown, serial_times, IPC_times, MP_times] where
        each value is the average of 'repeats' number of repeated trials"""
    trials = []
    print "Now running repeat trial#:"
    for trial in xrange(repeats):
        print str(trial+1)+",",
        serial_times = []
        IPC_times = []
        MP_times = []
        for darts in dart_trials:
            #print "\tNow throwing", darts, "darts for each method"
            serial_times.append(serial_pi(darts))
            IPC_times.append(IPcluster_pi(darts))
            MP_times.append(multiprocessing_pi(darts))
        trials.append(np.array([dart_trials, serial_times, IPC_times, MP_times]).T)
    return sum(trials)/float(len(trials)) # average over the number of repeats


# Out[9]:

#     
# 

# In[*]:

# Plotting
import matplotlib.pyplot as plt
#%matplotlib inline

results = darts_grid_search(np.logspace(1,5,5), 5)

# Plot execution times
f1, ax1 = plt.subplots()
#f1.set_size_inches(11.2,8.56) # size of figure
ax1.plot(results[:,0], results[:,1], c='red', lw=2, label='Simple') 
ax1.plot(results[:,0], results[:,3], c='cyan', lw=2, label='Multiprocessing')
ax1.plot(results[:,0], results[:,2], c='green', lw=2, label='IPcluster')
ax1.set_yscale('log')
ax1.set_xscale('log')

# Plot run times
ax2 = ax1.twinx() # double axis
ax2.plot(results[:,0], results[:,0]/results[:,1], c='red', ls='--', lw=2, label='Simple') 
ax2.plot(results[:,0], results[:,0]/results[:,3], c='cyan', ls='--', lw=2, label='Multiprocessing')
ax2.plot(results[:,0], results[:,0]/results[:,2], c='green', ls='--', lw=2, label='IPcluster')  

t = ax1.set_title('Parallel Processing Parametric Study', size=32, fontweight='bold', fontname='Times New Roman')
ax2.set_ylabel('Simulation Rate [darts/second], dashed line', size=20)
ax1.set_xlabel('# Darts Thrown', size=18) 
ax1.set_ylabel('Execution Time [seconds], solid line', size=18)
t.set_y(1.02) # move title up a little

# Render and format legend
ax1.legend(loc="upper left")
#f1.tight_layout()
plt.show()

#plt.savefig('stocks_matplotlib.png', dpi=150) # Save the figure


# In[10]:

print 'Serial:', serial_pi(10000)
print 'MP:', multiprocessing_pi(10000)
print 'IPC:', IPcluster_pi(10000)


# Out[10]:

#     Serial: 0.00576710700989
#     MP: 0.00967001914978
#     IPC: 0.0159289836884
# 
