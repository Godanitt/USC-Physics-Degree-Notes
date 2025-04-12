import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Tabla_Latex import *
    
df = pd.read_excel("Datos Crudos/Rayos_Cosmicos.ods", engine="odf", sheet_name="Angulos")
aux=0
header = df.columns.tolist()
valores = df.values.T.tolist()  # Transponer para que cada sublista sea una columna
valores=np.array(valores)
svalores =  np.ones(shape=(len(valores[:]),len(valores[0])))

valores[aux]=valores[aux]
svalores[aux]=2*svalores[aux]

aux=2
svalores[4+aux]=np.sqrt(valores[4+aux])
svalores[4+aux+1]=np.sqrt(valores[4+aux+1])
svalores[4+aux+2]=np.sqrt(valores[4+aux+2])
svalores[4+aux+3]=np.array([0.3]*len(valores[4+aux+3]))

m=aux+4+4
n=aux+4
for i in range(3):
    valores[m+i],svalores[m+i]=tasa(valores[n+i],svalores[n+i],valores[n+3],svalores[n+3])

aux=0
Tabla_latex(np.array([list(valores[aux])]+list(valores[n:])),
            np.array([list(svalores[aux])]+list(svalores[n:])),
            headers=["$d$ (cm)"]+header[n:],caption="Medidas de coincidencias a una distancia $33.3$ cm entre los detectores a diferentes ángulos.",
            filename="Tablas/Angulos.tex",label="Tab:angulo",columnformat="cccccccccccccccccccccc")


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
plt.xlabel("$\theta$ [$^{\circ}$]")
plt.ylabel("$n_{12}$ [#/s]")
plt.savefig("Graficas/Angulos.pdf",bbox_inches="tight")