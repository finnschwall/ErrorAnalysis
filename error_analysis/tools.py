import math

import sympy

from error_analysis import options

"""
Collection of internal methods that are often used and or not specific to a class
"""


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
        if i.length>1:
            l=i.length
    return l


#TODO make this less horrible inefficient. use lambdify or something
def eval(expr, var):
    listLength = 0
    for i in var:
        if i.length > listLength:
            listLength = i.length
    tExpr = [expr for i in range(listLength)]
    for curVar in var:
        if curVar.is_list:
            for i2 in range(listLength):
                tExpr[i2] = tExpr[i2].replace(curVar.symbol, curVar.value[i2])
                tExpr[i2] = tExpr[i2].replace(curVar.g_symbol, curVar.gauss_error[i2])
                tExpr[i2] = tExpr[i2].replace(curVar.m_symbol, curVar.max_error[i2])
        else:
            for i2 in range(listLength):
                tExpr[i2] = tExpr[i2].replace(curVar.symbol, curVar.value)
                tExpr[i2] = tExpr[i2].replace(curVar.g_symbol, curVar.gauss_error)
                tExpr[i2] = tExpr[i2].replace(curVar.m_symbol, curVar.max_error)
    return tExpr




# TODO prevent case b=c=0

def transform_to_sig(a, b, c):
    a = float(a)
    b = float(b)
    c = float(c)
    aExp = math.floor(math.log10(abs(a)))
    aT = a * 10 ** -aExp
    bT = b * 10 ** -aExp
    cT = c * 10 ** -aExp
    if options.no_rounding:
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
