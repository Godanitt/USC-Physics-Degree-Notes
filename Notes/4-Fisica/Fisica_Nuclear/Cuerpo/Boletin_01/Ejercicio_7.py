

import numpy as np
import matplotlib.pyplot as plt

# Aproximación a I(I+1)

def parabolica(x,b):
    y=b*x*(x+1)
    return y

def ajustar_b(x, y):
    """
    Calcula el valor de b en la aproximación f(x) = b * x * (x + 1) a los datos dados.
    
    Parámetros:
    x : array-like
        Valores de entrada.
    y : array-like
        Valores de salida.
    
    Retorna:
    b : float
        El coeficiente b que mejor ajusta la función en el sentido de mínimos cuadrados.
    """
    x = np.array(x)
    y = np.array(y)
    
    # Definir la variable auxiliar phi = x * (x + 1)
    phi = x * (x + 1)
    
    # Resolver el problema de mínimos cuadrados b*phi = y
    b = np.sum(phi * y) / np.sum(phi ** 2)
    
    return b


# Escribamos los niveles:

I=np.array([0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52])
EZr84=np.array([0,539.92,1262.81,1887.91,2136.39,3088.97,4068.7,5135.9,6302.4,7498.0,8743.6,10175.5,11821.1,13666.3,15659.9,18032.4,20618,23180.0,26830.1])
IZr84=I[0:len(EZr84)]

EZr86=np.array([0,751.75,1666.57,2669.88,3298.44,4326.12,5524.3,6321.08,7396.46,8650.0,10142.9,12060.9,14149.0,16050,18063,20532])
IZr86=I[0:len(EZr86)]

EEu156=np.array([0,344.53,797.39,1340.86,1959.2,2633.1,3314.6,3836.7,4380.4,5006.6,5716.7,6489.3,7315.9,8082.2,8848.8,9647.9,10414.6,11097,12035.4,13202.5,13967.0,14421.6,15764])
IEu156=I[0:len(EEu156)]

EEu160=np.array([0,125.47,389.37,765.01,1229.68,1760.88,2845.79,2931.38,3465.43,4020.9,4660.8,5707.6,6175.1,7027.6,7929.0,8865.6,9825.6,10808.8,11820.0,12865.4,13952.4,15086.7,16273.0,17512.8,18797.1,20141.9])
IEu160=I[0:len(EEu160)]



fig, axs = plt.subplots(2, 2, figsize=(8, 8))


axs[0,0].plot(IZr84,EZr84,".b")
axs[0,0].set_ylabel("E [keV]")
axs[0,0].set_xlabel("I")
axs[0,0].set_title("$^{84}$Zr Yrast line")
#axs[0,0].savefig("Yrast_Zr84.pdf")


axs[0,1].plot(IZr86,EZr86,".b")
axs[0,1].set_ylabel("E [keV]")
axs[0,1].set_xlabel("I")
axs[0,1].set_title("$^{86}$Zr Yrast line")
#axs[0,1].savefig("Yrast_Zr86.pdf")

axs[1,0].plot(IEu156,EEu156,".b")
axs[1,0].set_ylabel("E [keV]")
axs[1,0].set_xlabel("I")
axs[1,0].set_title("$^{156}$Eu Yrast line")
#axs[1,0].savefig("Yrast_Eu156.pdf")

axs[1,1].plot(EEu160,EEu160,".b")
axs[1,1].set_ylabel("E [keV]")
axs[1,1].set_xlabel("I")
axs[1,1].set_title("$^{160}$Eu Yrast line")
#axs[1,1].savefig("Yrast_Eu160.pdf")

fig.savefig("Yrast_total.pdf")

# Apartado b): calculo de I(omega):

E=[EZr84,EZr86,EEu156,EEu160]
I=[IZr84,IZr86,IEu156,IEu160]

nombres=np.array(["$^{84}$Zr","$^{86}$Zr","$^{156}$Eu","$^{160}$Eu"])
nombres2=np.array(["84Zr_inercia.pdf","86Zr_inercia.pdf","156Eu_inercia.pdf","160Eu_inercia.pdf"])

for i in range(len(E)):
    aux=np.diff(E[i])/(2*1000)
    #print("E",E[i])
    #print("diff",aux)
    Eaux=E[i][1:]
    Iaux=I[i][1:]
    Inercia=(Iaux*(Iaux+1))/(Eaux)
    plt.figure()
    plt.plot(aux**2,Inercia,".r")
    plt.xlabel("$\\omega^2$ [MeV$^2$]")
    plt.ylabel("$2\\mathcal{I}/2\\hbar^2$ [keV$^{-1}$]")
    plt.title("%s Inercia"%nombres[i])
    plt.savefig(nombres2[i],bbox_inches='tight')



# Ultimo apartado: ver bandas rotacionales

b=ajustar_b(IZr84,EZr84)
x=np.linspace(min(IZr84),max(IZr84),100)
axs[0,0].plot(x,parabolica(x,b),"r")