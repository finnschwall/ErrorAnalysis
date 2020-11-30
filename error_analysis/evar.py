import sympy
import matplotlib.pyplot as plt
import weakref
import math
import numpy as np
from varname import varname
from error_analysis import options


# TODO keep track wether vars have errors


class evar:
    """
    Data type which supports error propagation
    """
    var_dic = dict()
    dic_id = 0

    def __init__(self, value=None, gauss_error=None, max_error=None, name=None, unit=None):
        """
        Creates new instance of a variable. All non-set variables are assumed to be 0.

        :param value: The value/s of the variable. Can be list or single value
        :param gauss_error: error which is propagated by gaussian estimation. If value is list but this is not,
        :param max_error: error which is propagated by maximum error estimation.
        :param name: Display name in everything string related. Can be latex style
        :param unit: not implemented yet
        """
        # keep track of all involved variables
        # it should be tested if this is really faster than iterating over all existing variables

        if unit is not None:
            # add unit support for operands.
            print("thats not finished yet")

        if name == "INT_OP":
            self.name = "unknown"
            self.__id = -1
            self.has_gauss_error = True
            self.has_max_error = True
        else:
            self.__dependencies = set()
            self.__id = evar.dic_id
            self.__dependencies.add(self.__id)

            evar.dic_id += 1
            # to ensure correct garbage collection
            evar.var_dic[self.__id] = weakref.ref(self)

            self.symbol = sympy.symbols("v" + str(self.__id) + "v", real=True)
            self.g_symbol = sympy.symbols("g" + str(self.__id) + "g", real=True)
            self.m_symbol = sympy.symbols("m" + str(self.__id) + "m", real=True)
            self.__expr = self.symbol
            self.__shadow_expr = self.__expr
            self.__shadow_dependencies = self.__dependencies
            self.has_gauss_error = True
            self.has_max_error = True
            # value of var init
            if value is None:
                self.is_list = False
                self.value = 0
                self.length = 1
            else:
                if type(value) is list:
                    self.is_list = True
                    self.length = len(value)
                    self.value = np.array(value)
                else:
                    self.is_list = False
                    self.length = 1
                    self.value = value
            # gaussian error init
            if gauss_error is None:
                self.has_gauss_error = False
                if self.length == 1:
                    self.gauss_error = 0
                else:
                    self.gauss_error = np.zeros(self.length)
            else:
                if type(gauss_error) == list:
                    self.gauss_error = np.array(gauss_error)
                else:
                    if self.length == 1:
                        self.gauss_error = gauss_error
                    else:
                        self.gauss_error = np.full(self.length, gauss_error)

            # maximum error init
            if max_error is None:
                self.has_max_error = False
                if self.length == 1:
                    self.max_error = 0
                else:
                    self.max_error = np.zeros(self.length)
            else:
                if type(max_error) == list:
                    self.max_error = max_error
                else:
                    if self.length == 1:
                        self.max_error = max_error
                    else:
                        self.max_error = np.full(self.length, max_error)

            # set name
            if name is None:
                self.name = str(varname(raise_exc=False))
                # format accordingly e.g. E_g to E_{g}
            else:
                self.name = name

    def __del__(self):
        if self.__id != -1:
            del self.symbol
            del self.m_symbol
            del self.g_symbol
            del evar.var_dic[self.__id]

    # makes this non temporary variable
    def set_name(self, name):
        """
        Sets name for this variable and also makes it a "real" variable.
        Using it in equations will now longer give expression of defining equation of this variable

        :param name: the new name for the variable
        """
        self.__shadow_expr = self.__expr
        self.__shadow_dependencies = self.__dependencies
        self.__id = evar.dic_id
        self.__dependencies = {self.__id}
        evar.dic_id += 1
        evar.var_dic[self.__id] = weakref.ref(self)
        self.symbol = sympy.symbols("v" + str(self.__id) + "v")
        self.g_symbol = sympy.symbols("g" + str(self.__id) + "g")
        self.m_symbol = sympy.symbols("m" + str(self.__id) + "m")
        self.__expr = self.symbol
        self.has_gauss_error = True
        self.has_max_error = True
        self.name = name

    def to_variable(self, name):
        """
        Same as set_name. Exists for backwards compatability
        :param name: new name of this instance
        :return:
        """
        self.set_name(name)

    def __get_expr(self):
        if self.__id == -1:
            return self.__expr, self.__dependencies
        else:
            return self.__shadow_expr, self.__shadow_dependencies

    def __replace_ids(self, string):
        temp_str = string
        expr, dependencies = self.__get_expr()
        for i in dependencies:
            num = i
            temp_str = temp_str.replace("v" + str(num) + "v", evar.var_dic[num]().name)
            temp_str = temp_str.replace("g" + str(num) + "g",
                                        r"\sigma_{" + options.gauss_error_name + "_{" + evar.var_dic[
                                            i]().name + "}}")
            temp_str = temp_str.replace("m" + str(num) + "m",
                                        r"\sigma_{" + options.max_error_name + "_{" + evar.var_dic[i]().name + "}}")
        return temp_str

    def get_expr(self, print_as_latex=options.print_as_latex):
        """
        Gets expression (equation) of this variable

        :param print_as_latex: wether to print this latex ready or more readable for console. Default is defined by options
        :return: expression as string
        """
        expr, dependencies = self.__get_expr()
        if options.simplify_eqs:
            expr = sympy.simplify(expr)
        expr = self.__replace_ids(sympy.latex(expr)) if print_as_latex else self.__replace_ids(str(expr))
        return expr

    def get_gauss_error_str(self, error_vars=None, print_as_latex=options.print_as_latex):
        iterator = None
        expr, dependencies = self.__get_expr()
        if error_vars is None:
            iterator = [evar.var_dic[i]() for i in dependencies]
        else:
            iterator = error_vars
        gauss_error = 0
        for i in iterator:
            if not i.has_gauss_error:
                continue
            temp_expr = expr.diff(i.symbol)
            temp_expr *= i.g_symbol
            temp_expr = temp_expr ** 2
            gauss_error += temp_expr
        gauss_error = sympy.sqrt(gauss_error)
        if options.simplify_eqs:
            gauss_error = sympy.simplify(gauss_error)
        gauss_error = self.__replace_ids(sympy.latex(gauss_error)) if print_as_latex else self.__replace_ids(
            str(gauss_error))
        return gauss_error

    def get_max_error_str(self, error_vars=None, print_as_latex=options.print_as_latex):
        iterator = None
        expr, dependencies = self.__get_expr()
        if error_vars is None:
            iterator = [evar.var_dic[i]() for i in dependencies]
        else:
            iterator = error_vars
        max_error = 0
        for i in iterator:
            if not i.has_max_error:
                continue
            temp_expr = expr.diff(i.symbol)
            temp_expr *= i.m_symbol
            temp_expr = abs(temp_expr)
            max_error += temp_expr
        if options.simplify_eqs:
            max_error = sympy.simplify(max_error)
        max_error = self.__replace_ids(sympy.latex(max_error)) if print_as_latex else self.__replace_ids(str(max_error))
        return max_error

    def show(self, font_size=12):
        """
        Shows screen with all equations and values

        :param font_size: font size of everything
        :return:
        """
        text = ""
        text += "$" + self.to_str(print_expr=True, print_as_latex=True) + "$\n"
        text += "$" + self.to_str(print_gauss_error=True, print_as_latex=True) + "$\n"
        text += "$" + self.to_str(print_max_error=True, print_as_latex=True) + "$\n"
        t_str = self.get_value_str(print_as_latex=True)
        t_str = t_str.replace("\n", "$\n$")
        text += "$" + t_str + "$"
        plt.text(0, 0.1, text, fontsize=font_size)
        plt.axis("off")
        plt.show()

    # TODO less lazy version that runs faster
    def get_value_str(self, print_as_latex=options.print_as_latex, no_rounding=options.no_rounding):
        if self.length == 1:
            if no_rounding:
                a, b, c = self.value, self.gauss_error, self.max_error
                if print_as_latex:
                    return self.name + " = (" + str(a) + " \pm " + str(b) + " \pm " + str(c) + r")"
                else:
                    return self.name + " = (" + str(a) + " \pm " + str(b) + " \pm " + str(c) + ")"
            else:
                a, b, c, d = _Tools.transform_to_sig(self.value, self.gauss_error, self.max_error)
                if print_as_latex:
                    return self.name + " = (" + str(a) + " \pm " + str(b) + " \pm " + str(c) + r")\cdot 10^{" + str(
                        d) + "}"
                else:
                    return self.name + " = (" + str(a) + " \pm " + str(b) + " \pm " + str(c) + ")\cdot 10^{" + str(
                        d) + "}"
        else:
            string = ""
            for i in range(self.length):
                string += self[i].get_value_str(print_as_latex, no_rounding) + "\n"
            return string[:-1]

    # TODO more formatting options like return in align
    def to_str(self, print_values=False, print_expr=False, print_gauss_error=False, print_max_error=False,
               print_all=False, print_as_latex=options.print_as_latex):
        ret_str = ""
        if print_values == False and print_expr == False and print_gauss_error == False and print_max_error == False and print_all == False:
            ret_str = self.name
        if print_all:
            print_values = True
            print_expr = True
            print_gauss_error = True
            print_max_error = True
        if print_values:
            ret_str += self.get_value_str(print_as_latex)
            if print_gauss_error or print_max_error or print_expr:
                ret_str += "\n"
        if print_expr:
            ret_str += self.name + "=" + self.get_expr(print_as_latex)
            if print_gauss_error or print_max_error:
                ret_str += "\n"
        if print_gauss_error:
            ret_str += r"\sigma_{" + options.gauss_error_name + "_{" + self.name + "}}" + "=" + self.get_gauss_error_str(
                print_as_latex=print_as_latex)
            if print_max_error:
                ret_str += "\n"
        if print_max_error:
            ret_str += r"\sigma_{" + options.max_error_name + "_{" + self.name + "}}" + "=" + self.get_max_error_str(
                print_as_latex=print_as_latex)
        return ret_str

    def __str__(self):
        return self.to_str(True, print_as_latex=False)

    def __getitem__(self, key):
        if self.length > 1:
            return evar(self.value[key], self.gauss_error[key], self.max_error[key],
                        self.name + "_{" + str(key) + "}")
        else:
            if key == 0:
                return self.value
            elif key == 1:
                return self.gauss_error
            elif key == 2:
                return self.max_error
            else:
                raise IndexError("list index out of range")

    # TODO add check for correlations. sig_stat(x-x+d) e.g. should  just be sig_stat(d)
    # operators
    def __finish_operation(self):
        if type(self.value) is np.ndarray:
            self.length = len(self.value)
            if np.count_nonzero(self.gauss_error) > 0:
                self.has_gauss_error = True
            else:
                self.has_gauss_error = False
            if np.count_nonzero(self.max_error) > 0:
                self.has_max_error = True
            else:
                self.has_max_error = False
        else:
            self.length = 1
            if self.gauss_error == 0:
                self.has_gauss_error = False
            else:
                self.has_gauss_error = True
            if self.max_error == 0:
                self.has_max_error = False
            else:
                self.has_max_error = True

    # + and -
    # +
    def __add__(self, other):
        RET_VAR = evar(name="INT_OP")
        if (type(other) == evar):
            RET_VAR.value = self.value + other.value
            RET_VAR.gauss_error = np.sqrt(self.gauss_error ** 2 + other.gauss_error ** 2)
            RET_VAR.max_error = np.abs(self.max_error) + np.abs(other.max_error)
            RET_VAR.__expr = self.__expr + other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value + other
            RET_VAR.gauss_error = self.gauss_error
            RET_VAR.max_error = np.abs(self.max_error)
            RET_VAR.__expr = self.__expr + other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    def __radd__(self, other):
        return self + other

    # -
    def __sub__(self, other):
        RET_VAR = evar(name="INT_OP")
        if type(other) == evar:
            RET_VAR.value = self.value - other.value
            RET_VAR.gauss_error = np.sqrt(self.gauss_error ** 2 + other.gauss_error ** 2)
            RET_VAR.max_error = np.abs(self.max_error) + np.abs(other.max_error)
            RET_VAR.__expr = self.__expr - other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value - other
            RET_VAR.gauss_error = self.gauss_error
            RET_VAR.max_error = self.max_error
            RET_VAR.__expr = self.__expr - other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    # TODO make this less lazy and more efficient
    def __rsub__(self, other):
        return -self + other

    def __neg__(self):
        RET_VAR = evar(name="INT_OP")
        RET_VAR.value = -self.value
        RET_VAR.gauss_error = self.gauss_error
        RET_VAR.max_error = self.max_error
        RET_VAR.__expr = -self.__expr
        RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    # * and /
    # *
    def __mul__(self, other):
        RET_VAR = evar(name="INT_OP")
        if type(other) == evar:
            RET_VAR.value = self.value * other.value
            RET_VAR.gauss_error = np.sqrt((other.gauss_error * self.value) ** 2 + (other.value * self.gauss_error) ** 2)
            RET_VAR.max_error = np.abs(other.max_error * self.value) + np.abs(self.max_error * other.value)
            RET_VAR.__expr = self.__expr * other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value * other
            RET_VAR.gauss_error = self.gauss_error * other
            RET_VAR.max_error = self.max_error * other
            RET_VAR.__expr = self.__expr * other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    def __rmul__(self, other):
        return self * other

    # /

    def __truediv__(self, other):
        RET_VAR = evar(name="INT_OP")
        if type(other) == evar:
            RET_VAR.value = self.value / other.value
            RET_VAR.gauss_error = np.sqrt(
                (other.gauss_error * self.value) ** 2 + (other.value * self.gauss_error) ** 2) / (other.value ** 2)
            RET_VAR.max_error = np.abs(other.max_error * self.value / other.value ** 2) + np.abs(
                self.max_error / other.value)
            RET_VAR.__expr = self.__expr / other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value / other
            RET_VAR.gauss_error = self.gauss_error / other
            RET_VAR.max_error = np.abs(self.max_error / other)
            RET_VAR.__expr = self.__expr / other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    def __rtruediv__(self, other):
        RET_VAR = evar(name="INT_OP")
        RET_VAR.value = other / self.value
        RET_VAR.gauss_error = other * np.abs(self.gauss_error) / self.value ** 2
        RET_VAR.max_error = other * np.abs(self.max_error / self.value ** 2)
        RET_VAR.__expr = other / self.__expr
        RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    # ^
    def __pow__(self, other):
        RET_VAR = evar(name="INT_OP")
        if type(other) == evar:
            RET_VAR.value = self.value ** other.value
            inner = (self.gauss_error * other.value) ** 2 + (other.gauss_error * self.value * np.log(self.value)) ** 2
            RET_VAR.gauss_error = np.sqrt(inner * self.value ** (2 * other.value - 2))
            RET_VAR.max_error = np.abs(self.max_error * other.value * self.value ** (other.value - 1)) + np.abs(
                other.max_error * np.log(self.value) * self.value ** other.value)
            RET_VAR.__expr = self.__expr ** other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value ** other
            RET_VAR.gauss_error = np.sqrt(self.value ** (2 * other - 2)) * np.abs(self.gauss_error * other)
            RET_VAR.max_error = np.abs(self.max_error * other * self.value ** (other - 1))
            RET_VAR.__expr = self.__expr ** other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR

    def __rpow__(self, other):
        # other**self
        RET_VAR = evar(name="INT_OP")
        RET_VAR.value = other ** self.value
        RET_VAR.gauss_error = np.abs(self.gauss_error) * np.log(other) * other ** self.value
        RET_VAR.max_error = np.abs(self.max_error) * np.log(other) * other ** self.value
        RET_VAR.__expr = other ** self.__expr
        RET_VAR.__dependencies = self.__dependencies
        RET_VAR.__finish_operation()
        return RET_VAR


class _Tools:
    # TODO prevent case b=c=0
    @staticmethod
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


def Variable(a=None, b=None, c=None, d=None):
    """
    This exists solely for backwards compatability
    """
    return evar(a, b, c, d)
