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
mnSi=1.08*cte.electron_mass    # Masa del hueco en el silicio 300K) en m_e
mpSi= 0.55*cte.electron_mass   # Masa del electron en el silicio 300K) en m_e
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
    

####################################################
##### Ejercicios ###################################
####################################################


###################
### Ejercicio 5 ###
###################

NVSi=1.83*10**19
NVGaAs=9*10**18

print("--------------------------")
print("Soluciones al ejercicio 5:")
print("Apartado a)")
print("Masa en kg (Si):", masa_efectiva(NVSi,300))
print("Masa en me (Si)", masa_efectiva(NVSi,300)/cte.electron_mass)
print("Masa en kg (GaAs):", masa_efectiva(NVGaAs,300))
print("Masa en me (GaAs)", masa_efectiva(NVGaAs,300)/cte.electron_mass)
print("Apartado b)")
print("Nivel intríseco 300K",energía_intriseca(0,EgSi,300,1.0,0.19))
print("Nivel intríseco 300K",energía_intriseca(0,EgSi,1273.15,1.0,0.19))

plt.figure()
plt.plot([0,5],[0,0],"b")
plt.plot([0,5],[0.592,0.592],"r",label="300K")
plt.plot([0,5],[0.697,0.697],"g",label="1273.15K")
plt.plot([0,5],[EgSi,EgSi],"b")
plt.grid(True)
plt.legend()
plt.savefig("Ejercicio_01_5.pdf")

print("--------------------------")

###################
### Ejercicio 6 ###
###################
    
print("Ejercicio 6")
print("Apartado a)")
print("Nivel intríseco 300K",energía_intriseca(0,3.43,300,1.25,0.2))
print("--------------------------")

###################
### Ejercicio 7 ###
###################

Ec300=(1/2)*(Varshini(300,1.17)-(3/2)*(cte.Boltzmann*300/cte.e)*np.log(mpSi/mnSi))
Ec600=(1/2)*(Varshini(600,1.17)-(3/2)*(cte.Boltzmann*600/cte.e)*np.log(mpSi/mnSi))

Ev300=-(1/2)*(Varshini(300,1.17)+(3/2)*(cte.Boltzmann*300/cte.e)*np.log(mpSi/mnSi))
Ev600=-(1/2)*(Varshini(600,1.17)+(3/2)*(cte.Boltzmann*600/cte.e)*np.log(mpSi/mnSi))

Ef300=(cte.Boltzmann*300/cte.e)*np.log((10**17)/ni(300,mnSi,mpSi,Varshini(300,1.17)))
Ef600=(cte.Boltzmann*600/cte.e)*np.log((10**17)/ni(600,mnSi,mpSi,Varshini(600,1.17)))

print(ni(300,mnSi,mpSi,Varshini(300,1.17)))
print("Ejercicio 7")
print("Apartado a)")
print("E_c(300K)",Ec300)
print("E_c(600K)",Ec600)
print("E_v(300K)",Ev300)
print("E_v(600K)",Ev600)
print("E_F(300K)",Ef300)
print("E_F(600K)",Ef600)
print("Apartado b)")


plt.figure()
plt.plot([0,5],[0,0],"b",label="$E_i$")
plt.plot([0,2.5],[Ec300,Ec300],"r",linestyle="--",label="$E_c$(300K)")
plt.plot([0,2.5],[Ev300,Ev300],color="orange",linestyle="--",label="$E_v$(300K)")
plt.plot([0,2.5],[Ef300,Ef300],color="green",linestyle="--",label="$E_F$(300K)")

#plt.plot([2.5,5],[0,0],"-b",label="E_i(600K)")
plt.plot([2.5,5],[Ec600,Ec600],"r",label="$E_c$(600K)")
plt.plot([2.5,5],[Ev600,Ev600],color="orange",label="$E_v$(600K)")
plt.plot([2.5,5],[Ef600,Ef600],"g",label="$E_F$(600K)")
plt.grid(True)
plt.legend()
plt.savefig("Ejercicio_01_7.pdf")
#plt.show()
print("--------------------------")


###################
### Ejercicio 8 ###
###################

print("Ejercicio 8")
print("Apartado a)")
print("EF a ND=10**15 ",Energia_Fermi_ambiente(10**15,niSi300,300))
print("EF a ND=10**17 ",Energia_Fermi_ambiente(10**17,niSi300,300))
print("EF a ND=10**19 ",Energia_Fermi_ambiente(10**19,niSi300,300))
print("Apartado b)")
print("ND+ ",ND_efectivo(300,10**15,Energia_Fermi_ambiente(10**15,niSi300,300),-0.045)/10**15,"    para el nivel de Fermi",Energia_Fermi_ambiente(10**15,niSi300,300))
print("ND+ ",ND_efectivo(300,10**17,Energia_Fermi_ambiente(10**17,niSi300,300),-0.045),"    para el nivel de Fermi",Energia_Fermi_ambiente(10**17,niSi300,300))
print("ND+ ",ND_efectivo(300,10**19,Energia_Fermi_ambiente(10**19,niSi300,300),-0.045),"    para el nivel de Fermi",Energia_Fermi_ambiente(10**19,niSi300,300))
print("Apartado c)")

plt.figure()
plt.plot([0,6],[0,0],"b",label="$E_c$")
plt.plot([0,6],[-0.045,-0.045],"g",label="$E_D$")
plt.scatter
plt.plot([0,6],[-EgSi,-EgSi],"r",linestyle="--",label="$E_v$(300K)")
plt.plot([1,3,5],[Energia_Fermi_ambiente(10**15,niSi300,300),
                  Energia_Fermi_ambiente(10**17,niSi300,300),
                  Energia_Fermi_ambiente(10**19,niSi300,300)],".k",label="E_F")
plt.legend()
plt.xticks([1,3,5],["$10^{15}$","$10^{17}$","$10^{19}$"])
plt.xlabel("$N_D$ (cm$^{-3}$)")
plt.grid("True")
plt.savefig("Ejercicio_01_8.pdf")
#plt.show()
print("--------------------------")

