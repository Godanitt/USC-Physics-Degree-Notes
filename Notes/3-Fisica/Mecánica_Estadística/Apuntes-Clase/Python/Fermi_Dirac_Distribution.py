import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as cte

# Definción de funciones

def nr(E,T,mu):
    nr=1/(np.exp((E-mu)/(T))+1)
    return nr

def grafica(T,mu):
    plt.figure()
    E=np.linspace(0,5000,10000)
    for i in T:
        estados=nr(E,i,mu)
        plt.plot(E,estados,label="T=%i K"%i)
    plt.legend()
    plt.xticks([2500],["$ \epsilon_F $"])
    plt.xlabel("E")
    plt.ylabel("$n_r $")
    plt.savefig("03-Fermi-Dirac.pdf",dpi=300,bbox_inches="tight")    


# Definición de parámetros

mu=2500
T=np.array([0.001,100,298,1000])

# Programa

grafica(T,mu)
