AY250 Homework 11
Sean Lubner

Notes: 
* The data files being used are modified to remove a "double tab" between the word "Player" and "Team" in the first row of each data file.

* The different problem parts are broken up into separate cells in the main notebook, hw11.ipynb.  These should be run sequentially (and the results of previous runs can still be seen).

---------------- Problem (a) ----------------
The MLE is simply the success rate for a Bernoulli experiment.  Therefore, the number of successful hits, divided by the number of at bats, gives the MLE for each player.  This quantity is conveniently already calculated in the "AVG" (average) column of the data.

---------------- Problem (b) ----------------
A Beta function prior with mean 0.255 and variance 0.0011 takes as hyperparamters, alpha = 43.78, and beta = 127.92.  The model (PlayerModel.py) uses this Beta function as the prior distribution on the batting average, mu.  The liklihood is a binomial distribution, because a batting average is computed from Bernoulli experiments (hit or a miss).  The model is a simple model, because we are just trying to estimate a single number (the batting average) rather than an entire function.

---------------- Problem (c) ----------------
Convergence was confirmed by looking both at the traces of all mus, as well as the z-score plots for each mu.  They do converge.

---------------- Problem (d) ----------------
11 of the 13 players' full-season batting average falls within the 95% confidence interval.  See notebook for full table.
