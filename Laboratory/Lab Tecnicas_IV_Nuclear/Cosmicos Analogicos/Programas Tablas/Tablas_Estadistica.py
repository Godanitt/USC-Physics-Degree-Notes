import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Tabla_Latex import *
    
df = pd.read_csv("Programas Tablas/resultados_geiger_completo.csv")
print(df)
tiempo = df["Tiempo"].to_numpy()
cuentas = df["Valor"].to_numpy()
Diferencia = df["Diferencia"].to_numpy()

def agrupar_sumas(arr, grupo):
    resultado = []
    for i in range(0, len(arr), grupo):
        suma = sum(arr[i:i+grupo])
        resultado.append(suma)
    return resultado

    
def fun_histo(diferencia,s,nuevo=""):  
    Diferencia_real=np.array([])
    
    diferencia=agrupar_sumas(diferencia,s)    
    for i in range(0,len(diferencia)-1):
        if  -10000+(s*18)<(diferencia[i])<-10000:
            Diferencia_real=np.append(Diferencia_real,diferencia+9999)
        elif (diferencia[i])<0:
            continue
        elif (diferencia[i]>18*s):
            continue
        else:    
            Diferencia_real=np.append(Diferencia_real,diferencia[i])
            
    plt.figure()        
    plt.hist(Diferencia_real,bins=range(int(18*s)))
    plt.savefig("Graficas/Histo_%i"%s+nuevo+"s"+".pdf")
    
    cuentas, bins = np.histogram(Diferencia_real, 
                bins=range(0, int(max(Diferencia_real)+2)))

    tabla = pd.DataFrame({
        "Valor": bins[:-1],
        "Frecuencia": cuentas
    })
    
    bins=bins[:len(bins)-1]
    Tabla_latex(np.array([bins,cuentas]),
                np.array([bins,cuentas]),
                ["Frecuencia","Cuentas"],
                "Tablas/Histo_%i"%s+nuevo+"s.tex",
                "Valores del histograma %i"%s+nuevo+"s",
                "Tab:histo_%is"%s,
                "ccccc",
                flag=[False,False]
                )
    Tabla_csv(bins,cuentas,cuentas,cuentas,headers=["Bins","Cuentas","Cuentas","Cuentas"],nombre_archivo="GraficasROOT/Histo_%i"%s+nuevo+"s.csv")

fun_histo(Diferencia,1)
fun_histo(Diferencia,2)
fun_histo(Diferencia,5)
fun_histo(Diferencia,10)


    
df = pd.read_csv("Programas Tablas/Resultados_geiger_completo_2.csv")
print(df)
tiempo = df["Tiempo"].to_numpy()
cuentas = df["Valor"].to_numpy()
Diferencia = df["Diferencia"].to_numpy()


fun_histo(Diferencia,1,nuevo="m")
fun_histo(Diferencia,2,nuevo="m")
fun_histo(Diferencia,5,nuevo="m")
fun_histo(Diferencia,7,nuevo="m")