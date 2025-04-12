import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

def formato(valor,decimales=3,ss=1):
    if isinstance(valor, (int, float, np.number)):  # Acepta números reales y NumPy
        return  f"\\num{{{valor:.{decimales}f}({ss:.{decimales}f})}}"
    else:
        valor=float(valor)
        return  f"\\num{{{valor:.{decimales}e}({ss:.{decimales}f})}}"

def Tabla_latex(valores,svalores,headers,filename,caption,label,columnformat):
    """ 
    Args: dados unos valores y su incertidumbre, devuelve una tabla de latex.
    
        valores (array): _description_
        svalores (array): _description_
        headers (array): _description_
        filename (string): _description_
        caption (string): _description_
        label (string): _description_
        columnformat (string): _description_
    """
    valores_formateados = [
    [formato(col[i], 10, incert[i]) for i in range(len(col))]
    for col, incert in zip(valores, svalores)
    ]
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