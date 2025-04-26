# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:21:38 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
from tabulate import tabulate
from numpy.linalg import *

def I(beta):
    I=(np.sin(beta)/beta)**2
    return I

def beta(a,l,theta):
    beta=(np.pi*a/l)*(np.sin(theta))
    return beta

def lineal(x,a,b):
    y = a+b*x 
    return y

def mediaponderada(x,sx):
    xm=np.dot(x,1/sx**2)/sum(1/sx**2)
    sxm=1/np.sqrt(sum(1/sx**2))
    return xm,sxm

def regresion_lineal(x,y):
    a,b=curve_fit(lineal,x,y)[0]
    ss=curve_fit(lineal,x,y)[1]
    sa=np.sqrt(ss[0,0])
    sb=np.sqrt(ss[1,1])
    return a,b,sa,sb


def ajustelineal(x,y,sig): # Aquí metemos los dos valores y el peso estadístico (sig)
    H=np.array([[sum(1./sig**2),sum(x/sig**2)],[sum(x/sig**2),sum(x**2/sig**2)]])
    Delta=det(H)
    Z=np.array([sum(y/sig**2),sum((x*y)/sig**2)])
    ([a,b])=np.matmul(inv(H),Z)
    siga=np.sqrt(sum(x**2/sig**2)/Delta)
    sigb=np.sqrt(sum(1./sig**2)/Delta)
    return a,b,siga,sigb

def concatenarbueno(lista):
    a=np.zeros([len(lista[0]),len(lista)])
    for i in range(len(lista)):
        for j in range(len(lista[0])):
            a[j,i]=lista[i][j]
    return a


def plotea(x,y,a3,b3,i,L):
    plt.figure()
    bbox = dict(boxstyle="round", fc="0.9",alpha=0.7)
    u=np.linspace(min(x),max(x),20)
    v=lineal(u,a3,b3)
    plt.grid(True,linestyle="--")
    plt.xlabel("n")
    plt.ylabel("x (m)")
    plt.plot(u,v,color="blue",label="Regresion")
    plt.plot(x,y,".",color="red",label="Datos experimentales")
    plt.annotate("A=%.2f mm \nB=%.2f mm"%(b3*10**3,a3*10**3), (max(x)-2,min(y)+(max(y)-min(y))/5),  bbox=bbox)
    plt.legend()
    plt.title("Hendidura %d, z = %.2f m"%(i,L))


lamb=632.8*10**(-9) #nm

#%% 
# -------- PRIMERA FENDA --------------------

z1=192  
z2=201
z3=236.5
z4=265
z5=339

z1=np.array([192,201,236.5,265,339])*10**(-2)
n1=np.array([-3,-2,-1,1,2,3])
L1=np.array([-5.3,-3.8,-2.1,2.3,3.9,5.3])*10**(-2)  #192
n2=np.array([-3,-2,-1,1,2,3])
L2=np.array([-5.7,-4.1,-2.4,2.3,3.9,5.6])*10**(-2) #([-8.8,-7.2,,7.2,8.8])*10**(-2)  #201
n3=np.array([-3,-2,-1,1,2,3])
L3=np.array([-6.7,-4.8,-2.8,2.8,4.7,6.6])*10**(-2)  #236
n4=np.array([-3,-2,-1,1,2,3])
L4=np.array([-7.5,-5.4,-3.2,3.1,5.2,7.5])*10**(-2)  #265 ([-9.5,,9.5])
n5=np.array([-3,-2,-1,1,2,3])
L5=np.array([-9.5,-6.7,-4.1,4.0,6.7,9.5])*10**(-2)  #339


L1=np.array([L1,L2,L3,L4,L5])
n=np.array([-3,-2,-1,1,2,3])
a1=np.array([])
b1=np.array([])
sa1=np.array([])
sb1=np.array([])
for i in range(len(z1)):
    x=L1[i]
    a,b,sa,sb=ajustelineal(n,x,np.array([0.1*10**(-2)]*len(x)))
    a1=np.append(a1,a)
    b1=np.append(b1,b)
    sa1=np.append(sa1,sa)
    sb1=np.append(sb1,sb)
    plotea(n,x,a,b,1,z1[i])
    plt.savefig("Hendidura-1-%d.pdf"%(i+1),bbox_inches="tight")

sz1=np.array([5*10**(-2)]*len(z1))
D1=np.array([])
sD1=np.array([])
for i in range(len(b1)):
    D1=np.append(D1,lamb*z1[i]/b1[i])
    sD1=np.append(sD1,lamb*np.sqrt((sb1[i]*z1[i]/(b1[i])**2)**2
                                   +(sz1[i]/b1[i])**2))

    
print(np.average(D1)*10**(6), "um")

hola=concatenarbueno((z1,sz1,a1*10**3,sa1*10**3,b1*10**3,sb1*10**3,D1*10**6,sD1*10**6))
hola=np.array(hola,dtype=float)
tabla=tabulate(hola,tablefmt="latex",floatfmt=(".2f", ".2f",".2f",".2f",".2f",".2f",".1f",".1f"))
outfile=open("Datos1.txt","w")
outfile.write(tabla)
outfile.close()

a1,sa1=mediaponderada(D1, sD1)
print("a= %.2f s(a)= %.2f"%(a1*10**(6),sa1*10**(6)))

#%%
# -------- SEGUNDA FENDA --------------------

#fenda 2
z21=167.5
z22=199
z23=247
z24=283.5
z25=339
z2=np.array([167.5,199,247,283.5,339])*10**(-2)

n1=np.array([-4,-3,-2,-1,1,2,3,4])
L1=np.array([-3,-2.3,-1.7,-1,1,1.6,2.3,3.1]) #167.5
n2=np.array([-4,-3,-2,-1,1,2,3,4])
L2=np.array([-3,-2.3,-1.6,-1,1,1.6,2.3,3]) #199
n3=np.array([-4,-3,-2,-1,1,2,3,4])
L3=np.array([-4.5,-3.5,-2.4,-1.6,1.5,2.4,3.5,4.5]) #247
n4=np.array([-4,-3,-2,-1,1,2,3,4])
L4=np.array([-5.1,-3.9,-2.7,-1.6,1.7,2.8,3.9,5.1]) #283.5
n5=np.array([-4,-3,-2,-1,1,2,3,4])
L5=np.array([-6.2,-4.8,-3.4,-2,2,3.4,4.7,6.2]) #339

n=np.array([-4,-3,-2,-1,1,2,3,4])
L2=np.array([L1,L2,L3,L4,L5])*10**(-2)

a2=np.array([])
b2=np.array([])
sa2=np.array([])
sb2=np.array([])
for i in range(len(z2)):
    x=L2[i]
    a,b,sa,sb=ajustelineal(n,x,np.array([0.1*10**(-2)]*len(x)))
    a2=np.append(a2,a)
    b2=np.append(b2,b)
    sa2=np.append(sa2,sa)
    sb2=np.append(sb2,sb)
    plotea(n,x,a,b,2,z2[i])
    plt.savefig("Hendidura-2-%d.pdf"%(i+1),bbox_inches="tight")


sz2=np.array([5*10**(-2)]*len(z2))
D2=np.array([])
sD2=np.array([])
for i in range(len(b1)):
    D2=np.append(D2,lamb*z2[i]/b2[i])
    sD2=np.append(sD2,lamb*np.sqrt((sb2[i]*z2[i]/(b2[i])**2)**2
                                   +(sz2[i]/b2[i])**2))

hola2=concatenarbueno((z2,sz2,a2*10**3,sa2*10**3,b2*10**3,sb2*10**3,D2*10**6,sD2*10**6))
hola2=np.array(hola2,dtype=float)
tabla2=tabulate(hola2,tablefmt="latex",floatfmt=(".2f", ".2f",".2f",".2f",".2f",".2f",".1f",".1f"))
outfile=open("Datos2.txt","w")
outfile.write(tabla2)
outfile.close()
    
a2,sa2=mediaponderada(D2, sD2)
print("a= %.2f s(a)= %.2f"%(a2*10**(6),sa2*10**(6)))

#%%

teorico=np.array([9*0.0005/50,13*0.0005/50,])*10**6
steorico=np.array([1*0.0005/50,1*0.0005/50,])*10**6
print(teorico[0],steorico[0],"um")
print(teorico[1],steorico[1],"um")



# Estadistico de contraste:
    
t1=(abs(a1-73*10**(-6)))/(sa1*np.sqrt(len(D1)))
t2=(abs(a2-130*10**(-6)))/(sa2*np.sqrt(len(D2)))


print("t1",t1)
print("t2",t2)