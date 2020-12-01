import scipy.constants as con
from error_analysis.evar import *
"""
Can easily be expanded by using https://docs.scipy.org/doc/scipy/reference/constants.html 
Those are just ones that I used more often while developing
"""
# TODO add more
c = evar(con.c, name="c")
mu_0 = evar(con.mu_0, name=r"\mu_{0}")
epsilon_0 = evar(con.epsilon_0, name=r"\epsilon_{0}")
k_B = evar(con.k, name="k_{B}")
e = evar(con.e, name="e")

