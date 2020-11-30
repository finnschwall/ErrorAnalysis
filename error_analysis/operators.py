# TODO implement iadd isub imul itruediv
# TODO add tan sin cos exp log .....
# TODO add custom operator
from error_analysis.evar import *

"""
Contains often used operators.
 
"""

# TODO more common operators like cosh atan etc
# TODO add option for custom operator
def log(x):
    if type(x) is evar:
        RET_VAR = evar(name="INT_OP")
        RET_VAR.value = np.log(x.value)
        RET_VAR.gauss_error = np.abs(x.gauss_error / x.value)
        RET_VAR.max_error = np.abs(x.max_error / x.value)
        RET_VAR._evar__expr = sympy.log(x._evar__expr)
        RET_VAR._evar__dependencies = x._evar__dependencies
        RET_VAR._evar__finish_operation()
        return RET_VAR
    else:
        return np.log(x)


def exp(x):
    if type(x) is evar:
        RET_VAR = evar(name="INT_OP")
        RET_VAR.value = np.exp(x.value)
        RET_VAR.gauss_error = np.exp(x.value)*np.abs(x.gauss_error)
        RET_VAR.max_error = np.exp(x.value)*np.abs(x.max_error)
        RET_VAR._evar__expr = sympy.exp(x._evar__expr)
        RET_VAR._evar__dependencies = x._evar__dependencies
        RET_VAR._evar__finish_operation()
        return RET_VAR
    else:
        return np.exp(x)


def sin(x):
    if type(x) is evar:
        RET_VAR = evar(name="INT_OP")
        RET_VAR.value = np.sin(x.value)
        RET_VAR.gauss_error = np.abs(x.gauss_error*np.cos(x.value))
        RET_VAR.max_error = np.abs(x.max_error*np.cos(x.value))
        RET_VAR._evar__expr = sympy.sin(x._evar__expr)
        RET_VAR._evar__dependencies = x._evar__dependencies
        RET_VAR._evar__finish_operation()
        return RET_VAR
    else:
        return np.sin(x)

def cos(x):
    if type(x) is evar:
        RET_VAR = evar(name="INT_OP")
        RET_VAR.value = np.cos(x.value)
        RET_VAR.gauss_error = np.abs(x.gauss_error * np.sin(x.value))
        RET_VAR.max_error = np.abs(x.max_error * np.sin(x.value))
        RET_VAR._evar__expr = sympy.cos(x._evar__expr)
        RET_VAR._evar__dependencies = x._evar__dependencies
        RET_VAR._evar__finish_operation()
        return RET_VAR
    else:
        return np.cos(x)
