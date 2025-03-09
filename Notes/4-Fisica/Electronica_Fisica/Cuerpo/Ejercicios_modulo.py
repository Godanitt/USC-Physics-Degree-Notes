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
    Vbi=(k*T)*np.log(NA*ND/(ni**2))
    return Vbi

def fun_xp(NA,ND,KS,Vbi,Va=0):
    """ 
    Función que calcula xp (anchura en p de la región de vaciamiento) [cm]
        - NA = Numero de Aceptores excitados [cm-3]
        - ND = Numero de Dadores excitados [cm-3]
        - KS = Constante de 
        - Vbi = Voltaje de la unión pn en equilibrio (Vbi) [eV]
        - Va = Voltaje de polarización (0 default) [eV]
    """
    xp=np.sqrt(abs((2*KS*cte.epsilon_0/e)*(ND/(NA*(NA+ND)*10**(6)))*(Vbi-Va)))*10**2
    return xp

def fun_xn(NA,ND,KS,Vbi,Va=0):
    """ 
    Función que calcula xn (anchura en n de la región de vaciamiento) [cm]  
        - NA = Numero de Aceptores excitados [cm-3]      
        - ND = Numero de Dadores excitados [cm-3]
        - KS = Constante dieléctrica relativa []
        - Vbi = Voltaje de la unión pn en equilibrio [eV]
        - Va = Voltaje de polarización (0 default) [eV]
    """
    xn=np.sqrt(abs((2*KS*cte.epsilon_0/e)*(NA/(ND*(NA+ND)*10**(6)))*(Vbi-Va)))*10**2
    return xn

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
        - NC,NV = Densidades efectivas N_C y N_V [cm-3]
        - Eg = Energía el gap (por defecto silicio 1.12 eV) [eV]
        - T  = Temperatura (default 300K) [K]
    """
    ni=np.sqrt(NC*NV)*np.exp(-Eg/(2*k*T))
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

def fun_slope_lineal(NA,ND,KS):
    """ 
    Función que calcula la pendiente de V(x) en la región de vaciamiento [V/cm]
        - KS = permitividad relativa 
        - NA = Valor de los portadores aceptores [cm-3]. Es 0 si ND!=0
        - NA = Valor de los portadores dadores [cm-3]. Es 0 si NA!=0
    """
    slope=e*NA/(2*KS*cte.epsilon_0*10**(-2))-e*ND/(2*KS*cte.epsilon_0*10**(-2)) 
    return slope

def fun_grafica_bandas_pn(fig,Ec,Ev,Vbi,Ei,slope_p,slope_n,xn,xp,Va=0.0):
    """
    Función que grafica las bandas Ec,Ev,Ei,EF a lo largo de una union pn:
        - fig: figura en la que se representa.
        - Ec: energía de la banda de conducción respecto EF [eV]
        - Ev: energía de la banda de valecia respecto EF [eV]
        - Vbi: potencial Vbi [V]
        - Ei: energía intrínseca respecto EF [eV]
        - slope_p: pendiente de V(x) en la región de vaciamiento p [V/cm]
        - slope_n: pendiente de V(x) en la región de vaciamiento n [V/cm]
        - xn: tamaño de la zona de vaciamiento en n [cm]
        - xp: tamaño de la zona de vaciamiento en p [cm]    
        - Va = Voltaje de polarización (0 default) [eV]    
    """
    Vbieff=Vbi-Va
    plt.title("Bandas de Energía $V_A=$%.2f"%Va)
    W=xn+xp
    distancias=np.array([-2*xp,-xp,0,xn,xn+xp])
    plt.plot([min(distancias),max(distancias)],[0,0],color="black",label="$E_F$")
    for i in range(len(distancias)-1):
        if (i==0):
            plt.plot([distancias[i],distancias[i+1]],[Ec,Ec],color="red",label="$E_C$")
            plt.plot([distancias[i],distancias[i+1]],[Ev,Ev],color="blue",label="$E_V$")
            plt.plot([distancias[i],distancias[i+1]],[Ei,Ei],color="green",linestyle="--",label="$E_i$")
            plt.annotate("", xytext=(-7.2/4*xp, 0), xy=(-7.2/4*xp, Ec),arrowprops=dict(arrowstyle="<->"))
            plt.annotate("", xytext=(-6.2/4*xp, 0), xy=(-6.2/4*xp, Ei),arrowprops=dict(arrowstyle="<->"))
            plt.annotate("", xytext=(-6.2/4*xp, 0), xy=(-6.2/4*xp, Ev),arrowprops=dict(arrowstyle="<->"))
            plt.annotate("$E_c$=%.2f"%Ec, xy=(-7/4*xp, (Ec+Ei)/2))
            plt.annotate("$E_i$=%.2f"%Ei, xy=(-6/4*xp, Ei/2))
            plt.annotate("$E_v$=%.2f"%Ev, xy=(-6/4*xp, Ev/2))
            
        elif(i==1):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            plt.plot(x,-slope_p*(x+xp)**2+Ec,color="red")
            plt.plot(x,-slope_p*(x+xp)**2+Ev,color="blue")
            plt.plot(x,-slope_p*(x+xp)**2+Ei,color="green",linestyle="--")
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            plt.plot(x,-slope_n*(x-xn)**2+Ec-Vbieff,color="red")
            plt.plot(x,-slope_n*(x-xn)**2+Ev-Vbieff,color="blue")
            plt.plot(x,-slope_n*(x-xn)**2+Ei-Vbieff,color="green",linestyle="--")
        else:         
            plt.plot([distancias[i],distancias[i+1]],[Ec-Vbieff,Ec-Vbieff],color="red")
            plt.plot([distancias[i],distancias[i+1]],[Ev-Vbieff,Ev-Vbieff],color="blue")
            plt.plot([distancias[i],distancias[i+1]],[Ei-Vbieff,Ei-Vbieff],color="green",linestyle="--")
            plt.annotate("", xytext=(6/8*xp+xn, 0), xy=(6/8*xp+xn, Ec-Vbieff),arrowprops=dict(arrowstyle="<->"))
            plt.annotate("", xytext=(6/8*xp+xn, 0), xy=(6/8*xp+xn, Ei-Vbieff),arrowprops=dict(arrowstyle="<->"))
            plt.annotate("", xytext=(7/8*xp+xn, 0), xy=(7/8*xp+xn, Ev-Vbieff),arrowprops=dict(arrowstyle="<->"))
            plt.annotate("$E_c$=%.2f"%(Ec-Vbieff), xy=(0/8*xp+xn, (Ec-Vbieff)/2),bbox=dict(boxstyle="round",  ec="white",fc="w",alpha=0.6))
            plt.annotate("$E_i$=%.2f"%(Ei-Vbieff), xy=(0/8*xp+xn, (Ei-Vbieff)/2), bbox=dict(boxstyle="round",  ec="white",fc="w",alpha=0.6))
            plt.annotate("$E_v$=%.2f"%(Ev-Vbieff), xy=(0/8*xp+xn, (Ev+Ei)/2-Vbieff))         
    plt.xlabel("x [cm]")
    plt.ylabel("E [eV]")
    plt.grid(True,linestyle="--")
    plt.legend()
    

def fun_grafica_E_pn(fig,NA,ND,KS,xn,xp,Va,color2="red",linestyle2="-"):
    """
    Función que grafica las bandas Ec,Ev,Ei,EF a lo largo de una union pn:
        - fig: figura en la que se representa.
        - Ec: energía de la banda de conducción respecto EF [eV]
        - Ev: energía de la banda de valecia respecto EF [eV]
        - Vbi: potencial Vbi [V]
        - Ei: energía intrínseca respecto EF [eV]
        - slope_p: pendiente de V(x) en la región de vaciamiento p [V/cm]
        - slope_n: pendiente de V(x) en la región de vaciamiento n [V/cm]
        - xn: tamaño de la zona de vaciamiento en n [cm]
        - xp: tamaño de la zona de vaciamiento en p [cm]    
        - Va = Voltaje de polarización (0 default) [eV]    
        - color (string) = color del campo eléctrico (default red)
        - linestyle (string) = estilo de línea del campo eléctrico (default -)
    """
    plt.title("Campo eléctrico")
    distancias=np.array([-2*xp,-xp,0,xn,xn+xp])
    for i in range(len(distancias)-1):
        if (i==0):
            plt.plot([distancias[i],distancias[i+1]],[0,0],color=color2,linestyle=linestyle2,label="$V_A$=%.2f [V]"%Va)            
        elif(i==1):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            plt.plot(x,-(e*NA/(KS*cte.epsilon_0*10**(-2)))*(x+xp),linestyle=linestyle2,color=color2)
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            plt.plot(x,-(e*ND/(KS*cte.epsilon_0*10**(-2)))*(xn-x),linestyle=linestyle2,color=color2)
        else:         
            plt.plot([distancias[i],distancias[i+1]],[0,0],color=color2)

    plt.xlabel("x [cm]")
    plt.ylabel("$\\mathcal{E}$ [V/cm]")
    plt.grid(True,linestyle="--")
    

def fun_grafica_V_pn(fig,Vbi,slope_n,slope_p,xn,xp,Va,color2="red",linestyle2="-"):
    """
    Función que grafica las bandas Ec,Ev,Ei,EF a lo largo de una union pn:
        - fig: figura en la que se representa.
        - Vbi: potencial Vbi [V]
        - slope_p: pendiente de V(x) en la región de vaciamiento p [V/cm]
        - slope_n: pendiente de V(x) en la región de vaciamiento n [V/cm]
        - xn: tamaño de la zona de vaciamiento en n [cm]
        - xp: tamaño de la zona de vaciamiento en p [cm]    
        - Va = Voltaje de polarización (0 default) [eV]    
        - color (string) = color del campo eléctrico (default red)
        - linestyle (string) = estilo de línea del campo eléctrico (default -)
    """
    Vbieff=Vbi-Va
    plt.title("Bandas de Energía")
    W=xn+xp
    distancias=np.array([-2*xp,-xp,0,xn,xn+xp])
    for i in range(len(distancias)-1):
        if (i==0):
            plt.plot([distancias[i],distancias[i+1]],[0,0],color=color2,linestyle=linestyle2,label="$V_A$=%.2f"%Va)            
        elif(i==1):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            plt.plot(x,slope_p*(x+xp)**2,color=color2,linestyle=linestyle2)
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            plt.plot(x,slope_n*(x-xn)**2+Vbieff,color=color2,linestyle=linestyle2)
        else:         
            plt.plot([distancias[i],distancias[i+1]],[Vbieff,Vbieff],color=color2,linestyle=linestyle2) 
    plt.ylabel("V [V]")
    plt.grid(True,linestyle="--")
    


def fun_grafica_rho_pn(fig,xn,xp,NA,ND,Va,color2="red",linestyle2="-"):
    """
    Función que grafica las bandas Ec,Ev,Ei,EF a lo largo de una union pn:
        - fig: figura en la que se representa.
        - Vbi: potencial Vbi [V]
        - xn: tamaño de la zona de vaciamiento en n [cm]
        - xp: tamaño de la zona de vaciamiento en p [cm]  
        - NA = Valor de los portadores aceptores [cm-3]
        - ND = Valor de los portadores dadores [cm-3] 
        - Va = Voltaje de polarización (0 default) [eV]    
        - color (string) = color del campo eléctrico (default red)
        - linestyle (string) = estilo de línea del campo eléctrico (default -)
    """
    plt.title("Densidad de carga $\\rho$ [C/cm$^3$]")
    W=xn+xp
    distancias=np.array([-2*xp,-xp,0,xn,xn+xp])
    for i in range(len(distancias)-1):
        if (i==0):
            plt.plot([distancias[i],distancias[i+1]],[0,0],color=color2,linestyle=linestyle2,label="$V_A$=%.2f"%Va)            
        elif(i==1):
            x=np.linspace(distancias[i],distancias[i+1],2)   
            plt.plot(x,[-e*NA,-e*NA],color=color2,linestyle=linestyle2)
            plt.fill_between(x,[-e*NA,-e*NA],color="blue",alpha=0.1)
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],2)   
            plt.plot(x,[e*ND,e*ND],color=color2,linestyle=linestyle2)
            plt.fill_between(x,[e*ND,e*ND],color="red",alpha=0.1)
        else:         
            plt.plot([distancias[i],distancias[i+1]],[0,0],color=color2,linestyle=linestyle2) 
    plt.plot([-xp,-xp],[0,-NA*e],color=color2,linestyle=linestyle2)
    plt.plot([xn, xn],[0,ND*e],color=color2,linestyle=linestyle2)   
    plt.plot([0, 0],[-NA*e,ND*e],color=color2,linestyle=linestyle2)
    plt.xlabel("x [cm]")   
    plt.ylabel("$\\rho$ [C/cm$^{-3}$]")
    plt.grid(True,linestyle="--")