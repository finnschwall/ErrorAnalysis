"""
Contains often used operators.

Notes
----------
a stands for arc.

    asin=arcsin

"""
# TODO check for values i.e is somebody trying to calculate log(-10) or something
from error_analysis.evar import *
from error_analysis import tools


op_var = sympy.symbols("op_var", real=True)
op_var_e = sympy.symbols("op_var_e", real=True)


# About 80-110 times slower than pre coded numpy expression
def single_operator(expr, x):
    """

    Parameters
    ----------
    expr
        function pointer to sympy operator
    x
        variable to which this should be applied

    Returns
    -------
    error_analysis.evar.evar

    Examples
    ----------
    This is the current implementation of cosh

        if type(x) is evar:
            return single_operator(sympy.acosh, x)
        else:
            return np.arccosh(x)

    Notes
    -------
    Operators can be found at https://docs.sympy.org/latest/modules/functions/index.html .
    While being very slow (about 100-200 times compared to native), this can be helpful if a required operator is not implemented yet.
    Also if you see values that you deem unrealistic, there is a possibility that you've
    encountered a bug. Since this runs completely independent of the normal mechanism of evar you can check the
    results with this.
    """
    RET_VAR = evar(name="INT_OP")
    RET_VAR._evar__dependencies = x._evar__dependencies
    RET_VAR._evar__expr = expr(x._evar__expr)
    evalf = sympy.lambdify(op_var, expr(op_var))
    RET_VAR.value = evalf(x.value)
    error_expr = abs(expr(op_var).diff(op_var) * op_var_e)
    evale = sympy.lambdify([op_var, op_var_e], error_expr)
    RET_VAR.gauss_error = evale(x.value, x.gauss_error)
    RET_VAR.max_error = evale(x.value, x.max_error)
    RET_VAR._evar__finish_operation()
    return RET_VAR


# about (before optim 380) 80-100 times slower than pre coded numpy expression.
def custom_operation(expr, variables):
    """
    Alternative way to calculate entire expression.

    .. warning:: This can be several hundred times slower and crash the program
    Parameters
    ----------
    expr : str
        equation as string. all variables must be named v0... vi
    variables : list
        the vi as list of variables

    Returns
    -------
    error_analysis.evar.evar


    Examples
    ----------
    This

        x = operators.custom_operation("cos(v0)*v1+v2", [a, d, f])
    is equal to::

        x=cos(a)*d+f
    Notes
    ----------
    Values may vary from native evar calculations at high precision.
    """
    RET_VAR = evar(name="INT_OP")
    dependencies = set()
    expr = sympy.sympify(expr)
    for i in range(len(variables)):
        expr = expr.subs("v" + str(i), variables[i].symbol)
        dependencies.add(variables[i]._evar__id)
    RET_VAR._evar__expr = expr
    RET_VAR._evar__dependencies = dependencies
    gauss_expr = tools.get_gauss_expr(expr, variables)
    max_expr = tools.get_max_expr(expr, variables)
    RET_VAR.value = tools.eval_e(expr, variables)
    RET_VAR.max_error = tools.eval_m(max_expr, variables)
    RET_VAR.gauss_error = tools.eval_g(gauss_expr, variables)
    if type(RET_VAR.value) is list:
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


def sqrt(x):
    if type(x) is evar:
        return single_operator(sympy.sqrt, x)
    else:
        return np.sqrt(x)


# TODO make these to real numpy expressions
def sinh(x):
    if type(x) is evar:
        return single_operator(sympy.sinh, x)
    else:
        return np.sinh(x)


def cosh(x):
    if type(x) is evar:
        return single_operator(sympy.cosh, x)
    else:
        return np.cosh(x)


def atan(x):
    if type(x) is evar:
        return single_operator(sympy.atan, x)
    else:
        return np.arctan(x)


def asin(x):
    if type(x) is evar:
        return single_operator(sympy.asin, x)
    else:
        return np.arcsin(x)


def asinh(x):
    if type(x) is evar:
        return single_operator(sympy.asinh, x)
    else:
        return np.arcsinh(x)


def acos(x):
    if type(x) is evar:
        return single_operator(sympy.acos, x)
    else:
        return np.arccos(x)


def acosh(x):
    if type(x) is evar:
        return single_operator(sympy.acosh, x)
    else:
        return np.arccosh(x)
