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


svalores[aux]=0.014*valores[aux]
valores[aux]=valores[aux]*dFe


svalores[6]=np.sqrt(valores[6])
svalores[7]=np.sqrt(valores[7])
svalores[8]=np.sqrt(valores[8])
svalores[9]=np.array([0.13]*len(valores[9]))

m=10
n=6
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])


nacc,snacc,nr,snr=tasa_real(valores[m+2],svalores[m+2],valores[m+1],svalores[m+1],valores[m],svalores[m])

x=np.array([list(valores[aux]*7.874/10)]+list(valores[n:m+2])+[list(nacc)]+[list(nr)])
sx= np.array([list(svalores[aux]*7.874/10)]+list(svalores[n:m+2])+[list(snacc)]+[list(snr)])
header= ["$x_{\\text{Fe}}$ (kg/cm$^{-2}$)"]+header[n:m+2]+["$n_{acc}$ [s$^{-1}$]","$n_{r}$ [s$^{-1}$]"]

aux=1
Tabla_latex(x,sx,headers=header,caption="Medidas de atenuación blanda usando únicamente placas de hierro",
            filename="Tablas/Hierro.tex",label="Tab:hierro",columnformat="cccccccccccccccccccccc")

Tabla_csv(valores[aux]*7.874/10,svalores[aux]*7.874/10,nr,snr,headers=["x [mm]","u(x) [mm]", "nr [#/s]", "u(nr) [#/s]"],nombre_archivo="GraficasROOT/Hierro.csv")





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
plt.xlabel("x [mm]")
plt.ylabel("$n_{r}$ [#/s]")
plt.savefig("Graficas/Atenuacion_Fe2.pdf",bbox_inches="tight")


##################### PLOMO 1-10 HIERRO 20 ################3
   
df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Atenuacion_2")
aux=0
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[aux])))

svalores[aux]=0.014*valores[aux]
valores[aux]=valores[aux]*dPb

svalores[6]=np.sqrt(valores[6])
svalores[7]=np.sqrt(valores[7])
svalores[8]=np.sqrt(valores[8])
svalores[9]=np.array([0.13]*len(valores[9]))

m=10
n=6
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])

nacc,snacc,nr,snr=tasa_real(valores[m+2],svalores[m+2],valores[m+1],svalores[m+1],valores[m],svalores[m])

x=np.array([list(valores[aux]*11.340/10)]+list(valores[n:m+2])+[list(nacc)]+[list(nr)])
sx= np.array([list(svalores[aux]*11.340/10)]+list(svalores[n:m+2])+[list(snacc)]+[list(snr)])
header= ["$x_{\\text{Pb}}$ (kg/cm$^{-2}$)"]+header[n:m+2]+["$n_{acc}$ [s$^{-1}$]","$n_{r}$ [s$^{-1}$]"]

aux=0
Tabla_latex(x,sx,headers=header,caption="Medidas de atenuación dura usando únicamente placas de plomo con 20 de hierro",
            filename="Tablas/Plomo.tex",label="Tab:plomo_1",columnformat="cccccccccccccccccccccc")


Tabla_csv(valores[aux]*11.340/10,svalores[aux]*11.340/10,nr,snr,headers=["x [mm]","u(x) [mm]", "nr [#/s]", "u(nr) [#/s]"],nombre_archivo="GraficasROOT/HierroPlomo.csv")


plt.figure()
plt.errorbar(valores[aux,:]*11.340/10,nr,snr,svalores[aux,:],
    fmt='o',                       # círculo como marcador
    ecolor='cornflowerblue',                  # color de la barra de error
    capsize=5,                     # "sombrero" en los extremos
    markersize=8,
    markerfacecolor='darkblue',        # color del círculo
    markeredgecolor='black',       # borde negro
    markeredgewidth=1.5            # grosor del borde
)
plt.xlabel("x [mm]")
plt.ylabel("$n_{r}$ [#/s]")
plt.savefig("Graficas/Atenuacion_Pb.pdf",bbox_inches="tight")

##################### PLOMO 1-10 HIERRO 0 ################3
   
df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Atenuacion_3")
aux=0
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[aux])))

svalores[aux]=0.014*valores[aux]
valores[aux]=valores[aux]*dPb


svalores[6]=np.sqrt(valores[6])
svalores[7]=np.sqrt(valores[7])
svalores[8]=np.sqrt(valores[8])
svalores[9]=np.array([0.13]*len(valores[9]))

m=10
n=6
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])

nacc,snacc,nr,snr=tasa_real(valores[m+2],svalores[m+2],valores[m+1],svalores[m+1],valores[m],svalores[m])

x=np.array([list(valores[aux])]+list(valores[n:m+2])+[list(nacc)]+[list(nr)])
sx= np.array([list(svalores[aux])]+list(svalores[n:m+2])+[list(snacc)]+[list(snr)])
header= ["$x_{\\text{Pb}}$ (kg/cm$^{-2}$)"]+header[n:m+2]+["$n_{acc}$ [s$^{-1}$]","$n_{r}$ [s$^{-1}$]"]

aux=0
Tabla_latex(x,sx,headers=header,caption="Medidas de atenuación dura usando únicamente placas de plomo sin planchas de hierro",
            filename="Tablas/Plomo2.tex",label="Tab:plomo_2",columnformat="cccccccccccccccccccccc")


Tabla_csv(valores[aux],svalores[aux],nr,snr,headers=["x [mm]","u(x) [mm]", "nr [#/s]", "u(nr) [#/s]"],nombre_archivo="GraficasROOT/Plomo.csv")


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
plt.xlabel("x [kg/cm$^{-2}$]")
plt.ylabel("$n_{r}$ [#/s]")
plt.savefig("Graficas/Atenuacion_Pb2.pdf",bbox_inches="tight")

##############

print(7.874/(0.00562*10))

print(7.874*(0.0012*10)/((0.00562*10)**2))


print("****** Plomo  ******")

print(11.340/(0.00461*10))

print(11.340*(0.00092*10)/((0.00461*10)**2))


print("****** Plomo y hierro  ******")

print(11.340/(0.0017*10))

print(11.340*(0.00056*10)/((0.0017*10)**2))

print("****************************")

########### CELTIA #################################

df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Atenuacion_4")
aux=0
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[aux])))

svalores[aux]=0.014*valores[aux]
valores[aux]=valores[aux]*85


svalores[6]=np.sqrt(valores[6])
svalores[7]=np.sqrt(valores[7])
svalores[8]=np.sqrt(valores[8])
svalores[9]=np.array([0.13]*len(valores[9]))

m=10
n=6
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])

nacc,snacc,nr,snr=tasa_real(valores[m+2],svalores[m+2],valores[m+1],svalores[m+1],valores[m],svalores[m])

x=np.array([list(valores[aux])]+list(valores[n:m+2])+[list(nacc)]+[list(nr)])
sx= np.array([list(svalores[aux])]+list(svalores[n:m+2])+[list(snacc)]+[list(snr)])
header= ["$x_{\\text{Pb}}$ (mm)"]+header[n:m+2]+["$n_{acc}$ [s$^{-1}$]","$n_{r}$ [s$^{-1}$]"]

aux=0
Tabla_latex(x,sx,headers=header,caption="Medidas de atenuación dura usando 20 láminas de hierro, 10 planchas de plomo y bloques de plomo. Datos de Celtia Jabares.",
            filename="Tablas/PlomoCeltia.tex",label="Tab:plomoCeltia",columnformat="cccccccccccccccccccccc")


Tabla_csv(valores[aux],svalores[aux],nr,snr,headers=["x [mm]","u(x) [mm]", "nr [#/s]", "u(nr) [#/s]"],nombre_archivo="GraficasROOT/PlomoCeltia.csv")


df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Atenuacion_5")
aux=1
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[0])))


svalores[aux]=0.014*valores[aux]
valores[aux]=valores[aux]*dFe


svalores[6]=np.sqrt(valores[6])
svalores[7]=np.sqrt(valores[7])
svalores[8]=np.sqrt(valores[8])
svalores[9]=np.array([0.13]*len(valores[9]))

m=10
n=6
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])


nacc,snacc,nr,snr=tasa_real(valores[m+2],svalores[m+2],valores[m+1],svalores[m+1],valores[m],svalores[m])

x=np.array([list(valores[aux])]+list(valores[n:m+2])+[list(nacc)]+[list(nr)])
sx= np.array([list(svalores[aux])]+list(svalores[n:m+2])+[list(snacc)]+[list(snr)])
header= ["$x_{\\text{Fe}}$ (mm)"]+header[n:m+2]+["$n_{acc}$ [s$^{-1}$]","$n_{r}$ [s$^{-1}$]"]

aux=1
Tabla_latex(x,sx,headers=header,caption="Medidas de atenuación blanda usando únicamente placas de hierro,. Datos de Celtia Jabares.",
            filename="Tablas/HierroCeltia.tex",label="Tab:hierroceltia",columnformat="cccccccccccccccccccccc")

Tabla_csv(valores[aux],svalores[aux],nr,snr,headers=["x [mm]","u(x) [mm]", "nr [#/s]", "u(nr) [#/s]"],nombre_archivo="GraficasROOT/HierroCeltia.csv")



##############

print("****** Hierro  ******")

print(7.874/(0.00562*10))

print(7.874*(0.0012*10)/((0.00562*10)**2))


print("****** Plomo  ******")

print(11.340/(0.00461*10))

print(11.340*(0.00092*10)/((0.00461*10)**2))


print("****** Plomo y hierro  ******")

print(11.340/(0.0017*10))

print(11.340*(0.00056*10)/((0.0017*10)**2))

print("****** Hierro  Celtia ******")

print(7.874/(0.0242*10))

print(7.874*(0.0021*10)/((0.018*10)**2))

      
print("****** Plomo y hierro Celtia  ******")

print(11.340/(0.000975*10))

print(11.340*(0.00013*10)/((0.000975*10)**2))

