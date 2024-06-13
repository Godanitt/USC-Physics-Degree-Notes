# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 19:50:53 2024

@author: danie
"""

#

import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as so
import sympy as symp
import scipy.special as scipy
import scipy.constants as cte

s0 = 1
s = np.linspace(0.01,100,10000)

def amplitud(s,delta,s0):
    H = 1/np.sqrt((1-(s/s0)**2)**2+(2*delta*s/s0)**2)
    return H

delta=[0.05,0.2,0.4,0.5,1,1.5]

plt.figure()
plt.grid()

for i in range(len(delta)):
    f=i/6
    H = amplitud(s,delta[i],s0)
    H = 20*np.log10(H)
    plt.plot(s,H,label="$\delta_%d = %.2f $"%(i+1,delta[i]),color=(0.1+f,0.2+f/4,0.7))
    plt.xscale("log")
    plt.ylim(-30,25)
    plt.xlabel("$ \omega / \omega_0  $")
    plt.ylabel("$ |H(\omega)|$ (dB)")
    plt.legend()

plt.savefig("2.1-Bode.pdf")    
    

def angulo(s,delta,s0):
    H = - np.arctan((2*delta*s/s0)/((1-(s/s0)**2)))
    return H


plt.figure()
plt.grid()

for i in range(len(delta)):
    f=i/6
    H = angulo(s,delta[i],s0)
    for j in range(len(H)):
        if H[j]>0:
            H[j]=H[j]-np.pi
    H=H*360/(2*np.pi)        
    plt.plot(s,H,label="$\delta_%d = %.2f $"%(i+1,delta[i]),color=(0.1+f,0.2+f/4,0.7))
    
    plt.xlabel("$ \omega / \omega_0  $")
    plt.ylabel("$\measuredangle \ H(\omega) \ (^o) $")
    plt.legend()

# Filtros reales

def butterworth(s,s0,e,n):
    H = 1/np.sqrt(1+e**2*(s/s0)**(2*n))
    return H

def chebyshev(s,s0,e,n):
    H=[0]*len(s)
    for i in range(len(s)):
        if s[i]/s0 > 1:       
            H[i] = 1/np.sqrt(1+(e**2)*(np.cosh(n*np.arccosh(s[i]/s0)))**2)
        if s[i]/s0 < 1:       
            H[i] = 1/np.sqrt(1+(e**2)*(np.cos(n*np.arccos(s[i]/s0)))**2)
        if s[i]/s0 == 1:       
            H[i] = 1/np.sqrt(1+(e**2)*(np.cos(0)**2))
    return H


n=[1,2,3,4,5]

plt.figure()
plt.grid()

for i in range(len(n)):
    f=i/len(n)
    H = butterworth(s,s0,1,n[i])
    #H = 20*np.log10(H)
    plt.plot(s,H,label="$n = %d $"%(n[i]),color=(0.1+f,0.2+f/4,0.7))
    #plt.xscale("log")
    plt.xlim(0,2)
    plt.xlabel("$ \omega / \omega_0  $")
    plt.ylabel("$ |H(\omega)|$")
    plt.legend()

plt.savefig("2.3-Butterworth.pdf")    

plt.figure()
plt.grid()


n=[2,5]


for i in range(len(n)):
    f=i/len(n)
    H = chebyshev(s,s0,1,n[i])
    #H = 20*np.log10(H)
    plt.plot(s,H,label="$n = %d $"%(n[i]),color=(0.1+f,0.2+f/4,0.7))
    #plt.xscale("log")
    plt.xlim(0,2)
    plt.xlabel("$ \omega / \omega_0  $")
    plt.ylabel("$ |H(\omega)|$")
    plt.legend()

plt.savefig("2.3-Chebyshev.pdf")    

# Filtros activos

s=np.linspace(0,100,1000)
def Hpb(H0,s,s0):
    H = H0/np.sqrt(1+(s/s0)**2)
    return H
def Hpa(H0,s,s0):
    H = H0*s/np.sqrt(1+(s/s0)**2)
    return H


H0=10
H = Hpb(H0,s,s0)
H = 20*np.log10(H)
fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(8,3.5))
ax1.plot(s,H,label="",color="red")
ax1.set_xscale("log")
ax1.set_xlabel("$ \omega$ (dB)")
ax1.set_ylabel("$ |H(\omega)|$ (dec)")
s1=H0*s0
ax1.plot([0,s0],[20*np.log10(H0),20*np.log10(H0)],color="blue")
ax1.plot([s0,s1,100],[20*np.log10(H0),0,-20],color="blue")
ax1.set_xticks([s0,s1],["$\omega_0$","$\omega_1$"])
ax1.set_yticks([0,20*np.log10(H0)],["0","$|H_0|$"])


H0=10
H = Hpa(H0,s,s0)
H = 20*np.log10(H)
ax2.plot(s,H,label="",color="red")
ax2.set_xscale("log")
ax2.set_xlabel("$ \omega$ (dB)")
ax2.plot([s0,100],[20*np.log10(H0),20*np.log10(H0)],color="blue")
ax2.plot([0.1,s0],[0,20*np.log10(H0)],color="blue")
ax2.set_xticks([s0],["$\omega_0$"])
ax2.set_yticks([0,20*np.log10(H0)],["0","$|H_0|$"])
ax2.set_xlim(0.1,10)


plt.savefig("2.4-1orden.pdf")    


s=np.linspace(0,100,1000)
def Notch(H0,s,s0,Q):
    H=[0]*len(s)
    for i in range(len(s)):
        H[i] = H0*abs(-s[i]**2+s0**2)/np.sqrt((-s[i]**2+s0**2)**2+(s[i]*s0/Q)**2)
    return H

s = np.linspace(0.01,100,50000)
plt.figure()
H0=1
Q=0.25
s0=1
H = Notch(H0,s,s0,Q)
Hl = 20*np.log10(H)
plt.plot(s,H,label="",color="red")
plt.xscale("log")
plt.xlabel("$ \omega$ ")
plt.xlim(0.1,10)


s=np.linspace(0,100,1000)
def highpass(H0,s,s0,Q):
    H=[0]*len(s)
    for i in range(len(s)):
        H[i] = H0*(s[i]**2)/np.sqrt((-s[i]**2+s0**2)**2+(s[i]*s0/Q)**2)
    return H

s = np.linspace(0.001,1000,50000)
plt.figure()
H0=10
Q=0.25
s0=1
H = highpass(H0,s,s0,Q)
H = 20*np.log10(H)
plt.plot(s,H,label="",color="red")
plt.xscale("log")
plt.xlabel("$ \omega$ ")
plt.xlim(0.001,1000)

