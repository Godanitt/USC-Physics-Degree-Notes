import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import csv


def formato(valor,decimales=3,ss=1,flag=True):
    if flag: 
        if isinstance(valor, (int, float, np.number)):  # Acepta números reales y NumPy
            return  f"\\num{{{valor:.{decimales}f}({ss:.{decimales}f})}}"
        else:
            valor=float(valor)
            return  f"\\num{{{valor:.{decimales}e}({ss:.{decimales}f})}}"
    else:     
        if isinstance(valor, (int, float, np.number)):  # Acepta números reales y NumPy
            return  f"\\num{{{int(valor):5d}}}"
        else:
            valor=float(valor)
            return  f"\\num{{{int(valor):5d}}}"

def Tabla_latex(valores,svalores,headers,filename,caption,label,columnformat,flag=[True]):
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
            valor = formato(col[i], 10, incert[i], flag=flag[j])
            fila_formateada.append(valor)
        valores_formateados.append(fila_formateada)
        j+=1    

    df = pd.DataFrame({h: v for h, v in zip(headers, valores_formateados)})
    
    tabla_latex=df.to_latex(column_format=columnformat,
            header=True,
            index=False,
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

def tasa_real(N12,sN12,N1,sN1,N2,sN2):
    tau=13.74*10**(-6)
    stau=0.57*10**(-6)
    
    Nacc=2*N1*N2*tau
    sNacc=np.sqrt((stau*N1*N2)**2+(tau*sN1*N2)**2+(tau*N1*sN2)**2)
    Nr=N12-Nacc
    sNr=np.sqrt(sNacc**2+sN12**2)
    return Nacc,sNacc,Nr,sNr




def Tabla_csv(x, sx, y, sy, headers, nombre_archivo="salida.csv"):
    """ Saca una tabla a csv a partir de los valores x e y y su incertidumbre sx y sy

    Args:
        x (array): _description_
        sx (array): _description_
        y (array): _description_
        sy (array): _description_
        headers (array): 
        nombre_archivo (string): 
    """
    if not (len(x) == len(sx) == len(y) == len(sy)):
        raise ValueError("Todos los arrays deben tener la misma longitud.")

    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for i in range(len(x)):
            writer.writerow([x[i], sx[i], y[i], sy[i]])

   # print(f"Archivo guardado como: {nombre_archivo}")
    import numpy as np

def media_ponderada(x, sigma):
    """
    Calcula la media ponderada y su incertidumbre.

    Parámetros:
    x     : array-like. Valores medidos.
    sigma : array-like. Incertidumbres de cada valor.

    Retorna:
    (media_ponderada, incertidumbre_ponderada)
    """
    x = np.array(x)
    sigma = np.array(sigma)
    
    pesos = 1 / sigma**2
    media = np.sum(x * pesos) / np.sum(pesos)
    incertidumbre = np.sqrt(1 / np.sum(pesos))
    
    return media, incertidumbre
