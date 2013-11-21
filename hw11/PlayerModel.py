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
i=1 # which player?

# Prior
""" mu (Beta Function as conjugate prior to Binomial distribution liklihood)
    In 2010 the mean batting average was 0.255 and the variance between players was 0.0011.
    Using the values above and solving the two above equations: alpha=43.78, beta=127.92 """
mu = pymc.Beta('mu', alpha=43.78, beta=127.92)

# Model
""" Trivial model in this case """
@pymc.deterministic(plot=False)
def p_model(mu=mu):
    """ Simple model; just return the expected average """
    return mu

# Likelihood
""" A player either hits or misses => Binomial distribution """
xi = pymc.Binomial('xi', n=N[i], p=p_model, value=num_hits[i], observed=True)
