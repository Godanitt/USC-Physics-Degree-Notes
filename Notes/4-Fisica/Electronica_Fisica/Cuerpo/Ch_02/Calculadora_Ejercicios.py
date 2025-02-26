import numpy as np
import matplotlib.pyplot as plt
import scipy as spy
import scipy.constants as cte

###################################################
# Constantes ######################################
###################################################


T300=300        # Temperatura a 300 K
T1273=1273.15   # Temperatura a 1273.15 K (1000 ºC)
EgSi=1.12       # Energía del gap de silicio promedio
EgGe=0.66       # Energía del gap de gemranio promedio
EgGeAs=1.42     # Energía del gap de GeAs promedio
mnSi=1.18*cte.electron_mass    # Masa del hueco en el silicio 300K) en m_e
mpSi= 0.81*cte.electron_mass   # Masa del electron en el silicio 300K) en m_e
niSi300=(1.18)*10**(10)          # Concentración intrisenca en el silicio cm^-3
niGe300=2*10**(13)             # Concentración intrisenca en el Ge cm^-3
niGaAs300=2.25*10**(6)         # Concentración intrisenca en el GaAs cm^-3


####################################################
##### Funciones ####################################
####################################################

###################
# Funcion para calcular el nivel intrínseco Ei de un semicondutor
# dada una temperatura T, masas mp*, mn*, energías Ec y Ev
###################

def energía_intriseca(Ec,Ev,T,mp,mn): # Ec y Ev en eV, T en K, mp y mn en la misma unidad
    Ei=(Ec+Ev)/2+(3/4)*(cte.Boltzmann*T/cte.e)*np.log(mp/mn)
    return Ei # Ei en eV

###################
# Funcion para calcular la masa efectiva de un portador 
# dada una temperatura T y una densidad efectiva N
###################

def masa_efectiva(N,T): # N en cm^-3, T en K # 
    m=((N*10**6/(2))**(2/3))*(2*cte.hbar**2*np.pi/(cte.Boltzmann*T))
    return m


##################
# Funcion para calcular Eg en función de la temperatura y dos parámetros
# Función de Varshini
##################

def Varshini(T,Eg0): # T en K, Eg0 en eV
    Eg=Eg0-(4.73*10**(-4)*T**2)/(T+636)
    return Eg



##################
# Funcion para calcular el número de impurezas excitadas en función
# del número de átomos dadores, temperatura y energía de fermi
##################

def f_Nd(ND,T,EF,ED): # T en K, EF y ED en eV, ND cm-3
    Nd=ND/(1+2*np.e((EF-ED)/(cte.k*T/cte.e)))
    return Nd

##################
# Densidad equivalente para una masa y temperatura (portadores) 
##################

def Ncv(mn,T):
    Nc=(2*(mn*cte.Boltzmann*T/(2*np.pi*cte.hbar**2))**(3/2))/10**6
    return Nc

##################
# concentración intrínseca por unidad de volumen
##################

def ni(T,mn,mp,Eg): # T en K, EF y ED en eV, ND cm-3
    ni=np.sqrt(Ncv(mn,T)*Ncv(mp,T))*np.e**(-Eg*cte.e/(2*cte.Boltzmann*T))
    return ni


##################
# Conentración de impurezas en función del numero de átomos donadores/aceptores
# la energía de fermi, ED y la temperatura.
##################

def ND_efectivo(T,ND,EF,ED):
    ND_efectivo=ND/(1+2*np.e**((EF-ED)*cte.e/(cte.Boltzmann*T)))
    return ND_efectivo


##################
# Energía de Fermi en función de la ND y ni 
# Asumimos ionización total y temperatura ambiente (ni=10**-9)
##################

def Energia_Fermi_ambiente(Nd,ni,T): #energía_intriseca(0,1.12,300,mpSi,mnSi)+
    Energia=energía_intriseca(-EgSi,0,300,mpSi,mnSi)+(cte.Boltzmann*T/cte.e)*(np.log(Nd/ni))
    return Energia

##################
# Cálculo e la resistividad para n,p,un,up dados
##################

def resistividad(up,un,p,n):
    rho=1/(cte.e*(un*n+up*p))
    return rho

####################################################
##### Ejercicios ###################################
####################################################

###################
### Ejercicio 10 ##
###################

unGaAs=9200
upGaAs=320

# Apartado a)
rho=resistividad(upGaAs,upGaAs,niGaAs300,niGaAs300)

# Apartado b)
muimp150=((150/300)**(-1.5))*1300

# Apartado c)
mu1=250
mu2=650
mu=1/(1/mu1+1/mu2)

print("--------------------------")    
print("Ejercicio 10")
print("Apartado a)")
print("Resistividad GaAs intríseco 300K=%e"%rho)
print("Apartado b)")
print("Movilidad 150K=",muimp150)
print("Apartado c)")
print("Movilidad 150k=",mu)

###################
### Ejercicio 11 ##
###################

def mu_mayoritaria_n(N):
    mun=65+1265/(1+(N/(8.5*10**16))**0.72)
    return mun

def mu_mayoritaria_p(N):
    mun=48+447/(1+(N/(6.3*10**16))**0.76)
    return mun


def mu_minoritaria_n(N):
    mun=232+1180/(1+(N/(8*10**16))**0.9)
    return mun


def mu_minoritaria_p(N):
    mun=130+370/(1+(N/(8*10**16))**1.25)
    return mun



print("--------------------------")    
print("Ejercicio 11")
NA1=10**15
ND1=5*10**15
NA2=5*10**15
print("Apartado a)")    
print("n=%.2e \\cm^-3"%(niSi300**2/NA1 ))
print("\\mu_p=%.2e "%mu_mayoritaria_p(NA1))
print("\\mu_n=%.2e "%mu_minoritaria_n(NA1))
print("\\rho = %.2e"%resistividad(mu_mayoritaria_p(NA1),mu_minoritaria_n(NA1),NA1,niSi300**2/NA1))

print("Apartado b)")    
print("p=%.2e \\cm^-3"%(niSi300**2/ND1 ))
print("\\mu_n=%.2e \\tquad "%mu_mayoritaria_n(ND1))
print("\\mu_p=%.2e \\tquad "%mu_minoritaria_p(ND1))
print("\\rho = %.2e"%resistividad(mu_minoritaria_p(ND1),mu_mayoritaria_n(ND1),niSi300**2/ND1,ND1))


print("Apartado c)")    
print("n=%.2e \\cm^-3"%(niSi300**2/NA2 ))
print("\\mu_p=%.2e  "%mu_mayoritaria_p(NA2))
print("\\mu_n=%.2e  "%mu_minoritaria_n(NA2))
print("\\rho = %.2e"%resistividad(mu_mayoritaria_p(NA2),mu_minoritaria_n(NA2),NA2,niSi300**2/NA2))



###################
### Ejercicio 12 ##
###################

print("--------------------------")    
print("Ejercicio 12")
a=10**-6
print("Apartado a)")
print("E(x) = %.2e \\ V/m"%(cte.Boltzmann*300/(a*cte.e)))


###################
### Ejercicio 13 ##
###################

taup=3.13*10**-8
taun=1.25*10**-8
n1=niSi300*np.exp((EgSi-0.530-energía_intriseca(EgSi,0,300,mpSi,mnSi))/(cte.Boltzmann*300/cte.e))
p1=niSi300*np.exp(-(EgSi-0.530-energía_intriseca(EgSi,0,300,mpSi,mnSi))/(cte.Boltzmann*300/cte.e))
rho=0.5
n0=(mnSi/(3*rho*taun*cte.e**2))
print("--------------------------")    
print("Ejercicio 13")
print("E_T-E_i=",EgSi-0.530-energía_intriseca(EgSi,0,300,mpSi,mnSi))
print("E_i=",energía_intriseca(EgSi,0,300,mpSi,mnSi))
print("Apartado a)")
print("p_1=%.2e \\ \\cm^{-3} \\quad n_1=%.2e \\ \\cm^{-3} "%(n1,p1))
print("R= %.2e  \\ s^{-1}\\cm^{-3}"%(-(niSi300**2)/(taup*p1+taun*n1)))
print("Apartado b)")
print("\\mun_n=%.2e"%(3*cte.e*taun/mnSi))
print("n_0=  %.2e \\cm^{-3}"%n0)
print("R= %.2e  \\ s^{-1}\\cm^{-3}"%(-(niSi300**2)/(taup*p1+taun*(n1+n0))))

###################
### Ejercicio 14 ##
###################

GL = 10**18
taun=10**-5
taup=10**-5
ND=10**15
print("--------------------------")    
print("Ejercicio 14")
print("Apartado a)")
print("p_{n0}= %.2e \\cm^{-3}"%(niSi300**2/ND))
print("p= %.2e \\cm^{-3}"%(GL*taun+(niSi300**2)/ND))
print("n= %.2e \\cm^{-3}"%(GL*taun+ND))
print("Apartado b)")
print("Sin iluminacion: E_F=%.2e"%(energía_intriseca(EgSi,0,300,mpSi,mnSi)-(cte.Boltzmann*300/cte.e)*(np.log((niSi300**2)/(ND*niSi300)))))    
print("E_F=%.2e \\ \\eV"%(energía_intriseca(EgSi,0,300,mpSi,mnSi)-(cte.Boltzmann*300/cte.e)*(np.log((GL*taun+((niSi300)**2)/ND)/(niSi300)))))

      

###################
### Ejercicio 15 ##
###################

EiSi300=energía_intriseca(EgSi,0,300,mpSi,mnSi)

n=(niSi300*np.exp((EgSi*3/4-EiSi300)/(cte.Boltzmann*300/cte.e)))
p=(niSi300*np.exp(-(EgSi*1/4-EiSi300)/(cte.Boltzmann*300/cte.e)))
mun=mu_mayoritaria_n((niSi300*np.exp((EgSi*3/4-EiSi300)/(cte.Boltzmann*300/cte.e))))
mup=mu_minoritaria_p((niSi300*np.exp((EgSi*3/4-EiSi300)/(cte.Boltzmann*300/cte.e))))
print("--------------------------")    
print("Ejercicio 15")
print("Apartado a)")
print("n=%.2e"%n)
print("p=%.2e"%p)
print("\mu_n=%.2e"%mun)
print("\mu_p=%.2e"%mup)
print("rho=%.2e"%resistividad(mup,mun,p,n))
print("Apartado b)")

plt.figure(figsize=(6,4))
plt.plot([0,1],[0,0],"b")
plt.plot([1,2],[-1,-1],"b")
plt.plot([2,3],[0,0],"b")
plt.plot([1,1],[0,-1],"b")
plt.plot([2,2],[0,-1],"b")

plt.xlabel("x")
plt.ylabel("E [V/m]")
plt.xticks([1,1.5,2],["-W/2","0","W/2"])
plt.yticks([-1],["$-\\frac{1}{q}\\frac{E_g}{2W} $"])
plt.savefig("02_Ejercicio_15_E(x).pdf")

plt.figure(figsize=(6,4))
plt.plot([0,1],[0,0],"r")
plt.plot([1,2],[0,1],"r")
plt.plot([2,3],[1,1],"r")
plt.xlabel("x")
plt.ylabel("V [V]")
plt.xticks([1,1.5,2],["-W/2","0","W/2"])
plt.yticks([0,1],["0","$\\frac{E_g}{4q} $"])
plt.savefig("02_Ejercicio_15_V(x).pdf")

###################
### Ejercicio 16 ##
###################W
Ei0=energía_intriseca(2*EgSi/3,-EgSi/3,300,mpSi,mnSi)
print("--------------------------")    
print("Ejercicio 16")
print("Apartado a)")
print("Ei0=%.2e"%Ei0)


fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# Primera gráfica: seno
axs[0].plot([0,1], [1,1], color='blue')
axs[0].plot([1,1],[0,1],"b")
axs[0].plot([1,2], [0,0], color='blue')
axs[0].plot([2,2],[0,1],"b")
axs[0].plot([2,3], [1,1], color='blue')
axs[0].set_title('Campo eléctrico')
axs[0].set_xlabel('x')
axs[0].set_ylabel('$\\mathcal{E} (x)$')
axs[0].set_xticks([0,0.6,1,1.5,2,3],["0","$x_1$","L/3","$x_2$","2L/3","L"])

# Segunda gráfica: coseno
axs[1].plot([0,1], [1,0], color='red')
axs[1].plot([1,2], [0,0], color='red')
axs[1].plot([2,3], [0,-1], color='red')
axs[1].set_title('Potencial')
axs[1].set_xlabel('x')
axs[1].set_ylabel('$V(x)$')
axs[1].set_xticks([0,0.6,1,1.5,2,3],["0","$x_1$","L/3","$x_2$","2L/3","L"])

# Ajustar el layout para evitar superposiciones
plt.tight_layout()

plt.savefig("02_Ejercicio_16.pdf")



print("Apartado b)")
print("p=%.2e"%(niSi300*np.exp(Ei0/(cte.Boltzmann*300/cte.e))))
