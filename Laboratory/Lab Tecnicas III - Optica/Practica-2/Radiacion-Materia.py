# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 16:26:41 2024

@author: danie
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tabulate import tabulate

def incertidumbre(x):
    sx=np.sqrt(sum((x-(np.average(x)))**2)/((len(x)-1)*len(x)))
    return sx

def incertidumbrepropagada(sx,sy):
    sz = np.sqrt(sx**2+sy**2)
    return sz

def incertidumbrepropagadan(s):
    for i in range(len(s)):
        b=sum((s/len(s))**2)
    a=np.sqrt(b)
    return a

def concatenarbueno(lista):
    a=np.zeros([len(lista[0]),len(lista)])
    for i in range(len(lista)):
        for j in range(len(lista[0])):
            a[j,i]=lista[i][j]
    return a

# Ahora la practica

def n(gamma,alpha,salpha,sgamma):
    sa=salpha*np.pi/180
    sg=sgamma*np.pi/180
    gammam=np.average(gamma)
    alpham=np.average(alpha)
    seno1=np.sin(((gammam+alpham)/2)*(np.pi/180))
    cseno1=np.cos(((gammam+alpham)/2)*(np.pi/180))
    seno2=np.sin(((alpham)/2)*(np.pi/180))
    cseno2=np.cos(((alpham)/2)*(np.pi/180))
    n = (np.sin(((gamma+alpha)/2)*(np.pi/180)))/(np.sin((alpha/2)*(np.pi/180)))
    sn=np.sqrt((sa*(cseno1/seno2+seno1*cseno2/seno2**2))**2+(sg*(cseno1/seno2))**2)*(np.pi/(180*2))
    print(sn)
    sn=incertidumbrepropagada(sn, incertidumbre(n))
    n = np.average(n)
    return abs(n),sn

def phi(beta1,beta1min,beta2,beta2min):
    phi=360-abs(beta2-beta1)
    phimin=beta2min-beta1min
    phif=phi+phimin/60
    phig=phif//1
    phimin=60*(phif-phig)
    
    return np.array([phig,phimin])

beta1=np.array([20,21,23,21,22])
beta1min=np.array([40,9,10,34,54.5])
beta2=np.array([260,261,263,261,263])
beta2min=np.array([48,34,0,50,5])

sang=1/60

beta1=beta1+beta1min/60
beta2=beta2+beta2min/60
phia=360-beta1-beta2

alpha=np.average(phia)
salpha=incertidumbrepropagada(incertidumbre(phia),incertidumbrepropagadan(np.array([sang]*4)))

#print("\\alpha = %d º %d ' \\quad s(\\alpha) = %d ' "%(alpha//1,(alpha-alpha//1)*60,salpha*60))
print("\\alpha = %.2f^o \\quad s(\\alpha) = %.2f^o"%(alpha,salpha))

cero=np.array([320,320,320,320,320])
ceromin=np.array([0.5,43,40,42,37])
amarillo=np.array([26,26,26,26,26])
amarillomin=np.array([46,45,50,46,44])
rojo=np.array([26,26,26,26,26])
rojomin=np.array([21,20,20,18,15])
verde=np.array([27,27,27,27,27])
verdemin=np.array([10,10,20,15,9])
azul=np.array([29,29,29,29,29])
azulmin=np.array([5,12,13,10,9])


phiamarillo,phiamarillomin=phi(cero,ceromin,amarillo,amarillomin)
phiamarillo=(phiamarillo+phiamarillomin/60)
samarillo=incertidumbrepropagada(incertidumbre(phiamarillo),sang)
namarillo,snamarillo=n(phiamarillo,alpha,salpha,samarillo)


phiazul,phiazulmin=phi(cero,ceromin,azul,azulmin)
phiazul=(phiazul+phiazulmin/60)
sazul=incertidumbrepropagada(incertidumbre(phiazul),sang)
nazul,snazul=n(phiazul,alpha,salpha,sazul)


phiverde,phiverdemin=phi(cero,ceromin,verde,verdemin)
phiverde=(phiverde+phiverdemin/60)
sverde=incertidumbrepropagada(incertidumbre(phiverde),sang)
nverde,snverde=n(phiverde,alpha,salpha,sverde)


phirojo,phirojomin=phi(cero,ceromin,rojo,rojomin)
phirojo=(phirojo+phirojomin/60)
srojo=incertidumbrepropagada(incertidumbre(phirojo),sang)
nrojo,snrojo=n(phirojo,alpha,salpha,srojo)

lrojo=625
lamarillo=590
lverde=570
lazul=500

plt.figure(facecolor=(1,1,1))
plt.style.use("default")
plt.plot([lrojo],[nrojo],".",color="red",markersize=20,markeredgecolor='black')
plt.plot([lazul],[nazul],".",color="blue",markersize=20,markeredgecolor='black')
plt.plot([lverde],[nverde],".",color="green",markersize=20,markeredgecolor='black')
plt.plot([lamarillo],[namarillo],".",color="yellow",markersize=20,markeredgecolor='black')
plt.xlabel("$\lambda$ (nm)")
plt.ylabel("$n$")
plt.xlim(490,640)
plt.savefig("Indices.pdf")

color=np.array(["red","blue","green","yellow"])
l=np.array([lrojo,lazul,lverde,lamarillo])
l_2=1/(l**2)
plt.figure(facecolor=(1,1,1))
n_2=np.array([nrojo,nazul,nverde,namarillo])
sn_2=np.array([snrojo,snazul,snverde,snamarillo])

def f(x,a,b):
    y = a+b*x
    return y

sol,ssol=curve_fit(f,l_2,n_2,maxfev=5000)
a,b=sol
sa,sb=ssol[0,0],ssol[1,1]
sa=np.sqrt(sa)
sb=np.sqrt(sb)
print("A=%.5f \\quad s(A) = %.5f \\quad \\quad  B = %.2f \\quad s(B) = %.2f "%(a,sa,b,sb))
x=np.linspace(min(l_2),max(l_2),10)
y=f(x,a,b)
plt.grid(True,linestyle="--")
plt.plot(x,y,color="black",markersize=8)

for i in range(len(color)):
    plt.errorbar([l_2[i]],[n_2[i]],yerr=[sn_2[i]],fmt=".",color=color[i],capsize=3.0,markersize=15,markeredgecolor='black')
plt.xlabel("$1/\lambda^2 \ (nm^{-2})$")
plt.ylabel("$n$")
plt.savefig("Indices_21.pdf",bbox_inches="tight")

plt.figure()
plt.grid(True,linestyle="--")
plt.plot(x,y,color="black",markersize=8)

for i in range(len(color)):
    plt.errorbar([l_2[i]],[n_2[i]],fmt=".",color=color[i],capsize=3.0,markersize=15,markeredgecolor='black')
plt.xlabel("$1/\lambda^2 \ (nm^{-2})$")
plt.ylabel("$n$")
plt.savefig("Indices_22.pdf",bbox_inches="tight")

grados=np.array([np.average(phirojo),np.average(phiamarillo),np.average(phiverde),np.average(phiazul)])
sgrados=np.array([srojo,samarillo,sverde,sazul])
indice=np.array([nrojo,namarillo,nverde,nazul])
sindice=np.array([snrojo,snamarillo,snverde,snazul])
l_o=np.array([lrojo,lamarillo,lverde,lazul])

tabla=concatenarbueno((l_o,grados,sgrados,indice,sindice))
hola=tabulate(tabla,tablefmt="latex",floatfmt=(".1f",".2f",".2f",".5f",".5f"))

outfile=open("datos.txt", 'w')
outfile.write(hola)
outfile.close()