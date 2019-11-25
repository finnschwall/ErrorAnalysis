from sympy import *
from sympy.printing.mathml import mathml
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import scipy.constants as con
import weakref
import math
import numpy as np



class Debug:
    def createVars():
        a = Variable("1","0.2","0.23",name="a")
        b = Variable("3","0.11","0.12",name="b")
        c = Variable("5","0.05","0.34",name="c")
        d = Variable("7","0.4","0.01",name="d")
        e = Variable("9","0.1","0.12",name="e")
        f = Variable("11","0.3","0.23",name="f")
        return a,b,c,d,e,f
    def getCurrentId():
        return Variable.dicId-1
    def getId(a):
        return a._Variable__id
    def getExpr(a):
        return Variable.varDic[a._Variable__id]()._Variable__expr
    def isVariable(a):
        return a._Variable__isFormula
    def getDicInfo():
        a=[]
        for i in Variable.varDic:
            a.append(Variable.varDic[i]())
        return Debug.getInfo(a)
    def varToStringList(a):
        text = "-----------"
        for i in range(len(a)):
            text+=Debug.getAllInfo(a[i])
            text+="\n-----------"
    def getInfo(a):
        if type(a) is list:
            text = "-----------"
            for i in range(len(a)):
                text+=Debug.getInfo(a[i])
                text+="\n-----------"
            return text
        else:
            info= ""
            info+="\nname       =\t"+a.name
            info+="\nID         =\t"+str(a._Variable__id)
            info+="\nisList     =\t"+str(a.isList)
            info+="\nlistLength =\t"+str(a.length)
            info+="\nisFormula  =\t"+str(a._Variable__isFormula)
            info+="\nexpression =\t"+str(a._Variable__expr)
            info+="\nvalue      =\t"+str(a.value)
            info+="\nhasGaussErr=\t"+str(a.hasGaussErr)
            info+="\nGaussErr   =\t"+str(a.gaussErr)
            info+="\nhasMaxErr  =\t"+str(a.hasMaxErr)
            info+="\nMaxErr     =\t"+str(a.maxErr)
            return info
    
class Options:
    printAsLatex=True
    gaussErrName =  "stat"
    maxErrName=     "sys"
    forceNumericOutput = False
    showLatex = False
    forceEvaluation = True
    noRounding = False
    fastMode = False


class Plot:
    def show(self):
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        for i in range(len(self.x)):
            xVals = self.x[i]
            yVals = self.y[i]
            if self.plotType[i] is 0:
                if self.hasLegend:
                    plt.plot(xVals,yVals,self.marker[i],label=self.name[i])
                else:
                    plt.plot(xVals,yVals,self.marker[i])
            elif self.plotType[i] is 1:
                print("hello")
                if self.hasLegend:
                    plt.errorbar(xVals,yVals,yerr=self.opt1[i],fmt = 'o',label=self.name[i])
                else:
                    plt.errorbar(xVals,yVals,yerr=self.opt1[i],fmt = 'o')
        if self.hasLegend:
            plt.legend(loc="best")
        plt.show()
    def linFunc(x,m,b):
        return m*x+b
    #todo Put in own class.
    #todo create general regression
    def fromLinearRegression(x,y,xLabel=None,yLabel=None,name=None,regressionName=None,marker=None):
        ret = Plot(x,y,xLabel,yLabel,name,marker)
        popt, pcov = [],[]
        if y.hasGaussErr:
            minVal = y.value[np.argmin(y.value)]*10**-3
            sig = [i+minVal for i in y.gaussErr]
            popt, pcov = curve_fit(Plot.linFunc,x.value,y.value,sigma=sig,absolute_sigma=True)
            ret.plotType[0]=1
            ret.opt1[0] = y.gaussErr
        else:
            popt, pcov = curve_fit(Plot.linFunc,x.value,y.value)
        statErr = np.sqrt(np.diag(pcov))
        minIndex = np.argmin(x.value)
        maxIndex = np.argmax(x.value)
        xReg= [x.value[minIndex],x.value[maxIndex]]
        yReg = [Plot.linFunc(i,*popt) for i in xReg]
        ret.x.append(xReg)
        ret.y.append(yReg)
        ret.marker.append("-")
        ret.plotType.append(0)
        ret.opt1.append(0)
        if regressionName is None:
            ret.name.append("Regression "+name)
        else:
            ret.name.append(regressionName)
        m = Variable(popt[0],statErr[0],name="m")
        b=0
        if y.hasMaxErr:
            b = Variable(popt[1],statErr[1],y.maxErr[0],name="m")
        else:
            b = Variable(popt[1],statErr[1],name="m")
        return ret,m,b

    def __init__(self,x,y,xLabel=None,yLabel=None,name=None,marker=None):
        self.hasLegend=False
        self.x = [x.value]
        self.y = [y.value]
        self.opt1 = [0]
        self.plotType = [0]
        if marker is None:
            self.marker = ["x"]
        else:
            self.marker = [marker]
        if xLabel is None:
            self.xLabel = x.name
        else:
            self.xLabel = xLabel
        if yLabel is None:
            self.yLabel = y.name
        else:
            self.yLabel = yLabel
        if name is None:
            self.name = [""]
        else:
            self.name = [name]
            self.hasLegend=True

#TODO fix memory
class Variable:
    varDic = dict()
    dicId = 0
    
    #very temporary solution
    keepCont = dict()
    
    def __init__(self,value=None,gaussErr=None,maxErr=None,name=None,expr=None):
        #internal variables. don't touch
        self.__isFormula=True
        self.__id = Variable.dicId
        Variable.dicId+=1
        #to ensure correct garbage collection
        Variable.varDic[self.__id]=weakref.ref(self)
        Variable.keepCont[self.__id]=self
        self.symbol = symbols("v"+str(self.__id)+"v")
        self.gSymbol = symbols("g"+str(self.__id)+"g")
        self.mSymbol = symbols("m"+str(self.__id)+"m")
        self.hasGaussErr=True
        self.hasMaxErr=True
        #value of var init
        if value is None:
            self.isList = False
            self.value = [0]
            self.length = 1
        else:
            if type(value) is list:
                self.isList = True
                self.length = len(value)
                self.value= value
            else:
                self.isList = False
                self.length = 1
                self.value=[value]
        #gaussian error init
        if gaussErr is None:
            self.hasGaussErr=False
            if self.length is 1:
                self.gaussErr = [0]
            else:
                self.gaussErr = [0 for i in range(0,self.length)]
        else:
            if type(gaussErr) is list:
                self.gaussErr = gaussErr
            else:
                self.gaussErr = [gaussErr for i in range(0,self.length)]

        #maximum error init
        if maxErr is None:
            self.hasMaxErr=False
            if self.length is 1:
                self.maxErr = [0]
            else:
                self.maxErr = [0 for i in range(0,self.length)]
        else:
            if type(maxErr) is list:
                self.maxErr = maxErr
            else:
                self.maxErr = [maxErr for i in range(0,self.length)]

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
        if not(gaussErr is None and maxErr is None and value is None):
            self.__isFormula=False
    
    def __del__(self):
        del self.symbol
        del self.gSymbol
        del self.mSymbol
        del Variable.varDic[self.__id]


    def show(self,fontSize=12):
        temp1 = Options.printAsLatex
        temp2 = Options.forceNumericOutput
        Options.printAsLatex = True
        Options.forceNumericOutput = False
        plt.text(0, 1,"$"+str(self)+"$",fontsize=fontSize)
        Options.printAsLatex = temp1
        Options.forceNumericOutput = temp2
        plt.axis("off")
        plt.show()
        
    def __imul__(self, other):
        self.__isFormula=True
        if(type(other)==Variable):
            self.__expr= self.__expr*other.__expr
        else:
            self.__expr=self.__expr*other
        return self
            
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
        return [self.value[key],self.gaussErr[key],self.maxErr[key]]
    
    def toVariable(self,name=None):
        if  name is not None:
            self.name = name
        var = _Tools.getVarsInExpr(self.__expr)
        value=_Tools.eval(self.__expr,var)
        gaussErr = self.getGaussError(None,numeric=True)
        maxErr = self.getMaxError(None,numeric=True)
        self.value = value
        self.gaussErr = gaussErr
        self.maxErr = maxErr
        self.__expr = self.symbol
        self.__isFormula=False
        
    def returnVariable(self,name=None):
        tName =""
        if name is None:
            if self.hasName is True:
                tName = self.name
            else:
                tName = "temp"
        else:
            tName=name
        var = _Tools.getVarsInExpr(self.__expr)
        value=_Tools.eval(self.__expr,var)
        gaussErr = self.getGaussError(None,numeric=True)
        maxErr = self.getMaxError(None,numeric=True)
        if len(value) is 1:
            nVar = Variable(value[0],gaussErr[0],maxErr[0],tName)
        else:
            nVar = Variable(value,gaussErr,maxErr,tName)
        return nVar
    
    def getGaussError(self,partDerivs=None,numeric=False):
        var = _Tools.getVarsInExpr(self.__expr)
        if partDerivs is None:
            partDerivs=var
        gaussExpr = self.__calcGauss(partDerivs)
        if numeric:
            return _Tools.eval(gaussExpr,var)
        else:
            name = r"\sigma_{"+Options.gaussErrName+"_{" +self.name +"}}"
            g = Variable(name=name)
            g.__isFormula=True
            g.__expr = gaussExpr
            g.hasError=False
            return g

    def __calcGauss(self,partDerivs):
        gaussError = 0
        for curVar in partDerivs:
            tempExpr=self.__expr.diff(curVar.symbol)
            tempExpr*=curVar.gSymbol
            tempExpr=tempExpr**2
            gaussError+=tempExpr
        gaussError = gaussError**0.5
        return gaussError

    def getMaxError(self,partDerivs=None,numeric=False):
        var = _Tools.getVarsInExpr(self.__expr)
        if partDerivs is None:
            partDerivs=var
        maxExpr = self.__calcMax(partDerivs)
        if numeric:
            return _Tools.eval(maxExpr,var)
        else:
            name = r"\sigma_{"+Options.maxErrName+"_{" +self.name +"}}"
            m = Variable(name=name)
            m.__isFormula=True
            m.__expr = maxExpr
            m.hasError=False
            return m
    
    def __calcMax(self,partDerivs):
        maxError = 0
        for curVar in partDerivs:
            tempExpr=self.__expr.diff(curVar.symbol)
            tempExpr*=curVar.gSymbol
            tempExpr=abs(tempExpr)
            maxError+=tempExpr
        return maxError

    
    def setName(self,name):
        self.hasName=True
        self.name = name

    def eval(self):
        var = _Tools.getVarsInExpr(self.__expr)
        return _Tools.eval(self.__expr,var)

    def __str__(self):
        if self.__isFormula:
            if Options.forceNumericOutput is False:
                return self.name +" = "+ _Tools.toStr(self.__expr)
            else:
                return str(self.returnVariable("temp"))
        else:
            if self.length > 1:
                retStr = ""
                if not self.hasMaxErr and not self.hasGaussErr:
                    for i in range(self.length):
                        if Options.printAsLatex:
                            retStr += self.name +"_{"+str(i) + "} = " +str(self.value[i])+"\n"
                        else:
                            retStr += self.name +"_"+str(i) + " = " +str(self.value[i])+"\n"
                else:
                    for i in range(self.length):
                        a,b,c,d = _Tools.transformToSig(self.value[i],self.gaussErr[i],self.maxErr[i])
                        if Options.printAsLatex:
                            retStr += self.name+"_{"+str(i) + "} = ("+str(self.value[i])+" \pm " + str(self.gaussErr[i]) + " \pm " +str(self.maxErr[i])+")\n"
                        else:
                            retStr += self.name+"_"+str(i) + " = ("+str(self.value[i])+" \pm " + str(self.gaussErr[i]) + " \pm " +str(self.maxErr[i])+")\n"
                return retStr[:-1]
            else:
                if not self.hasMaxErr and not self.hasGaussErr:
                    return self.name +" = " +str(self.value[0])
                a,b,c,d = _Tools.transformToSig(self.value[0],self.gaussErr[0],self.maxErr[0])
                if Options.printAsLatex:
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
        if Options.noRounding:
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
            if i.length > listLength:
                listLength= i.length
        tExpr = [expr for i in range(listLength)]
        for curVar in var:
            if curVar.isList:
                for i2 in range(listLength):
                    tExpr[i2] = tExpr[i2].replace(curVar.symbol,curVar.value[i2])
                    tExpr[i2] = tExpr[i2].replace(curVar.gSymbol,curVar.gaussErr[i2])
                    tExpr[i2] = tExpr[i2].replace(curVar.mSymbol,curVar.maxErr[i2])
            else:
                for i2 in range(listLength):
                    tExpr[i2] = tExpr[i2].replace(curVar.symbol,curVar.value[0])
                    tExpr[i2] = tExpr[i2].replace(curVar.gSymbol,curVar.gaussErr[0])
                    tExpr[i2] = tExpr[i2].replace(curVar.mSymbol,curVar.maxErr[0])
        if Options.forceEvaluation:
            tExpr = [N(i) for i in tExpr]
        return tExpr

    def getVarsInExpr(expr):
        var = []
        for i in expr.free_symbols:
            s = str(i)
            if 'v' in s:
                iId = int(str(i).replace("v",""))
                length = Variable.varDic[iId]().length
                var.append(Variable.varDic[iId]())
        return var
    def toStr(expr):
        tempStr=""
        if Options.printAsLatex:
            tempStr = latex(expr)
        else:
            tempStr= str(expr)
        for i in Variable.varDic:
            num = i
            tempStr = tempStr.replace("v"+str(num)+"v",Variable.varDic[i]().name)
            tempStr = tempStr.replace("g"+str(num)+"g",r"\sigma_{"+Options.gaussErrName+"_{"+Variable.varDic[i]().name+"}}")
            tempStr = tempStr.replace("m"+str(num)+"m",r"\sigma_{"+Options.maxErrName+"_{"+Variable.varDic[i]().name+"}}")
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
