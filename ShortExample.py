from ErrorAnalysis import *




#this dictates wether print() gives string in latex style or not
Options.printAsLatex=False

#dictates wether fractions or something like tan(a) will be numericaly evaluated. standard is true
Options.forceEvaluation = True

#causes every output to be numeric. standard is false
##Options.forceNumericOutput=True

##library might take a long time on first execution
####Variable declaration####

#Examples for declaration
#standard constructor
a = Variable(1,0.2,0.23,name="a")

#variable with latex name. \ must be escaped or r is necessary before string
beta = Variable(3,0.11,0.12,name=r"\beta")

# variable with systematic error =0
c = Variable(5,maxErr=0.05,name="c")

# variable with statistical error = 0
d = Variable(7,0.01,name="d")

#nameless variable. will be printed with unknown name
e = Variable(9,0.1,0.12)

#only a variable
f = Variable(name="f")

#DON'T DO THIS
#g = Variable()

#Variables can also be lists
g = [1,2,3,4,5]
h = [2,3,4,5,6]
g = Variable(g,name="g")
h = Variable(h,name="h")

#non set lists will be a list of 0s. here the systematic error is 0
iValue = [2,3,4,5,6]
iStatError = [0.3,0,2,0.4,0.3]

i = Variable(iValue,iStatError,name="i")

#here everything is set
jValue = [1,1.2,1.4,0.9]
jStatError = [0.1,0.2,0.1,0.3]
jSysError = 0.3

j = Variable(jValue,jStatError,jSysError)

### mathematical operations ####

#new variables can be created simply by using standard operators
#Available standard operators: Tan Sin Cos, Atan Asin Acos, Sinh Cosh, Exp
k = beta*Tan(a)+c/d

#formulas can simply be printed
print(k)


#name of this new variable can be set too
k.setName("k")
print(k)

#Formula can also be displayed. might not work
#k.showFormula()

#evaluate and get value list
v=k.eval()
print(v)

#get statistical error (gaussian error estimation)
statK = k.getGaussError()
##statK.show()
#or as string
print(statK)
      
#get systematic error (maximum error estimation)
sysK = k.getMaxError()
##sysK.show()
#or as string
print(sysK)


#only get error for specific variables
significantVariables = [c,d]
statK = k.getGaussError(significantVariables)
##statK.show()
#or
#k.getGaussError(significantVariables).show()

#variables can also be transformed to make calculation easier.
k = k.toVariable()
# this causes k to be fully evaluated. neccessary precision is automatically evaluated
print(k)
#note: expression for k is now lost. all variables that are not in scope anymore and were used in k will now be deleted









