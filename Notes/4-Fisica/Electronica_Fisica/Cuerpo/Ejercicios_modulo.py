import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import scipy.constants as cte

##################################
# Constantes universales #########
##################################

k=cte.Boltzmann/cte.e # [eV/T]
e=cte.e               # [C]
me=cte.electron_mass  # [kg]

##################################
# Constantes importantes #########
##################################

EgSi=1.12       # Energía del gap de silicio promedio
EgGe=0.66       # Energía del gap de gemranio promedio
EgGeAs=1.42     # Energía del gap de GeAs promedio
mnSi=1.18*cte.electron_mass    # Masa del hueco en el silicio 300K) en m_e
mpSi= 0.81*cte.electron_mass   # Masa del electron en el silicio 300K) en m_e
niSi300=(1.18)*10**(10)        # Concentración intrisenca en el silicio cm^-3
niGe300=2*10**(13)             # Concentración intrisenca en el Ge cm^-3
niGaAs300=2.25*10**(6)         # Concentración intrisenca en el GaAs cm^-3


##################################
# Definimos funciones ############
##################################

def fun_Vbi(NA,ND,ni,T=300.0):
    """
    Función que calcula Vbi [eV]
        - NA = Numero de Aceptores excitados [cm-3]
        - ND = Numero de Dadores excitados [cm-3]
        - ni = Concetración intrínseca [cm-3]
        - T  = Tempeartura (default 300K)
    """
    Vbi=(k*T/e)*np.log(NA*ND/(ni**2))
    return Vbi

def fun_xp(NA,ND,KS,Vbieff):
    """ 
    Función que calcula xp (anchura en p de la región de vaciamiento) [cm]
        -NA = Numero de Aceptores excitados [cm-3]
        -ND = Numero de Dadores excitados [cm-3]
        -KS = Constante de 
        -Vbieff = Voltaje de la unión pn en equilibrio (Vbi) o en polarización (Vbi+VA) [eV]
    """
    xp=(2*KS*cte.epsilon_0/e)*(ND/(NA*(NA+ND)))*(Vbieff*e) 
    return xp

def fun_xn(NA,ND,KS,Vbi):
    """ 
    Función que calcula xn (anchura en n de la región de vaciamiento) [cm]  
        - NA = Numero de Aceptores excitados [cm-3]      
        - ND = Numero de Dadores excitados [cm-3]
        - KS = Constante dieléctrica relativa []
        - Vbi = Voltaje de la unión pn en equilibrio [eV]
    """
    xp=(2*KS*cte.epsilon_0/e)*(NA/(ND*(NA+ND)))*(Vbi*e) 
    return xp

def fun_Ei(ni,Na,Nd,T=300):
    """ 
    Función que calcula Ei (enegía intrínseca respecto el nivel de Fermi EF=0) [eV]
        - NA = Numero de Aceptores excitados [cm-3]
        - ND = Numero de Dadores excitados [cm-3]
        - ni = Concetración intrínseca [cm-3]
        - T  = Temperatura (default 300K)
    """
    Ei=k*T*(-np.log(Nd/ni)+np.log(Na/ni))
    return Ei

def fun_NCV(mnp,T=300):
    """ 
    Función que calcula NC o NV si introducimos mn o mp [cm^-3]
        - mnp = mp (si NV) o mc (si NV)  [kg]
        - T  = Temperatura (default 300K) [K]
    """
    NCV=(1/10**6)*2*(e*mnp*k*T/(2*np.pi*cte.hbar**2))**(3/2)
    return NCV


def fun_ni(NC,NV,Eg=EgSi,T=300):
    """ 
    Función que calcula ni (concetración intrínseca) [cm^-3]
        - NC,NV = [cm-3]
        - Eg = Energía el gap (por defecto silicio 1.12 eV) [eV]
        - T  = Temperatura (default 300K) [K]
    """
    ni=np.sqrt(NC*NV)*np.exp(-Eg/(k*T))
    return ni


def fun_Ec(mn,Ei,ni,T=300):
    """ 
    Función que calcula Ec (energía de la banda de conducción respecto el nivel de Fermi EF=0) [cm^-3]
        - mn = Masa de los electrones en la esta [kg]
        - Ei = Energía intrínseca respecto nivel de fermi [eV]
        - T  = Temperatura (default 300K) [K]
    """
    ni=Ei+k*T*np.log(fun_NCV(mn,T)/ni)
    return ni

def fun_Ev(Ec,Eg=1.12):
    """ 
    Función que calcula Ec (energía de la banda de valencia respecto el nivel de Fermi EF=0) [cm^-3]
        - Ec = Energía del a banda de conducción (respecto el nivel de Fermi) [eV]
        - Eg = Energía el gap (por defecto silicio 1.12 eV) [eV]
    """
    Ev=Ec-Eg
    return Ev

def fun_mnp(tau,mu):
    """ 
    Función que calcula la masa del hueco/electrón [kg]
        - tau = vida media del electron/hueco [s]
        - mu = movilidad del electron/hueco [cm2/V*s]
    """
    mnp=3*e*tau/(mu*10**(-4))
    return mnp