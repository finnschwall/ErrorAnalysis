from error_analysis import *
from error_analysis import options

# There are several options. All of them and their explanation can be found in options.py
# e.g. this dictates wether any string creating function returns string in latex style or not
options.print_as_latex = False

####Variable declaration####
# The whole purpose of this library is to provide a data type which supports error propagation
# this is called variable
# the constructor params are: Variable(value, gauss_error, max_error, name)
# the errors are characterized by their way of propagation (square or maximum)
# lists are supported for every type (except name obviously)
# all non specified are supposed to be 0. (or list of 0s)
# in this case every operation is perfomed element wise

# here few examples for variable declarations
# this creates a = (1.0 \pm 0.0 \pm 0.23)
a = Variable(1, 0, 0.23, "a")

# this creates \beta = (5.0 \pm 0.011 \pm 0.0)\cdot 10^{1}
beta = Variable(50, 0.11, name=r"\beta")
# which we can easily verify by
print(beta)

# variable with systematic error =0 and a non set name. (if you're lucky and the python magic works it's "c" otherwise it's "None")
c = Variable(5, max_error=0.05)

# Variables can, as stated above, also be lists
# in this case the gaussian and systematic error are lists of zeros
g = [1, 2, 3, 4, 5]
g = Variable(g, name="g")

# it is possible to give single value for one of the errors. in this case the systematic error will be 0.1 for every i in h
h_value = [2, 3, 4, 5, 6]
h_stat_error = [0.3, 0, 2, 0.4, 0.3]
h = Variable(h_value, h_stat_error, 0.1, name="i")

# we can retrieve a single variable from a "list" variable
j = h[0]
# this will give us i_{0} = (2.0 \pm 0.3 \pm 0.1)\cdot 10^{0}
print(j)

### mathematical operations ####

# new variables can be created simply by using standard operators.
# obviously dimensions of variables should be 1 or equal
k = beta ** 2 + c * g / h

# we can again get the value but now we will get a whole list, since the operations on k are perfomed per element
# notice that k does not yet have a name
print(k)

# if you require the actual equation or for one of the errors you have several options
# there is .get_gauss_error_str() and k.get_max_error_str() which function identically
print(k.get_gauss_error_str())  # will give the equation for the gauss_error in latex.
print(k.get_max_error_str(
    print_as_latex=False))  # will give the equation for the maximum errir in a more readable format.
# normaly the library will check which variables actually have errors and include them accordingly. but you can also do it manually
print(k.get_gauss_error_str([beta, c]))  # this will only give gaussian_error with respect to beta and c
# you can also just get the expression itself
print(k.get_expr())  # just prints beta**2+c*g/h
# if you prefer a more copy and paste ready version you can use .to_str()
print(k.to_str(print_values=True, print_expr=True))  # which would print the values and the expression with variable
# name included
# additional parameters are  print_gauss_error, print_max_error, print_all
# if you just want a qucik look at a variable you can use
k.show() # which will show you everything about that variable

# we saw many times that k does not have a name yet. we could change that with
# k.set_name("k")
# printing now would include the k at the start
# there is also a functional difference: by setting the name you create a "real" variable
# look at this
l = k + c
print(l.get_expr())
k.set_name(k)
m = k + c
print(m.get_expr())
# the first print statement will give us: beta**2+c*g/h+c
# while the second one gives: k+c.
# the same applies to the errors
