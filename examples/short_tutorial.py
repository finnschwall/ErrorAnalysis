from error_analysis import *

# this declares a variable with value=500, gauss_error=10, max_error=10
a = (500, 10, 10, "a")

# declares variable as list. sig_max = 0.05 for every entry now
b = evar([5, 7, 9, 10],[1.930923, 0.13322, 0.7474, 0.37827], 0.05, "c")

#here gauss error is 0 everywhere
c = evar([1.0123, 2.1823, 3.19292, 4.9494], max_error= 0.28, name="a")

# values can be accessed with .value .gauss_error .max_error
print(c.value)

c = a*b+c**a #you can creat new vars with standard operators

d = asin(a) #or with more advanced ones

print(c.get_gauss_error(as_latex=True)) #prints gauss error latex style
print(c.get_value_str(scientific=False)) #prints values of c in non scientif notation

