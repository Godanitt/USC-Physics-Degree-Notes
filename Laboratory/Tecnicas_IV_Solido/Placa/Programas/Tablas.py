
import numpy as np
import pandas as pd
import matplotlib.pyplot as PARSE_DECLTYPES
def J(I,d,r):
  #  print(2*np.pi*r)
    return I/(d*2*np.pi*r)

def formato_seguro(valor, decimales=2):
    if isinstance(valor, (int, float, np.number)):  # Acepta números reales y NumPy
        return f"\\SI{{{valor:.{decimales}e}}}{{}}"
    elif valor in ("$\\overline{V}_+$", "$\\overline{V}_-$"):
        return str(valor)
    else:
        return str(valor)[:7]  # o "N/A" "\\SI{"+str(valor)[:7]+"}{}"

def generar_tabla_IVJ(I, V, J, caption="Mi caption", label="tab:mi_tabla", filename="tabla.tex"):
    # Crear DataFrame
    formato = f"{{:.{3}f}}"
    formato2 = f"{{:.{4}f}}"

    # Crear DataFrame con formato aplicado
    df = pd.DataFrame({
        r"$I$ [A]": [formato.format(x) for x in I],
        r"$V$ [mV]": [formato2.format(x) for x in V],
        r"$J$ [A/cm$^2$]": [formato.format(x) for x in J]
    })

    # Convertir a LaTeX
    tabla_latex = df.to_latex(index=False, escape=False, column_format="ccc")
    df = df.round(2)
    # Envolver con entorno table + caption + label
    tabla_completa = "\\begin{table}[h!]\n"
    tabla_completa += "    \\centering\n"
    tabla_completa += tabla_latex
    tabla_completa += f"    \\caption{{{caption}}}\n"
    tabla_completa += f"    \\label{{{label}}}\n"
    tabla_completa += "\\end{table}\n"

    # Guardar en archivo
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tabla_completa)

    print(f"Tabla guardada en '{filename}'")


def generar_tabla_Vpn(Vp,Vn, caption="Mi caption", label="tab:mi_tabla", filename="tabla.tex"):
    # Crear DataFrame
    # Crear DataFrame con formato aplicado
    df = pd.DataFrame({
        r"$V_+$ [mV]": [formato_seguro(x,3) for x in Vp],
        r"$V_-$ [mV]": [formato_seguro(x,3) for x in Vn],
    })
    df=df.T

    # Convertir a LaTeX
    tabla_latex = df.to_latex(index=True, escape=False,  header=False,column_format="c|cccc|ccc")
    # Envolver con entorno table + caption + label
    tabla_completa = "\\begin{table}[h!]\n"
    tabla_completa += "    \\centering\n"
    tabla_completa += tabla_latex
    tabla_completa += f"    \\caption{{{caption}}}\n"
    tabla_completa += f"    \\label{{{label}}}\n"
    tabla_completa += "\\end{table}\n"

    # Guardar en archivo
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tabla_completa)

    print(f"Tabla guardada en '{filename}'")
    

def generar_tabla_S(S,R, caption="Mi caption", label="tab:mi_tabla", filename="tabla.tex"):
    # Crear DataFrame
    # Crear DataFrame con formato aplicado
    formato = f"{{:.{0}f}}"
    formato2 = f"{{:.{7}f}}"


    df = pd.DataFrame({
        r"$\sigma$ [S/cm]": [formato.format(x) for x in S],
        r"$\rho$ [$\Omega$cm]": [formato2.format(x) for x in R]
    })

    # Convertir a LaTeX
    tabla_latex = df.to_latex(index=False, escape=False,header=True,column_format="cc")
    # Envolver con entorno table + caption + label
    tabla_completa = "\\begin{table}[h!]\n"
    tabla_completa += "    \\centering\n"
    tabla_completa += tabla_latex
    tabla_completa += f"    \\caption{{{caption}}}\n"
    tabla_completa += f"    \\label{{{label}}}\n"
    tabla_completa += "\\end{table}\n"

    # Guardar en archivo
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tabla_completa)

    print(f"Tabla guardada en '{filename}'")

#######################################################################


I1 =np.array( [1.593,1.984,2.486,2.988])
V1 =np.array( [0.4624,0.5748,0.7210,0.8660])

Vp1=np.array([8.665,8.663,8.667,8.665]) # Equivalente a V_+
Vn1=np.array([15.37,15.35,15.36,15.38]) # Equivalente a V_-

I2 =np.array( [1.576,1.979,2.486,2.986])
V2 =np.array( [0.4570,0.5733,0.7200,0.8648])
    
V3 =np.array( [0.0009,0.0014,0.0017,0.0022])
I3 =np.array( [1.575,2.020,2.490,3.051])
    
I4 =np.array( [1.609,1.970,2.576,2.963])
V4 =np.array( [0.0001,0.0002,0.0009,0.0013])

I5 =np.array( [1.592,1.970,2.576,2.963])
V5 =np.array( [0.4667,0.5915,0.7491,0.8884])

I6 =np.array( [1.603,2.020,2.539,3.070])
V6 =np.array( [0.4700,0.5908,0.7418,0.8969])
    

I=np.array([I1,I2,I3,I4,I5,I6])
V=np.array([V1,V2,V3,V4,V5,V6])

Vp=np.array([Vp1])*10**(-2)
Vn=np.array([Vn1])*10**(-2)

gamma=3*10**5 # S /cm
d=0.001 # en m

r1=(-1.570+7.834)/2*10**(-3) # en m



for i in range(len(I)):
    generar_tabla_IVJ(
        I[i], V[i], J(I[i],d*10**2,r1*10**2),
        caption="Tabla de la valores para la disposición %i con $r=%.3f$ cm"%(i+1,r1*10**2),
        label="Tab:VIJ_%i"%(i+1),
        filename="Tablas/Tabla_VJI_%i.tex"%(i+1)
    )
    generar_tabla_IVJ(
        np.array([I[i,3]]), np.array([V[i,3]]), np.array([J(I[i,3],d*10**2,r1*10**2)]),
        caption="Tabla de la valores para la disposición %i con $r=%.3f$ cm"%(i+1,r1*10**2),
        label="Tab:VIJ_mini_%i"%(i+1),
        filename="Tablas/Tabla_VJI_mini_%i.tex"%(i+1)
    )


for i in range(len(Vp)):
    Vmp=sum(Vn[i])/len(Vn[i])
    Vmn=sum(Vp[i])/len(Vp[i])
    generar_tabla_Vpn(
        np.append(Vp[i],np.array(["$\\overline{V}_+$","$\\overline{V}_-$","$dV$"])), 
        np.append(Vn[i],np.array([Vmp,Vmn,abs(Vmp-Vmn)])),
        caption="Tabla de la valores para la disposición %i de $V_+$ y $V_-$"%(i+1),
        label="Tab:Vpn_%i"%(i+1),
        filename="Tablas/Tabla_Vpn_%i.tex"%(i+1)
    )
    
for i in range(len(Vp)):
    Vmp=sum(Vn[i])/len(Vn[i])
    Vmn=sum(Vp[i])/len(Vp[i])
    #DV=abs(Vmp-Vmn)
    DV=13.39*10**(-2)
    sigmaexp=gamma*DV/V[i,3]
    rhoexp=1/sigmaexp
    generar_tabla_S(
        np.array([sigmaexp]),np.array([rhoexp]),
        caption="Tabla de la valores para la disposición %i de $\\sigma$ y $\\rho $"%(i+1),
        label="Tab:RS_%i"%(i+1),
        filename="Tablas/Tabla_SR_%i.tex"%(i+1)
    )