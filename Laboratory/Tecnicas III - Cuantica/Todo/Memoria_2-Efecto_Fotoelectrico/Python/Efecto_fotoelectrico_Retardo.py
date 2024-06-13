# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:00:32 2024

@author: danie
"""
import numpy as np
from Efecto_fotoelectrico_Funciones import concatenarbueno
from tabulate import tabulate
from Efecto_fotoelectrico_Datos import l
from Efecto_fotoelectrico_Resultados_Cortes import h,sh
from Efecto_fotoelectrico_Resultados_Exponencial import C,sC,B,sB
from Efecto_fotoelectrico_Resultados_Arbitrario import V0,sV0
from Efecto_fotoelectrico_Funciones import lineal
from scipy.optimize import curve_fit
import scipy.constants as cte


outfile=open("lambda.txt","w")
for i in range(len(V0)):
    outfile.write("\\begin{table}[h!] \\centering \n")
    outfile.write("\\begin{tabular}{c|c|c} \n")
    outfile.write(" & $V_0$ (V) & $s(V_0)$ (V) \\\ \hline \n")
    outfile.write("Metodo 1 & %.2f & % .2f \\\ \n"%(V0[i],sV0[i]))
    outfile.write("Metodo 2 & %.3f & % .3f \\\ \n"%(-h[i],sh[i]))
    outfile.write("Metodo 3-1 & %.4f & % .4f \\\ \n"%(-C[i],sC[i]))
    sC2=np.sqrt(sC[i]**2+sB[i]**2/B[i]**4)
    outfile.write("Metodo 3-2 & %.4f & % .4f \\\ \hline\n"%(-C[i]+1/B[i],sC2))
    outfile.write("\\end{tabular}")
    outfile.write("\\caption{tabla de valores de $V_0$ para $\lambda=%d$ nm} \n"%(l[i]*10**9))
    outfile.write("\\label{Tab:3.%d} \n"%(i+1))
    outfile.write("\\end{table} \n")
    outfile.write("\n \n \n")
outfile.close()




V0=np.array([V0,-h,-C,-C+1/B])
sV0=np.array([sV0,sh,-sC,np.sqrt(sC**2+sB**2/B**4)])

def saca_constantes(V0,l,sV0):
    a1=np.array([])
    b1=np.array([])
    sa1=np.array([])
    sb1=np.array([])
    
    a2=np.array([])
    b2=np.array([])
    sa2=np.array([])
    sb2=np.array([])
    for i in range(len(V0)):
        datos,ss=curve_fit(lineal,1/l,V0[i],sigma=sV0[i],p0=(-1.5,1200),maxfev=5000)
        a0,b0=datos
        sa0,sb0=np.sqrt(ss[0,0]),np.sqrt(ss[1,1])
        a1=np.append(a1,a0)
        b1=np.append(b1,b0)
        sa1=np.append(sa1,sa0)
        sb1=np.append(sb1,sb0)
        
        datos,ss=curve_fit(lineal,1/l[1:],V0[i,1:],sigma=sV0[i,1:],p0=(-1.5,1200),maxfev=5000)
        a0,b0=datos
        sa0,sb0=np.sqrt(ss[0,0]),np.sqrt(ss[1,1])
        a2=np.append(a2,a0)
        b2=np.append(b2,b0)
        sa2=np.append(sa2,sa0)
        sb2=np.append(sb2,sb0)
    h1=b1*cte.e/cte.c
    sh1=sb1*cte.e/cte.c
    W1=cte.e*a1
    sW1=cte.e*sa1
    h2=b2*cte.e/cte.c
    sh2=sb2*cte.e/cte.c
    W2=cte.e*a2
    sW2=cte.e*sa2
    mu01=W1/h1
    smu01=np.sqrt((sW1/h1)**2+(sh1*W1/h2**2)**2)
    mu02=W2/h2
    smu02=np.sqrt((sW2/h2)**2+(sh2*W2/h2**2)**2)
    return b1,sb1,b2,sb2,h1,h2,W1,W2,mu01,mu02,sh1,sh2,sW1,sW2,smu01,smu02
    
def printeame_latex(nombre_archivo,h1,h2,sh1,sh2,header,d):
    outfile=open("%s.txt"%nombre_archivo,"w")
    outfile.write("\\begin{table}[h!] \\centering \n")
    outfile.write("\\begin{tabular}{c|c|c|c|c} \n")
    outfile.write(" & %s & %s & %s & %s \\\ \hline \n"%(header[0],header[1],header[2],header[3]))
    for i in range(len(h1)):
        outfile.write("Metodo %d & %.2f $\cdot 10^{%d}$ & %.2f $\cdot 10^{%d}$ & %.2f $\cdot 10^{%d}$ & %.2f $\cdot 10^{%d}$ \\\ \n"%(i+1,h1[i],d,sh1[i],d,h2[i],d,sh2[i],d))
    outfile.write("\\end{tabular}")
    outfile.write("\\caption{tabla de las constantes de Planck para cada método.} \n"%(l[i]*10**9))
    outfile.write("\\label{Tab:4.1} \n")
    outfile.write("\\end{table} \n")
    outfile.write("\n \n \n")
    outfile.close()


def printeame_latex2(nombre_archivo,h1,h2,sh1,sh2,header,d):
    outfile=open("%s.txt"%nombre_archivo,"w")
    outfile.write("\\begin{table}[h!] \\centering \n")
    outfile.write("\\begin{tabular}{c|c|c|c|c} \n")
    outfile.write(" & %s & %s & %s & %s \\\ \hline \n"%(header[0],header[1],header[2],header[3]))
    for i in range(len(h1)):
        outfile.write("Metodo %d  & %.2f  & %.2f & %.2f  & %.2f  \\\ \n"%(i+1,h1[i],sh1[i],h2[i],sh2[i]))
    outfile.write("\\end{tabular}")
    outfile.write("\\caption{tabla de la función de trabajo para cada método.} \n"%(l[i]*10**9))
    outfile.write("\\label{Tab:4.2} \n")
    outfile.write("\\end{table} \n")
    outfile.write("\n \n \n")
    outfile.close()


b1,sb1,b2,sb2,h1,h2,W1,W2,mu01,mu02,sh1,sh2,sW1,sW2,smu01,smu02=saca_constantes(V0, l, sV0)

header1=np.array(["$h_1$ (J$\cdot$s)","$s(h_1)$ (J$\cdot$s)",
                  "$h_2$ (J$\cdot$s)","$s(h_2)$ (J$\cdot$s)"])
printeame_latex("constante_plank",h1*10**34,h2*10**34,sh1*10**34,sh2*10**34,header1,34)


header2=np.array(["$W_1$ (eV)","$s(W_1)$ (eV)",
                  "$W_2$ (eV)","$s(W_2)$ (eV)"])
printeame_latex2("funcion_trabajo", -W1/cte.e, -W2/cte.e, sW1/cte.e, sW2/cte.e, header2,5)


header3=np.array(["$\\nu_{0_1}$ (Hz)","$s(\\nu_{0_1})$ (Hz)",
                  "$\\nu_{0_2}$ (Hz)","$s(\\nu_{0_2})$ (Hz)"])
printeame_latex("frecuencia_0",-mu01/10**14,-mu02/10**14,smu01/10**14,smu02/10**14,header3,14)


header4=np.array(["$b_{1}$ (kV$\cdot$nm)","$s(b_{1})$ (kV$\cdot$nm)",
                  "$b_{2}$ (kV$\cdot$nm)","$s(b_{2})$ (kV$\cdot$nm)"])
printeame_latex2("pendiente",b1*10**6,b2*10**6,sb1*10**6,sb2*10**6,header4,0)


def media(x,sx):
    xm=(x[0]+x[1]+x[3])/3
    sxm=np.sqrt((sx[0]**+sx[1]**2+sx[3]**2)/3**2)
    return xm,sxm

print(media(h2*10**34,sh2*10**34))
print(media(-W2/cte.e,sW2/cte.e))
print(media(-mu02/10**14,smu02/10**14))

#$s(h_1)$ (J$\cdot$s)
































