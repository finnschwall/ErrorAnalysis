from error_analysis import *


beta1 = Variable(1.56305412*10**-2    ,0.002              ,6.82326938*10**-4,r"\beta1")
a = Variable(91.3587077                 ,8.98282212         ,2.16304994)
wr= Variable(8.33404081*10**2          ,6.82326938*10**-3  ,1.64303289*10**-3,r"\omega_{r}")
d= Variable(2.28,0,0.1)
theta = Variable(1/2*25*10**-3*(2*10**-3)**2,name=r"\Theta")
e = Variable(1.602176634*10**-19)
me = Variable(9.1093837015*10**-31)
vstab = Variable(np.pi*(2*10**-3)**2*0.25)


ar = a/(4*beta1**2*wr**2)
ar.to_variable()
alpha  = Atan(ar/(2*d))
alpha.to_variable(r"\alpha")


betaVal = [0.037321316942706066, 0.033359071100090766, 0.034102199093836195]
betaStat= [0.0014644979183988565, 0.0014017198699761955, 0.0007014384562264148]
betaSys = [0.0020013171612657333, 0.0025681834482709624, 0.002850652999236956]

beta = Variable(betaVal,betaStat,betaSys,name=r"\beta")
dmax = 2*beta*wr*alpha*theta
dmax.to_variable("dmax")
print(dmax)
