# PlayerModel.py

"""
A model for batting averages for baseball players

switchpoint: s ~ U(0,111)
early_mean: e ~ Exp(1.)
late_mean: l ~ Exp(1.)
disasters: D[t] ~ Poisson(early if t <= s, l otherwise)
"""

import pymc
import numpy as np
import pandas as pd

# load in data
data = pd.read_table('laa_2011_April.txt')
N = data['AB'] # number of at-bats for each player
num_hits = data['H'] # number of successful hits for each player

# Prior
""" mu (Beta Function as conjugate prior to Binomial distribution liklihood)
    In 2010 the mean batting average was 0.255 and the variance between players was 0.0011.
    Using the values above and solving the two above equations: alpha=43.78, beta=127.92 """
mus = []
for i in np.arange(len(N)):
    mus.append(pymc.Beta('mu'+str(i), alpha=43.78, beta=127.92))

# Model
""" Trivial model in this case """
@pymc.deterministic(plot=False)
def p_model(mus=mus):
    """ Simple model; just return the expected average """
    return mus

# Likelihood
""" A player either hits or misses => Binomial distribution """
xs = []
for i in np.arange(len(N)):
    xs.append(pymc.Binomial('x'+str(i), n=N[i], p=p_model[i],
                                   value=num_hits[i], observed=True))
