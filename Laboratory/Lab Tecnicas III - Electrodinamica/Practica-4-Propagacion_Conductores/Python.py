# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 16:58:22 2023

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

###############################################################################
################################### DATOS #####################################
###############################################################################

fe= np.array([50,70,100,150,200,300,500,700,1000,1500,2000,3000,5000,7000,10000
,12000,13000,13500,14000,15000,20000,30000,40000,49700,50000,70000,100000,150000,200000])

V2 = np.array([10.50,13.60,19.20,28.40,36.80,49.80,80.00,96.00,110.20,121.60,127.00
,130.00,130.00,128.00,124.00,120.00,118.00,118.00,116.00,113.00,100.00,74.40,55.30
,40.00,40.00,23.20,11.00,4.70,1.78])

V1 = np.array([10.10,13.10,17.20,25.20,32.80,44.40,68.00,82.00,94.40,105.40,111.20,
124.00,140.00,156.00,182.00,204.00,212.00,216.00,232.00,240.00,268.00,326.00,344.00,
350.00,350.00,340.00,320.00,288.00,270.00])

phi = np.array([1.70,2.00,2.50,3.60,4.10,5.20,6.50,7.50,9.10,13.20,20.00,31.00,
46.50,58.00,74.00,84.50,88.00,90.00,92.00,96.00,109.00,137.00,160.00,180.00,181.00,
210.00,252.00,305.00,340.00,])

rad = phi*2*np.pi/360

N2 = 200
N1 = 100
N0 = 100
R2= 7.5*0.001
R1 =12.5*0.001
d = 0.001
E=(V2/V1)*((N1*R1)/(N2*R2))

sigmat=5.1*10**(7)

fase = E*np.cos(rad)
cuadratura = E*np.sin(rad)

###############################################################################
################################## TABLAS #####################################
###############################################################################

outfile=open("datosexperimentales1.txt", 'w')
outfile.write(" \\hline \ $f$ (Hz) &  $V_1$ (mV) & $V_2$ (mV)  & $\phi$ (º)  &  $ |E_2/E_1|$ & $\mathcal{F}$ (mV) & $\mathcal{C}$ (mV)  \\\ \hline \n")
for i in range(len(fe)):
    outfile.write("%d  \t & %.1f \t & %.1f \t & %.1f   & %.3f \t & %.3f \t & %.3f \t \\\ \n "%(fe[i],V1[i],V2[i],phi[i],E[i],fase[i],cuadratura[i]))
outfile.write("\\hline")    
outfile.close()

outfile=open("datosexperimentales2.txt", 'w')
outfile.write(" \\hline \ $f$ (Hz) &  $ |E_2/E_1|$ & $\mathcal{F}$ (mV) & $\mathcal{C}$ (mV)  \\\ \hline \n")
for i in range(len(fe)):
    outfile.write("%d  \t & %.3f \t & %.3f \t & %.3f \t \\\ \n "%(fe[i],E[i],fase[i],cuadratura[i]))
outfile.write("\\hline")    
outfile.close()

###############################################################################
############################### DATOS TEORICOS ################################
###############################################################################


# arcotangente(x):
#    f=0
#    for i in range(1):
#        f += (((-1)**i)*(x**(2*i+1)))/(2*i+1)
#    return f

ft = np.linspace(min(fe), max(fe),10000)
omegat = ft*2*np.pi

beta = np.sqrt((cte.mu_0)*sigmat*omegat/2)

Et = np.sqrt(1/((np.cos(beta*d)*np.cosh(beta*d))**2+(np.sin(beta*d)*np.sinh(beta*d))**2))

phit = np.arctan((np.sin(beta*d)*np.sinh(beta*d))/(np.cos(beta*d)*np.cosh(beta*d)))

phitg = phit*360/(2*np.pi)


print(phitg)

flag = False
flag2= False
for i in range(len(phitg)):
    if(phitg[i]<0):
        flag = True
    if(flag):
        phit[i]=((phit[i]))+np.pi
        phitg[i]=((phitg[i]))+180
    if i>2:
        if(phitg[i]-phitg[i-1]<0):
            flag2=True
    if(flag2):
        phit[i]=((phit[i]))+np.pi
        phitg[i]=((phitg[i]))+180
        
        
plt.plot(phitg,np.cos(phit),".",color="blue")
plt.plot(phi,np.cos(rad),".",color="red")

#phit = arcotangente((np.sin(beta*d)*np.sinh(beta*d))/(np.cos(beta*d)*np.cosh(beta*d)))
cuat  = Et*np.sin(phit)
faset = Et*np.cos(phit)

# Calculamos las conductividades originailes

fsigma=np.array([13500,49700])
nsigma=np.array([1,2])
def sigma(f,n):
    sigma = (np.pi**2*n**2)/(2*(2*np.pi*f)*cte.mu_0*d**2)
    sigma = sigma/(10**7)
    return sigma

sigmaexp=sigma(fsigma,nsigma)


outfile=open("datosexperimentales3.txt", 'w')
outfile.write(" \\hline \ $n &  $f$ \ (Hz) & $\sigma$ (S/m)   \\\ \hline \n")
for i in range(len(sigmaexp)):
    outfile.write("%d  \t & %d \t & $ %.2f \cdot 10^7 $ \t \\\ \n "%(nsigma[i],fsigma[i],sigmaexp[i]))
outfile.write("\\hline")    
outfile.close()


# Calculamos beta a martir de la sigma experimental media



# Comparacion de la fase/cuadratura para las frecuencias:
    
F=np.array([0,-0.076])
C=np.array([0.364,-0.001])

def FoC(nsgima):
    beta=(nsigma*np.pi/2)/d
    F = np.sqrt(1/((np.cos(beta*d)*np.cosh(beta*d))**2+(np.sin(beta*d)*np.sinh(beta*d))**2))
    return F

Esigma=FoC(nsigma)

Fteorico=np.array([0,-Esigma[1]])
Cteorico=np.array([Esigma[0],0])

outfile=open("datosexperimentales4.txt", 'w')
outfile.write(" \\hline \ $n$ &  $f$ \ (Hz) &  $\mathcal{F}_{exp}$ &  $\mathcal{F}_{teo}$  & $\mathcal{C}_{exp}t$  &  $\mathcal{C}_{teo}$ \\\ \hline \n")
for i in range(len(sigmaexp)):
    outfile.write("%d  \t & %d \t & %.3f & %.3f & %.3f & %.3f \t \\\ \n "%(nsigma[i],fsigma[i],F[i],Fteorico[i],C[i],Cteorico[i]))
outfile.write("\\hline")    
outfile.close()

###############################################################################
################################## GRAFICOS ###################################
###############################################################################


f,  axs = plt.subplots(1, 1, figsize=(6,4))

axs.plot(fe,E,"+",color="green",label="$|E_2/E_1|$",markersize=7)
axs.plot(fe,cuadratura,"1",color="blue",label="$\\mathcal{C}$",markersize=7)
axs.plot(fe,fase,"2",color="red",label="$\\mathcal{F}$",markersize=7)
axs.set_xscale("log")
axs.set_xlabel("$f$ (Hz)")
axs.legend()
axs.grid(linestyle="--")

f.savefig("Figura-4.1.pdf")


f,  axs = plt.subplots(1, 1, figsize=(6,4))


axs.plot(ft,cuat,color="royalblue",label="$\\mathcal{C}_{teor}$")
axs.plot(ft,faset,color="tomato",label="$\\mathcal{F}_{teor}$")
axs.plot(fe,cuadratura,"1",color="blue",label="$\\mathcal{C}_{exp}$",markersize=7)
axs.plot(fe,fase,"2",color="red",label="$\\mathcal{F}_{exp}$",markersize=7)
axs.set_xscale("log")
axs.set_xlabel("$f$ (Hz)")
axs.legend()
axs.grid(linestyle="--")

f.savefig("Figura-4.2.pdf")
flag=True
j=0
while(flag):
    j+=1
    if fe[j]==1000:
        fe=fe[0:j+1]
        cuadratura=cuadratura[0:j+1]
        fase=fase[0:j+1]
        flag=False
        
        
ft = np.linspace(min(fe), max(fe),1000)
omegat = ft*2*np.pi
beta = np.sqrt((cte.mu_0)*sigmat*omegat/2)
Et = np.sqrt(1/((np.cos(beta*d)*np.cosh(beta*d))**2+(np.sin(beta*d)*np.sinh(beta*d))**2))
phit = np.arctan((np.sin(beta*d)*np.sinh(beta*d))/(np.cos(beta*d)*np.cosh(beta*d)))
phitg = phit*360/(2*np.pi)
cuat  = Et*np.sin(phit)
faset = Et*np.cos(phit)


f,  ax1 = plt.subplots(1, 1, figsize=(6,4))
ax1.plot(ft,faset,color="tomato",label="$\\mathcal{F}_{teor}$")
ax1.plot(fe,fase,"2",color="red",label="$\\mathcal{F}_{exp}$",markersize=7)
ax1.set_xscale("log")
ax1.set_xlabel("$f$ (Hz)")
ax1.set_ylim(0.8,1.05)
ax1.legend(loc="lower right")
f.savefig("Figura-4.3.1.pdf")

f,  ax2 = plt.subplots(1, 1, figsize=(6,4))
ax2.plot(ft,cuat,color="royalblue",label="$\\mathcal{C}_{teor}$")
ax2.plot(fe,cuadratura,"2",color="blue",label="$\\mathcal{C}_{exp}$",markersize=7)
ax2.set_xscale("log")
ax2.set_xlabel("$f$ (Hz)")
ax2.legend(loc="lower right")
f.savefig("Figura-4.3.2.pdf")

omegat = fe*2*np.pi
beta = np.sqrt((cte.mu_0)*sigmat*omegat/2)
Et = np.sqrt(1/((np.cos(beta*d)*np.cosh(beta*d))**2+(np.sin(beta*d)*np.sinh(beta*d))**2))
phit = np.arctan((np.sin(beta*d)*np.sinh(beta*d))/(np.cos(beta*d)*np.cosh(beta*d)))
phitg = phit*360/(2*np.pi)
cuat  = Et*np.sin(phit)
faset = Et*np.cos(phit)



outfile=open("datosexperimentales5.txt", 'w')
outfile.write(" \\hline \   $f$ \ (Hz) &  $\mathcal{F}_{exp}$ &  $\mathcal{F}_{teo}$  & $\mathcal{C}_{exp}t$  &  $\mathcal{C}_{teo}$ \\\ \hline \n")
for i in range(len(fe)):
    outfile.write(" %d \t & %.3f & %.3f & %.3f & %.3f \t \\\ \n "%(fe[i],fase[i],faset[i],cuadratura[i],cuat[i]))
outfile.write("\\hline")    
outfile.close()


plt.savefig("Figura-4.3.pdf")


# Ultima grafica

d1=0.7

long=2*d1
k=2*np.pi

d2=d1+long/2

x1 = np.linspace(0,d1,1000)
x2 = np.linspace(d1,d2,1000)
x3 = np.linspace(d2,d1*3,1000)

a0=1

y1 = np.sin(x1*k*2)
y2 = np.sin(x2*k*2)*(1-(x2-d1)**2)
y3 = np.sin(x3*k*2)*(1-(d2-d1)**2)

plt.figure(figsize=(6.5,4.3))
plt.plot(x1,y1,color="blue",label="Antes del condcutor")
plt.plot(x2,y2,color="green",label="En el condcutor")
plt.plot(x3,y3,color="red",label="Despues del condcutor")
plt.xticks([d1,d2],["$d_1$","$d_2$"])
plt.yticks([],[])
plt.legend()


plt.savefig("Figura-4.4.pdf")
