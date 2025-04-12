import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Tabla_Latex import *
    
df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Ventana de Coincidencias")

def tasa(N,sN,t,st):
    """ Devuelve los valores de la tasa y la incertidumbre de la tasa.

    Args:
        N (_type_): _description_
        sN (_type_): _description_
        t (_type_): _description_
        st (_type_): _description_
    """
    valor=N/t
    uvalor=np.sqrt((sN/t)**2+(st*N/t**2)**2)
    return valor,uvalor
    

header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[0])))

svalores[4]=np.sqrt(valores[4])
svalores[5]=np.sqrt(valores[5])
svalores[6]=np.sqrt(valores[6])
svalores[7]=np.array([0.3]*len(valores[0]))
print(valores)

for i in range(3):
    
    valores[8+i],svalores[8+i]=tasa(valores[4+i],svalores[4+i],valores[7],svalores[7])

valores[11]=valores[10]/(2*valores[8]*valores[9])*10**6
svalores[11]=np.sqrt((svalores[10]/(2*valores[8]*valores[9]))**2+
                     (svalores[9]*valores[10]/(2*valores[8]*(valores[9])**2))**2+
                     (svalores[8]*valores[10]/(2*(valores[8])**2*valores[9]))**2)
svalores[11]=svalores[11]*10**6
print(valores)
Tabla_latex(valores[4:],svalores[4:],
            headers=header[4:],caption="Ventana de coincidencias",
            filename="Tablas/Ventana.tex",label="Tab:ventana_01",columnformat="cccccccccccccccccccccc")