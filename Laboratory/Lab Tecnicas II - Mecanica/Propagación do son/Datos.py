# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 09:36:42 2022

@author: PC
""" 

"""

import numpy as np
import math as mth
import matplotlib.pyplot as plt
import pylab as py

distancia = np.linspace(3,60,20)
tiempo =  [2-0.2, 2-0.25, 2-0.3, 2-0.45, 2-0.5,2-0.6, 2-0.7,2-0.8, 2-0.9,2-0.95, 2-1.05, 2-1.15, 2-1.2, 2-1.3, 2-1.4, 2-1.5, 2-1.6, 2-1.7, 2-1.8, 2-1.9]

tiempos=[0]*20

for i in range(len(tiempo)):
    tiempos[i] = tiempo[len(tiempo)-i-1]
 [2-0.2, 2-0.25, 2-0.3, 2-0.45, 2-0.5,2-0.6, 2-0.7,2-0.8, 2-0.9,2-0.95, 2-1.05, 2-1.15, 2-1.2, 2-1.3, 2-1.4, 2-1.5, 2-1.6, 2-1.7, 2-1.8, 2-1.9]
plt.grid(True)
p = py.polyfit(tiempos, distancia,1)
h = py.polyval(p,tiempos)
plt.plot(tiempos,distancia, "r.")
plt.plot(tiempos,h)

"""
import sys
import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
from IPython.display import display, Latex
import pandas as pd
pd.set_option('precision', 2)

import modulo_1 as md











"""

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



y=np.array(np.linspace(3,60,20))

n=len(y)

tiempo =  [2-0.2, 2-0.25, 2-0.3, 2-0.45, 2-0.5,2-0.6, 2-0.7,2-0.8, 2-0.9,2-0.95, 2-1.05, 2-1.15, 2-1.2, 2-1.3, 2-1.4, 2-1.5, 2-1.6, 2-1.7, 2-1.8, 2-1.9]

x=[0]*20

for i in range(n):
    x[i] = tiempo[n-i-1]


sigy = 

x=np.array(x)
y=np.array(y)

datos = pd.DataFrame({'x': x, 'y': y},index=np.arange(n)+1)
display(datos)

cadena  = '\\begin{array}{|r|r|} \hline x & y \\\\ \hline'
for i in range(10):
    cadena += '%3.2f & %3.2f \\\\' % (x[i],y[i])
cadena += '\hline \end{array}'

display(Latex(cadena))

ymed=media(y)
display(Latex(r'$ \bar{y} =%i $' % ymed))


sigbar=sigmab(y)
display(Latex(r'$\sigma(\bar y)=%i $' % sigbar))

sigi=np.sqrt(y)

uy=np.array([0.2]*len(y))

datossig = pd.DataFrame({'x': x,'y': y ,'sig': uy},index=np.arange(n)+1)
display(datossig)

a,b,siga,sigb,r = ajustelinealponderado(x,y,uy)

display(Latex('$a$=%3.2f , $\sigma_{a}$=%3.2f' % (a,siga) ))
display(Latex('$b$=%3.2f , $\sigma_{b}$=%3.2f' % (b,sigb) ))


outfile=open("datos1.txt", 'w')
outfile.write(" a \t & s(a) \t & b \t & s(b) \t & r \\\ \n")
outfile.write("%f \t & %2f \t & %f \t & %2f \t & %f"%(a,siga,b,sigb,r))
outfile.close()

#___________________________________________________________________________________________________#

Y= a + b*x


plt.figure(figsize=(7,6))
plt.plot(x,y, '.')
plt.plot(x,Y)
plt.grid()
plt.show()

plt.figure(figsize=(7,6))

plt.grid(True)
plt.errorbar(x, y, fmt= '.', yerr=uy, label=("f = 65,7 hz"))
plt.xlabel("t (ms)")
plt.ylabel("l (cm)")
plt.xlim(0, max(x)*1.1)
plt.ylim(-5, max(y)*1.1)
x[0]=0
Y= a + b*x
plt.plot(x,Y)

plt.savefig("regresiónlineal.png")

#-------------------Parte 2 --------------------Parte 2-------------------Parte 2------------------#

#Ahora vamos a calcular las frecuencias de onda:

#semiabierto

T = np.array([2.7*2*10**-3,1.2*0.002,2.8*0.0005,2*0.0005,1.6*0.0005])
sT  =np.array([0.4,0.4,0.1,0.1,0.1])

n=len(T)

v = b*10
sigv = sigb*10

def function(T,sT,v,sigv,n):
    sigT = np.zeros([5])
    
    for i in range(len(T)):
        sigT[i]=sT[i]*10**-3

    f = np.zeros([5])

    for i in range(len(T)):
        f[i] = T[i]**(-1)

    sigf = np.zeros([n])

    for i in range(n):
        sigf[i]=(sigT[i]/T[i]**2)
    
    lamb=np.zeros([n])
    siglamb=np.zeros([n])

    for i in range(n):
        lamb[i] = v/f[i]

    for i in range(n):
        siglamb[i] = np.sqrt((sigv/f[i])**2+(v*sigf[i]/f[i]**2)**2)
        
    return(f,sigf,lamb,siglamb)

f,sigf,lamb,siglamb = function(T,sT, v, sigv,n)

outfile=open("datos2.txt", 'w')
outfile.write("\\hline \n")
outfile.write(" modo \t & $f_i \ (Hz)$ \t &  $s(f_i) \ (Hz) $ \t & $\lambda_i \(m)$ \t & $s(\lambda_i) \ (m) $  \\\ \\hline \n")
for i in range(n):
     outfile.write("%d \t & %f \t & %f \t & %f \t & %f  \\\ \n "%(i+1,f[i],sigf[i],lamb[i],siglamb[i]))
outfile.close()

#abierto

T1=np.array([4.6*10**-3,2.5*10**-3, 1.6*10**-3, 1.2*10**-3,0.95*10**-3])
sT1=np.array([0.2,0.1,0.1,0.1,0.1])

f1,sigf1,lamb1,siglamb1 = function(T1,sT1, v, sigv,n)

outfile=open("datos3.txt", 'w')
outfile.write("\\hline \n")
outfile.write(" modo \t & $f_i \ (Hz)$ \t &  $s(f_i) \ (Hz) $ \t & $\lambda_i \(m)$ \t & $s(\lambda_i) \ (m) $  \\\ \\hline \n")
for i in range(n):
     outfile.write("%d \t & %f \t & %f \t & %f \t & %f  \\\ \n "%(i+1,f1[i],sigf1[i],lamb1[i],siglamb1[i]))
outfile.close()

#funciones

def funcion(lambn,L,n):
    fun=np.zeros([5])
    for i in range(n):
        fun[i]=(L*4/lambn[i])
    return(fun)

#semiabierto


fun=funcion(lamb,0.6,n)


outfile=open("datos4.txt", 'w')
outfile.write("\hline  \n $f_1$ \t & $f_2$ \t & $f_3$ \t & $f_4$ \t & $f_5$ \\\ \hline \n")
outfile.write("%f \t & %f \t & %f \t & %f \t & %f \t  t \n \\hline "%(fun[0],fun[1],fun[2],fun[3],fun[4]))
outfile.close()

#abierto

fun1=funcion(lamb1,0.8,n)


outfile=open("datos5.txt", 'w')
outfile.write("\hline  \n $f_1$ \t & $f_2$ \t & $f_3$ \t & $f_4$ \t & $f_5$ \\\ \hline \n")
outfile.write("%f \t & %f \t & %f \t & %f \t & %f \t  \n \\hline "%(fun1[0],fun1[1],fun1[2],fun1[3],fun1[4]))
outfile.close()

"""
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#+++++++++++++++++++++++++++++++++++++++ GIROSCOPIO +++++++++++++++++++++++++++++++++++++++++++++++++#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# -- PARTE 2 --------------------------------------------------------------------------------------------------
"""
sigw=0.4
sigT=0.25       

#Serie1:

w1=[12.3,11.1,19.1,14.6,10.9]
T1=[14.8,13.1,21.4,17.22,12.99] 

#Serie2:

w2=[20.3,13.5,25.1,19.8,16.8]
T2=[24.08,15.65,28.43,23.51,19.00]   
    
#Serie3: 

w3=[26.2,22.2,17.9,13.9,13.4]
T3=[30.46,24.83,20.89,17.41,17.05]


n=len(T1)
f1=np.zeros([5])
f2=np.zeros([5])
f3=np.zeros([5])

for i in range(n):
    f1[i]=T1[i]**(-1)
    f2[i]=T1[i]**(-1)
    f3[i]=T1[i]**(-1)

sigf1=np.zeros([5])
sigf2=np.zeros([5])
sigf3=np.zeros([5])

for i in range(n):
    sigf1[i]=sigT/f1[i]
    sigf2[i]=sigT/f2[i]
    sigf3[i]=sigT/f3[i]
    

outfile=open("datos1.txt", 'w')
outfile.write("\hline $ w_1 $ \t $ w_2 $ \t & $w_3$ \t & $f_1$ \t & $s(f_1)$ \t & $f_2$ \t & $s(f_2)$ \t & f_3 \t &  s(f_3) \\\ \hline \n")
for i in range(n):
    outfile.write("%f \t & %f \t & %f \t & %f \t & %f \t & %f \t & %f \t & %f \t & %f \n "%(w1[i],w2[i],w3[i],f1[i],sigf1[i],f2[i],sigf2[i], f3[i], sigf3[i]))
outfile.close()

# -- PARTE 3 -----------------------------------------------------------------------------------------

#Serie1:
    
sigw=0.4    
sigt=0.25
nut=4
    
t1=[2.86,3.22,3.08,5.10]
w11=[21.8,17.5,13.9,9.45]
w12=[21.3,17.2,13.2,9.20]    

#Serie2:

t2=[2.73,2.24,2.56]
w21=[17.1,21.0,19.0,16.3,14.0]
w22=[16.9, 20.8,18.8,16.1,13.8]
    
#Serie3:
    
t3=[2.61,3.51,3.72,2.34,5.73]
w31=[20.3,15.2,14.10,23.7,10.9]
w32=[20.0,14.9,13.7,23.4,10.6]

# -- PARTE 4 -----------------------------------------------------------------------------------------

# Calculo de la aceleración:

sigr=0.02
sigm1=1
sigh=0.2
sigt=0.25

m1=60
r=2.5

h=[94.8,63.5,50.2,32.7,108.0]
t=[7.69, 5.86,5.26,3.88,7.94]

#Calculo de la constante k:

sigm2=99
sigT10=4.37

T10=4.37

#Calculo del primer momento de inercia I1 e I2



#Calculo del segundo momento de inercia I3

sigT10=0.25
T10=[8.81,8.49,8.58,8.27,9.04] 

"""
