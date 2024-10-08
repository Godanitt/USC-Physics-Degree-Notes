import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as cte

# Definción de funciones

def nr(E,T,mu):
    nr=1/(np.exp((E-mu)/(T))+1)
    return nr

def grafica(T,mu):
    plt.figure(figsize=(6,3.8))
    E=np.linspace(0,5000,10000)
    Color=np.array(["red","blue","green","orange"])
    k=0
    for i in T:
        estados=nr(E,i,mu)
        plt.plot(E/mu,estados,color=Color[k],label="T=%i K"%i)
        k+=1
    
    plt.annotate("", (0.8,1.1), xytext=(1.2, 1.1),
            arrowprops=dict(facecolor='black',arrowstyle="<->"))

    plt.annotate("$k_BT$", (1,1.2), xytext=(0.95,1.15))    
    plt.legend()
    plt.grid(linestyle="--")
    plt.xlabel("Energia [$\\varepsilon_F$]")
    plt.ylabel("$f_{FD}$")
    plt.ylim(-0.1,1.3)
    plt.savefig("06-Fermi-Dirac.pdf",dpi=300,bbox_inches="tight")    


# Definición de parámetros

mu=2500
T=np.array([0.001,100,298,1000])

# Programa

grafica(T,mu)
