from error_analysis import *
from error_analysis import options

# There are several options. All of them and their explanations can be found in options.py
# e.g. this dictates whether any string creating function returns string in latex style or not
options.as_latex = False
# all options are overridden by specified function parameters. So you can e.g. still get the equation of a variable
# by using var.get_expr(as_latex=True)

# one very important option which is also a parameter for many functions is error_mode
# options.error_mode = ErrorMode.COMBINED
# this would cause all output to be reduced to one error which is calculated by sigma= sqrt(gauss^2+max^2)
# options.error_mode = ErrorMode.NONE would ignore errors altogether


####evar declaration####
# The main purpose of this library is to provide a data type which supports error propagation
# this type is called evar
# the constructor params are: evar(value, gauss_error, max_error, name)
# the errors are characterized by their way of propagation (square or maximum)
# lists are supported for every type (except name obviously)
# all non specified types are supposed to be 0. (or list of 0s)
# in the list case every operation is perfomed element wise

# here a few examples for variable declarations
# this creates a = (1.0 \pm 0.0 \pm 0.23)
a = evar(1, 0, 0.23, "a")

# this creates \beta = (5.0 \pm 0.011 \pm 0.0)\cdot 10^{1}
beta = evar(50, 0.11, name=r"\beta")
# which we can easily verify by
print(beta)
# how print works exactly is specified by the options

# variable with systematic error =0 and a non set name. (if you're lucky and the python magic works it's "c" otherwise it's "None")
c = evar(5, max_error=0.05)

# Variables can, as stated above, also be lists
# in this case the gaussian and systematic error are lists of zeros
g = [1, 2, 3, 4, 5]
g = evar(g, name="g")

# it is possible to give single value for one of the errors. in this case the systematic error will be 0.1 for every i in h
h_value = [2, 3, 4, 5, 6]
h_stat_error = [0.3, 0, 2, 0.4, 0.3]
h = evar(h_value, h_stat_error, 0.1, name="i")

# we can retrieve a single variable from a "list" variable
j = h[0]
# this will give us i_{0} = (2.0 \pm 0.3 \pm 0.1)\cdot 10^{0}
print(j)
# list slicing is also supported
h2 = h[1:3]
# this will give us a new variable which has the same values as h between 1 and 3
print(h2)

# we see that the values are printed nicely in scientific format and the relevant digits are
# calculated automatically. If something more specific is desired you can use get_value_str
print(h2.get_value_str(error_mode=ErrorMode.GAUSS, no_rounding=True))  # this will print just the gaussian error and
# not automatic rounding will be perfomed.

### mathematical operations ####

# new variables can be created simply by using standard operators.
# obviously dimensions of variables should be 1 or equal
k = beta ** 2 + c * g / h

# for more advanced stuff use the operators module
# if you do from error_analysis import * it will be included automatically
l = exp(beta + h)
# NEVER EVER do this:
# l = sin(l)
# this will create a circular reference and cause a crash
# you can however do this
# l *= 5
# l += 10  and so on

# if an operator is not included or the result looks really strange and you think you've encountered a bug
# there is another way to calculate a variable. Be warned that this method is about 90-110 times slower
l_alternative = custom_operation("exp(v0+v1)", [beta, h])  # this produces the same result as l.
# all variables in string must be named v0 .. vi or parsing will fail

# if you require the actual equation or the equation for one of the errors you have several options
# there is .get_gauss_error() and k.get_max_error() for the errors which function identically
# for the expression itself there is get_expr()
print(k.get_expr(with_name=False))  # just prints beta**2+c*g/h. The parameter excludes the variable name in front
print(k.get_gauss_error())  # will give the equation for the gauss_error in latex.
print(k.get_max_error(as_latex=False))  # will give the equation for the maximum error in a more readable format.
# normaly the library will check which variables actually have errors and include them accordingly.
# But you can also do it manually
print(k.get_gauss_error([beta, c]))  # this will only give gaussian_error with respect to beta and c

# if you just want a quick look at a variable you can use
k.show()  # which will show you everything about that variable in a new window (latex style)

# we saw many times that k does not have a name yet. we could change that with
# k.set_name("k")
# printing now would include the k at the start
# there is also a functional difference: by setting the name you create a "real" variable
# look at this
l = k + c
print(l.get_expr(with_name=False))
k.set_name("k")
m = k + c
print(m.get_expr(with_name=False))
# the first print statement will give us: beta**2+c*g/h+c
# while the second one gives: k+c.
# it does however not have any influence on the values


# there is also a class for easier regressions (a wrapper for scipy.curve_fit). It supports evars and normal lists
# you can use it e.g. like this
from error_analysis.regression import *

xvar = evar([1.0123, 2.1823, 3.19292, 4.9494], [1.930923, 0.13322, 0.7474, 0.37827], 0.28, "xvar")
yvar = evar([5, 7, 9, 10], [1.930923, 0.13322, 0.7474, 0.37827], 0.05, name="yvar")


def lin_func(x, m, b): # x value argument must always be first
    return m * x + b


reg = Regression(lin_func, xvar, yvar, error_mode=ErrorMode.GAUSS) #creates the regression and only takes gauss error
#into account. default is ErrorMode.COMBINED. If ErrorMode.NONE then no sigma will be applied to regression
plt.errorbar(reg.x, reg.y, yerr=reg.y_err, fmt='none') #with the data provided by the reg class you can easily make a plot
plt.plot(reg.x, reg.y, "x")
plt.plot(reg.x, reg.y_reg)
plt.show()

# the parameters are also available as variables with the error from the regression already applied
m = reg.func_args[0] # the size of func_args (obviously) depends on the amout of arguments of your function
b = reg.func_args[1]
print(m)
print(b)

# for linear regressions a shortcut is available
# reg, m, b = lin_reg(xvar, yvar, error_mode = ErrorMode.GAUSS) this would do the same
