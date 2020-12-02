from error_analysis import *
from  error_analysis.regression import *
from error_analysis import debug
import os


a = evar([1.0123, 2.1823, 3.19292, 4.9494], [1.930923, 0.13322, 0.7474, 0.37827], 0.28, "a")
b = evar(50, 0.11, 0.12, "b")
c = evar([5, 7, 9, 10],[1.930923, 0.13322, 0.7474, 0.37827], 0.05, name="c")
d = evar(200, 0.41, 1.12, "d")
e = evar(9)
f = evar(100, name="f")


lin_func = lambda x , m ,b : m*x+b
reg = Regression(lin_func, a, c)
plt.errorbar(reg.x , reg.y, yerr=reg.y_err , fmt='none')
plt.plot(reg.x, reg.y, "x")
plt.plot(reg.x, reg.y_reg)
plt.show()


