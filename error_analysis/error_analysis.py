from sympy import *
from sympy.printing.mathml import mathml
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import scipy.constants as con
import weakref
import math
import numpy as np
import scipy.constants as con
from varname import varname, nameof
import logging

#General TODO
#fix naming. PEP8 is nicer anyway
#add scientific constants with symbols

#TODO add option for working with single error
#TODO implement fast mode
#BUG options don't work as parameters
class Options:
    #when false than string will be printed in more readable format
    print_as_latex=True
    #name of gauss error for printing
    gauss_error_name =  "stat"
    #name of maximum error for printing
    max_error_name=     "sys"
    #library will normaly look for siginificant places and cut numbers accordingly.
    #can be deactivated with this option
    no_rounding = False
    #Ignore expressions and just calculate. Significantly faster but doesn't allow
    #printing of gauss max or own expression.
    #WARNING: this will cause immediate garbage collection
    #also not finished yet. lol
    fast_mode = False
    #simplify equations before printing them
    #some simplifcations like sqrt(b*b)=sqrt(b^2)=|b| cannot be prevented
    simplify_eqs = True



#TODO keep track wether vars have errors
class Variable:
    var_dic = dict()
    dic_id = 0
    
    def __init__(self,value=None,gauss_error=None,max_error=None,name=None,unit=None):
        #keep track of all involved variables
        #it should be tested if this is really faster than iterating over all existing variables
        self.__dependencies = set()
        if unit != None:
            #add unit support for operands.
            print("thats not finished yet")

        if name == "INT_OP":
            self.name="unknown"
            self.__id = -1
            self.has_gauss_error=True
            self.has_max_error=True
        else:
            self.__id = Variable.dic_id
            self.__dependencies.add(self.__id)
            
            Variable.dic_id+=1
            #to ensure correct garbage collection
            Variable.var_dic[self.__id]=weakref.ref(self)

            self.symbol = symbols("v"+str(self.__id)+"v",real=True)
            self.g_symbol = symbols("g"+str(self.__id)+"g",real=True)
            self.m_symbol = symbols("m"+str(self.__id)+"m",real=True)
            self.__expr = self.symbol
            self.__shadow_expr = self.__expr
            self.__shadow_dependencies = self.__dependencies
            self.has_gauss_error=True
            self.has_max_error=True
            #value of var init
            if value is None:
                print("Variable without values was created.\nIt's very likely that this will cause problems")
                self.is_list = False
                self.value = 0
                self.length = 1
            else:
                if type(value) is list:
                    self.is_list = True
                    self.length = len(value)
                    self.value= np.array(value)
                else:
                    self.is_list = False
                    self.length = 1
                    self.value = value
            #gaussian error init
            if gauss_error is None:
                self.has_gauss_error=False
                if self.length == 1:
                    self.gauss_error = 0
                else:
                    self.gauss_error = [0 for i in range(0,self.length)]
            else:
                if type(gauss_error) == list:
                    self.gauss_error = np.array(gauss_error)
                else:
                    if self.length==1:
                        self.gauss_error = gauss_error
                    else:
                        self.gauss_error = np.full(self.length,gauss_error)

            #maximum error init
            if max_error is None:
                self.has_max_error=False
                if self.length == 1:
                    self.max_error = 0
                else:
                    self.max_error = np.zeros(self.length)
            else:
                if type(max_error) == list:
                    self.max_error = max_error
                else:
                    if self.length ==1:
                        self.max_error= max_error
                    else:
                        self.max_error = np.full(self.length,max_error)


            #set name
            if name is None:
                self.name=str(varname())
                #format accordingly e.g. E_g to E_{g}
            else:
                self.name=name
    
    def __del__(self):
        if self.__id != -1:
            del self.symbol
            del self.m_symbol
            del self.g_symbol
            del Variable.var_dic[self.__id]


#makes this non temporary variable
    def set_name(self,name):
        self.__shadow_expr = self.__expr
        self.__shadow_dependencies = self.__dependencies
        self.__id = Variable.dic_id
        self.__dependencies ={self.__id}
        Variable.dic_id+=1
        Variable.var_dic[self.__id]=weakref.ref(self)
        self.symbol = symbols("v"+str(self.__id)+"v")
        self.g_symbol = symbols("g"+str(self.__id)+"g")
        self.m_symbol = symbols("m"+str(self.__id)+"m")
        self.__expr = self.symbol
        self.has_gauss_error=True
        self.has_max_error=True
        self.name = name

    def __get_expr(self):
        if self.__id ==-1:
            return self.__expr, self.__dependencies
        else:
            return self.__shadow_expr,self.__shadow_dependencies
    
    def __replace_ids(self,string):
        temp_str = string
        expr, dependencies = self.__get_expr()
        for i in dependencies:
            num = i
            temp_str = temp_str.replace("v"+str(num)+"v",Variable.var_dic[i]().name)
            temp_str = temp_str.replace("g"+str(num)+"g",r"\sigma_{"+Options.gauss_error_name+"_{"+Variable.var_dic[i]().name+"}}")
            temp_str = temp_str.replace("m"+str(num)+"m",r"\sigma_{"+Options.max_error_name+"_{"+Variable.var_dic[i]().name+"}}")
        return temp_str

    def get_expr(self,print_as_latex=Options.print_as_latex):
        expr, dependencies = self.__get_expr()
        if Options.simplify_eqs:
            expr = simplify(expr)
        expr = self.__replace_ids(latex(expr)) if print_as_latex else self.__replace_ids(str(expr))
        return expr

    def get_gauss_error_str(self,error_vars=None,print_as_latex=Options.print_as_latex):
        iterator = None
        expr, dependencies = self.__get_expr()
        if error_vars == None:
            iterator = [Variable.var_dic[i]() for i in dependencies]
        else:
            iterator=error_vars
        gauss_error=0
        for i in iterator:
            if i.has_gauss_error == False:
                continue
            temp_expr=expr.diff(i.symbol)
            temp_expr*=i.g_symbol
            temp_expr=temp_expr**2
            gauss_error+=temp_expr
        gauss_error = sqrt(gauss_error)
        if Options.simplify_eqs:
            gauss_error = simplify(gauss_error)
        gauss_error = self.__replace_ids(latex(gauss_error)) if print_as_latex else self.__replace_ids(str(gauss_error))
        return gauss_error
    

    def get_max_error_str(self,error_vars=None,print_as_latex=Options.print_as_latex):
        iterator = None
        expr, dependencies = self.__get_expr()
        if error_vars == None:
            iterator = [Variable.var_dic[i]() for i in dependencies]
        else:
            iterator=error_vars
        max_error=0
        for i in iterator:
            if i.has_max_error ==False:
                continue
            temp_expr=expr.diff(i.symbol)
            temp_expr*=i.m_symbol
            temp_expr=abs(temp_expr)
            max_error+=temp_expr
        if Options.simplify_eqs:
            max_error = simplify(max_error)
        max_error = self.__replace_ids(latex(max_error)) if print_as_latex else self.__replace_ids(str(max_error))
        return max_error


    def show(self,fontSize=12):
        text = ""
        text += "$"+self.to_str(print_expr=True,print_as_latex=True) +"$\n"
        text += "$"+self.to_str(print_gauss_error=True,print_as_latex=True)+"$\n"
        text += "$"+self.to_str(print_max_error=True,print_as_latex=True)+"$\n"
        t_str = self.get_value_str(print_as_latex=True)
        t_str = t_str.replace("\n","$\n$")
        text += "$"+t_str+"$"
        plt.text(0, 0.1,text,fontsize=fontSize)
        plt.axis("off")
        plt.show()


    #TODO less lazy version that runs faster
    def get_value_str(self,print_as_latex=Options.print_as_latex,no_rounding=Options.no_rounding):
        if self.length ==1:
            if no_rounding:
                a,b,c = self.value,self.gauss_error,self.max_error
                if print_as_latex:
                    return self.name+" = ("+str(a)+" \pm " + str(b) + " \pm " +str(c)+r")"
                else:
                    return self.name+" = ("+str(a)+" \pm " + str(b) + " \pm " +str(c)+")"
            else:
                a,b,c,d = _Tools.transform_to_sig(self.value,self.gauss_error,self.max_error)
                if print_as_latex:
                    return self.name+" = ("+str(a)+" \pm " + str(b) + " \pm " +str(c)+r")\cdot 10^{"+str(d)+"}"
                else:
                    return self.name+" = ("+str(a)+" \pm " + str(b) + " \pm " +str(c)+")\cdot 10^{"+str(d)+"}"
        else:
            string = ""
            for i in range(self.length):
                string+=self[i].get_value_str(print_as_latex,no_rounding)+"\n"
            return string[:-1]
            

    def to_str(self,print_values=False,print_expr=False,print_gauss_error=False,print_max_error=False,print_all=False,print_as_latex=Options.print_as_latex):
        ret_str = ""
        if print_values == False and print_expr==False and print_gauss_error==False and print_max_error==False and print_all==False:
            ret_str = self.name
        if print_all:
            print_values=True
            print_expr=True
            print_gauss_error=True
            print_max_error=True
        if print_values:
            ret_str += self.get_value_str(print_as_latex)
            if print_gauss_error or print_max_error or print_expr:
                ret_str += "\n"
        if print_expr:
            ret_str+= self.name+"="+self.get_expr(print_as_latex)
            if print_gauss_error or print_max_error:
                ret_str += "\n"
        if print_gauss_error:
            ret_str+= r"\sigma_{"+Options.gauss_error_name+"_{"+self.name+"}}"+"="+self.get_gauss_error_str(print_as_latex=print_as_latex)
            if print_max_error:
                ret_str += "\n"
        if print_max_error:
            ret_str+= r"\sigma_{"+Options.max_error_name+"_{"+self.name+"}}"+"="+self.get_max_error_str(print_as_latex=print_as_latex)
        return ret_str

    
    def __str__(self):
        return self.to_str(True,print_as_latex=False)
        
    def __getitem__(self, key):
        if self.length>1:
            return Variable(self.value[key],self.gauss_error[key],self.max_error[key],self.name+"_{"+str(key)+"}")
        else:
            if key ==0:
                return self.value
            elif key==1:
                return self.gauss_error
            elif key ==2:
                return self.max_error
            else:
                raise IndexError("list index out of range")

    #operators

    #+ and -
    #+
    def __add__(self,other):
        RET_VAR = Variable(name="INT_OP")
        if(type(other)==Variable):
            RET_VAR.value = self.value+other.value
            RET_VAR.gauss_error = np.sqrt(self.gauss_error**2+other.gauss_error**2)
            RET_VAR.max_error = np.abs(self.max_error)+np.abs(other.max_error)
            RET_VAR.__expr=self.__expr+other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value+other
            RET_VAR.gauss_error =self.gauss_error
            RET_VAR.max_error = np.abs(self.max_error)
            RET_VAR.__expr=self.__expr+other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.length = len(RET_VAR.value)
        return RET_VAR
    def __radd__(self,other):
        return self+other
    #-
    def __sub__(self,other):
        RET_VAR = Variable(name="INT_OP")
        if(type(other)==Variable):
            RET_VAR.value = self.value-other.value
            RET_VAR.gauss_error = np.sqrt(self.gauss_error**2+other.gauss_error**2)
            RET_VAR.max_error = np.abs(self.max_error)+np.abs(other.max_error)
            RET_VAR.__expr=self.__expr-other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value-other
            RET_VAR.gauss_error = self.gauss_error
            RET_VAR.max_error = self.max_error
            RET_VAR.__expr=self.__expr-other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.length = len(RET_VAR.value)
        return RET_VAR
    #TODO make this less lazy and more efficient
    def __rsub__(self,other):
        return -self+other
    def __neg__(self):
        RET_VAR = Variable(name="INT_OP")
        RET_VAR.value = -self.value
        RET_VAR.gauss_error =  self.gauss_error
        RET_VAR.max_error = self.max_error
        RET_VAR.__expr= -self.__expr
        RET_VAR.__dependencies = self.__dependencies
        RET_VAR.length = len(RET_VAR.value)
        return RET_VAR

    # * and /
    #*
    def __mul__(self,other):
        RET_VAR = Variable(name="INT_OP")
        if(type(other)==Variable):
            RET_VAR.value = self.value*other.value
            RET_VAR.gauss_error =  np.sqrt((other.gauss_error*self.value)**2+(other.value*self.gauss_error)**2) 
            RET_VAR.max_error = np.abs(other.max_error*self.value)+np.abs(self.max_error*other.value)
            RET_VAR.__expr=self.__expr*other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value*other
            RET_VAR.gauss_error = self.gauss_error*other
            RET_VAR.max_error = self.max_error*other
            RET_VAR.__expr=self.__expr*other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.length = len(RET_VAR.value)
        return RET_VAR
    def __rmul__(self,other):
        return self*other
    #/
    
    def __truediv__(self,other):
        RET_VAR = Variable(name="INT_OP")
        if(type(other)==Variable):
            RET_VAR.value = self.value/other.value
            RET_VAR.gauss_error =  np.sqrt((other.gauss_error*self.value)**2+(other.value*self.gauss_error)**2)/(other.value**2) 
            RET_VAR.max_error = np.abs(other.max_error*self.value/other.value**2)+np.abs(self.max_error/other.value)
            RET_VAR.__expr=self.__expr/other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value/other
            RET_VAR.gauss_error = self.gauss_error/other
            RET_VAR.max_error = np.abs(self.max_error/other)
            RET_VAR.__expr=self.__expr/other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.length = len(RET_VAR.value)
        return RET_VAR
    
    def __rtruediv__(self,other):
        RET_VAR = Variable(name="INT_OP")
        RET_VAR.value = other/self.value
        RET_VAR.gauss_error = other*np.abs(self.gauss_error)/self.value**2
        RET_VAR.max_error = other*np.abs(self.max_error/self.value**2)
        RET_VAR.__expr=other/self.__expr
        RET_VAR.__dependencies = self.__dependencies
        RET_VAR.length = len(RET_VAR.value)
        return RET_VAR

    #^ 
    def __pow__(self,other):
        RET_VAR = Variable(name="INT_OP")
        if(type(other)==Variable):
            RET_VAR.value = self.value**other.value
            RET_VAR.gauss_error =  self.gauss_error
            RET_VAR.max_error = self.max_error
            RET_VAR.__expr=self.__expr**other.__expr
            RET_VAR.__dependencies = other.__dependencies | self.__dependencies
        else:
            RET_VAR.value = self.value**other
            RET_VAR.gauss_error = np.sqrt(self.value**(2*other-2))*np.abs(self.gauss_error*other)
            RET_VAR.max_error = np.abs(self.max_error*other*self.value**(other-1))
            RET_VAR.__expr=self.__expr**other
            RET_VAR.__dependencies = self.__dependencies
        RET_VAR.length = len(RET_VAR.value)
        return RET_VAR



class LinearRegression:
    #create two vars from lin reg
    def __init__():
        pass
class Regression:
    #create n vars from reg
    def __init__():
        pass

class Plot:
    #create plot from var, linreg or normal reg.
    #add errorbars etc accordingly
    def __init__():
        pass


class _Tools:
    #TODO prevent case b=c=0
    def transform_to_sig(a,b,c):
        a= float(a)
        b=float(b)
        c=float(c)
        aExp = math.floor(math.log10(abs(a)))
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



class Debug:
    def create_vars():
        a = Variable(1,0.2,0.23,name="a")
        b = Variable(3,0.11,0.12,name="b")
        c = Variable(5,0.05,0.34,name="c")
        d = Variable(7,0.4,0.01,name="d")
        e = Variable(9,0.1,0.12,name="e")
        f = Variable(11,0.3,0.23,name="f")
        return a,b,c,d,e,f
    def get_current_id():
        return Variable.dic_id-1
    def get_id(a):
        return a._Variable__id
    def get_expr(a):
        return Variable.var_dic[a._Variable__id]()._Variable__expr
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
            print(text)
        else:
            info= ""
            info+="\nname           =\t"+a.name
            info+="\nID             =\t"+str(a._Variable__id)
            #info+="\nis_list         =\t"+str(a.is_list)
            #info+="\nlistLength     =\t"+str(a.length)
            info+="\ncontained var  =\t"+str(a._Variable__dependencies)
            info+="\nexpression     =\t"+str(a._Variable__expr)
            info+="\nvalue          =\t"+str(a.value)
            info+="\nhas_gauss_error=\t"+str(a.has_gauss_error)
            info+="\nGaussErr       =\t"+str(a.gauss_error)
            info+="\nhas_max_error      =\t"+str(a.has_max_error)
            info+="\nMaxErr         =\t"+str(a.max_error)
            print(info)
    def get_options():
        info=""
        info+="print_as_latex       : "+str(Options.print_as_latex)
        info+="\nno_rounding          : "+str(Options.no_rounding)
        info+="\ngauss_error_name     : "+str(Options.gauss_error_name)
        info+="\nmax_error_name       : "+str(Options.max_error_name)
        print(info)
