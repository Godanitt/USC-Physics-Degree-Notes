import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Tabla_Latex import *
    
df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Eficiencia Distancia")
aux=0
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[0])))

valores[aux]=valores[aux]+1+1.795
svalores[aux]=svalores[aux]*0.21

aux=1
svalores[4+aux]=np.sqrt(valores[4+aux])
svalores[4+aux+1]=np.sqrt(valores[4+aux+1])
svalores[4+aux+2]=np.sqrt(valores[4+aux+2])
svalores[4+aux+3]=np.array([0.13]*len(valores[4+aux+3]))


m=aux+4+4
n=aux+4
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])

nacc,snacc,nr,snr=tasa_real(valores[m+2],svalores[m+2],valores[m+1],svalores[m+1],valores[m],svalores[m])

aux=0
x=np.array([list(valores[aux])]+list(valores[n:m+2])+[list(nacc)]+[list(nr)])
sx= np.array([list(svalores[aux])]+list(svalores[n:m+2])+[list(snacc)]+[list(snr)])
header= ["$d_{\\text{real}}$ (cm)"]+header[n:m+2]+["$n_{acc}$ [s$^{-1}$]","$n_{r}$ [s$^{-1}$]"]
print(x)
Tabla_latex(x,sx,headers=header,caption="Medidas de coincidencias a una distancia $d$ entre los detectores.",
            filename="Tablas/Distancia.tex",label="Tab:distancia",columnformat="cccccccccccccccccccccc")

Tabla_csv(valores[aux],svalores[aux],nr,snr,headers=["d [cm]","u(x) [cm]", "nr [#/s]", "u(nr) [#/s]"],nombre_archivo="GraficasROOT/Distancias.csv")


plt.figure()
plt.errorbar(valores[aux,:],nr,snr,svalores[aux,:],
    fmt='o',                       # círculo como marcador
    ecolor='cornflowerblue',                  # color de la barra de error
    capsize=5,                     # "sombrero" en los extremos
    markersize=8,
    markerfacecolor='darkblue',        # color del círculo
    markeredgecolor='black',       # borde negro
    markeredgewidth=1.5            # grosor del borde
)
plt.xlabel("$d$ [cm]")
plt.ylabel("$n_{12}$ [#/s]")
plt.savefig("Graficas/Distancias.pdf",bbox_inches="tight")


import pandas as pd

# Cargar el archivo CSV proporcionado
file_path = "Datos Crudos/Eficiencias.csv"
df = pd.read_csv(file_path)

# Guardar cada columna en un array independiente
distancia = df['distancia'].values
sim_n1 = df['sim_n1'].values
err_sim_n1 = df['err_sim_n1'].values
sim_n2 = df['sim_n2'].values
err_sim_n2 = df['err_sim_n2'].values

x1=np.array([distancia,nr/nr[0],sim_n1/nr[0],sim_n2/nr[0]])
sx1=np.array([svalores[0],snr/nr[0],err_sim_n1/nr[0],err_sim_n2/nr[0]])
header1= ["$d_{\\text{real}}$ (cm)","$\epsilon_{g}$","$\epsilon_{\\text{MC}}^1$","$\epsilon_{\\text{MC}}^2$"]

Tabla_latex(x1,sx1,headers=header1,caption="Medidas de la eficiencia.",
            filename="Tablas/Eficiencia.tex",label="Tab:montecarlo",columnformat="cccccccccccccccccccccc")
