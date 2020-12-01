from scipy.optimize import curve_fit
from error_analysis.evar import *


# TODO add whatever regression
# TODO add specific linear regression

def __lin_func(x, m, b):
    return m * x + b


class Regression:
    """
    evar wrapper for curve_fit. Also works on normals lists

    """
    def __init__(self, func, x, y, error_mode=ErrorMode.COMBINED):
        """
        for arbitrary regressions

        :param func: function to fit. must start with x
        :param x: x values
        :param y: y values
        :param error_mode: see ErrorMode
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
        for i in range(len(popt)):
            self.func_args.append(evar(popt[i], stat_err[i], name="arg_{" + str(i) + "}"))
        self.func = func
        self.popt = popt
        self.x = x_value
        self.y = y_value
        self.y_reg = func(x_value, *popt)
        self.y_err = sig


def lin_reg(x, y, error_mode=ErrorMode.COMBINED):
    reg = Regression(__lin_func, x, y, error_mode)
    m, b = reg.func_args[0], reg.func_args[1]
    m.set_name("m")
    b.set_name("b")
    return reg, m, b
