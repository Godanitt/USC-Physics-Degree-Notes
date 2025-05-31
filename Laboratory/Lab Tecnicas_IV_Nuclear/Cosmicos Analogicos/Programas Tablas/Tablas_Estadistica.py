import sys
import os
from scipy.stats import poisson,chisquare,norm
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)


def formato(valor,decimales=1,ss=1,flag=True,typ="float"):
    if flag: 
        if isinstance(valor, (int, float, np.number)):  # Acepta números reales y NumPy
            return  f"\\num{{{valor:.{decimales}f}({ss:.{decimales}f})}}"
        else:
            valor=float(valor)
            return  f"\\num{{{valor:.{decimales}e}({ss:.{decimales}f})}}"
    elif not(flag) and typ == "float":     
        if isinstance(valor, (int, float, np.number)):  # Acepta números reales y NumPy
            return  f"\\num{{{valor:.{decimales}f}}}"
        else:
            valor=float(valor)
            return  f"\\num{{{valor:.{decimales}f}}}"
    else:
        if isinstance(valor, (int, float, np.number)):  # Acepta números reales y NumPy
            return  f"\\num{{{int(valor):5d}}}"
        else:
            valor=float(valor)
            return  f"\\num{{{int(valor):5d}}}"

def Tabla_latex(index,valores,svalores,headers,filename,caption,label,columnformat,flag=[True],typ=["int"]):
    """  
    Summary: dados unos valores y su incertidumbre, devuelve una tabla de latex.

    Args:
        valores (array): _description_
        svalores (array): _description_
        headers (array): _description_
        filename (string): _description_
        caption (string): _description_
        label (string): _description_
        columnformat (string): _description_
        flag (bool): _description_
        """
        
    if len(flag)==1:
        flag=flag*len(valores)
        
        
    valores_formateados = []
    j=0
    for col, incert in zip(valores, svalores):
        fila_formateada = []
        for i in range(len(col)):
            valor = formato(col[i], 2, incert[i], flag=flag[j],typ=typ[j])
            fila_formateada.append(valor)
        valores_formateados.append(fila_formateada)
        j+=1    

    df = pd.DataFrame({h: v for h, v in zip(headers, valores_formateados)},index=index)
    
    tabla_latex=df.to_latex(column_format=columnformat,
            header=True,
            index=True,
            caption=caption,
            label=label,
            position="H"
            )
    tabla_completa = "\\begin{center}\n"
    tabla_completa += tabla_latex
    tabla_completa += "\\end{center}\n"

    # Guardar en archivo
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tabla_completa)

    print(f"Tabla guardada en '{filename}'")
    
 ########################################################   
 ########################################################
 ########################################################
 ########################################################
 ########################################################
 ########################################################
    
def agrupar_sumas(arr, grupo):
    resultado = []
    for i in range(0, len(arr), grupo):
        suma = sum(arr[i:i+grupo])
        resultado.append(suma)
    return resultado

def chi2_fun(bins,cuentas,NP):
    cuentasfinal=np.array([])
    NPfinal=np.array([])
    chi2i=np.array([])
    lims=np.array([])
    
    sto=0
    flag=True
    NPaux=0
    cuentasaux=0
    for i in range(len(bins)):
        sto+=cuentas[i]
        if sto<6 and flag:
            cuentasaux+=cuentas[i]
            NPaux+=NP[i]
            min="%i-"%bins[i]
            flag=False
            
        if sto<6 and not(flag):
            cuentasaux+=cuentas[i]
            NPaux+=NP[i]
            flag=False
        if sto>=6 and not(flag):
            cuentasaux+=cuentas[i]
            NPaux+=NP[i]
                   
            lims=np.append(lims,min+"%i"%bins[i]) 
            chi2=((cuentasaux-NPaux)**2)/(cuentasaux)
            
            chi2i=np.append(chi2i,chi2)
            NPfinal=np.append(NPfinal,NPaux)
            cuentasfinal=np.append(cuentasfinal,cuentasaux)
            
    
            sto=0
            flag=True
            NPaux=0
            cuentasaux=0
            sto=0
            
        if sto>=6 and (flag):
            chi2=((cuentas[i]-NP[i])**2)/(cuentas[i])
            
            lims=np.append(lims,"%i"%bins[i]) 
            chi2i=np.append(chi2i,chi2)
            NPfinal=np.append(NPfinal,NP[i])
            cuentasfinal=np.append(cuentasfinal,cuentas[i])
            
            sto=0
            flag=True
            NPaux=0
            cuentasaux=0
            sto=0
            
        if((i==len(bins)-1) and sto<6):
            sto=0
            sto=0
            flag=True
            NPaux=0
            cuentasaux=0
            flag2=True
            for j in range(len(bins)):
                sto+=cuentas[i-j]
                if flag and sto>5:
                    cuentasaux+=cuentas[i-j]
                    NPaux+=NP[i-j]
                    
                    chi2=((cuentasaux-NPaux)**2)/(cuentasaux)
                    
                    chi2i[len(chi2i)-1]=chi2
                    lims[len(lims)-1]="%i-%i"%(i-j,i)
                    NPfinal[len(NPfinal)-1]=NPaux
                    cuentasfinal[len(cuentasfinal)-1]=cuentasaux
                    
                    flag=False
                elif flag:    
                    cuentasaux+=cuentas[i-j]
                    NPaux+=NP[i-j]
                else:
                    continue 
                   
    
    chi2=np.sum(chi2i)
    ndf=len(chi2i)-2
    
    return chi2,ndf,chi2i,lims,NPfinal,cuentasfinal

########################################################
########################################################
########################################################
########################################################
########################################################
    
def fun_histo(diferencia,s,capt=""):  
    valor=30
    Diferencia_real=np.array([])
    if capt == "manual":
        valor = 21
    elif capt == "m":
        if s == 1:
            valor = 4
        elif s == 2:
            valor = 7    
        elif s == 5:
            valor = 14
        elif s == 7:
            valor = 21
    elif capt == "":
        if s == 1:
            valor = 30
        elif s == 2:
            valor = 40
        elif s == 5:
            valor = 80
        elif s == 10:
            valor = 130

    # Valor por defecto si no se asignó en ningún bloque anterior
    if valor is None:
        print(f"[WARNING] No se asignó un valor para capt={capt}, s={s}. Usando valor=30 por defecto.")
        valor = 30

    valor += 2
            
    valor=valor+2
    diferencia=agrupar_sumas(diferencia,s)    
    for i in range(0,len(diferencia)-1):
        if  -10000+(valor)<(diferencia[i])<-10000:
            Diferencia_real=np.append(Diferencia_real,diferencia+9999)
        elif (diferencia[i])<0:
            continue
        elif (diferencia[i]>valor):
            continue
        else:    
            Diferencia_real=np.append(Diferencia_real,diferencia[i])
            
    datos = Diferencia_real    
    
    
    frecuencias, bordes, parches = plt.hist(datos, bins=range(0,valor), edgecolor='black', align='left')
    
    bins=bordes[0:len(bordes)-1]
    
    cuentas=np.sum(frecuencias)
    media = np.dot(frecuencias,bins)/cuentas
    
    NP = cuentas*poisson.pmf(bins,media)    
    NPgauss = cuentas*norm.pdf(bins, loc=media, scale=np.sqrt(media))   
    
    chi2,ndf,chi2i,lims,NPfinal,cuentasfinal=chi2_fun(bins,frecuencias,NP)
    chi2gauss,ndfgauss,chi2igauss,limsgauss,NPfinalgauss,cuentasfinalgauss=chi2_fun(bins,frecuencias,NPgauss)
    

    plt.figure()
    plt.hist(datos, bins=range(0,valor),color="cornflowerblue", edgecolor='white', align='left')
    plt.plot(bins,NP,".",color="red",label="Poisson")
    plt.plot(bins,NPgauss,".",color="green",label="Gauss")
    plt.legend(loc="lower right")
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.text(valor*0.7, max(frecuencias)*0.7, 'Cuentas = %i \n $\\mu$ = %.2f  \n ndf=%i \n Poisson: \n $\\chi^2=$ %.2f \n Gauss: \n $\\chi^2=%.2f$ '%(cuentas,media,ndf,chi2,chi2gauss),
            bbox=dict(facecolor='white', edgecolor='black'),
            fontsize=10)

    plt.savefig("Graficas/Histo_"+"%i"%s+capt+"s.pdf",bbox_inches="tight")
    
    index=lims
    valores=np.array([cuentasfinal,NPfinal,chi2i,NPfinalgauss,chi2igauss])
    svalores=valores
    headers=["$h(x_j)$","$N \\cdot P_{\\text{poisson}} (x_j)$","$\\chi^2_{\\text{poisson}}(x_j)$","$N \\cdot P_{\\text{gauss}} (x_j)$","$\\chi^2_{\\text{gauss}}(x_j)$"]
    filename="Tablas/Histo_%i"%s+capt+"s.tex"
    caption="Tabla para %i s con $\\mu=%.2f$, $N=%i$, $\\chi^2_{\\text{Poisson}}=%.2f$  y $\\chi^2_{\\text{Gauss}}=%.2f$"%(s,media,cuentas,chi2,chi2gauss)
    label="Tab:histo_"+capt+"_%is"%s
    flag=[False,False,False,False,False]
    typ=["int","float","float","float","float"]
    Tabla_latex(index,valores,svalores,headers,filename,caption,label, "cccccccc",flag=flag,typ=typ)
    print("Histograma ",s,capt," hecho")
    
 
    

########################################################
########################################################
########################################################
########################################################
########################################################
########################################################
    
    
    

# Primera gráfica: 

df = pd.read_csv("Programas Tablas/Lecturas_geiger.csv")

tiempo = df["Tiempo"].to_numpy()
cuentas = df["Valor"].to_numpy()
Diferencia = df["Diferencia"].to_numpy()

Diferencia=np.array(Diferencia)
fun_histo(Diferencia,1,capt="manual")


    
df = pd.read_csv("Programas Tablas/resultados_geiger_completo.csv")
tiempo = df["Tiempo"].to_numpy()
cuentas = df["Valor"].to_numpy()
Diferencia = df["Diferencia"].to_numpy()

fun_histo(Diferencia,1)
fun_histo(Diferencia,2)
fun_histo(Diferencia,5)
fun_histo(Diferencia,10)


    
df = pd.read_csv("Programas Tablas/Resultados_geiger_completo_2.csv")
tiempo = df["Tiempo"].to_numpy()
cuentas = df["Valor"].to_numpy()
Diferencia = df["Diferencia"].to_numpy()


fun_histo(Diferencia,1,capt="m")
fun_histo(Diferencia,2,capt="m")
fun_histo(Diferencia,5,capt="m")
fun_histo(Diferencia,7,capt="m")