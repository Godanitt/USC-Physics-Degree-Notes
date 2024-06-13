# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:40:42 2022

@author: PC
"""
"""
import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
from IPython.display import display, Latex
import pandas as pd

"""


import numpy as np
from numpy.linalg import *
from matplotlib import *
from matplotlib import pyplot as plt
from IPython.display import display, Latex
import pandas as pd
pd.set_option('precision', 2)

# -- --- --- -- -- --- -- -- - -- - - - - - -- -- - -- - -


def media(xlist):
    return sum(xlist)/len(xlist)

def sigma(xlist):
    return np.sqrt(sum((xlist-media(xlist))**2)/(1.*len(xlist)*(len(xlist)-1.)))

def sigmab(xlist):
    return np.sqrt(sum((xlist-media(xlist))**2)/(1.*len(xlist)*(len(xlist)-1)))

def utotal(ua,ub):
    return np.sqrt(ua**2+ub**2)

#ajuste lineal y=a+bx
def ajustelinealponderado(x,y,sig): # Aquí metemos los dos valores y el peso estadístico (sig)

    H=np.array([[sum(1./sig**2),sum(x/sig**2)],[sum(x/sig**2),sum(x**2/sig**2)]])
    Delta=det(H)
    Z=np.array([sum(y/sig**2),sum((x*y)/sig**2)])
    
    ([a,b])=np.matmul(inv(H),Z)
    
    siga=np.sqrt(sum(x**2/sig**2)/Delta)
    sigb=np.sqrt(sum(1./sig**2)/Delta)
    
    r = np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))
    
    return a,b,siga,sigb,r

def ajustelineal(x,y):
    HX=len(x)*(np.dot(x,x))-sum(x)**2
    HY=len(y)*(np.dot(y,y))-sum(y)**2
    a = (sum(y)*sum(x**2)-sum(x)*sum(x*y))/(HX)
    b = (len(x)*sum(x*y)-sum(x)*sum(y))/(HX)
    s=np.sqrt(sum((y-a-b*x)**2)/(len(x)-2))
    siga=s*np.sqrt((sum(x**2))/HX)
    sigb=s*np.sqrt(len(x)/HX)
    r=(len(x)*sum(x*y)-sum(x)*sum(y))/(np.sqrt(HX*HY))
    return a,b,siga,sigb,r

def mediaponderada(u,sigu):
    w=np.zeros([len(sigu)])
    for i in range(len(sigu)):
        w[i]=1/sigu[i]**2
    k=sum(w)
    media=np.dot(u,w)/k
    s = 1/np.sqrt(k)
    return media, s

def incertidumbretipoA(u,medu):
    siga=np.ones([len(u)])
    for i in range(len(u)):
        siga[i] = np.sqrt(((np.dot(u[i],u[i])/len(u[i]))-np.dot(medu[i],medu[i]))/(len(u)-1))
    return siga

# -- OSCILADOR AMORTIGUADADO ------------------------------------------------------------------------ #

I=np.array([0,0.3,0.6,0.9,1.1])
sigI=0.02
sigT=0.25
sI = np.ones([5])*sigI

sigT=0.25
T00 = [48.63,48.64]
n00 = 25
T03 = [38.95,38.75]
n03 = 20
T06 = [9.67,9.84,9.75,9.66]
n06 = 5
T09 = [5.66,5.74,5.78]
n09 = 3
T11 = [3.16,2.94,3.02,3.11]
n11 = 1.5

T = np.array([T00, T03, T06, T09, T11], dtype=object) 
n = np.array([n00,n03,n06,n09,n11])
n0 = np.array([3,2,1,0.5,0.5])

TM=np.ones([len(n)]) 
sTM=np.ones([len(n)]) 

for i in range(len(n)):
    TM[i] = media(T[i])
    
sigTA = incertidumbretipoA(T,TM)

for i in range(len(n)):
    sTM[i] = np.sqrt(sigT**2 + ((sigTA[i]) / np.sqrt(n[i]))**2)

sigA = 0.2
A11=np.array([[-19.0,4.2,-3.2, -0.8, -1.6],[-19.0,4.6,-3.5, -0.8, -1.6],[-19.0,4.6,-3.6, -0.6, -1.6]])
A09=np.array([[-19,8.2,-7.2,1.8,-3.1],[-19,8.2,-7.2,1.9,-3.2]])
A06=np.array([[-19,-12.2,8,-5.6,-4,-2.9,-2.4,-2],[-19,-12.1,8,-5.4,-3.9,-3,-2.4,-2]])
A03=np.array([[-19,-15,-11.8,-9.4,-7.6,-6,-4.9,-4]])
A00=np.array([[-19,-18.4,-17.4,-17,-16.2,-15.6,-14.8,-14,-13.4,-12.8]])
m=np.array([3,2,1,0.5,0.5])

A = np.array([A00,A03,A06,A09,A11], dtype=object)

AM =np.ones([len(A)])
AM = np.array(AM, dtype=object)

for i in range(len(A)):
    for j in range(len(A[i])):
        z = np.ones([len(A[i])])
        p = 0
        l = A[i]
        q = np.array([])
        print(l)
        for k in range(len(l[j])):
            z=l[0:len(l),k]
            p=media(z)
            print(p)
            q=np.append(q,p)
            AM[i]=q

#Calculamos los valores de y

for i in range(len(AM)):
    AM[i]+= 1.4

div = np.ones([len(AM)])
div = np.array(div,dtype=object)
for i in range(len(AM)):
    k=abs(19-1.4)/AM[i]
    print("k=",k)
    div[i]=np.log(abs(k))

    
#Calculamos los valores de sigy
    

sdiv = np.ones([len(AM)])
sdiv = np.array(div,dtype=object)
for i in range(len(sdiv)):
    k=np.ones([len(AM[i])])
    for j in range(len(AM[i])):
        k[j]=sigA/(np.sqrt(abs(AM[i][j])))
    print("sk= ", k)
    sdiv[i] = k
    
#Calculamos los valores de x

t = np.ones([len(TM)])
t = np.array(t,dtype=object) 
for i in range(len(T)):
    print(TM[i]/n[i])
    t[i] = (TM[i]/n[i])


tm = np.ones([len(AM)]) * 0
tm = np.array(tm,dtype=object)
k = 0
for i in range(len(t)):
    q = np.ones([len(AM[i])])
    for j in range(len(AM[i])):
        q[j]=k*t[i]*m[i]
        k+=1
    tm[i]=q
    k = 0
    

#Preparamos regresiones lineales para calclar gamma

ai = np.ones([len(AM)])
ai = np.array(ai,dtype=object)
bi = np.ones([len(AM)])
bi = np.array(bi,dtype=object)
ri = np.ones([len(AM)])
ri = np.array(ri, dtype=object)

sai = np.ones([len(AM)])
sai = np.array(sai,dtype=object)
sbi = np.ones([len(AM)])
sbi = np.array(sbi,dtype=object)
    
#Calculo de regresiones lineales

yi = div 
xi = tm
sy = sdiv

for i in range(len(xi)):
    print("valores regresión", ajustelinealponderado(xi[i],yi[i],sy[i]))
    ai[i],sai[i],bi[i],sbi[i],ri[i]=ajustelinealponderado(xi[i], yi[i], sy[i])
  
    
#Calculo de plots

plt.show()
plt.
plt.plot([0,1,2],[0,1,2],"r")

"""
plot(list(tm[1]),list(AM[1]),"b")

for i in range(len(I)):
    figure()
    plot(tm[i],AM[i],".r")
    
    p = np.array([])
    x = np.linspace(0, max(t[i]),100)
    y = np.ones([len(x)])
    y = np.array(y,dtype=object)
    for j in range(len(tm[i])):
        p = np.append(p, np.exp(bi[i]*x))
    y[i]=p
    plot(x,y)
"""    

# -- OSCILADOR AMORTIGUADO Y AMORTECIDO ----------------------------------------


sigT = 0.25
sigA = 0.2

T51 = np.array([[46.43*5/3,77.95],[25.08,25.16],[15.7,15.26],[10.92,11.01],[8.68,8,65],[7.06,7.08],[11.86,11.87],[10.53,10.56],[9.85,9.89],[9.51,9.36],[9.76,9.74],[9.64,9.59]], dtype=object)
f1 = np.ones([len(T51)])
for i in range(len(T51)):
    print(media(T51[i]))
    f1[i] = (media(T51[i])/5)**(-1)

A1 = np.array([[-0.8,-1.7],[-1.7,-0.7],[-0.5,-2],[0.8,-3.3],[0.2,-2.2],[-1.7,-0.7],[0.2,-2.6],[-5.7,3.2],[-10,7.4],[6.3,3.8],[-11,8.4],[-9.1,6.6]])

AM1 = np.ones([len(A1)])

for i in range(len(A1)):
    AM1[i] = (abs(A1[i,1])+abs(A1[i,0]))/2



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


T52 = np.array([46.07,21.48,13.40,11.1,10.24,9.29,9.13,7.06,10.05,9.85])

A2 = np.array([[-1.6,-0.7],[-2.2,-0.4],[-2.8,0.4],[-3.8,1.4],[1.4,-3.8],[-3.2,0.6],[1.7,-0.8],[-4.1,1.6],[-4.2,1.7]],dtype=object)

f2 = np.ones([len(T52)])
for i in range(len(T52)):
    f2[i] = ((T52[i])/5)**(-1)

AM2 = np.ones([len(A2)])

for i in range(len(A2)):
    AM2[i] = (abs(A2[i,1])+abs(A2[i,0]))/2



"""
for i in range(len(A)):
    k = 0
    for j in range(len(A[i])):
        for z in range(len(A[i][j]))


sigAA = incertidumbretipoA(A,AM)
sAM = np.zeros([len(A)])

for i in range(len(n)):
    sAM[i] = np.sqrt(sigA**2 + ((sigTA[i]) / np.sqrt(n[i]))**2)
    """