import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Tabla_Latex import *

dFe=1.6 # mm
dPb=7.5 # mm

########################## HIERRO 0-20 #########################################
    
    
df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Atenuacion")
aux=1
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[0])))

valores[aux]=valores[aux]*dFe
svalores[aux]=valores[aux]*0.1

svalores[6]=np.sqrt(valores[6])
svalores[7]=np.sqrt(valores[7])
svalores[8]=np.sqrt(valores[8])
svalores[9]=np.array([0.3]*len(valores[9]))

m=10
n=6
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])


Tabla_latex(np.array([list(valores[aux])]+list(valores[n:])),
            np.array([list(svalores[aux])]+list(svalores[n:])),
            headers=["$x_{\\text{Fe}}$ (mm)"]+header[n:],caption="Medidas de atenuación blanda usando únicamente placas de hierro",
            filename="Tablas/Hierro.tex",label="Tab:hierro",columnformat="cccccccccccccccccccccc")


print(valores)
plt.figure()
plt.errorbar(valores[aux,:],valores[len(valores)-1,:],svalores[len(svalores)-1,:],svalores[aux,:],
    fmt='o',                       # círculo como marcador
    ecolor='cornflowerblue',                  # color de la barra de error
    capsize=5,                     # "sombrero" en los extremos
    markersize=8,
    markerfacecolor='darkblue',        # color del círculo
    markeredgecolor='black',       # borde negro
    markeredgewidth=1.5            # grosor del borde
)
plt.xlabel("x [mm]")
plt.ylabel("$n_{12}$ [#/s]")
plt.savefig("Graficas/Atenuacion_Fe.pdf",bbox_inches="tight")


##################### PLOMO 1-10 HIERRO 20 ################3
   
df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Atenuacion_2")
aux=0
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[aux])))

valores[aux]=valores[aux]*dPb
svalores[aux]=valores[aux]*0.1

svalores[6]=np.sqrt(valores[6])
svalores[7]=np.sqrt(valores[7])
svalores[8]=np.sqrt(valores[8])
svalores[9]=np.array([0.3]*len(valores[9]))

m=10
n=6
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])


Tabla_latex(np.array([list(valores[aux])]+list(valores[n:])),
            np.array([list(svalores[aux])]+list(svalores[n:])),
            headers=["$x_{\\text{Pb}}$ (mm)"]+header[n:],caption="Medidas de atenuación dura usando únicamente placas de plomo con 20 de hierro",
            filename="Tablas/Plomo.tex",label="Tab:plomo_1",columnformat="cccccccccccccccccccccc")


print(valores)
plt.figure()
plt.errorbar(valores[aux,:],valores[len(valores)-1,:],svalores[len(svalores)-1,:],svalores[aux,:],
    fmt='o',                       # círculo como marcador
    ecolor='cornflowerblue',                  # color de la barra de error
    capsize=5,                     # "sombrero" en los extremos
    markersize=8,
    markerfacecolor='darkblue',        # color del círculo
    markeredgecolor='black',       # borde negro
    markeredgewidth=1.5            # grosor del borde
)
plt.xlabel("x [mm]")
plt.ylabel("$n_{12}$ [#/s]")
plt.savefig("Graficas/Atenuacion_Pb.pdf",bbox_inches="tight")

##################### PLOMO 1-10 HIERRO 0 ################3
   
df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Atenuacion_3")
aux=0
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[aux])))

valores[aux]=valores[aux]*dPb
svalores[aux]=valores[aux]*0.1

svalores[6]=np.sqrt(valores[6])
svalores[7]=np.sqrt(valores[7])
svalores[8]=np.sqrt(valores[8])
svalores[9]=np.array([0.3]*len(valores[9]))

m=10
n=6
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])


Tabla_latex(np.array([list(valores[aux])]+list(valores[n:])),
            np.array([list(svalores[aux])]+list(svalores[n:])),
            headers=["$x_{\\text{Pb}}$ (mm)"]+header[n:],caption="Medidas de atenuación dura usando únicamente placas de plomo sin laminas de hierro",
            filename="Tablas/Plomo2.tex",label="Tab:plomo_2",columnformat="cccccccccccccccccccccc")


print(valores)
plt.figure()
plt.errorbar(valores[aux,:],valores[len(valores)-1,:],svalores[len(svalores)-1,:],svalores[aux,:],
    fmt='o',                       # círculo como marcador
    ecolor='cornflowerblue',                  # color de la barra de error
    capsize=5,                     # "sombrero" en los extremos
    markersize=8,
    markerfacecolor='darkblue',        # color del círculo
    markeredgecolor='black',       # borde negro
    markeredgewidth=1.5            # grosor del borde
)
plt.xlabel("x [mm]")
plt.ylabel("$n_{12}$ [#/s]")
plt.savefig("Graficas/Atenuacion_Pb2.pdf",bbox_inches="tight")