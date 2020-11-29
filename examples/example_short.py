from error_analysis import *
from error_analysis import debug
a = Variable([1.0123, 2.1823, 3.19292, 4.9494], [1.930923, 0.13322, 0.7474, 0.37827], 0.28, "a")

b = Variable(50, 0.11, 0.12, "b")
c = Variable([5, 7, 9, 10], max_error=0.05, name="c")
d = Variable(200, 0.41, 1.12, "d")
e = Variable(9, 0, 0.12)

f = Variable(100, name="f")

x = 5**a
debug.get_info(x)
x.show(20)
