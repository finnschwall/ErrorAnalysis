from error_analysis import *

###in progress###
a = Variable(5,0.1,0.2,name="a")
b = Variable(9,name="b")
c = a+b
print(c)
c.to_variable("c")
print(c)

