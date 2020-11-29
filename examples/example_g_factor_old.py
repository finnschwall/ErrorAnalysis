from error_analysis import *


beta1 = Variable(1.56305412*10**-2    ,0.002              ,6.82326938*10**-4,r"\beta1")
a = Variable(91.3587077                 ,8.98282212         ,2.16304994,"a")
wr= Variable(83.33404081          ,6.82326938*10**-3  ,1.64303289*10**-3,r"\omega_{r}")
d= Variable(2.28,0,0.1)
theta = Variable(1/2*25*10**-3*(2*10**-3)**2,name=r"\Theta")
e = Variable(1.602176634*10**-19,name="e")
me = Variable(9.1093837015*10**-31,name="m_{e}")
vstab = Variable(np.pi*(2*10**-3)**2*0.25,name="A_{rod}")

a*=1/100

ar = a/(4*beta1**2*wr**2)
ar.to_variable()
alpha  = Atan(ar/(2*d))
alpha.to_variable(r"\alpha")


betaVal = [0.037321316942706066, 0.033359071100090766, 0.034102199093836195]
betaStat= [0.0014644979183988565, 0.0014017198699761955, 0.0007014384562264148]
betaSys = [0.0020013171612657333, 0.0025681834482709624, 0.002850652999236956]

beta = Variable(betaVal,betaStat,betaSys,name=r"\beta")
dmax = 2*beta*wr*alpha*theta
dmax.set_name(r"D_{max}")
dmax.to_variable()
print(dmax)
##print()
##print(dmax.get_max_error())
##dmax.to_variable("dmax")
##print()
##print(dmax)

dmdtVal = [-499241082.0962259,-530787227.6114469,-546560300.3690574] 

dmdtG = Variable(dmdtVal,name=r" \frac{dM}{dt}")
g =-2*me*vstab/(e*dmax)*dmdtG
g.set_name("g")
print(g)
print()
print(g.get_gauss_error([dmax,dmdtG]))
print()
print(g.get_max_error([dmax,dmdtG]))

##
print(g.to_variable("g"))

fstab=np.pi*(2/(1000))**2
fspule= np.pi*(4.3/(2*100))**2
mu0=1.25663706212*10**-6
n1=1845
n2=1000
l=0.25
a=-1/(mu0*n2*fstab)
b=n1*fspule/(fstab*l)

IVal = [0.500,0.600,0.700]

uIndVal = [1.725,1.871,1.941]


I = Variable(IVal,0,0.03)
uind = Variable(uIndVal,0,0.01)
##uind*=10
dmdt = a*uind+b*wr*I
dmdt.to_variable("dmdt")
g = -2*me*vstab/(e*dmax)*dmdt
##g*=10
g.to_variable("g")
print(g)




