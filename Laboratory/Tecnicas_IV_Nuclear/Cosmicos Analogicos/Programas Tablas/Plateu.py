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

svalores[3]=np.array([0.01]*len(valores[0]))
svalores[4]=np.sqrt(valores[4])
svalores[5]=np.sqrt(valores[5])
svalores[6]=np.sqrt(valores[6])
svalores[7]=np.array([0.3]*len(valores[0]))
print(valores)

for i in range(3):
    valores[8+i],svalores[8+i]=tasa(valores[4+i],svalores[4+i],valores[7],svalores[7])


print(valores)
Tabla_latex(np.array([list(valores[3])]+list(valores[4:])),
            np.array([list(svalores[3])]+list(svalores[4:])),
            headers=[header[3]]+header[4:],caption="Medidas fijando el voltaje umbral",
            filename="Tablas/PlateuU.tex",label="Tab:plateu_U",columnformat="cccccccccccccccccccccc")


df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Caracterizacion V")

header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[0])))

svalores[2]=np.array([0.01]*len(valores[0]))
svalores[4]=np.sqrt(valores[4])
svalores[5]=np.sqrt(valores[5])
svalores[6]=np.sqrt(valores[6])
svalores[7]=np.array([0.3]*len(valores[0]))
print(valores)

for i in range(3):
    valores[8+i],svalores[8+i]=tasa(valores[4+i],svalores[4+i],valores[7],svalores[7])


print(valores)
Tabla_latex(np.array([list(valores[2])]+list(valores[4:])),
            np.array([list(svalores[2])]+list(svalores[4:])),
            headers=[header[2]]+header[4:],caption="Medidas fijando el voltaje de ganancia",
            filename="Tablas/PlateuV.tex",label="Tab:plateu_V",columnformat="cccccccccccccccccccccc")
