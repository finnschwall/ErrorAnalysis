from error_analysis import options
from error_analysis import evar


def create_vars():
    a = evar(1, 0.2, 0.23, name="a")
    b = evar(3, 0.11, 0.12, name="b")
    c = evar(5, 0.05, 0.34, name="c")
    d = evar(7, 0.4, 0.01, name="d")
    e = evar(9, 0.1, 0.12, name="e")
    f = evar(11, 0.3, 0.23, name="f")
    return a, b, c, d, e, f


def get_current_id():
    return evar.dic_id - 1


def get_id(a):
    return a._evar__id


def get_expr(a):
    return evar.var_dic[a._evar__id]()._evar__expr


def get_dic_info():
    a = []
    for i in evar.var_dic:
        get_info(evar.var_dic[i]())


def get_info(a):
    if type(a) is list:
        for i in range(len(a)):
            get_info(i)
    else:
        info = ""
        info += "\nname           =\t" + a.name
        info += "\nID             =\t" + str(a._evar__id)
        # info+="\nis_list         =\t"+str(a.is_list)
        # info+="\nlistLength     =\t"+str(a.length)
        info += "\ncontained var  =\t" + str(a._evar__dependencies)
        info += "\nexpression     =\t" + str(a._evar__expr)
        info += "\nvalue          =\t" + str(a.value)
        info += "\nhas_gauss_error=\t" + str(a.has_gauss_error)
        info += "\nGaussErr       =\t" + str(a.gauss_error)
        info += "\nhas_max_error  =\t" + str(a.has_max_error)
        info += "\nMaxErr         =\t" + str(a.max_error)
        print(info)


def get_options():
    info = ""
    info += "print_as_latex       : " + str(options.print_as_latex)
    info += "\nno_rounding          : " + str(options.no_rounding)
    info += "\ngauss_error_name     : " + str(options.gauss_error_name)
    info += "\nmax_error_name       : " + str(options.max_error_name)
    print(info)
