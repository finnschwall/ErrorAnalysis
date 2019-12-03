from sympy import *
from sympy.printing.mathml import mathml
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import scipy.constants as con
import weakref
import math
import numpy as np



class Debug:
    def create_vars():
        a = Variable("1","0.2","0.23",name="a")
        b = Variable("3","0.11","0.12",name="b")
        c = Variable("5","0.05","0.34",name="c")
        d = Variable("7","0.4","0.01",name="d")
        e = Variable("9","0.1","0.12",name="e")
        f = Variable("11","0.3","0.23",name="f")
        return a,b,c,d,e,f
    def get_current_id():
        return Variable.dic_id-1
    def get_id(a):
        return a._Variable__id
    def get_expr(a):
        return Variable.var_dic[a._Variable__id]()._Variable__expr
    def is_variable(a):
        return a._Variable__isFormula
    def get_dic_info():
        a=[]
        for i in Variable.var_dic:
            a.append(Variable.var_dic[i]())
        return Debug.get_info(a)
    def var_to_string_list(a):
        text = "-----------"
        for i in range(len(a)):
            text+=Debug.getAllInfo(a[i])
            text+="\n-----------"
    def get_info(a):
        if type(a) is list:
            text = "-----------"
            for i in range(len(a)):
                text+=Debug.get_info(a[i])
                text+="\n-----------"
            return text
        else:
            info= ""
            info+="\nname           =\t"+a.name
            info+="\nID             =\t"+str(a._Variable__id)
            info+="\nis_list         =\t"+str(a.is_list)
            info+="\nlistLength     =\t"+str(a.length)
            info+="\nisFormula      =\t"+str(a._Variable__isFormula)
            info+="\nexpression     =\t"+str(a._Variable__expr)
            info+="\nvalue          =\t"+str(a.value)
            info+="\nhas_gauss_error=\t"+str(a.has_gauss_error)
            info+="\nGaussErr       =\t"+str(a.gauss_error)
            info+="\nhas_max_error      =\t"+str(a.has_max_error)
            info+="\nMaxErr         =\t"+str(a.max_error)
            return info
    def get_options():
        info=""
        info+="print_as_latex       : "+str(Options.print_as_latex)
        info+="\nforce_numeric_output : "+str(Options.force_numeric_output)
        info+="\nno_rounding          : "+str(Options.no_rounding)
        info+="\nforce_evaluation     : "+str(Options.force_evaluation)
        info+="\ngauss_error_name     : "+str(Options.gauss_error_name)
        info+="\nmax_error_name       : "+str(Options.max_error_name)
        return info
    
class Options:
    print_as_latex=True
    gauss_error_name =  "stat"
    max_error_name=     "sys"
    force_numeric_output = False
    show_latex = False
    force_evaluation = True
    no_rounding = False
    fast_mode = False
    simplify_eqs = True

class Regression:
    def __init__(x,y,expr):
        print(expr)
    

class Plot:
    def show(self):
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        for i in range(len(self.x)):
            xVals = self.x[i]
            yVals = self.y[i]
            if self.plot_type[i] is 0:
                if self.has_legend:
                    plt.plot(xVals,yVals,self.marker[i],label=self.name[i])
                else:
                    plt.plot(xVals,yVals,self.marker[i])
            elif self.plot_type[i] is 1:
                if self.has_legend:
                    plt.errorbar(xVals,yVals,yerr=self.opt1[i],fmt = 'o',label=self.name[i])
                else:
                    plt.errorbar(xVals,yVals,yerr=self.opt1[i],fmt = 'o')
        if self.has_legend:
            plt.legend(loc="best")
        plt.show()
    def lin_func(x,m,b):
        return m*x+b
    #todo Put in own class.
    #todo create general regression
    def from_linear_regression(x,y,xlabel=None,ylabel=None,name=None,regression_name=None,marker=None):
        ret = Plot(x,y,xlabel,ylabel,name,marker)
        popt, pcov = [],[]
        if y.has_gauss_error:
            minVal = y.value[np.argmin(y.value)]*10**-3
            sig = [i+minVal for i in y.gauss_error]
            popt, pcov = curve_fit(Plot.lin_func,x.value,y.value,sigma=sig,absolute_sigma=True)
            ret.plot_type[0]=1
            ret.opt1[0] = y.gauss_error
        else:
            popt, pcov = curve_fit(Plot.lin_func,x.value,y.value)
        statErr = np.sqrt(np.diag(pcov))
        minIndex = np.argmin(x.value)
        maxIndex = np.argmax(x.value)
        xReg= [x.value[minIndex],x.value[maxIndex]]
        yReg = [Plot.lin_func(i,*popt) for i in xReg]
        ret.x.append(xReg)
        ret.y.append(yReg)
        ret.marker.append("-")
        ret.plot_type.append(0)
        ret.opt1.append(0)
        if regression_name is None:
            ret.name.append("Regression "+name)
        else:
            ret.name.append(regression_name)
        m = Variable(popt[0],statErr[0],name="m")
        b=0
        if y.has_max_error:
            b = Variable(popt[1],statErr[1],y.max_error[0],name="m")
        else:
            b = Variable(popt[1],statErr[1],name="m")
        return ret,m,b

    def __init__(self,x,y,xlabel=None,ylabel=None,name=None,marker=None):
        self.has_legend=False
        self.x = [x.value]
        self.y = [y.value]
        self.opt1 = [0]
        self.plot_type = [0]
        if marker is None:
            self.marker = ["x"]
        else:
            self.marker = [marker]
        if xlabel is None:
            self.xlabel = x.name
        else:
            self.xlabel = xlabel
        if ylabel is None:
            self.ylabel = y.name
        else:
            self.ylabel = ylabel
        if name is None:
            self.name = [""]
        else:
            self.name = [name]
            self.has_legend=True
    
    def __add__(self,other):
        new_plot = Plot.__new__(Plot)
        new_plot.xlabel = self.xlabel
        new_plot.ylabel = self.ylabel
        new_plot.x = self.x+other.x
        new_plot.y = self.y+other.y
        new_plot.marker = self.marker+other.marker
        new_plot.name = self.name+other.name
        new_plot.opt1 = self.opt1+other.opt1
        new_plot.has_legend = self.has_legend
        new_plot.plot_type =self.plot_type+other.plot_type
        return new_plot
        
#TODO fix memory
class Variable:
    var_dic = dict()
    dic_id = 0
    
    #very temporary solution
    #keepCont = dict()
    
    def __init__(self,value=None,gauss_error=None,max_error=None,name=None,expr=None):
        #internal variables. don't touch
        self.dependencies = set()
        self.__isFormula=True
        self.__id = Variable.dic_id
        Variable.dic_id+=1
        #to ensure correct garbage collection
        Variable.var_dic[self.__id]=weakref.ref(self)

        #KEEP
        #Variable.keepCont[self.__id]=self
        self.symbol = symbols("v"+str(self.__id)+"v")
        self.gSymbol = symbols("g"+str(self.__id)+"g")
        self.mSymbol = symbols("m"+str(self.__id)+"m")
        self.has_gauss_error=True
        self.has_max_error=True
        #value of var init
        if value is None:
            self.is_list = False
            self.value = [0]
            self.length = 1
        else:
            if type(value) is list:
                self.is_list = True
                self.length = len(value)
                self.value= value
            else:
                self.is_list = False
                self.length = 1
                self.value=[value]
        #gaussian error init
        if gauss_error is None:
            self.has_gauss_error=False
            if self.length is 1:
                self.gauss_error = [0]
            else:
                self.gauss_error = [0 for i in range(0,self.length)]
        else:
            if type(gauss_error) is list:
                self.gauss_error = gauss_error
            else:
                self.gauss_error = [gauss_error for i in range(0,self.length)]

        #maximum error init
        if max_error is None:
            self.has_max_error=False
            if self.length is 1:
                self.max_error = [0]
            else:
                self.max_error = [0 for i in range(0,self.length)]
        else:
            if type(max_error) is list:
                self.max_error = max_error
            else:
                self.max_error = [max_error for i in range(0,self.length)]

        #expr evaluating
        if expr is None:
            self.__expr = self.symbol
        else:
            raise NotImplementedError

        #set name
        if name is None:
            self.name="UnnamedVariable"
            self.hasName=False
        else:
            self.hasName=True
            self.name=name
        if not(gauss_error is None and max_error is None and value is None):
            self.__isFormula=False
    
    def __del__(self):
        del self.symbol
        del self.gSymbol
        del self.mSymbol
        del Variable.var_dic[self.__id]


    def show(self,fontSize=12):
        temp1 = Options.print_as_latex
        temp2 = Options.force_numeric_output
        Options.print_as_latex = True
        Options.force_numeric_output = False
        plt.text(0, 1,"$"+str(self)+"$",fontsize=fontSize)
        Options.print_as_latex = temp1
        Options.force_numeric_output = temp2
        plt.axis("off")
        plt.show()
 
            
    def __sub__(self,other):
        temp = Variable()
        if(type(other)==Variable):
            nexpr= self.__expr-other.__expr
            temp.__expr=nexpr
            return temp
        else:
            nexpr= self.__expr-other
            temp.__expr=nexpr
            return temp
        
    def __isub__(self,other):
        self.__isFormula=True
        if(type(other)==Variable):
            self.__expr= self.__expr-other.__expr
        else:
            self.__expr=self.__expr-other
        return self
    
    def __add__(self,other):
        temp = Variable()
        if(type(other)==Variable):
            nexpr= self.__expr+other.__expr
            temp.__expr=nexpr
            return temp
        else:
            nexpr= self.__expr+other
            temp.__expr=nexpr
            return temp
           
    def __iadd__(self, other):
        self.__isFormula=True
        if(type(other)==Variable):
            self.__expr= self.__expr+other.__expr
        else:
            self.__expr=self.__expr+other
        return self
    
    def __mul__(self,other):
        temp = Variable()
        if(type(other)==Variable):
            nexpr= self.__expr*other.__expr
            temp.__expr=nexpr
            return temp
        else:
            nexpr= self.__expr*other
            temp.__expr=nexpr
            return temp
           
    def __imul__(self, other):
        self.__isFormula=True
        if(type(other)==Variable):
            self.__expr= self.__expr*other.__expr
        else:
            self.__expr=self.__expr*other
        return self

    def __truediv__(self,other):
        temp = Variable()
        if(type(other)==Variable):
            nexpr= self.__expr/other.__expr
            temp.__expr=nexpr
            return temp
        else:
            nexpr= self.__expr/other
            temp.__expr=nexpr
            return temp
               
    def __itruediv__(self, other):
        self.__isFormula=True
        if(type(other)==Variable):
            self.__expr= self.__expr/other.__expr
        else:
            self.__expr=self.__expr/other
        return self

    def __pow__(self,other):
        temp = Variable()
        if(type(other)==Variable):
            nexpr= self.__expr**other.__expr
            temp.__expr=nexpr
            return temp
        else:
            nexpr= self.__expr**other
            temp.__expr=nexpr
            return temp
    def __ipow__(self, other):
        self.__isFormula=True
        if(type(other)==Variable):
            self.__expr= self.__expr**other.__expr
        else:
            self.__expr=self.__expr**other
        return self

    def __rtruediv__(self,other):
        temp = Variable()
        if(type(other)==Variable):
            nexpr= other.__expr/self.__expr
            temp.__expr=nexpr
            return temp
        else:
            nexpr= other/self.__expr
            temp.__expr=nexpr
            return temp

    def __rsub__(self,other):
        temp = Variable()
        if(type(other)==Variable):
            nexpr= other.__expr-self.__expr
            temp.__expr=nexpr
            return temp
        else:
            nexpr= other-self.__expr
            temp.__expr=nexpr
            return temp
    def __getitem__(self, key):
        return [self.value[key],self.gauss_error[key],self.max_error[key]]
    
    def to_variable(self,name=None):
        if  name is not None:
            self.name = name
        var = _Tools.get_vars_in_expr(self.__expr)
        value=_Tools.eval(self.__expr,var)
        gauss_error = self.get_gauss_error(None,numeric=True)
        max_error = self.get_max_error(None,numeric=True)
        self.value = value
        self.is_list = True if len(value)!=1 else False
        self.gauss_error = gauss_error
        self.has_gauss_error = True if gauss_error !=0 else False
        self.has_max_error = True if max_error !=0 else False
        self.max_error = max_error
        self.__expr = self.symbol
        self.__isFormula=False
        return self
        
    def returnVariable(self,name=None):
        tName =""
        if name is None:
            if self.hasName is True:
                tName = self.name
            else:
                tName = "temp"
        else:
            tName=name
        var = _Tools.get_vars_in_expr(self.__expr)
        value=_Tools.eval(self.__expr,var)
        gauss_error = self.get_gauss_error(None,numeric=True)
        max_error = self.get_max_error(None,numeric=True)
        if len(value) is 1:
            nVar = Variable(value[0],gauss_error[0],max_error[0],tName)
        else:
            nVar = Variable(value,gauss_error,max_error,tName)
        return nVar
    
    def get_gauss_error(self,part_derivs=None,numeric=False):
        var = _Tools.get_vars_in_expr(self.__expr)
        if part_derivs is None:
            part_derivs=var
        gaussExpr = simplify(self.__calcGauss(part_derivs))
        if numeric:
            return _Tools.eval(gaussExpr,var)
        else:
            name = r"\sigma_{"+Options.gauss_error_name+"_{" +self.name +"}}"
            g = Variable(name=name)
            g.__isFormula=True
            g.__expr = gaussExpr
            g.hasError=False
            return g

    def __calcGauss(self,part_derivs):
        gauss_error = 0
        for curVar in part_derivs:
            tempExpr=self.__expr.diff(curVar.symbol)
            tempExpr*=curVar.gSymbol
            tempExpr=tempExpr**2
            gauss_error+=tempExpr
        gauss_error = gauss_error**0.5
        return gauss_error

    def get_max_error(self,part_derivs=None,numeric=False):
        var = _Tools.get_vars_in_expr(self.__expr)
        if part_derivs is None:
            part_derivs=var
        maxExpr = simplify(self.__calcMax(part_derivs))
        if numeric:
            return _Tools.eval(maxExpr,var)
        else:
            name = r"\sigma_{"+Options.max_error_name+"_{" +self.name +"}}"
            m = Variable(name=name)
            m.__isFormula=True
            m.__expr = maxExpr
            m.hasError=False
            return m
    
    def __calcMax(self,part_derivs):
        max_error = 0
        for curVar in part_derivs:
            tempExpr=self.__expr.diff(curVar.symbol)
            tempExpr*=curVar.mSymbol
            tempExpr=abs(tempExpr)
            max_error+=tempExpr
        return max_error

    
    def set_name(self,name):
        self.hasName=True
        self.name = name

    def eval(self):
        var = _Tools.get_vars_in_expr(self.__expr)
        return _Tools.eval(self.__expr,var)

    def __str__(self):
        if self.__isFormula:
            if Options.force_numeric_output is False:
                return self.name +" = "+ _Tools.toStr(self.__expr)
            else:
                return str(self.returnVariable("temp"))
        else:
            if self.is_list:
                retStr = ""
                if not self.has_max_error and not self.has_gauss_error:
                    for i in range(len(self.value)):
                        if Options.print_as_latex:
                            retStr += self.name +"_{"+str(i) + "} = " +str(self.value[i])+"\n"
                        else:
                            retStr += self.name +"_"+str(i) + " = " +str(self.value[i])+"\n"
                else:
                    for i in range(len(self.value)):
                        a,b,c,d = _Tools.transformToSig(self.value[i],self.gauss_error[i],self.max_error[i])
                        if Options.print_as_latex:
                            retStr += self.name+"_{"+str(i) + "} = ("+str(a)+" \pm " + str(b) + " \pm " +str(c)+r")\cdot 10^{"+str(d)+"}\n"
                        else:
                            retStr += self.name+"_"+str(i) + " = ("+str(a)+" \pm " + str(b) + " \pm " +str(c)+")*10^"+str(d)+"\n"
                return retStr[:-1]
            else:
                if not self.has_max_error and not self.has_gauss_error:
                    return self.name +" = " +str(self.value[0])
                a,b,c,d = _Tools.transformToSig(self.value[0],self.gauss_error[0],self.max_error[0])
                if Options.print_as_latex:
                    return self.name+" = ("+str(a)+" \pm " + str(b) + " \pm " +str(c)+r")\cdot 10^{"+str(d)+"}"
                else:
                    return self.name+" = ("+str(a)+" \pm " + str(b) + " \pm " +str(c)+")\cdot 10^{"+str(d)+"}"
                           
    __rmul__ = __mul__
    __radd__ = __add__

#internal heavily used methods
class _Tools:
    #TODO prevent case b=c=0
    def transformToSig(a,b,c):
        aExp = math.floor(math.log10(a))
        aT = a*10**-aExp
        bT = b*10**-aExp
        cT = c*10**-aExp
        if Options.no_rounding:
            return aT,bT,cT,aExp
        
        if b != 0:
            bExp =math.floor(math.log10(bT))
        else:
            bExp = 1
        if c != 0:
            cExp =math.floor(math.log10(cT))
        else:
            cExp = 1
        
        if cExp>1 or bExp>1:
            return round(aT),round(bT),round(cT),aExp
        if abs(bExp) > abs(cExp):
            return round(aT,abs(bExp)+1),round(bT,abs(bExp)+1),round(cT,abs(bExp)+1),aExp
        else:
            return round(aT,abs(cExp)+1),round(bT,abs(cExp)+1),round(cT,abs(cExp)+1),aExp


    
    def eval(expr,var):
        listLength=0
        for i in var:
            if len(i.value) > listLength:
                listLength= len(i.value)
        tExpr = [expr for i in range(listLength)]
        for curVar in var:
            if curVar.is_list:
                for i2 in range(listLength):
                    tExpr[i2] = tExpr[i2].replace(curVar.symbol,curVar.value[i2])
                    tExpr[i2] = tExpr[i2].replace(curVar.gSymbol,curVar.gauss_error[i2])
                    tExpr[i2] = tExpr[i2].replace(curVar.mSymbol,curVar.max_error[i2])
            else:
                for i2 in range(listLength):
                    tExpr[i2] = tExpr[i2].replace(curVar.symbol,curVar.value[0])
                    tExpr[i2] = tExpr[i2].replace(curVar.gSymbol,curVar.gauss_error[0])
                    tExpr[i2] = tExpr[i2].replace(curVar.mSymbol,curVar.max_error[0])
        if Options.force_evaluation:
            tExpr = [N(i) for i in tExpr]
        return tExpr

    def get_vars_in_expr(expr):
        var = []
        for i in expr.free_symbols:
            s = str(i)
            if 'v' in s:
                iId = int(str(i).replace("v",""))
                length = Variable.var_dic[iId]().length
                var.append(Variable.var_dic[iId]())
        return var
    def toStr(expr):
        tempStr=""
        if Options.print_as_latex:
            tempStr = latex(expr)
        else:
            tempStr= str(expr)
        for i in Variable.var_dic:
            num = i
            tempStr = tempStr.replace("v"+str(num)+"v",Variable.var_dic[i]().name)
            tempStr = tempStr.replace("g"+str(num)+"g",r"\sigma_{"+Options.gauss_error_name+"_{"+Variable.var_dic[i]().name+"}}")
            tempStr = tempStr.replace("m"+str(num)+"m",r"\sigma_{"+Options.max_error_name+"_{"+Variable.var_dic[i]().name+"}}")
        return tempStr


def Tan(a):
    temp = Variable()
    temp._Variable__expr=tan(a._Variable__expr)
    return temp
def Sin(a):
    temp = Variable()
    temp._Variable__expr=sin(a._Variable__expr)
    return temp
def Cos(a):
    temp = Variable()
    temp._Variable__expr=cos(a._Variable__expr)
    return temp
def Exp(a):
    temp = Variable()
    temp._Variable__expr=exp(a._Variable__expr)
    return temp
def Atan(a):
    temp = Variable()
    temp._Variable__expr=atan(a._Variable__expr)
    return temp
def Acos(a):
    temp = Variable()
    temp._Variable__expr=acos(a._Variable__expr)
    return temp
def Asin(a):
    temp = Variable()
    temp._Variable__expr=asin(a._Variable__expr)
    return temp
def Sinh(a):
    temp = Variable()
    temp._Variable__expr=sinh(a._Variable__expr)
    return temp
def Cosh(a):
    temp = Variable()
    temp._Variable__expr=cosh(a._Variable__expr)
    return temp
