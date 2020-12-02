"""
Tools for curve fitting
"""
from scipy.optimize import curve_fit
from error_analysis.evar import *


# TODO add whatever regression
# TODO add specific linear regression

def __lin_func(x, m, b):
    return m * x + b

# TODO add support for error on x axis
class Regression:
    """
    evar wrapper for scipy.curve_fit. Also works on normals lists.

    Notes
    ----------
    error on x axis is not supported yet

    Examples
    ----------

        lin_func = lambda x , m ,b : m*x+b
        reg = Regression(lin_func, xvar, yvar)
        plt.errorbar(reg.x, reg.y, yerr=reg.y_err, fmt='none')
        plt.plot(reg.x, reg.y, "x")
        m, b = reg.func_args[0], reg.func_args[1]
    """
    def __init__(self, func, x, y, error_mode=ErrorMode.COMBINED):
        """

        Parameters
        ----------
        func
            function to fit. must start with x
        x : list or error_analysis.evar.evar
            x values
        y : list or error_analysis.evar.evar
            y values
        error_mode : error_analysis.evar.ErrorMode
            Which error is considered in regression. ErrorMode.BOTH is not supported
        """
        if type(x) is evar:
            x_value = x.value
        else:
            x_value = x
        if type(y) is evar:
            y_value = y.value
        else:
            y_value = y
            error_mode = None
        if len(x_value) != len(y_value):
            raise Exception("Array sizes don't match")
        if error_mode == ErrorMode.NONE:
            popt, pcov = curve_fit(func, x.value, y.value)
            sig = np.zeros(len(x_value))
        else:
            sig = None
            if error_mode == ErrorMode.COMBINED:
                sig = y.get_combined_error()
            elif error_mode == ErrorMode.MAX:
                sig = y.max_error
            elif error_mode == ErrorMode.GAUSS:
                sig = y.gauss_error
            # scipy fails when one too small value is included
            min_val = y_value[np.argmin(y_value)] * 10 ** -3
            sig = [i + min_val for i in sig]
            popt, pcov = curve_fit(func, x.value, y.value, sigma=sig, absolute_sigma=True)
        stat_err = np.sqrt(np.diag(pcov))

        self.func_args = []
        """evars with fit parameter values and errors."""
        for i in range(len(popt)):
            self.func_args.append(evar(popt[i], stat_err[i], name="arg_{" + str(i) + "}"))
        self.func = func
        self.popt = popt
        self.x = x_value
        """original x values"""
        self.y = y_value
        """original y values"""
        self.y_reg = func(x_value, *popt)
        """y values calculated by regression"""
        self.y_err = sig
        """errors which were applied for regression"""


def lin_reg(x, y, error_mode=ErrorMode.COMBINED):
    """ Shortcut for linear regression

    Returns
    ----------
    reg : Regression
        regression instance
    m : error_analysis.evar.evar
        slope
    b : error_analysis.evar.evar
        offset
    """
    reg = Regression(__lin_func, x, y, error_mode)
    m, b = reg.func_args[0], reg.func_args[1]
    m.set_name("m")
    b.set_name("b")
    return reg, m, b
