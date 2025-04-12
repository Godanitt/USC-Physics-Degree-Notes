
import numpy as np
import pandas as pd
import matplotlib.pyplot as PARSE_DECLTYPES
def J(I,d,r):
  #  print(2*np.pi*r)
    return I/(d*2*np.pi*r)
def sI(I):
  #  print(2*np.pi*r)
    return 0.002+I/100
def sV(I):
  #  print(2*np.pi*r)
    return 0.0002+I/200
def sJ1(I):
  #  print(2*np.pi*r)
    return 0.0002/(d*2*np.pi*r)+I/100
def sJ2(I):
  #  print(2*np.pi*r)
    return 0.0002/(d*2*np.pi*r)+I/100
def uncertainty(x):
    return np.std(x, ddof=1) / np.sqrt(len(x))

def media_ponderada(valores, errores):
    """
    Calcula la media ponderada y su incertidumbre.

    Parámetros:
    - valores: lista de valores A_i
    - errores: lista de incertidumbres s(A_i)

    Retorna:
    - media ponderada
    - incertidumbre de la media ponderada
    """
    import numpy as np

    valores = np.array(valores)
    errores = np.array(errores)

    pesos = 1 / errores**2
    media = np.sum(valores * pesos) / np.sum(pesos)
    sigma_media = 1 / np.sqrt(np.sum(pesos))

    return media, sigma_media

def formato_seguro(valor,decimales=2,i=0,sV=[0,0,0]):
    if isinstance(valor, (int, float, np.number)):  # Acepta números reales y NumPy
        if i>3:
            if sV[i-4]<0.001:
                return f"\\SI{{{valor:.{2}f}}}{{}}"
            else:            
                return f"\\SI{{{valor:.{2}f}}}{{}} $\pm$ {sV[i-4]:.{2}f}"
        else:            
            return f"\\SI{{{valor:.{decimales}f}}}{{}}"

    elif valor in ("$\\overline{V}_+$ [$\mu$V]","$\\overline{V}_-$ [$\mu$V]","$\\Delta V_{\simu}$ [$\mu$V]"):
        return str(valor)
    else:
        valor=float(valor)
        return  f"\\SI{{{valor:.{decimales}e}}}{{}}" # o "N/A"
    
def formato_seguro2(valor,decimales=2,ss=1):
    if isinstance(valor, (int, float, np.number)):  # Acepta números reales y NumPy
        return  f"\\num{{{valor:.{decimales}f}({ss:.{decimales}f})}}"
    else:
        valor=float(valor)
        return  f"\\num{{{valor:.{decimales}e}({ss:.{decimales}f})}}"
    

def generar_tabla_IVJ(I, V, J1,J2, caption="Mi caption", label="tab:mi_tabla", filename="tabla.tex"):
    # Crear DataFrame
    formato = f"{{:.{3}f}}"
    formato_err = f"{{:.{3}f}}"
    formato2 = f"{{:.{4}f}}"
    formato_err2 = f"{{:.{4}f}}"
    formato3 = f"{{:.{2}f}}"
    formato_err3 = f"{{:.{2}f}}"


    # Crear DataFrame con formato aplicado
    df = pd.DataFrame({
        r"$I$ [A]": [f"{formato.format(x)} $\pm$ {formato_err.format(sI(x))}" for x in I],      
        r"$V$ [V]": [f"{formato2.format(x)} $\pm$ {formato_err2.format(sV(x))}" for x in V],      
        r"$J_1$ [A/cm$^2$]":[f"{formato3.format(x)} $\pm$ {formato_err3.format(sI(x))}" for x in J1], 
        r"$J_2$ [A/cm$^2$]":[f"{formato3.format(x)} $\pm$ {formato_err3.format(sI(x))}" for x in J2], 

    })

    # Convertir a LaTeX
    tabla_latex = df.to_latex(index=False, escape=False, column_format="cccc")
    df = df.round(2)
    # Envolver con entorno table + caption + label
    tabla_completa = "\\begin{table}[H]\n"
    tabla_completa += "    \\centering\n"
    tabla_completa += tabla_latex
    tabla_completa += f"    \\caption{{{caption}}}\n"
    tabla_completa += f"    \\label{{{label}}}\n"
    tabla_completa += "\\end{table}\n"

    # Guardar en archivo
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tabla_completa)

    print(f"Tabla guardada en '{filename}'")


def generar_tabla_Vpn(Vp,Vn,sVp=0,sVn=0,sDV=0, caption="Mi caption", label="tab:mi_tabla", filename="tabla.tex"):
    # Crear DataFrame
    # Crear DataFrame con formato aplicado
    df = pd.DataFrame({
        r"$V_+$ [mV]": [formato_seguro(Vp[i],3,i) for i in range(len(Vp))],
        r"$V_-$ [mV]": [formato_seguro(Vn[i],4,i,np.array([sVn,sVp,sDV])) for i in range(len(Vn))],
    })
    df=df.T

    # Convertir a LaTeX
    tabla_latex = df.to_latex(index=True, escape=False,  header=False,column_format="c|cccc|ccc")
    # Envolver con entorno table + caption + label
    tabla_completa = "\\begin{table}[H]\n"
    tabla_completa += "    \\centering\n"
    tabla_completa += tabla_latex
    tabla_completa += f"    \\caption{{{caption}}}\n"
    tabla_completa += f"    \\label{{{label}}}\n"
    tabla_completa += "\\end{table}\n"

    # Guardar en archivo
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tabla_completa)

    print(f"Tabla guardada en '{filename}'")
    

def generar_tabla_S(S,R,uS,uR,  caption="Mi caption", label="tab:mi_tabla", filename="tabla.tex",flag1=False):
    # Crear DataFrame
    # Crear DataFrame con formato aplicado
    formato = f"{{:.{0}f}}"
    formato2 = f"{{:.{9}f}}"

    df = pd.DataFrame({
        r"$\sigma_{\exp}$ [S/cm]": [formato_seguro2(S[i],3,uS[i]) for i in range(len(S))],
        r"$\rho_{\exp}$ [$\Omega  \cdot$cm]": [formato_seguro2(R[i],8,uR[i]) for i in range(len(R))]
    })

    # Convertir a LaTeX
    if flag1:
        df.index = ["Diposición %i"%i for i in range(1, 7)]   # Index desde 100
    tabla_latex = df.to_latex(index=flag1, escape=False,header=True,column_format="ccc")
    # Envolver con entorno table + caption + label

    # Guardar en archivo
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tabla_latex)

    print(f"Tabla guardada en '{filename}'")

def generar_tabla_S2(S,R,uS,uR, caption="Mi caption", label="tab:mi_tabla", filename="tabla.tex",flag1=False):
    # Crear DataFrame
    # Crear DataFrame con formato aplicado
    formato = f"{{:.{0}f}}"
    formato2 = f"{{:.{9}f}}"

    df = pd.DataFrame({
        r"$\sigma_{\exp}$ [S/cm]": [formato_seguro2(S[i],3,uS[i]) for i in range(len(S))],
        r"$\rho_{\exp}$ [$\Omega \cdot$cm]": [formato_seguro2(R[i],9,uR[i]) for i in range(len(R))]
    })

    # Convertir a LaTeX
    if flag1:
        df.index = ["Diposición %i"%i for i in range(1, 7)]   # Index desde 100
    tabla_latex = df.to_latex(index=flag1, escape=False,header=True,column_format="ccccc")
    # Envolver con entorno table + caption + label
    tabla_completa = "\\begin{table}[H]\n"
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

Vp1=np.array([3.075,3.069,3.077,3.072]) # Equivalente a V_+
Vn1=np.array([1.733,1.733,1.733,1.733]) # Equivalente a V_-

I2 =np.array( [1.576,1.979,2.486,2.986])
V2 =np.array( [0.4570,0.5733,0.7200,0.8648])

Vp2=np.array([3.499,3.50,3.501,3.501]) # Equivalente a V_+
Vn2=np.array([2.161,2.162,2.160,2.160]) # Equivalente a V_-

V3 =np.array( [0.0009,0.0014,0.0017,0.0022])
I3 =np.array( [1.575,2.020,2.490,3.051])
    
Vp3=np.array([2.203,2.203,2.203,2.203]) # Equivalente a V_+
Vn3=np.array([2.207,2.207,2.207,2.207]) # Equivalente a V_-

I4 =np.array( [1.609,1.970,2.576,2.963])
V4 =np.array( [0.0001,0.0002,0.0009,0.0013])

Vp4=np.array([1.404,1.404,1.404,1.404]) # Equivalente a V_+
Vn4=np.array([1.399,1.399,1.399,1.399]) # Equivalente a V_-

I5 =np.array( [1.592, 2.024, 2.534, 3.034])
V5 =np.array( [0.4667,0.5915,0.7491,0.8884])

Vp5=np.array([2.191,2.190,2.193,2.191]) # Equivalente a V_+
Vn5=np.array([3.559,3.553,3.560,3.556]) # Equivalente a V_-


I6 =np.array( [1.603,2.020,2.539,3.070])
V6 =np.array( [0.4700,0.5908,0.7418,0.8969])

Vp6=np.array([3.158,3.158,3.157,3.157]) # Equivalente a V_+
Vn6=np.array([1.775,1.776,1.776,1.776]) # Equivalente a V_-

    

I=np.array([I1,I2,I3,I4,I5,I6])
V=np.array([V1,V2,V3,V4,V5,V6])

Vp_1=np.array([Vp1,Vp2,Vp3,Vp4,Vp5,Vp6])*10**(-1)
Vn_1=np.array([Vn1,Vn2,Vn3,Vn4,Vn5,Vn6])*10**(-1)

#######################################################################

Vp1=np.array([3.027,3.029,3.024,3.020]) # Equivalente a V_+
Vn1=np.array([1.685,1.685,1.685,1.685]) # Equivalente a V_-

Vp2=np.array([3.450,3.449,3.451,3.452]) # Equivalente a V_+
Vn2=np.array([2.111,2.110,2.112,2.114]) # Equivalente a V_-

Vp3=np.array([1.720,1.720,1.720,1.720]) # Equivalente a V_+
Vn3=np.array([1.716,1.716,1.716,1.716]) # Equivalente a V_-

Vn4=np.array([1.666,1.666,1.666,1.666]) # Equivalente a V_+
Vp4=np.array([1.671,1.671,1.671,1.671]) # Equivalente a V_-

Vp5=np.array([3.507,3.500,3.509,3.504]) # Equivalente a V_+
Vn5=np.array([2.141,2.139,2.140,2.142]) # Equivalente a V_-

Vp6=np.array([3.107,3.106,3.109,3.108]) # Equivalente a V_+
Vn6=np.array([1.727,1.726,1.727,1.726]) # Equivalente a V_-


Vp_2=np.array([Vp1,Vp2,Vp3,Vp4,Vp5,Vp6])*10**(-1)
Vn_2=np.array([Vn1,Vn2,Vn3,Vn4,Vn5,Vn6])*10**(-1)

gamma=3*10**5 # S /cm
d=0.001 # en m

r1=((-1.570+7.834)/2)*10**(-3) # en m
r2=(10**(-3))*(4*6.13)/(2*np.pi)

#####################################################################


for i in range(len(I)):
    generar_tabla_IVJ(
        I[i], V[i], J(I[i],d*10**2,r1*10**2),J(I[i],d*10**2,r2*10**2),
        caption="Tabla de la valores para la disposición %i $r_1=%.3f$ y $r_2= %.3f $ cm "%(i+1,r1*10**2,r2*10**2),
        label="Tab:VIJ_%i"%(i+1),
        filename="Tablas/Tabla_VJI-%i.tex"%(i+1)
    )
    generar_tabla_IVJ(
        np.array([I[i,3]]), np.array([V[i,3]]), np.array([J(I[i,3],d*10**2,r1*10**2)]),np.array([J(I[i,3],d*10**2,r2*10**2)]),
        caption="Tabla de la valores para la disposición %i $r_1=%.3f$ y $r_2=%.3f$ cm "%(i+1,r1*10**2,r2*10**2),
        label="Tab:VIJ_mini_%i"%(i+1),
        filename="Tablas/Tabla_VJI_mini-%i.tex"%(i+1)
    )

#####################################################################

for i in range(len(Vp_1)):
    Vmp=sum(Vn_1[i])/len(Vn_1[i])
    Vmn=sum(Vp_1[i])/len(Vp_1[i])
    sVp=uncertainty(Vp_1[i])
    sVn=uncertainty(Vn_1[i])
    sDV=(sVp**2+sVn**2)**(1/2)
    generar_tabla_Vpn(
        np.append(Vp_1[i],np.array(["$\\overline{V}_+$ [$\mu$V]","$\\overline{V}_-$ [$\mu$V]","$\\Delta V_{\simu}$ [$\mu$V]"])), 
        np.append(Vn_1[i],np.array([Vmp*1000,Vmn*1000,abs(Vmp*1000-Vmn*1000)])),sVp*1000,sVn*1000,sDV*1000,
        caption="Tabla de la valores para la disposición %i de $V_+$ y $V_-$ con r=%.2f cm"%(i+1,r1*100),
        label="Tab:Vpn1_%i"%(i+1),
        filename="Tablas/Tabla_Vpn1-%i.tex"%(i+1)
    )

for i in range(len(Vp_1)):
    Vmp=sum(Vn_1[i])/len(Vn_1[i])
    Vmn=sum(Vp_1[i])/len(Vp_1[i])
    DV=abs(Vmp-Vmn)
    sigmaexp=gamma*DV/V[i,3]
    rhoexp=1/sigmaexp
    sVp=uncertainty(Vp_1[i])
    sVn=uncertainty(Vn_1[i])
    sDV=(sVp**2+sVn**2)**(1/2)
    usigma=np.sqrt((sDV/V[i,3])**2+(sV(V[i,3])*DV/(V[i,3])**2)**2)*gamma
    generar_tabla_S(
        np.array([sigmaexp]),np.array([rhoexp]),np.array([usigma]),np.array([usigma/sigmaexp**2]),
        caption="Tabla de la valores para la disposición %i de $\\sigma$ y $\\rho r=%.2f $"%(i+1,r2*100),
        label="Tab:RS_%i"%(i+1),
        filename="Tablas/Tabla_SR1-%i.tex"%(i+1)
    )

for i in range(len(Vp_2)):
    Vmp=sum(Vn_2[i])/len(Vn_2[i])
    Vmn=sum(Vp_2[i])/len(Vp_2[i])
    sVp=uncertainty(Vp_2[i])
    sVn=uncertainty(Vn_2[i])
    sDV=(sVp**2+sVn**2)**(1/2)
    generar_tabla_Vpn(
        np.append(Vp_2[i],np.array(["$\\overline{V}_+$ [$\mu$V]","$\\overline{V}_-$ [$\mu$V]","$\\Delta V_{\simu}$ [$\mu$V]"])), 
        np.append(Vn_2[i],np.array([Vmp*1000,Vmn*1000,abs(Vmp*1000-Vmn*1000)])),sVp*1000,sVn*1000,sDV*1000,
        caption="Tabla de la valores para la disposición %i de $V_+$ y $V_-$ con r=%.2f cm"%(i+1,r2*100),
        label="Tab:Vpn2_%i"%(i+1),
        filename="Tablas/Tabla_Vpn2-%i.tex"%(i+1)
    )
    
for i in range(len(Vp_2)):
    Vmp=sum(Vn_2[i])/len(Vn_2[i])
    Vmn=sum(Vp_2[i])/len(Vp_2[i])
    DV=abs(Vmp-Vmn)
    sigmaexp=gamma*DV/V[i,3]
    rhoexp=1/sigmaexp
    sVp=uncertainty(Vp_2[i])
    sVn=uncertainty(Vn_2[i])
    sDV=(sVp**2+sVn**2)**(1/2)
    usigma=np.sqrt((sDV/V[i,3])**2+(sV(V[i,3])*DV/(V[i,3])**2)**2)*gamma
    generar_tabla_S(
        np.array([sigmaexp]),np.array([rhoexp]),np.array([usigma]),np.array([usigma/sigmaexp**2]),
        caption="Tabla de la valores para la disposición %i de $\\sigma$ y $\\rho r=%.2f $"%(i+1,r2*100),
        label="Tab:RS_%i"%(i+1),
        filename="Tablas/Tabla_SR2-%i.tex"%(i+1)
    )

#####################################################################

n = len(Vp_1)  # Número de bloques de datos
Vmp = np.zeros(n)
Vmn = np.zeros(n)
DV = np.zeros(n)
sigmaexp1 = np.zeros(n)
rhoexp1 = np.zeros(n)
sVp= np.zeros(n)
sVn= np.zeros(n)
sDV= np.zeros(n)
usigma1=np.zeros(n)
sigmaexp2 = np.zeros(n)
rhoexp2 = np.zeros(n)
usigma2=np.zeros(n)


# Cálculo
for i in range(n):
    Vmp[i] = np.mean(Vn_1[i])  # Promedio de Vn en el bloque i
    Vmn[i] = np.mean(Vp_1[i])  # Promedio de Vp en el bloque i
    DV[i] = abs(Vmp[i] - Vmn[i])
    sigmaexp1[i]=gamma*DV[i]/V[i,3]
    rhoexp1[i]=1/sigmaexp1[i]
    sVp[i]=uncertainty(Vp_1[i])
    sVn[i]=uncertainty(Vn_1[i])
    sDV[i]=(sVp[i]**2+sVn[i]**2)**(1/2)
    usigma1[i]=np.sqrt((sDV[i]/V[i,3])**2+(sV(V[i,3])*DV[i]/(V[i,3])**2)**2)*gamma

generar_tabla_S2(
    sigmaexp1,rhoexp1,usigma1,usigma1/sigmaexp1**2,
    caption="Tabla de la valores para $r=%.2f$ cm de $\\sigma$ y $\\rho $"%(r1*100),
    label="Tab:S1",
    filename="Tablas/Tabla_S1.tex",
    flag1=True)

for i in range(n):
    Vmp[i] = np.mean(Vn_2[i])  # Promedio de Vn en el bloque i
    Vmn[i] = np.mean(Vp_2[i])  # Promedio de Vp en el bloque i
    DV[i] = abs(Vmp[i] - Vmn[i])
    sigmaexp2[i]=gamma*DV[i]/V[i,3]
    rhoexp2[i]=1/sigmaexp2[i]
    sVp[i]=uncertainty(Vp_2[i])
    sVn[i]=uncertainty(Vn_2[i])
    sDV[i]=(sVp[i]**2+sVn[i]**2)**(1/2)
    usigma2[i]=np.sqrt((sDV[i]/V[i,3])**2+(sV(V[i,3])*DV[i]/(V[i,3])**2)**2)*gamma

generar_tabla_S2(
    sigmaexp2,rhoexp2,usigma2,usigma2/sigmaexp2**2,
    caption="Tabla de la valores para $r=%.2f$ cm de $\\sigma$ y $\\rho $"%(r2*100),
    label="Tab:S2",
    filename="Tablas/Tabla_S2.tex",
    flag1=True)

aux=sigmaexp1[4:]
sigmaexp1=sigmaexp1[0:2]
sigmaexp1=np.append(sigmaexp1,aux)

aux=usigma1[4:]
usigma1=usigma1[0:2]
usigma1=np.append(usigma1,aux)

sigma1,usigma1=media_ponderada(sigmaexp1,usigma1)
print(sigma1,usigma1)


aux=sigmaexp2[4:]
sigmaexp2=sigmaexp2[0:2]
sigmaexp2=np.append(sigmaexp2,aux)
aux=usigma2[4:]
usigma2=usigma2[0:2]
usigma2=np.append(usigma2,aux)

print(usigma2)
sigma2,usigma2=media_ponderada(sigmaexp2,usigma2)
print(sigma2,usigma2)


generar_tabla_S2(
    np.array([sigma1]),np.array([1/sigma1]),np.array([usigma1]),np.array([usigma1/sigma1**2]),
    caption="Valor medio para $r=%.2f$ cm de $\\sigma$ y $\\rho $"%(r1*100),
    label="Tab:S3",
    filename="Tablas/Tabla_S3.tex",
    flag1=False)


generar_tabla_S2(
    [sigma2],[1/sigma2],[usigma2],[usigma2/sigma2**2],
    caption="Valor medio para $r=%.2f$ cm de $\\sigma$ y $\\rho $"%(r2*100),
    label="Tab:S4",
    filename="Tablas/Tabla_S4.tex",
    flag1=False)

sigma3,usigma3=media_ponderada(np.array([sigma1,sigma2]),np.array([usigma1,usigma2]))

print(sigma3,usigma3)



generar_tabla_S2(
    [sigma3],[1/sigma3],[usigma3],[usigma3/sigma3**2],
    caption="Valor medio definitvo de $\\sigma$ y $\\rho $",
    label="Tab:S5",
    filename="Tablas/Tabla_S5.tex",
    flag1=False)
