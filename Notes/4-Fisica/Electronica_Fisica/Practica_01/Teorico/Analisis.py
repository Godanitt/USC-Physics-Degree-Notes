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

def fun_grafica_bandas_pn(fig,Ec,Ev,Vbi,Ei,slope_p,slope_n,xn,xp,LN,LP,Va=0.0,T=300,alpha1=1.0,flag="False"):
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
        - T = Temperatura (300K default) [T]
        - alpha = valor de la opacidad de las líneas
        - flag = si True rellena la región +-3kT de gris (estudio degeneración)(False default).
    """
    Vbieff=Vbi-Va
    plt.title("Bandas de Energía Teóricas $V_A=$%.2f"%Va)
    
    # Escalamos todo a micrometros
  #  xn=xn*10**(4)
  #  xp=xp*10**(4)
  #  slope_n=slope_n*10**(-4)
  #  slope_p=slope_p*10**(-4)
    
 #   mini=(-xp-xn)/0.7
 #   maxi=(xp+xn)/0.7
 #   W=xn+xp
    mini=-10**(-3)
    maxi=10**(-3)
    distancias=np.array([mini,-xp,0,xn,maxi])
    plt.tight_layout()
    if Va>0:
        Vaeff=Va
    elif Va<0:
        Vaeff=k*T*(np.log(1+np.e)) 
    if not(Va==0):    
        plt.plot([-xp,maxi],[0,0],color="purple",label="$E_{Fn}$")
        plt.plot([mini,xn],[-Va,-Va],color="black",label="$E_{Fp}$")
        plt.plot([xn,xn+LP*np.log(abs(np.exp(Vaeff/(k*T))-1))],[-Va,0],color="black")
        plt.plot([-LN*np.log(abs(np.exp(Vaeff/(k*T))-1))-xp,-xp],[-Va,0],color="purple")
    else:     
        plt.plot([min(distancias),max(distancias)],[0,0],color="black",linestyle="-",label="$E_{F0}$",alpha=0.5)
    for i in range(len(distancias)-1):
        if (i==0):
            label1="$E_c$"
            label2="$E_v$"
            label3="$E_i$"
            if not(alpha1==1.0):            
                label1="$E_{c0}$"
                label2="$E_{v0}$"
                label3="$E_{i0}$"
            plt.plot([distancias[i],distancias[i+1]],[Ec-Va,Ec-Va],color="red",label=label1,alpha=alpha1)
            plt.plot([distancias[i],distancias[i+1]],[Ev-Va,Ev-Va],color="blue",label=label2,alpha=alpha1)
            plt.plot([distancias[i],distancias[i+1]],[Ei-Va,Ei-Va],color="green",linestyle="-",label=label3,alpha=alpha1)
            if (flag==True):
                plt.fill_between([distancias[i],distancias[i+1]], [Ec-3*k*T]*2,  [Ec+3*k*T]*2,color="red",alpha=.2, linewidth=0)
                plt.fill_between([distancias[i],distancias[i+1]], [Ev-3*k*T]*2,  [Ev+3*k*T]*2,color="blue",alpha=.2, linewidth=0)
                
       #     plt.annotate("", xytext=(7.2/8*mini, 0), xy=(7.2/8*mini, Ec),arrowprops=dict(arrowstyle="<->"))
       #     plt.annotate("", xytext=(6.2/8*mini, 0), xy=(6.2/8*mini, Ei),arrowprops=dict(arrowstyle="<->"))
       #     plt.annotate("", xytext=(6.2/8*mini, 0), xy=(6.2/8*mini, Ev),arrowprops=dict(arrowstyle="<->"))
       #     plt.annotate("$E_c$=%.2f"%Ec, xy=(7/8*mini, (Ec+Ei)/2),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
       #     plt.annotate("$E_i$=%.2f"%Ei, xy=(6/8*mini, Ei/2),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
       #     plt.annotate("$E_v$=%.2f"%Ev, xy=(6/8*mini, Ev/2),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
            
        elif(i==1):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            plt.plot(x,-slope_p*(x+xp)**2+Ec-Va,color="red",alpha=alpha1)
            plt.plot(x,-slope_p*(x+xp)**2+Ev-Va,color="blue",alpha=alpha1)
            plt.plot(x,-slope_p*(x+xp)**2+Ei-Va,color="green",linestyle="-",alpha=alpha1)       
            if (flag==True):
                plt.fill_between(x, -slope_p*(x+xp)**2+Ec-3*k*T,  -slope_p*(x+xp)**2+Ec+3*k*T,color="red",alpha=.2, linewidth=0)
                plt.fill_between(x, -slope_p*(x+xp)**2+Ev-3*k*T,  -slope_p*(x+xp)**2+Ev+3*k*T,color="blue",alpha=.2, linewidth=0)
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            plt.plot(x,-slope_n*(x-xn)**2+Ec-Vbi,color="red",alpha=alpha1)
            plt.plot(x,-slope_n*(x-xn)**2+Ev-Vbi,color="blue",alpha=alpha1)
            plt.plot(x,-slope_n*(x-xn)**2+Ei-Vbi,color="green",linestyle="-",alpha=alpha1)
            if (flag==True):
                plt.fill_between(x, -slope_n*(x-xn)**2+Ec-Vbieff-3*k*T,  -slope_n*(x-xn)**2+Ec-Vbieff+3*k*T,color="red",alpha=.2, linewidth=0)
                plt.fill_between(x, -slope_n*(x-xn)**2+Ev-Vbieff-3*k*T,  -slope_n*(x-xn)**2+Ev-Vbieff+3*k*T,color="blue",alpha=.2, linewidth=0)
        else:         
            plt.plot([distancias[i],distancias[i+1]],[Ec-Vbi,Ec-Vbi],color="red",alpha=alpha1)
            plt.plot([distancias[i],distancias[i+1]],[Ev-Vbi,Ev-Vbi],color="blue",alpha=alpha1)
            plt.plot([distancias[i],distancias[i+1]],[Ei-Vbi,Ei-Vbi],color="green",linestyle="-",alpha=alpha1)
            
            if (flag==True):
                plt.fill_between([distancias[i],distancias[i+1]], [Ec-Vbieff-3*k*T]*2,  [Ec-Vbieff+3*k*T]*2,color="red",alpha=.2, linewidth=0)
                plt.fill_between([distancias[i],distancias[i+1]], [Ev-Vbieff-3*k*T]*2,  [Ev-Vbieff+3*k*T]*2,color="blue",alpha=.2, linewidth=0)
                
        #    plt.annotate("", xytext=(6/8*maxi, 0), xy=(6/8*maxi, Ec-Vbieff),arrowprops=dict(arrowstyle="<->"))
        #    plt.annotate("", xytext=(6/8*maxi, 0), xy=(6/8*maxi, Ei-Vbieff),arrowprops=dict(arrowstyle="<->"))
        #    plt.annotate("", xytext=(7/8*maxi, 0), xy=(7/8*maxi, Ev-Vbieff),arrowprops=dict(arrowstyle="<->"))
        #    plt.annotate("$E_c$=%.2f"%(Ec-Vbieff), xy=(6/8*maxi-(mini+maxi)/10, (Ec-Vbieff)/2),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
        #    plt.annotate("$E_i$=%.2f"%(Ei-Vbieff), xy=(6/8*maxi-(mini+maxi)/10, (Ei-Vbieff)/2), bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
        #    plt.annotate("$E_v$=%.2f"%(Ev-Vbieff), xy=(7/8*maxi-(mini+maxi)/10, (Ev+Ei)/2-Vbieff),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))         
    plt.xlabel("x [$\\mu$m]")
    plt.ylabel("E [eV]")
    plt.grid(True,linestyle="--")
    #plt.xticks([-xp,0,xn],["$x_p$=%.2e"%xp," ","$x_n$=%.2e"%xn])
    plt.xticks(np.linspace(-0.0010,0.0010,9),["-10","-7.5","-5","-2.5","-0","2.5","5","7.5","10"])
    plt.legend()
    

def fun_grafica_E_pn(fig,NA,ND,KS,xn,xp,Va,color2="red",linestyle2="-"):
    """
    Función que grafica el campo eléctrico a lo largo de una union pn:
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
    plt.title("Campo eléctrico $\\mathcal{E}$ teórico")
    plt.tight_layout()
   
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
    Función que grafica el potencial eléctrico
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
    plt.title("Potencial V(x) teórico")
    W=xn+xp
    distancias=np.array([-2*xp,-xp,0,xn,xn+xp])
    plt.tight_layout()
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
    plt.ylabel("x [cm]")
    plt.grid(True,linestyle="--")
    


def fun_grafica_rho_pn(fig,xn,xp,NA,ND,Va,color2="red",linestyle2="-"):
    """
    Función que grafica las densidad de carga
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
    plt.title("Densidad de carga $\\rho$ [C/cm$^3$] teórico")
    W=xn+xp
    distancias=np.array([-2*xp,-xp,0,xn,xn+xp])
    plt.tight_layout()
    for i in range(len(distancias)-1):
        if (i==0):
            plt.plot([distancias[i],distancias[i+1]],[0,0],color=color2,linestyle=linestyle2,label="$V_A$=%.2f"%Va)            
        elif(i==1):
            x=np.linspace(distancias[i],distancias[i+1],2)   
            plt.plot(x,[-e*NA,-e*NA],color=color2,linestyle=linestyle2)
       #     plt.fill_between(x,[-e*NA,-e*NA],color="blue",alpha=0.1)
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],2)   
            plt.plot(x,[e*ND,e*ND],color=color2,linestyle=linestyle2)
       #     plt.fill_between(x,[e*ND,e*ND],color="red",alpha=0.1)
        else:         
            plt.plot([distancias[i],distancias[i+1]],[0,0],color=color2,linestyle=linestyle2) 
    plt.plot([-xp,-xp],[0,-NA*e],color=color2,linestyle=linestyle2)
    plt.plot([xn, xn],[0,ND*e],color=color2,linestyle=linestyle2)   
    plt.plot([0, 0],[-NA*e,ND*e],color=color2,linestyle=linestyle2)
    plt.xlabel("x [cm]")   
    plt.ylabel("$\\rho$ [C/cm$^{-3}$]")
    
    plt.grid(True,linestyle="--")
    
    
def fun_INxp(A,DN,LN,ni,NA,Va,xp=0,x1p=np.inf,T=300):
    """
    Función que calcula el valor de I_N(-xp) en amperios:
        - DN = Coeficiente de difusión de portadores electron [cm]
        - LN = Longitud media de difusión de portadores electrón [cm]
        - ni = Densidad intrínseca de los portadores [cm^-3]
        - NA = Valor de los portadores aceptores [cm-3]
        - Va = Voltaje de polarización (0 default) [eV]  
        - xn: tamaño de la zona de vaciamiento en n (default 0) [cm]
        - x1n= longitud de la zona masiva p (default infinto)  [cm] 
        - T  = Temperatura (default 300K) [K] 
    """
    INxp =(A*e*DN/LN)*((ni**2)/NA)*(np.exp(Va/(k*T))-1)*(1/np.tanh((x1p-xp)/LN))
    return INxp
    
def fun_IPxn(A,DP,LP,ni,ND,Va,xn=0,x1n=np.inf,T=300):
    """
    Función que calcula el valor de I_N(-xp) en amperios:
        - DP= Coeficiente de difusión de portadores hueco [cm]
        - LP = Longitud media de difusión de portadores hueco [cm]
        - ni = Densidad intrínseca de los portadores [cm^-3]
        - ND = Valor de los portadores dadores [cm-3] 
        - Va = Voltaje de polarización (0 default) [eV]   
        - xn: tamaño de la zona de vaciamiento en n (default 0) [cm]
        - x1n= longitud de la zona masiva p (default infinto)  [cm]
        - T  = Temperatura (default 300K) [K] 
    """
    IPxn =(A*e*DP/LP)*((ni**2)/ND)*(np.exp(Va/(k*T))-1)*(1/np.tanh((x1n-xn)/LP))
    return IPxn

def fun_D(mu,T=300.0):
    """
    Función que calcula el valor del coeficiente de difusión D [cm2/s]
        - mu = Movilidad del electron/hueco [cm2/V s]
        - T  = Temperatura (default 300K) [K] 
    """
    D = mu*(k*T)
    return D 


def fun_L(D,tau):
    """
    Función que calcula el valor de la longitud media de difusión L [cm]
        - D = Coeficiente de difusión [cm2/s]
        - tau  = Tiempo de vida del portador [s]
    """
    L = np.sqrt(D*tau)
    return L

def fun_grafica_I_pn(fig,xn,xp,INxp,IPxn,LN,LP,x1n,x1p,Va,T=300.0,flag=False):
    """
    Función que grafica la Intensidad a lo largo de una union pn:
        - fig: figura en la que se representa.
        - xn: tamaño de la zona de vaciamiento en n [cm]
        - xp: tamaño de la zona de vaciamiento en p [cm] 
        - INxp: valor de I_N(x_p) [A]
        - IPxn: valor de I_P(x_n) [A]
        - Va = Voltaje de polarización (0 default) [eV]    
        - LN = Longitud media de difusión de portadores electron [cm]
        - LP = Longitud media de difusión de portadores hueco [cm]
        - x1n = longitud de la zona masiva n [cm]
        - x1p = longitud de la zona masiva p [cm]
        - Va = Valor de V_A [V]
        - Flag (Bool) = Si verdadero -> aproximacion diodo estrecho.         
        - T = Temperatura (default 300) [K]
    """
    plt.title("Intensidades [A] para $V_A$=%.2f [V] teórico"%Va)
    I=INxp+IPxn
    aux=""
    if (I<0):
        aux="-"
        I=-1.0*I
        INxp=-1.0*INxp
        IPxn=-1.0*IPxn       
        
    distancias=np.array([-3*LN,-xp,xn,3*LP])
    plt.tight_layout()
    
    if flag:
        distancias=np.array([-x1p,-xp,xn,x1n])
        
    for i in range(len(distancias)-1):
        if (i==0):
            x=np.linspace(distancias[i],distancias[i+1],50)  
            In=(np.cosh((x1p+x)/LN))/(np.cosh((x1p-xp)/LN))
         #  print("In",In)
            plt.plot(x,[I]*len(x),color="green",linestyle="-",label="$I_T$")
            plt.plot(x,I-INxp*In,linestyle="-.",color="red",label="$I_P$")  
            plt.plot(x,INxp*In,linestyle="-.",color="blue",label="$I_N$")     
        elif(i==1): 
            plt.plot([-xp,xn],[IPxn,IPxn],linestyle="-.",color="red")
            plt.plot([-xp,xn],[INxp,INxp],linestyle="-.",color="blue")
            plt.plot([-xp,xn],[I,I],linestyle="-",color="green")
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            Ip=(np.cosh((x1n-x)/LP))/(np.cosh((x1n-xn)/LP))
            plt.plot(x,[I]*len(x),linestyle="-",color="green")
            plt.plot(x,I-IPxn*Ip,linestyle="-.",color="blue") 
            plt.plot(x,IPxn*Ip,linestyle="-.",color="red")

    plt.xlabel("x [cm]")
    plt.ylabel(aux+"$I$ [A]")
   # plt.yscale('log') 
    plt.grid(True,linestyle="--")
    
def fun_Efield_max(NA,xp,KS):
    """
    Función que el valor del campo eléctrico máximo [V/cm]
        - NA = Valor de la densidad de aceptores [cm^-3]
        - xp = Posición de xp [cm]
        - KS = Permitivdad relativa
    """
    Emax=-e*NA*(10**2)*xp/(KS*cte.epsilon_0)
    return Emax  
    
def fun_grafica_minoritarios(fig,NA,ND,ni,LP,LN,Va,xn,xp,x1n,x1p,T=300.0,Flag=False,flag=True,color2="red",linestyle2="-"):
    """
    Función que grafica los portadores minoritarios
        - fig: figura en la que se representa.
        - NA = Valor de los portadores aceptores [cm-3]
        - ND = Valor de los portadores dadores [cm-3] 
        - ni = densidad de portadores intrínseca [cm-3]
        - LN = Longitud media de difusión de portadores electron [cm]
        - LP = Longitud media de difusión de portadores hueco [cm]
        - xn: tamaño de la zona de vaciamiento en n [cm]
        - xp: tamaño de la zona de vaciamiento en p [cm]   
        - x1n = longitud de la zona masiva n [cm]
        - Va = Voltaje de polarización (0 default) [eV]  
        - x1p = longitud de la zona masiva p [cm]
        - Flag (Bool) = Si verdadero -> aproximacion diodo estrecho.         
        - T = Temperatura (default 300) [K]
        - color (string) = color del campo eléctrico (default red)
        - linestyle (string)     plt.xticks(np.linspace(-0.0010,0.0010,9),["-10","-7.5","-5","-2.5","-0","2.5","5","7.5","10"])
= estilo de línea del campo eléctrico (default -)
    """
    
    plt.title("Densidades $n_{n0}$ y $p_{n0}$ teórico")   
    k=cte.k/cte.e     
    distancias=np.array([-3*xp,-xp,xn,3*xn])
    plt.tight_layout()
    x1p = float(x1p)
    x1n = float(x1n)
    xn=xn
    x1n=x1n*10**(-4)
    xp=xp
    x1p=x1p*10**(-4)
    if Flag:
        distancias=np.array([-x1p,-xp,xn,x1n])
    print("")    
    if Va>0:
        fun=max    
        plt.xlim(-0.0010,0.0010)    
        plt.ylim(10**3,10**18)  
    else:    
        fun=min
        plt.xlim(-0.0010,0.0010)  
        plt.ylim(0.1,10**18)
        
    for i in range(len(distancias)-1):
        if (i==0):
            x=np.linspace(distancias[i],distancias[i+1],10000)  
            n_p=((ni**2)/NA)+((ni**2)/NA)*(np.exp(Va/(k*T))-1.00)*(np.sinh((x1p+x)/LN))/(np.sinh((x1p-xp)/LN))
            plt.plot(x,n_p,color="blue",linestyle="-",label="n")     
            plt.plot([distancias[i],distancias[i+1]],[NA,NA],color="blue") 
        if (i==1):  
            plt.plot([distancias[i],distancias[i+1]],[fun(n_p),ND],color="blue")   
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],10000) 
            pn=((ni**2)/ND)+((ni**2)/ND)*(np.exp(Va/(k*T))-1.00)*(np.sinh((x1n-x)/LP))/(np.sinh((x1n-xn)/LP))  
            plt.plot(x,pn,color="red",linestyle="-",label="p")
            plt.plot([distancias[i-1],distancias[i-1+1]],[NA,fun(pn)],color="red")
            print("******************************")
            print("distancias",distancias) 
            print("******************************")
            plt.plot([distancias[i],distancias[i+1]],[ND,ND],color="blue") 
            
    plt.plot([distancias[0],0],[NA,NA],color="green",label="Dopado")    
    plt.plot([0,0],[NA,ND],color="green")     
    plt.plot([0,max(distancias)],[ND,ND],color="green",)         
   # plt.annotate("$n_{p}$", xy=(-x1n/2,ni**2/min([ND,NA])), bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
   # plt.annotate("$p_{n}$", xy=(x1p/2,ni**2/min([ND,NA])),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))  
    plt.xlabel("x [cm]")
    plt.ylabel("Portadores de carga [cm$^{-3}$]")
    plt.tight_layout()
    plt.yscale('log')  
    if (flag==True):    
        plt.xlabel("x [$\\mu$m]")
        plt.xticks(np.linspace(-0.0010,0.0010,9),["-10","-7.5","-5","-2.5","-0","2.5","5","7.5","10"])

    plt.grid(True,linestyle="--")
    
    
def fun_grafica_IV(fig,I0,Va,T=300):
    if Va>0:
        V=np.linspace(0,Va,50)
    if Va<0:
        V=np.linspace(Va,0,50)
    plt.plot(V,I0*(np.exp(V/(k*T))-1),color="blue")
    #plt.tight_layout()
    plt.title("Curva IV teórico")
    plt.xlabel("$V_A$ [V]")
    plt.ylabel("$J_0$ [A/cm$^2$]")
    plt.grid(True,linestyle="--")
    
    