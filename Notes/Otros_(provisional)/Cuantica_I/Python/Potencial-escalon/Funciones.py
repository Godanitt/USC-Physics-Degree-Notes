# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:51:00 2023

@author: danie
"""
import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
from math import e
import scipy.optimize as so
import sympy as symp
import scipy.special as scipy
import scipy.constants as cte
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

plt.figure()

# Potencial escalon

ax1=plt.subplot(2,1,1)
m=3
num=3
E0=1*cte.e
E=0.5*cte.e

x1=np.linspace(-5,0,num)
y1=num*[0]
ax1.plot(x1,y1,color="green")


x2=np.linspace(0,0,num)
y2=np.linspace(0,E0/cte.e,num)
ax1.plot(x2,y2,"green")

x3=np.linspace(0,5,num)
y3=num*[E0/cte.e]
ax1.plot(x3,y3,"green",label="$E_0$")

x4=np.linspace(-5,5,num)
y4=np.linspace(E/cte.e,E/cte.e,num)
ax1.plot(x4,y4,color="darkgreen",linestyle="--",label="$E$")

plt.legend()


ax1.set_xlabel('$x$')
ax1.set_ylabel('$E \ (eV)$')
ax1.grid("True")
ax1.set_xlim(-m,m)
ax1.set_ylim(-0.25,1.25)


ax1.plot()

# Funciones de onda

ax2=plt.subplot(2,1,2)
k1=10**(-9)*np.sqrt(2*cte.m_e*E)/cte.hbar
k2=10**(-9)*np.sqrt(2*cte.m_e*abs(E0-E))/cte.hbar


x1=np.linspace(-5,0,100)
y1=1*np.cos(k1*x1)+np.cos(k1*x1+np.pi/2)
ax2.plot(x1,y1,"blue",label="$\Psi_1$")



x3=np.linspace(0,5,100)
y3=1*np.exp(-k2*x3)
ax2.plot(x3,y3,"red",label="$\Psi_2$")

ax2.set_xlabel('$x \ (nm)$')
ax2.set_ylabel('$\Psi (x)$')
ax2.grid("True")
ax2.set_xlim(-m,m)
ax2.set_ylim(-1.75,1.75)

plt.legend(loc='upper right')



plt.savefig("Potencial-escalon1.pdf")

# Ahora hacemos el caso para E>E0


plt.figure()


ax1=plt.subplot(2,1,1)
m=3
num=3
E0=1*cte.e
E=1.5*cte.e

x1=np.linspace(-5,0,num)
y1=num*[0]
ax1.plot(x1,y1,color="green")


x2=np.linspace(0,0,num)
y2=np.linspace(0,E0/cte.e,num)
ax1.plot(x2,y2,"green")

x3=np.linspace(0,5,num)
y3=num*[E0/cte.e]
ax1.plot(x3,y3,"green",label="$E_0$")

x4=np.linspace(-5,5,num)
y4=np.linspace(E/cte.e,E/cte.e,num)
ax1.plot(x4,y4,color="darkgreen",linestyle="--",label="$E$")

plt.legend()


ax1.set_xlabel('$x$')
ax1.set_ylabel('$E \ (eV)$')
ax1.grid("True")
ax1.set_xlim(-m,m)
ax1.set_ylim(-0.25,E/cte.e+0.25)


ax1.plot()

# Funciones de onda

ax2=plt.subplot(2,1,2)
k1=10**(-9)*np.sqrt(2*cte.m_e*E)/cte.hbar
k2=10**(-9)*np.sqrt(2*cte.m_e*abs(E0-E))/cte.hbar

A=1
B=(k1-k2)/(k1+k2)*A
C=(2*k1)/(k1+k2)*A


x1=np.linspace(-5,0,100)
y1=A*np.cos(k1*x1)+B*np.cos(k1*x1)
ax2.plot(x1,y1,"blue",label="$\Psi_1$")


x3=np.linspace(0,5,100)
y3=C*np.cos(k2*x3)
ax2.plot(x3,y3,"red",label="$\Psi_2$")

ax2.set_xlabel('$x \ (nm)$')
ax2.set_ylabel('$\Psi (x)$')
ax2.grid("True")
ax2.set_xlim(-m,m)
ax2.set_ylim(-1.75,1.75)

plt.legend(loc='upper right')

# Vamos a hacer la barrera del potencial


plt.figure()

a=1

ax1=plt.subplot(1,1,1)
m=3
num=3
E0=1*cte.e
E=1.5*cte.e

x1=np.linspace(-a,0,num)
y1=num*[0]
ax1.plot(x1,y1,color="green")


x2=np.linspace(0,0,num)
y2=np.linspace(0,E0/cte.e,num)
ax1.plot(x2,y2,"green")

x3=np.linspace(0,a,num)
y3=num*[E0/cte.e]
ax1.plot(x3,y3,"green",label="$E_0$")



x4=np.linspace(a,a,num)
y4=np.linspace(0,E0/cte.e,num)
ax1.plot(x4,y4,"green")

x5=np.linspace(a,2*a,num)
y5=num*[0]
ax1.plot(x5,y5,"green")

"""
x6=np.linspace(-5,5,num)
y6=np.linspace(E/cte.e,E/cte.e,num)
ax1.plot(x6,y6,color="darkgreen",linestyle="--",label="$E$")
"""

plt.legend()


ax1.set_xlabel('$x \ (a)$')
ax1.set_ylabel('$E \ (eV)$')
ax1.grid(False)
ax1.set_xlim(-a,2*a)
ax1.set_ylim(-0.2,E0/cte.e+1)
"""
xstick=7*[0]
xlabels=7*[0]
for i in range(7):
    xstick[i]=-a+a/2*i
    if type(xstick[i])==int:
        xlabels[i]="$%.1f a$"%(xstick[i]/a)
    if type(xstick[i])==float:
        xlabels[i]="$%.1f \cdot a$"%(xstick[i]/a)

plt.xticks(ticks=xstick,labels=xlabels)
"""
plt.savefig("Barrera-potencial.pdf")

# Vamos a hacer las graficas del ejercicio 9 del tema III


f, (ax1, ax2) = plt.subplots(2, 1, figsize=(12.00787402,9.5))

m=25
num=3
E0=1*cte.e
E=1.376*cte.e
a = 10


x1=np.linspace(-31,-a,num)
y1=num*[0]
ax1.plot(x1,y1,color="green",linewidth=3)


x2=np.linspace(-a,-a,num)
y2=np.linspace(0,E0/cte.e,num)
ax1.plot(x2,y2,"green",linewidth=3)

x3=np.linspace(-a,0,num)
y3=num*[E0/cte.e]
ax1.plot(x3,y3,"green",label="$E_0$",linewidth=3)

x4=np.linspace(-100,100,num)
y4=np.linspace(E/cte.e,E/cte.e,num)
ax1.plot(x4,y4,color="darkgreen",linestyle="--",label="$E$",linewidth=3)


x5=np.linspace(0,0,num)
y5=np.linspace(E0/cte.e,5,num)
ax1.plot(x5,y5,"green",linewidth=3)

ax1.legend()


ax1.set_xlabel('$x$')
ax1.set_ylabel('$E \ (eV)$')
ax1.grid("True")
ax1.set_xlim(-m,m-m/1.1)
ax1.set_ylim(-0.25,E/cte.e+0.25)




k1=10**(-10)*np.sqrt(2*cte.m_e*E)/cte.hbar
k2=10**(-10)*np.sqrt(2*cte.m_e*abs(E0-E))/cte.hbar
k=k1

A=1
B=1
C=k**2/((k2*np.cos(k2*a))**2+(k*np.sin(k2*a))**2)*A

x=np.linspace(-31,-a,100)
y1=(1-np.cos(2*k*(x+a)))**2+(np.sin(2*k*(x+a)))**2
#y1=(np.cos(k1*x)+np.cos(k1*x)*np.cos(-2*k*a)-np.sin(k*x)*np.sin(-2*k*a))**2+(np.sin(k*x)-np.sin(k*x)*np.sin(-2*k*a)-np.cos(2*k*a)*np.sin(k*x))**2
ax2.plot(x,y1,"blue",label="$\Psi_1$",linewidth=3)


x3=np.linspace(-a,0,100)
y3=4*C*(np.sin(k2*x3))**2
ax2.plot(x3,y3,"red",label="$\Psi_2$",linewidth=3)


x3=np.linspace(0,20,100)
y3=np.array(100*[0])
ax2.plot(x3,y3,"green",label="$\Psi_3$",linewidth=3)



ax2.set_xlabel('$x \ (\AA) $' )
ax2.set_ylabel('$|\Psi|^2 (x)$')
ax2.grid("True")
ax2.set_xlim(-m,m-m/1.1)
ax2.set_ylim(-0.25,20)


plt.legend(loc='upper right')


plt.savefig("Ej9-T3.pdf")