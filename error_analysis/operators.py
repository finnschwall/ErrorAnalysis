# TODO implement iadd isub imul itruediv
# TODO more common operators like cosh atan etc
# TODO improve custom operator
from error_analysis.evar import *
from error_analysis import tools

"""
Contains often used operators.
 
"""


def custom_operation(expr, vars):
    RET_VAR = evar(name="INT_OP")
    dependencies = set()
    expr = sympy.sympify(expr)
    for i in range(len(vars)):
        expr = expr.subs("v" + str(i), vars[i].symbol)
        dependencies.add(vars[i]._evar__id)
    RET_VAR._evar__expr = expr
    RET_VAR._evar__dependencies = dependencies
    gauss_expr = tools.get_gauss_expr(expr, vars)
    max_expr = tools.get_max_expr(expr, vars)
    RET_VAR.value = tools.eval(expr, vars)
    RET_VAR.max_error = tools.eval(max_expr, vars)
    RET_VAR.gauss_error = tools.eval(gauss_expr, vars)
    if len(RET_VAR.value)>1:
        RET_VAR.value = np.array(RET_VAR.value)
        RET_VAR.gauss_error = np.array(RET_VAR.gauss_error)
        RET_VAR.max_error = np.array(RET_VAR.max_error)
    RET_VAR._evar__finish_operation()
    return RET_VAR


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
        RET_VAR.gauss_error = np.exp(x.value) * np.abs(x.gauss_error)
        RET_VAR.max_error = np.exp(x.value) * np.abs(x.max_error)
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
        RET_VAR.gauss_error = np.abs(x.gauss_error * np.cos(x.value))
        RET_VAR.max_error = np.abs(x.max_error * np.cos(x.value))
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
