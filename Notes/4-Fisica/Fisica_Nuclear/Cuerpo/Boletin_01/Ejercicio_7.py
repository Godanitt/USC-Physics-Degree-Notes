import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def generar_tabla_latex(nombres_columnas, *arrays, nombre_archivo="tabla.tex"):
    """
    Genera una tabla en formato LaTeX a partir de arrays usando pandas.

    Parámetros:
        nombres_columnas (list): Lista con los nombres de las columnas.
        *arrays (list): Listas o arrays con los datos de cada columna.
        nombre_archivo (str): Nombre del archivo donde se guardará la tabla (por defecto "tabla.tex").
    
    Retorna:
        str: Código LaTeX de la tabla.
    """
    # Verificar que todos los arrays tienen la misma longitud
    longitud = len(arrays[0])
    if not all(len(arr) == longitud for arr in arrays):
        raise ValueError("Todos los arrays deben tener la misma longitud")

    # Crear DataFrame
    df = pd.DataFrame({nombre: arr for nombre, arr in zip(nombres_columnas, arrays)})

    # Generar código LaTeX
    tabla_latex = df.to_latex(index=False, caption="Tabla generada con Python y pandas", label="tab:datos")

    # Guardar en un archivo
    with open(nombre_archivo, "w") as f:
        f.write(tabla_latex)

    return tabla_latex

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
fig, axs = plt.subplots(2, 2, figsize=(6, 6),layout='constrained')

axs[0,0].plot(IZr84,EZr84,".b")
axs[0,0].set_ylabel("E [keV]")
axs[0,0].set_xlabel("I")
axs[0,0].set_title("$^{84}$Zr Yrast line")
axs[0,0].grid(linestyle="--")
#axs[0,0].savefig("Yrast_Zr84.pdf")

axs[0,1].plot(IZr86,EZr86,".b")
axs[0,1].set_ylabel("E [keV]")
axs[0,1].set_xlabel("I")
axs[0,1].set_title("$^{86}$Zr Yrast line")
axs[0,1].grid(linestyle="--")
#axs[0,1].savefig("Yrast_Zr86.pdf")

axs[1,0].plot(IEu156,EEu156,".b")
axs[1,0].set_ylabel("E [keV]")
axs[1,0].set_xlabel("I")
axs[1,0].set_title("$^{156}$Eu Yrast line")
axs[1,0].grid(linestyle="--")
#axs[1,0].savefig("Yrast_Eu156.pdf")

axs[1,1].plot(IEu160,EEu160,".b")
axs[1,1].set_ylabel("E [keV]")
axs[1,1].grid(linestyle="--")
axs[1,1].set_xlabel("I")
axs[1,1].set_title("$^{160}$Eu Yrast line")
#axs[1,1].savefig("Yrast_Eu160.pdf")
#fig.savefig("Yrast_total.pdf")# Apartado b): calculo de I(omega):

fig.savefig("Yrast.pdf")

E=[EZr84,EZr86,EEu156,EEu160]
I=[IZr84,IZr86,IEu156,IEu160]

nombres=np.array(["$^{84}$Zr","$^{86}$Zr","$^{156}$Eu","$^{160}$Eu"])
nombres2=np.array(["84Zr_inercia.pdf","86Zr_inercia.pdf","156Eu_inercia.pdf","160Eu_inercia.pdf"])
fig, axs = plt.subplots(2, 2, figsize=(7, 7),layout='constrained')
fig2 = plt.figure()
for i in range(len(E)//2):
    for j in range(len(E)//2):
        #print("E",E[i])
        #print("diff",aux)
        Eaux=E[2*i+j][1:]
        Iaux=I[2*i+j][1:]
        
        aux1=np.diff(E[i*2+j])/(1000)
        aux2=1/(np.sqrt(Iaux*(Iaux+1))-np.sqrt((Iaux-1)*(Iaux-2)))
        aux=aux1*(aux2)
        
        Inercia=(Iaux*(Iaux+1))/(Eaux)
        axs[i,j].plot(aux**2,Inercia,linestyle="-",color="red",marker="o")
        axs[i,j].set_xlabel("$\hbar^2 \\omega^2$ [MeV$^2$]")
        axs[i,j].set_ylabel("$2\\mathcal{I}/2\\hbar^2$ [keV$^{-1}$]")
        axs[i,j].set_title("%s Inercia"%nombres[2*i+j])
        plt.plot(aux**2,Inercia,linestyle="-",marker="o",markeredgecolor="black",
                      markersize=5,label=nombres[2*i+j])

plt.xlabel("$\hbar^2 \\omega^2$ [MeV$^2$]")
plt.ylabel("$2\\mathcal{I}/2\\hbar^2$ [keV$^{-1}$]")
plt.title("$Ical(E)$")     
plt.legend()
fig.savefig("Incercia.pdf",bbox_inches='tight')
fig2.savefig("Incercia_2.pdf",bbox_inches='tight')

from scipy.optimize import curve_fit

def linear_model(x, a, b):
    return a + b * x
def quadratic_model(x, a, b):
    return a + b * x**2    
def linear_fit(x_data, y_data):
    params, _ = curve_fit(linear_model, x_data, y_data)
    return params  # Devuelve (a, b)
def quadratic_fit(x_data, y_data):
    params, _ = curve_fit(quadratic_model, x_data, y_data)
    return params  # Devuelve (a, b)

auxiliar=[[0,3],[0,3,6],[0,6,14],[0,8,13]]
fig, axs = plt.subplots(2, 2, figsize=(6, 6),layout='constrained')
for i in range(len(E)//2):
    for j in range(len(E)//2):
        aux=np.diff(E[i*2+j])/(2*1000)
        Eaux=E[2*i+j][1:]
        Iaux=I[2*i+j][1:]
        axs[i,j].set_xlabel("I")
        axs[i,j].set_ylabel("E [keV")
        axs[i,j].set_ylim(min(Eaux)-200,max(Eaux)+200)
        axs[i,j].set_title("%s"%nombres[2*i+j])
        axs[i,j].grid(linestyle="--")
        Iaux2=np.linspace(min(Iaux),max(Iaux),100)
        for k in range(len(auxiliar[2*i+j])-1):
            a,b=quadratic_fit(Iaux[auxiliar[2*i+j][k]:auxiliar[2*i+j][k+1]],Eaux[auxiliar[2*i+j][k]:auxiliar[2*i+j][k+1]])
            axs[i,j].plot(Iaux2,quadratic_model(Iaux2,a,b))
    
        a,b=quadratic_fit(Iaux[auxiliar[2*i+j][k]:],Eaux[auxiliar[2*i+j][k]:])
        axs[i,j].plot(Iaux2,quadratic_model(Iaux2,a,b))
        axs[i,j].plot(Iaux,Eaux,".r")
import scipy.constants as cte

fig.savefig("Rotacional_band.pdf")  
beta = [0.177,0.148,0.189,0.303]
Z = [40,40,63,63]
A = [84,86,156,160]
Defecto_masa = [-71422,-77969,-64212,-66064]

def Isolid(Delta,beta,A,Z):
    R=10**(-12)*1.2*A**(1/3) # [m]
    m=((931.4941*1000) + Delta- Z*510.998950) # [keV/c²]
    m =  (cte.e/1000)*(1/cte.c**2)*m
    y = (2/5)*(A*m*R**2)*(1+(beta/3)*(1+0.16*beta)) # [kg*m²]
    return y


def Ifluid(Delta,beta,A,Z):
    m=((931.4941*1000) + Delta- Z*510.998950) # [keV/c²]
    m =  (cte.e/1000)*(1/cte.c**2)*m
    R=10**(-12)*1.2*A**(1/3) # [m]
    y = (9/(8*np.pi))*(A*m*beta*R**2) # [kg*m²]
    return y

Isol=np.zeros((4))
Iflu=np.zeros((4))
for i in range(len(beta)):
    Isol[i]=Isolid(Defecto_masa[i],beta[i],A[i],Z[i])*2/(cte.hbar**2) # Así lo doy en [1/J]
    Iflu[i]=Ifluid(Defecto_masa[i],beta[i],A[i],Z[i])*2/(cte.hbar**2) # Así lo doy en [1/J]
Isol=Isol*((cte.e*10**3))    
Iflu=Iflu*((cte.e*10**3))

print("Isol",Isol)
print("Isol",Iflu)

I=np.array([Isol,Iflu])
auxiliar2=["$\mathcal{I}_{sol}$","$\mathcal{I}_{flu}$"]
generar_tabla_latex([" ","$^{84}$Zr","$^{86}$Zr","$^{156}$Eu","$^{160}$Eu"],auxiliar2,I[:,0],I[:,1],I[:,2],I[:,3],nombre_archivo="Inercia.tex")


nombres=np.array(["$^{84}$Zr","$^{86}$Zr","$^{156}$Eu","$^{160}$Eu"])
nombres2=np.array(["84Zr_inercia.pdf","86Zr_inercia.pdf","156Eu_inercia.pdf","160Eu_inercia.pdf"])
fig, axs = plt.subplots(2, 2, figsize=(7, 7),layout='constrained')
for i in range(len(E)//2):
    for j in range(len(E)//2):
        #print("E",E[i])
        #print("diff",aux)
        Eaux=E[2*i+j][1:]
        Iaux=I[2*i+j][1:]
        
        aux1=np.diff(E[i*2+j])/(1000)
        aux2=1/(np.sqrt(Iaux*(Iaux+1))-np.sqrt((Iaux-1)*(Iaux-2)))
        aux=aux1*(aux2)
        
        Inercia=(Iaux*(Iaux+1))/(Eaux)
        axs[i,j].plot([min(aux**2),max(aux**2)],[Iflu[i*2+j]]*2,color="green",linestyle="--",label="$\mathcal{I}_{flu}$")
        axs[i,j].plot([min(aux**2),max(aux**2)],[Isol[i*2+j]]*2,color="blue",linestyle="--",label="$\mathcal{I}_{sol}$")
        axs[i,j].plot(aux**2,Inercia,linestyle="-",color="red",marker="o",markeredgecolor="black",
                      markersize=5,markerfacecolor="red",label="$\mathcal{I}(\omega)$")
        axs[i,j].set_xlabel("$\hbar^2 \\omega^2$ [MeV$^2$]")
        axs[i,j].set_ylabel("$2\\mathcal{I}/2\\hbar^2$ [keV$^{-1}$]")
        axs[i,j].set_title("%s Inercia"%nombres[2*i+j])
        axs[i,j].legend()
        
fig.savefig("I_Sol_fluid.pdf")        
print("Energías del siguiente 84Zr")
print(1262.81/539.92)
print(1887.91/1262.81)
print(1887.91/539.92)
print(2136.9/539.92)
print("Energías del siguiente 86Zr")
print(1666.57/751.75)
print(2669.88/1666.57)
print(2669.88/751.75)
print(3298.44/751.75)