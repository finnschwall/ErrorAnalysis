"""
Collection of internal methods that are often used and or not specific to a class

"""


import math
import sympy




def get_max_expr(expr, error_vars):
    max_error = 0
    for i in error_vars:
        max_error += abs(expr.diff(i.symbol) * i.m_symbol)
    return max_error


def get_gauss_expr(expr, error_vars):
    gauss_error = 0
    for i in error_vars:
        gauss_error += (expr.diff(i.symbol) * i.g_symbol) ** 2
    return sympy.sqrt(gauss_error)


def get_length_array(array):
    l = 1
    for i in array:
        if i.length > 1:
            l = i.length
    return l


def eval_e(expr, var):
    symbols = []
    values = []
    for i in var:
        symbols.append(i.symbol)
        values.append(i.value)
    f = sympy.lambdify(symbols, expr)
    return f(*values)


def eval_g(expr, var):
    symbols = []
    values = []
    for i in var:
        symbols.append(i.symbol)
        symbols.append(i.g_symbol)
        values.append(i.value)
        values.append(i.gauss_error)
    f = sympy.lambdify(symbols, expr)
    return f(*values)


def eval_m(expr, var):
    symbols = []
    values = []
    for i in var:
        symbols.append(i.symbol)
        symbols.append(i.m_symbol)
        values.append(i.value)
        values.append(i.max_error)
    f = sympy.lambdify(symbols, expr)
    return f(*values)


# TODO prevent case b=c=0

def transform_to_sig(a, b, c, no_rounding=True):
    a = float(a)
    b = float(b)
    c = float(c)
    aExp = math.floor(math.log10(abs(a)))
    aT = a * 10 ** -aExp
    bT = b * 10 ** -aExp
    cT = c * 10 ** -aExp
    if no_rounding:
        return aT, bT, cT, aExp
    if b != 0:
        bExp = math.floor(math.log10(bT))
    else:
        bExp = 1
    if c != 0:
        cExp = math.floor(math.log10(cT))
    else:
        cExp = 1

    if cExp > 1 or bExp > 1:
        return round(aT), round(bT), round(cT), aExp
    if abs(bExp) > abs(cExp):
        return round(aT, abs(bExp) + 1), round(bT, abs(bExp) + 1), round(cT, abs(bExp) + 1), aExp
    else:
        return round(aT, abs(cExp) + 1), round(bT, abs(cExp) + 1), round(cT, abs(cExp) + 1), aExp


def Variable(a=None, b=None, c=None, d=None):
    """
    This exists solely for backwards compatibility
    """
    return evar(a, b, c, d)
