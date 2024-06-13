# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 20:50:20 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt

delta=np.linspace(2*np.pi,6*np.pi+np.pi,500)

R=np.array([0.2,0.6,0.9])

def F(R):
    return 4*R/(1-R)**2

def It(delta,R):
    It=1/(1+F(R)*(np.sin(delta/2))**2)
    return It


def Ir(delta,R):
    Ir=(F(R)*(np.sin(delta/2))**2)/(1+F(R)*(np.sin(delta/2))**2)
    return Ir


def printea_sticks(x):
    pos=np.array([])
    nombre=np.array([])
    for i in range(3):
        pos=np.append(pos,0+2*np.pi*(i+1))
        nombre=np.append(nombre,"$%d\pi$"%((i+1)*2))
        
    for i in range(3):
        pos=np.append(pos,3*np.pi+np.pi*i*2)
        nombre=np.append(nombre,"$%d\pi$"%(i*2+3))
    plt.xticks(pos,nombre,fontsize=9)

plt.figure()
for i in range(len(R)):
    plt.plot(delta,It(delta,R[i]),label="F=%.1f R=%.1f"%(F(R)[i],R[i]))
plt.xlabel("$\delta$")
plt.ylabel("$I_t/I$")
printea_sticks(delta)
plt.grid()
plt.xlim(2*np.pi,6*np.pi+np.pi)
plt.legend(loc="upper left")
plt.savefig("04-It.pdf")

plt.figure()
for i in range(len(R)):
    plt.plot(delta,Ir(delta,R[i]),label="F=%.1f R=%.1f"%(F(R)[i],R[i]))
plt.xlabel("$\delta$")
plt.ylabel("$I_r/I$")
printea_sticks(delta)
plt.xlim(2*np.pi,6*np.pi+np.pi)
plt.grid()
plt.legend(loc="upper left")
plt.savefig("04-Ir.pdf")



x, y = np.mgrid[-20:20:200j, -20:20:200j]

def r(x,y):
    r=np.sqrt(x**2+y**2)
    return r



fig, ax = plt.subplots(1, 1)
pcm = ax.pcolor(x, y, It(r(x,y),R[2]), cmap='binary', shading='nearest')
plt.savefig("04-Fabry_Perot_It-F360.pdf")

fig, ax = plt.subplots(1, 1)
pcm = ax.pcolor(x, y, It(r(x,y),R[1]), cmap='binary', shading='nearest')
plt.savefig("04-Fabry_Perot_It-F15.pdf")