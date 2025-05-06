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
EgGaAs=1.42     # Energía del gap de GaAs promedio
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
def fun_grafica_bandas_pn(fig, Ec, Ev, Vbi, Ei, slope_p, slope_n, xn, xp, Va=0.0, T=300, alpha=1.0, prop=1.0, flag=False,flag1=False,LN=0.0, LP=0.0, x0=0, NP="PN"):
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
        - flag1 = si True entonces printea el anotate de la zona N 
        - x0 = si es cero, entonces el punto entre xp y xn es cero, si no, x0
        - NP = si "NP" activa la forma NP. En cuaqluier otro caso se hace PN. 

    """
    k = 8.617333262145e-5  # eV/K
    Vbieff = Vbi - Va
    Ec = Ec + Va
    Ei = Ei + Va
    Ev = Ev + Va
    mini = ((-xp - xn) / 0.7)*prop+x0
    maxi = (xp + xn) / 0.7 + x0
    xn=xn+x0
    xp=xp+x0

    #if NP == "NP":
        # Intercambio de zonas y pendientes
        #xp, xn = xn, xp
        #slope_p, slope_n = slope_n, slope_p

    plt.title(f"Bandas de Energía $V_A=${Va:.2f} V")
    s = -1 if NP == "NP" else 1

    #if s == -1:
    #    plt.xlim(maxi, mini)
    #    print("")
    #else:
    #   % plt.xlim(mini, maxi)

    distancias = np.array([mini , -xp , 0 , xn , maxi])
    if s==-1:
        distancias = np.array([mini/2, -(xn-x0)+x0 , 0+x0 , (xp-x0)+x0, maxi])


    plt.tight_layout()

    if Va > 0:
        Vaeff = Va
    elif Va < 0:
        Vaeff = k * T * (np.log(1 + np.e))
    else:
        Vaeff = 0

    # Niveles de Fermi
    if Va != 0:
        maxi1 = LP * np.log(abs(np.exp(Vaeff / (k * T)) - 1)) + xn/100
        mini1 = -LN * np.log(abs(np.exp(Vaeff / (k * T)) - 1)) + xp/100
        if NP=="NP":  
            plt.plot([distancias[3], min(distancias)], [0, 0], color="purple", label="$E_{Fn}$")
            plt.plot([max(distancias), distancias[1]], [-Va, -Va], color="black", label="$E_{Fp}$")
            plt.plot([distancias[1],distancias[1] + maxi1], [-Va, 0], color="black")
            plt.plot([mini1 + distancias[3], distancias[3]], [-Va, 0], color="purple")
            
        else:    
            plt.plot([distancias[1], max(distancias)], [0, 0], color="purple", label="$E_{Fn}$")
            plt.plot([min(distancias), distancias[3]], [-Va, -Va], color="black", label="$E_{Fp}$")
            plt.plot([distancias[3],distancias[3] + maxi1], [-Va, 0], color="black")
            plt.plot([mini1 + distancias[1], distancias[1]], [-Va, 0], color="purple")
    else:
        plt.plot([min(distancias), max(distancias)], [0, 0], color="black", linestyle="-", label="$E_{F0}$", alpha=0.5)

    # Graficado de bandas por regiones
    for i in range(len(distancias) - 1):
        x_i = distancias[i]
        x_ip1 = distancias[i + 1]

        if s==-1:
            j=len(distancias)-i-1
            x_ip1 = distancias[j]
            x_i = distancias[j - 1]

        if i == 0:
            plt.plot([x_i, x_ip1], [Ec, Ec], color="red", label="$E_C$")
            plt.plot([x_i, x_ip1], [Ev, Ev], color="blue", label="$E_V$")
            plt.plot([x_i, x_ip1], [Ei, Ei], color="green", linestyle="--", label="$E_i$")
            if flag:
                plt.fill_between([x_i, x_ip1], [Ec - 3 * k * T] * 2, [Ec + 3 * k * T] * 2, color="red", alpha=0.2)
                plt.fill_between([x_i, x_ip1], [Ev - 3 * k * T] * 2, [Ev + 3 * k * T] * 2, color="blue", alpha=0.2)
                
            plt.annotate("", xytext=((7.2)/8*x_i, 0), xy=(7.2/8*x_i, Ec),arrowprops=dict(arrowstyle="<->"))
            plt.annotate("", xytext=((6.2)/8*x_i, 0), xy=(6.2/8*x_i, Ei),arrowprops=dict(arrowstyle="<->"))
            plt.annotate("", xytext=((6.2)/8*x_i, 0), xy=(6.2/8*x_i, Ev),arrowprops=dict(arrowstyle="<->"))
            plt.annotate("$E_c$=%.2f"%Ec, xy=(7/8*x_i, (Ec+Ei)/2),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
            plt.annotate("$E_i$=%.2f"%Ei, xy=(6/8*x_i, Ei/2),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
            plt.annotate("$E_v$=%.2f"%Ev, xy=(6/8*x_i, Ev/2),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
            

        elif i == 1:
            if s==-1:
                #aux=Vbi
                #x_i=x0-(xp-x0)
                #x_ip1=x0
                print("")
            x = np.linspace(x_i, x_ip1, 100)
            y_shift = -1*slope_p * (abs(x) - abs(xp))**2
            plt.plot(x, y_shift + Ec, color="red")
            plt.plot(x, y_shift + Ev, color="blue")
            plt.plot(x, y_shift + Ei, color="green", linestyle="--")
            if flag:
                plt.fill_between(x, y_shift + Ec - 3 * k * T, y_shift + Ec + 3 * k * T, color="red", alpha=0.2)
                plt.fill_between(x, y_shift + Ev - 3 * k * T, y_shift + Ev + 3 * k * T, color="blue", alpha=0.2)

        elif i == 2:
            aux=0
            if s==-1:
                #aux=Vbi
                x_i=x0-(xn-x0)
                x_ip1=x0
                
            x = np.linspace(x_i, x_ip1, 100)
            y_shift = -1*slope_n * (abs(x) - abs(x0-(xn-x0)))**2
            plt.plot(x, y_shift + Ec - Vbieff + aux, color="red")
            plt.plot(x, y_shift + Ev - Vbieff  + aux, color="blue")
            plt.plot(x, y_shift + Ei - Vbieff + aux, color="green", linestyle="--")
            if flag:
                plt.fill_between(x, y_shift + Ec - Vbieff - 3 * k * T, y_shift + Ec - Vbieff + 3 * k * T, color="red", alpha=0.2)
                plt.fill_between(x, y_shift + Ev - Vbieff - 3 * k * T, y_shift + Ev - Vbieff + 3 * k * T, color="blue", alpha=0.2)
            if flag1:    
                plt.annotate("", xytext=(6/8*x_i, 0), xy=(6/8*x_i, Ec-Vbieff),arrowprops=dict(arrowstyle="<->"))
                plt.annotate("", xytext=(6/8*x_i, 0), xy=(6/8*x_i, Ei-Vbieff),arrowprops=dict(arrowstyle="<->"))
                plt.annotate("", xytext=(7/8*x_i, 0), xy=(7/8*x_i, Ev-Vbieff),arrowprops=dict(arrowstyle="<->"))
                plt.annotate("$E_c$=%.3f"%(Ec-Vbieff), xy=(6/8*x_i-(-mini+maxi)/10, (Ec-Vbieff)/2),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
                plt.annotate("$E_i$=%.3f"%(Ei-Vbieff), xy=(6/8*x_i-(-mini+maxi)/10, (Ei-Vbieff)/2), bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))
                plt.annotate("$E_v$=%.3f"%(Ev-Vbieff), xy=(7/8*x_i-(-mini+maxi)/10, (Ev+Ei)/2-Vbieff),bbox=dict(boxstyle="round",  ec="grey",fc="white",alpha=0.7))             
    
        else:
            plt.plot([x_i, x_ip1], [Ec - Vbieff] * 2, color="red")
            plt.plot([x_i, x_ip1], [Ev - Vbieff] * 2, color="blue")
            plt.plot([x_i, x_ip1], [Ei - Vbieff] * 2, color="green", linestyle="--")
            if flag:
                plt.fill_between([x_i, x_ip1], [Ec - Vbieff - 3 * k * T] * 2, [Ec - Vbieff + 3 * k * T] * 2, color="red", alpha=0.2)
                plt.fill_between([x_i, x_ip1], [Ev - Vbieff - 3 * k * T] * 2, [Ev - Vbieff + 3 * k * T] * 2, color="blue", alpha=0.2)

            plt.xlabel("x [cm]")
    plt.ylabel("E [eV]")
    plt.grid(True, linestyle="--")

    ##if s < 0:
    #    x = np.linspace(mini, maxi, 8)
    #    plt.xticks(s * x, [f"{val:.1e}" for val in x])

    plt.legend()

    

def fun_grafica_E_pn(fig,NA,ND,KS,xn,xp,Va,x0=0,color2="red",linestyle2="-",NP="PN"):
    """
    Función que grafica las bandas campo eléctrico a lo largo de una union pn:
        - fig: figura en la que se representa.
        - Ec: energía de la banda de conducción respecto EF [eV]
        - Ev: energía de la banda de valecia respecto EF [eV]
        - Vbi: potencial Vbi [V]
        - Ei: energía intrínseca respecto EF [eV]
        - slope_p: pendiente de V(x) en la región de vaciamiento p [V/cm]
        - slope_n: pendiente de V(x) en la región de vaciamiento n [V/cm]
        - xn: tamaño de la zona de vaciamientoVa en n [cm]
        - xp: tamaño de la zona de vaciamiento en p [cm]    
        - Va = Voltaje de polarización (0 default) [eV]    
        - x0 = Punto del NP
        - color (string) = color del campo eléctrico (default red)
        - linestyle (string) = estilo de línea del campo eléctrico (default -)
    """
    plt.title("Campo eléctrico")
    distancias=np.array([-xn-xp,-xp,0,xn,xn+xp])
    s=1
    if (NP=="NP"):
        s=-1
    if s==-1:
        distancias=np.array([-xn-xp,-xn,0,xp,xn+xp])+x0
    for i in range(len(distancias)-1):
        x_i = distancias[i]
        x_ip1 = distancias[i + 1]
            
        if (i==0):
            plt.plot([x_i,x_ip1],[0,0],color=color2,linestyle=linestyle2,label="$V_A$=%.2f [V]"%Va)            
        elif(i==1):
            x=np.linspace(x_i,x_ip1,50)   
            aux=0
            aux2=1
            if s==-1:
                aux=-xn+x0-xp
                aux2=ND/NA
            plt.plot(x,-s*(e*aux2*NA/(KS*cte.epsilon_0*10**(-2)))*abs((abs(x)-abs(aux+xp))),linestyle=linestyle2,color=color2)
        elif(i==2):
            x=np.linspace(x_i,x_ip1,50)   
            aux=0
            aux2=1
            if s==-1:
                aux=xn+x0+xp
                aux2=NA/ND
            plt.plot(x,-s*(e*ND*aux2/(KS*cte.epsilon_0*10**(-2)))*abs(abs(xn-aux)-abs(x)),linestyle=linestyle2,color=color2)
        else:         
            plt.plot([x_i,x_ip1],[0,0],color=color2)

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
    plt.title("Potencial V(x)")
    W=xn+xp
    s=1
    distancias=np.array([-2*xp,-xp,0,xn,xn+xp])
    for i in range(len(distancias)-1):
        
        x_i = distancias[i]
        x_ip1 = distancias[i + 1]

        if s==-1:
            j=len(distancias)-i-1
            x_ip1 = distancias[j]
            x_i = distancias[j - 1]
        if (i==0):
            plt.plot([x_i ,x_ip1],[0,0],color=color2,linestyle=linestyle2,label="$V_A$=%.2f"%Va)            
        elif(i==1):
            x=np.linspace(x_i ,x_ip1,50)   
            plt.plot(x,slope_p*(x+xp)**2,color=color2,linestyle=linestyle2)
        elif(i==2):
            x=np.linspace(x_i ,x_ip1,50)   
            plt.plot(x,slope_n*(x-xn)**2+Vbieff,color=color2,linestyle=linestyle2)
        else:         
            plt.plot([x_i ,x_ip1],[Vbieff,Vbieff],color=color2,linestyle=linestyle2) 
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

def fun_grafica_I_pn(fig,xn,xp,INxp,IPxn,LN,LP,x1n,x1p,Va,T=300.0,flag=False,NP="PN"):
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
        - NP = si "NP" activa la forma NP. En cuaqluier otro caso se hace PN. 
    """
    plt.title("Intensidades [A] para $V_A$=%.2f [V]"%Va)
    s=1
    if (NP=="NP"):
        s=-1
    I=INxp+IPxn
    aux=""
    if (I<0):
        aux="-"
        I=-1.0*I
        INxp=-1.0*INxp
        IPxn=-1.0*IPxn       
        
    distancias=np.array([-3*LN,-xp,xn,3*LP])
    
    if flag:
        distancias=np.array([-x1p,-xp,xn,x1n])
        
    for i in range(len(distancias)-1):
        if (i==0):
            x=np.linspace(distancias[i],distancias[i+1],50)  
            In=(np.cosh((x1p+x)/LN))/(np.cosh((x1p-xp)/LN))
         #  print("In",In)
            plt.plot(x,[I]*len(x),color="green",linestyle="-",label="$I_T$")
            plt.plot(x,I-INxp*In,linestyle="-",color="red",label="$I_P$")  
            plt.plot(x,INxp*In,linestyle="-",color="blue",label="$I_N$")     
        elif(i==1): 
            plt.plot([-xp,xn],[IPxn,IPxn],linestyle="-",color="red")
            plt.plot([-xp,xn],[INxp,INxp],linestyle="-",color="blue")
            plt.plot([-xp,xn],[I,I],linestyle="-",color="green")
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],50)   
            Ip=(np.cosh((x1n-x)/LP))/(np.cosh((x1n-xn)/LP))
            plt.plot(x,[I]*len(x),linestyle="-",color="green")
            plt.plot(x,I-IPxn*Ip,linestyle="-",color="blue") 
            plt.plot(x,IPxn*Ip,linestyle="-",color="red")

    plt.xlabel("x [cm]")
    plt.ylabel(aux+"$I$ [A]")
    if s<0:
        x=np.linspace(max(distancias),min(distancias),8)
        labels = [f"{num:.1e}" for num in s*x]
        plt.xticks(x,labels)
        plt.xlim(max(distancias),min(distancias))
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
    
def fun_grafica_minoritarios(fig,NA,ND,ni,LP,LN,Va,xn,xp,x1n,x1p,T=300.0,Flag=False,color2="red",linestyle2="-"):
    """
    Función que grafica las bandas Ec,Ev,Ei,EF a lo largo de una union pn:
        - fig: figura en la que se representa.
        - NA = Valor de los portadores aceptores [cm-3]
        - ND = Valor de los portadores dadores [cm-3] 
        - ni = densidad de portadores intrínseca [cm-3]
        - LN = Longitud media de difusión de portadores electron [cm]
        - LP = Longitud media de difusión de portadores hueco [cm]
        - Va = Voltaje de polarización (0 default) [eV]  
        - xn: tamaño de la zona de vaciamiento en n [cm]
        - xp: tamaño de la zona de vaciamiento en p [cm]   
        - x1n = longitud de la zona masiva n [cm] (si queremos diodo no estrecho usamos valor grande)
        - x1p = longitud de la zona masiva p [cm] (si queremos diodo no estrecho usamos valor grande)
        - Flag (Bool) = Si verdadero -> aproximacion diodo estrecho.         
        - T = Temperatura (default 300) [K]
        - color (string) = color del campo eléctrico (default red)
        - linestyle (string) = estilo de línea del campo eléctrico (default -)
    """
    
    plt.title("Densidades $n_{n0}$ y $p_{n0}$")   
    k=cte.k/cte.e     
    distancias=np.array([-100*LP,-xp,xn,100*LN])
    x1p = float(x1p)
    x1n = float(x1n)
    if Flag:
        distancias=np.array([-x1p,-xp,xn,x1n])
        
    if Va>0:
        fun=max    
    else:    
        fun=min
        
    for i in range(len(distancias)-1):
        if (i==0):
            x=np.linspace(distancias[i],distancias[i+1],100000)  
            n_p=((ni**2)/NA)+((ni**2)/NA)*(np.exp(Va/(k*T))-1.00)*(np.sinh((x1p+x)/LN))/(np.sinh((x1p-xp)/LN))
            plt.plot(x,n_p,color="red",linestyle=linestyle2,label="n")  
            plt.plot([distancias[i],distancias[i+1]],[NA,NA],color="blue",label="p")  
        elif(i==1):  
            plt.plot([distancias[i],distancias[i+1]],[fun(n_p),ND],color="red",linestyle="-")
        elif(i==2):
            x=np.linspace(distancias[i],distancias[i+1],100000) 
            pn=((ni**2)/ND)+((ni**2)/ND)*(np.exp(Va/(k*T))-1.00)*(np.sinh((x1n-x)/LP))/(np.sinh((x1n-xn)/LP))  
            plt.plot(x,pn,color="blue")
            plt.plot([distancias[i-1],distancias[i-1+1]],[NA,fun(pn)],color="blue")
            plt.plot([distancias[i],distancias[i+1]],[ND,ND],color="red")
            
    plt.plot([distancias[0],0],[NA,NA],color="green",label="Dopado")    
    plt.plot([0,0],[NA,ND],color="green")     
    plt.plot([0,max(distancias)],[ND,ND],color="green",)    
    plt.xlabel("x [cm]")
    plt.ylabel("Portadores de carga [cm$^{-3}$]")
    plt.yscale('log') 
    plt.grid(True,linestyle="--")
    
    
def fun_bandasPNP(fig,NA1,NA2,ND,ni,Va1,Va2,KS,Eg,mp,mn,T,prop=1.0,nombre_pdf="Prueba.pdf"):
    """                                                             
    Función que grafica las bandas Ec,Ev,Ei,EF a lo largo de un PNP
        - fig: figura en la que se representa.
    """                 


    print("ni1=%.3e"%ni)
    
    Vbi=fun_Vbi(NA1,ND,ni,T)

    print("Vbi1=%.3e"%Vbi)
    print("KS11=%.2e"%KS)

    xn=fun_xn(NA1,ND,KS,Vbi,Va1)
    xp=fun_xp(NA1,ND,KS,Vbi,Va1)

    print("xn1=%.3e"%xn)
    print("xp1=%.3e"%xp)

    Ei=fun_Ei(ni,NA1,ni)-Va1
    Ec=fun_Ec(mn,Ei,ni,T)
    Ev=fun_Ev(Ec,Eg)
    print("Ei1=",Ei)
    print("Ev1=",Ev)
    Vbi=fun_Vbi(NA1,ND,ni,T)

    slope_p=fun_slope_lineal(NA1,0,KS)
    slope_n=fun_slope_lineal(0,ND,KS)
    maxi1=(xp+xn)/0.7

                                   
    fun_grafica_bandas_pn(fig,Ec,Ev,Vbi,Ei,slope_p,slope_n,xn,xp,Va1,x0=0.0,flag1=False)
    
    Vbi=fun_Vbi(NA2,ND,ni,T)

    print("Vbi2=%.3e"%Vbi)
    print("KS12=%.2e"%KS)

    xn2=fun_xn(NA2,ND,KS,Vbi,Va2)
    xp2=fun_xp(NA2,ND,KS,Vbi,Va2)
    mini1=(xp+xn)/0.7

    print("xn2=%.3e"%xn2)
    print("xp2=%.3e"%xp2)

    Ei=fun_Ei(ni,NA2,ni)-2*Va2+Va1
    Ec=fun_Ec(mn,Ei,ni,T)
    Ev=fun_Ev(Ec,Eg)

    slope_p=fun_slope_lineal(NA2,0,KS)
    slope_n=fun_slope_lineal(0,ND,KS)

    fun_grafica_bandas_pn(fig,Ec,Ev,Vbi,Ei,slope_p,slope_n,xn2,xp2,Va2,x0=1.2*prop*(maxi1+mini1+xn),prop=prop,flag1=True,NP="NP")
    
    plt.title("Transistor PNP a $V_{EB}$=%.2f y $V_{BC}$=%.2f"%(Va1,Va2))
    
    #plt.ylim(-2,2)
    plt.savefig(nombre_pdf)
def fun_PNPCampoElectrico(fig,NA1,NA2,ND,ni,Va1,Va2,KS,T,prop=1.0,nombre_pdf="Prueba.pdf"):
    """                                                             
    Función que grafica el Campo eléctrico a lo largo de un PNP
        - fig: figura en la que se representa.
    """         
    Vbi1=fun_Vbi(NA2,ND,ni,T)
    xn1=fun_xn(NA1,ND,KS,Vbi1,Va1)
    xp1=fun_xp(NA1,ND,KS,Vbi1,Va1)
    Vbi2=fun_Vbi(NA2,ND,ni,T)

    xn2=fun_xn(NA2,ND,KS,Vbi2,Va2)
    xp2=fun_xp(NA2,ND,KS,Vbi2,Va2)
    E1=fun_Efield_max(NA1,xp1,KS)
    E2=fun_Efield_max(NA2,xp2,KS)
    print("Electrico 1 maximo=%.2e V/cm"%E1)
    print("Electrico 2 maximo=%.2e V/cm"%E2)
    fun_grafica_E_pn(fig,NA1,ND,KS,xn1,xp1,Va1,x0=0,color2="red",linestyle2="-",NP="PN")
    fun_grafica_E_pn(fig,NA2,ND,KS,xn2,xp2,Va2,x0=(xn2+xp2+xp1+xn1*2)*prop,color2="blue",linestyle2="-",NP="NP")

    plt.savefig(nombre_pdf)
    
def fun_PNPPotencial(fig,NA1,NA2,ND,ni,Va1,Va2,KS,T,prop=1.0,nombre_pdf="Prueba.pdf"):
    """                                                             
    Función que grafica el potencial a lo largo de un PNP
        - fig: figura en la que se representa.
    """         
    plt.savefig(nombre_pdf)
    
def fun_PNPminoritarios(fig,NA1,NA2,ND,ni,Va1,Va2,KS,mun,mup,taun,taup,T,x1=0.0,W=0.0,x2=0.0,prop=1.0,nombre_pdf="Prueba.pdf"):
    """                                                             
    Función que grafica el potencial a lo largo de un PNP
        - fig: figura en la que se representa.
    """         
    
    Vbi1=fun_Vbi(NA2,ND,ni,T)
    xn1=fun_xn(NA1,ND,KS,Vbi1,Va1)
    xp1=fun_xp(NA1,ND,KS,Vbi1,Va1)
    Vbi2=fun_Vbi(NA2,ND,ni,T)
    xn2=fun_xn(NA2,ND,KS,Vbi2,Va2)
    xp2=fun_xp(NA2,ND,KS,Vbi2,Va2)
    
    DN=fun_D(mun)
    DP=fun_D(mup)
    LN=fun_L(DN,taun)
    LP=fun_L(DP,taup)
    
    print("Dn=%.5e"%DN)
    print("Dp=%.5e"%DP)
    print("Ln=%.5e"%LN)
    print("Lp=%.5e"%LP)

    print("\SI{x_p=%.5e }{[cm]}"%xp1)
    print("\SI{x_n=%.5e}{[cm]}"%xn1)
    fun_grafica_minoritarios(fig,NA1,ND,ni,LP,LN,Va1,xn1,xp1, x1,W/2,x0=0,T=300.0,Flag=False,color2="red",linestyle2="-")    
    
    
    print("\SI{x_p=%.5e }{[cm]}"%xp1)
    print("\SI{x_n=%.5e}{[cm]}"%xn1)
    fun_grafica_minoritarios(fig,NA1,ND,ni,LP,LN,Va1,xn2,xp2,W/2,x2p,x0=W,T=300.0,Flag=False,color2="red",linestyle2="-")    
    
    plt.savefig(nombre_pdf)
    