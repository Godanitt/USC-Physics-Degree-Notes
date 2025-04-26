import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Tabla_Latex import *
    
df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Caracterizacion U")

    
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[0])))

svalores[3]=np.sqrt((abs(valores[3])/100+np.array([0.002]*len(valores[3])))**2+(valores[3]/100)**2)
print("**********",svalores[3])
svalores[4]=np.sqrt(valores[4])
svalores[5]=np.sqrt(valores[5])
svalores[6]=np.sqrt(valores[6])
svalores[7]=np.array([0.13]*len(valores[0]))
print(valores)

for i in range(3):
    valores[8+i],svalores[8+i]=tasa(valores[4+i],svalores[4+i],valores[7],svalores[7])


nacc,snacc,nr,snr=tasa_real(valores[10],svalores[10],valores[8],svalores[8],valores[9],svalores[9])
n=len(valores)

x=np.array([list(valores[3])]+list(valores[4:n-1])+[list(nacc)]+[list(nr)])
sx= np.array([list(svalores[3])]+list(svalores[4:n-1])+[list(snacc)]+[list(snr)])
header= [header[3]]+header[4:n-1]+["$n_{acc}$ [s$^{-1}$]","$n_{r}$ [s$^{-1}$]"]


Tabla_latex(x,sx,headers=header,caption="Medidas variando el alto voltaje $U_1$.",
            filename="Tablas/PlateuU.tex",label="Tab:plateu_U",columnformat="cccccccccccccccccccccc")

Tabla_csv(valores[3],svalores[3],nr,snr,headers=["U [kV]","u(U) [kV]", "n12 [#/s]", "u(n12) [#/s]"],nombre_archivo="GraficasROOT/PlateuU.csv")




#################################################################

df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Caracterizacion V")

header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[0])))

svalores[2]=np.sqrt((valores[2]/100+np.array([0.002]*len(valores[2])))**2+(valores[2]/100)**2)
svalores[4]=np.sqrt(valores[4])
svalores[5]=np.sqrt(valores[5])
svalores[6]=np.sqrt(valores[6])
svalores[7]=np.array([0.13]*len(valores[0]))
print(valores)

for i in range(3):
    valores[8+i],svalores[8+i]=tasa(valores[4+i],svalores[4+i],valores[7],svalores[7])

nacc,snacc,nr,snr=tasa_real(valores[10],svalores[10],valores[8],svalores[8],valores[9],svalores[9])
n=len(valores)

x=np.array([list(valores[2])]+list(valores[4:n-1])+[list(nacc)]+[list(nr)])
sx= np.array([list(svalores[2])]+list(svalores[4:n-1])+[list(snacc)]+[list(snr)])
header= [header[2]]+header[4:n-1]+["$n_{acc}$ [s$^{-1}$]","$n_{r}$ [s$^{-1}$]"]


Tabla_latex(x,sx,headers=header,caption="Medidas variando el alto voltaje $V_1$.",
            filename="Tablas/PlateuV.tex",label="Tab:plateu_V",columnformat="cccccccccccccccccccccc")

Tabla_csv(valores[2],svalores[2],nr,snr,headers=["V [kV]","u(V) [kV]", "n12 [#/s]", "u(n12) [#/s]"],nombre_archivo="GraficasROOT/PlateuV.csv")
