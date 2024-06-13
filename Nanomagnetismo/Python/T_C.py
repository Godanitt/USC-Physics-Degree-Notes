# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:56:19 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as cte

muB = cte.physical_constants['Bohr magneton'][0]

y=np.linspace(-4,4,1000)


plt.plot(y,np.tanh(y),"k")  
plt.plot(y,1/np.tanh(y)-1/y,"k")     
plt.annotate("$J=1/2$", (0,0.8))
plt.annotate("$J=\infty$", (1.3,0.2))
plt.xlabel("$y$")
plt.ylabel("$B_J(y)$")
    
plt.savefig("02-Brillouin.pdf",bbox_inches="tight")


plt.figure()

#%%

J=1/2


def M(y,T):
    return T*(y)

y=np.linspace(-2,2,1000)


plt.plot(y,np.tanh(y),"k")  
plt.plot(y,M(y,0.5),"red",label="$T<T_C$")
plt.plot(y[249:751],M(y[249:751],1),"blue",label="$T=T_C$")
plt.plot(y[375:625],M(y[375:625],2),"green",label="$T>T_C$")

plt.plot(y,[1]*len(y),"-.k")
plt.plot(y,[-1]*len(y),"-.k")

plt.ylim(-1.3,1.3)
plt.xlim(-2,2)
plt.plot([-1000,1000],[0,0],"k",linewidth=0.7)
plt.plot([0,0],[-15000,15000],"k",linewidth=0.7)

plt.xlabel("$y$")
plt.ylabel("$M/M_S$")
plt.ylim(-1.3,1.3)
plt.legend()
    
plt.savefig("05-TC.pdf",bbox_inches="tight")

#%%

plt.figure()
J=1/2


def M(y,T,y0):
    return T*(y-3*y0)

y=np.linspace(-2,2,1000)


plt.ylim(-1.3,1.3)
plt.xlim(-2,2)

plt.plot(y,np.tanh(y),"k")  
plt.plot(y[220:925],M(y[220:925],0.7,0.1),"red",label="$T<T_C$")
plt.plot(y[325:825],M(y[325:825],1,0.1),"blue",label="$T=T_C$")
plt.plot(y[450:700],M(y[450:700],2,0.1),"green",label="$T>T_C$")

plt.plot(y,[1]*len(y),"-.k")
plt.plot(y,[-1]*len(y),"-.k")

plt.plot([-1000,1000],[0,0],"k",linewidth=0.7)
plt.plot([0,0],[-15000,15000],"k",linewidth=0.7)

plt.xlabel("$y$")
plt.ylabel("$M/M_S$")
plt.ylim(-1.3,1.3)
plt.legend()
    
plt.savefig("05-TC-B.pdf",bbox_inches="tight")


#%%

def g_lande(S,L):
    J=S+L
    return (3/2)+(S*(S+1)-L*(L-1))/(2*J*(J+1))

def  Bmf(S,T):
    bmf=(3*cte.Boltzmann*T)/((S+1)*g_lande(S, 0)*muB)
    return bmf
print(Bmf(1/2,1043))

print((8.489*10**28*2.2*muB*cte.mu_0))

#%%


plt.figure()
def F(M,T,TC):
    F0=0
    a0=1
    b=1
    return F0+a0*(T-TC)*M**2+b*M**4

M=np.linspace(-15,15,100)

plt.plot(M,F(M,150,100),"g",label="$T>T_C$",linewidth=2)
plt.plot(M,F(M,100,100),"b",label="$T=T_C$",linewidth=2)
plt.plot(M,F(M,0,100),"r",label="$T<T_C$",linewidth=2)

plt.plot([-1000,1000],[0,0],"k",linewidth=0.7)
plt.plot([0,0],[-15000,15000],"k",linewidth=0.7)

plt.xlabel("$M$")
plt.ylabel("$F(M)$")
plt.legend()

plt.xticks([],[])
plt.yticks([],[])

plt.ylim(-3000,3300)
plt.xlim(-15,15)

plt.savefig("06-Landau.pdf",bbox_inches="tight")

#%%

plt.figure(figsize=(7,7))
E = np.arange(0.0, 10.0, 0.01)
mu=5

def g(E):
    g=E**(1/2)
    return g

def f(E,mu,T):
    mu=5
    f=1/(1+np.exp((E-mu)/T))
    return f

ax1 = plt.subplot(221) 
ax1.plot(E,f(E,mu,0.00000001),color="black",label="$k_BT=0$")
ax1.plot(E,f(E,mu,0.1),color="blue",label="$k_BT=0.1$")
ax1.plot(E,f(E,mu,0.5),color="green",label="$k_BT=0.5$")
ax1.plot(E,f(E,mu,1),color="red",label="$k_BT=1$")
ax1.legend()
ax1.set_title('(a)')
ax1.set_xticks([mu],["$\mu$"])
ax1.set_yticks([],[])
ax1.set_xlabel("E")
ax1.set_ylabel("f(E)")

ax2 = plt.subplot(222)
ax2.plot(E,g(E),color="black")
ax2.set_title('(b)')
ax2.set_xticks([mu],["$\mu$"])
ax2.set_yticks([],[])
ax2.set_xlabel("E")
ax2.set_ylabel("g(E)")

ax3 = plt.subplot(212)
ax3.set_title('(c)')

ax3.plot(E,g(E)*f(E,mu,0.00000001),color="black",label="$k_BT=0$")
ax3.plot(E,g(E)*f(E,mu,0.1),color="blue",label="$k_BT=0.1$")
ax3.plot(E,g(E)*f(E,mu,0.5),color="green",label="$k_BT=0.5$")
ax3.plot(E,g(E)*f(E,mu,1),color="red",label="$k_BT=1$")
ax3.set_xticks([mu],["$\mu$"])
ax3.set_yticks([],[])
ax3.set_xlabel("E")
ax3.set_ylabel("f(E)g(E)")
ax3.legend()

plt.savefig("07-Fermi-function.pdf",bbox_inches="tight")

