from error_analysis import *
from  error_analysis.regression import *
from error_analysis import debug
import os

print(os.path.abspath('../error_analysis'))
# TODO add short example for most basic operations

# a = evar([1.0123, 2.1823, 3.19292, 4.9494], [1.930923, 0.13322, 0.7474, 0.37827], 0.28, "a")
# b = evar(50, 0.11, 0.12, "b")
# c = evar([5, 7, 9, 10],[1.930923, 0.13322, 0.7474, 0.37827], 0.05, name="c")
# d = evar(200, 0.41, 1.12, "d")
# e = evar(9)
# f = evar(100, name="f")
#
#
# reg, m, b = lin_reg(a, c)
# plt.errorbar(reg.x , reg.y, yerr=reg.y_err , fmt='none')
# plt.plot(reg.x, reg.y, "x")
# plt.plot(reg.x, reg.y_reg)
# plt.show()

# x = operators.custom_operation("cos(v0)*v1+v2", [a, d, f])
# x.show()
# y.show()
# debug.get_info(y)
# y.show(20)
