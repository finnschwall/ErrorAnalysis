from error_analysis import *
from error_analysis import debug
from error_analysis import operators
a = evar([1.0123, 2.1823, 3.19292, 4.9494], [1.930923, 0.13322, 0.7474, 0.37827], 0.28, "a")

b = evar(50, 0.11, 0.12, "b")
c = evar([5, 7, 9, 10], max_error=0.05, name="c")
d = evar(200, 0.41, 1.12, "d")
e = evar(9)

f = evar(100, name="f")

y = operators.cos(a)
y.show(20)



