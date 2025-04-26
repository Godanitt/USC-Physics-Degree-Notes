# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:26:38 2023

@author: danie
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
from math import e
import scipy.optimize as so
import modulo_1_aproximador  as md

def ajustelinealponderado(x,y,sig): # Aquí metemos los dos valores y la incertidumbre de y(sig)

    H=np.array([[sum(1./sig**2),sum(x/sig**2)],[sum(x/sig**2),sum(x**2/sig**2)]])
    Delta=lng.det(H)
    Z=np.array([sum(y/sig**2),sum((x*y)/sig**2)])
    
    ([a,b])=np.matmul(lng.inv(H),Z)
    
    siga=np.sqrt(sum(x**2/sig**2)/Delta)
    sigb=np.sqrt(sum(1./sig**2)/Delta)
    
    r = np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))
    
    return a,b,siga,sigb



def mediaponderada(u,sigu):
    w=np.zeros([len(sigu)])
    for i in range(len(sigu)):
        w[i]=1/sigu[i]**2
    k=sum(w)
    media=np.dot(u,w)/k
    s = 1/np.sqrt(k)
    
    return [media, s]

def media(u):
    m=sum(u)/len(u)
    return m

def mediaponderada2(u,sigu):
    w=np.zeros([len(sigu)])
    for i in range(len(sigu)):
        w[i]=1/(sigu[i]**2)
    k=sum(w)
    media=np.dot(u,w)/k
    
    s1 = np.sqrt((sum((u-media)**2))/(len(u)*(len(u)-1)))
    s2 = 1/np.sqrt(k)
    
    s =np.sqrt(s1**2 + s2**2)
    
    return [media, s]


#------------------------------------------------------------------------------


I11 = 0.525 
sI11 = 0.005
V1 = 120.7 
sV1= 1

T11=np.array([[13.8,13.8,0],[14.1,13.9,2],[14.5,13.9,3],[14.9,14.0,4],[15.2,14.1,5],
              [15.7,14.1,6],[15.9,14.2,7],[16.4,14.3,8],[16.7,14.4,9],[17.0,14.4,10],
              [17.3,14.6,11],[17.6,14.6,12],[17.8,14.6,13],[17.9,14.6,14],[18.2,14.7,15],
              [18.5,14.8,16],[18.6,14.7,17],[18.8,14.7,18],[18.9,14.7,19],[19.1,14.6,20],
              [19.2,14.6,21],[19.3,14.5,22],[19.4,14.5,23],[19.5,14.5,24],[19.7,14.6,25],
              [19.8,14.6,26],[19.9,14.5,27],[19.9,14.5,28],[20.0,14.6,29],[20.1,14.6,30],
              [20.4,14.6,32],[20.5,14.6,33],[20.5,14.6,34],[20.6,14.5,35],[20.6,14.4,36],
              [20.7,14.5,37],[20.8,14.5,38],[20.8,14.5,39],[20.9,14.4,40],[20.9,14.5,41],
              [21.0,14.5,42],[21.0,14.5,43],[21.1,14.5,44],[21.1,14.7,45],[21.2,14.6,46],
              [21.1,14.6,47],[21.2,14.5,48],[21.2,14.5,49],[21.3,14.6,50],[21.3,14.5,51],
              [21.3,14.5,52]])


sT=5/60


# -----


I12 = 1.001
sI12 = 0.01
V1 = 120.0 
sV1= 1

T12=np.array([[21.2,14.5,0],[20.2,14.5,1],[19.6,15.2,2],[19.2,15.3,3],
              [18.9,15.3,4],[18.6,15.2,5],[18.4,15.3,6],[18.2,15.2,7],
              [17.9,15.2,8],[17.7,15.2,9],[17.6,15.0,10],[17.4,15.0,11],
              [17.3,15.1,12],[17.1,15.2,13],[17.0,15.1,14],[16.9,15.1,15],
              [16.8,15.1,16],[16.7,15.1,18],[16.6,15.1,19],[16.4,15.1,20],
              [16.4,15.1,21],[16.2,15.1,22],[16.1,15.1,23],[16.1,15.1,24],
              [16.0,15.1,25],[16.0,15.1,26],[16.0,15.1,27],[16.0,15.1,28]])


# -----

I13 = 1.522
sI13 = 0.01
V1 = 120.0 
sV1= 1

T13 = np.array([[15.5,15.3,0],[14.9,16.0,1],[14.3,16.0,2],[14.0,16.1,3],
                [13.7,16.0,4],[13.4,16.0,5],[13.1,16.0,6],[13.0,15.9,7],
                [12.6,15.9,8],[12.4,15.9,9],[12.4,15.9,10],[12.1,15.8,11],
                [12.0,15.8,12],[11.9,15.8,13],[11.8,15.8,14],[11.6,15.8,15],
                [11.5,15.8,16],[11.4,15.8,17],[11.3,15.7,18],[11.2,15.7,19],
                [11.1,15.8,20],[11.1,15.8,21],[11.0,15.8,22],[10.9,15.8,23],
                [10.8,15.8,24],[10.8,15.8,25],[10.7,15.8,26],[10.7,15.7,27],
                [10.7,15.8,28]])


# -----


I14= 2.00
sI14 = 0.01
V4 = 120.0 
sV4= 1

T14 = np.array([[10.3,16.0,0],[9.5,16.8,1],[9.1,17.0,2],[8.8,17.1,3],[8.5,17.0,4],
                [8.3,16.9,5],[8.2,16.9,5.5],[8.1,16.8,6],[8.0,16.8,6.5]])

# Segundo intento

I21 = 0.512 
sI21 = 0.01
V2= 150
sV2 = 1

T21=np.array([[12.0,13.3,0],[13.4,13.4,1],[14.5,13.7,2],[15.4,13.7,3],
              [16.4,13.8,4],[17.2,13.8,5],[18.0,14.0,6],[18.6,14.1,7],
              [19.2,14.3,8],[19.9,14.2,9],[20.6,14.2,10],[21.1,14.4,11],
              [21.6,14.5,12],[22.1,14.5,13],[22.5,14.6,14],[22.9,14.6,15],
              [23.4,14.6,16],[23.6,14.7,17],[24.1,14.7,18],[24.4,14.7,19],
              [24.8,14.8,20],[24.9,14.8,21],[25.4,14.9,22],[25.7,15.0,23],
              [26.0,15.1,24],[26.2,15.1,25],[26.4,15.1,26],[26.6,15.2,27],
              [26.8,15.1,28],[27.0,15.0,29],[27.2,15.0,30],[27.4,15.0,31],
              [27.6,15.2,32],[27.7,15.1,33],[27.8,15.2,34],[28.0,15.2,35],
              [28.1,15.2,36],[28.2,15.2,37],[28.4,15.3,38],[28.5,15.3,39],
              [28.6,15.4,40],[28.7,15.3,41],[28.8,15.4,42],[28.9,15.4,43],
              [29.0,15.4,44],[29.0,15.4,45],[29.1,15.4,46],[29.2,15.4,47],
              [29.2,15.4,48]])
                                                                                         

# -----

I22 =1.013
sI22 = 0.01

T22=np.array([[29.0,15.6,0],[28.3,16.4,1],[27.8,16.5,2],[27.4,16.5,3],
              [27.1,16.5,4],[27.0,16.5,5],[26.8,16.4,6],[26.6,16.4,7],
              [26.3,16.4,8],[26.2,16.2,9],[26.0,16.2,10],[25.9,16.2,11],
              [25.8,16.2,12],[25.7,16.2,13],[25.5,16.2,14],[25.5,16.4,15],
              [25.4,16.2,16],[25.3,16.2,17],[25.2,16.2,18],[25.1,16.2,19],
              [25.0,16.2,20],[25.0,16.2,21],[24.9,16.2,22],[24.8,16.1,23],
              [24.8,16.1,24],[24.7,16.1,25],[24.7,16.2,26],[24.5,16.1,27],
              [24.4,16.1,28],[24.4,16.2,29]])

             

# ----- 


I23 = 1.511
I23 = 1.49
sI23 = 0.01

T23 = np.array([[24.2,16.9,0],[24.0,16.9,1],[22.9,17.4,2],[22.6,17.4,3],
                [22.3,17.4,4],[22.0,17.3,5],[21.8,17.3,6],[21.6,17.2,7],
                [21.5,17.3,8],[21.3,17.2,9],[21.1,17.2,10],[21.0,17.2,11],
                [20.8,17.3,12],[20.7,17.3,13],[20.6,17.3,14],[20.4,17.3,15],
                [20.3,17.2,16],[20.1,17.2,17],[20.0,17.2,18],[20.0,17.2,19],
                [19.9,17.2,20],[19.9,17.2,21],[19.8,17.2,22],[19.7,17.2,23],
                [19.6,17.2,24],[19.5,17.2,25],[19.4,17.2,26],[19.4,17.1,27],
                [19.3,17.2,28],[19.3,17.0,29],[19.2,16.9,30],[19.2,16.9,31],
                [19.2,16.9,32]])


# -- Tablas



T=np.array([T11,T12,T13,T14,T21,T22,T23])
I=np.array([I11,I12,I13,I14,I21,I22,I23])
V0=np.array([120,120,120,120,150,150,150])
sI = np.ones(len(I))*0.01


# ---------------------------------------------------------------------------


def f(t,A,B,C):
    y = A + B*(np.exp(-(C*t)))
    return y


T2I = np.zeros(len(T))
sT2I = np.zeros(len(T))
T1M = np.zeros(len(T))
sT1M = np.zeros(len(T))
QP = np.zeros(len(T))
sQP = np.zeros(len(T))

lambdaM  = 0.9378876789404914
slambdaM = 0.010123203249968609

R = [1023.694205993717901, 4.448932990758462935e+00]
ri = [-7.972231497930885, 0.010990837447029]
    

   
plt.figure()
   

#Regresiones

def f(t,A,B,C):
    y = A + B*(np.exp(-(C*t)))
    return y

Tnext=0



for i in range(len(T)):
    P = T[i]
    T1 = P[:,1]
    T2 = P[:,0]
    sT = np.array([0.1]*len(T1))
    t  = P[:,2]
    Tnext = max(t)
    
    par = [max(T2)+0.5,media(T1),0.05]
    sol = so.curve_fit(f,t,T2,p0=(par))
    
    
    T2I[i] = sol[0][0]
    sT2I[i] = sol[1][0,0]
    
    T1M[i] = mediaponderada2(T1,sT)[0]
    sT1M[i] = mediaponderada2(T1,sT)[1]
    
    A,B,C = sol[0]
    sa,sb,sc = np.diag(sol[1])
    
    
    """
    x = np.linspace(min(t),max(t))
    print(sol[0])
    
    y = f(x,sol[0][0],sol[0][1],sol[0][2])
    """
    
    QP[i]  = (V0[i]**2)/R[0]-lambdaM*(T2I[i]-T1M[i])-(I[i]**2)*(ri[0])/2
    sQP[i] = np.sqrt((2*V0[i]/R[0])**2+((V0[i]**2)*R[1]/(R[0]**2))**2+((T2I[i]-T1M[i])*slambdaM)**2
              +((lambdaM)**2)*(sT1M[i]**2+sT2I[i]**2)+(I[i]*ri[0]*sI[i])**2+((I[i]**2)*ri[1]/2)**2)
    
    
    outfile=open("Coeficientes.txt","a")
    outfile.write("\\begin{table}[h!] \t \centering \n")
    outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
    outfile.write("\\hline \n")
    outfile.write("$A \ (C^o)$ & $s(A) \\ (C^o)$ & $ B  \ (C^o)$ & $s(B) \ (C^o)$ & $C \ (\mathrm{min}^{-1}) $&  $s(C) \ (\mathrm{min}^{-1}) $ \\\ \\hline \n")
    outfile.write("%f  & %f &  %f & %f & %f & %f \\\ \n\\hline\n"%(A,md.aproximaciondecimales(sa),B,md.aproximaciondecimales(sb),C,md.aproximaciondecimales(sc)))
    outfile.write("\\end{tabular} \n")
    outfile.write("\\caption{Valores del ajuste exponencial para $V_0 = %d V$ e $I = %.3f A$} \n"%(V0[i],I[i]))
    outfile.write("\\label{tab:} \n")
    outfile.write("\\end{table} \n \n \n \n \n")
    outfile.close()
    outfile.close()
    
    
    
    
    """
    outfile=open("datos.txt", 'a')
    outfile.write("\\subsubsection{Estacionario %d}\n"%(i+1))
    outfile.write("En este estacionario hemos seleccionado las siguientes magnitudes de intensidad y voltaje  \n")
    outfile.write("\\begin{equation} \n")
    outfile.write("\\begin{array}{lllllll}\n")
    outfile.write("I & = & %.2f A & \ \ & s(I) & = & 0.01  A \\\ \n "%(I[i]))
    outfile.write("V_0 & = & %d V & \ \ & s(V_0) & = & 1 V\n"%(V0[i]))
    outfile.write("\\end{array} \n")
    outfile.write("\\end{equation} \n ")
    
    outfile.write("Haciendo el ajuste exponencial (fig \\ref{Fig:graficapeltier%d} y la media de al tempertatura del foco frío obtenemos que para el valor estacionario las temperaturas serán: \n"%(i+1))
    outfile.write("\\begin{equation} \n")
    outfile.write("\\begin{array}{lllllll}\n")
    outfile.write("T_2^{\infty} & = & %.4f C^o &  \ \ &  s(T_2^{\infty}) & =  & %.4f  C^o \\\ \n "%(T2I[i],sT2I[i]))
    outfile.write("T_1 & = & %.4f  C^o & \ \ & s(T_1) & = & %.4f  C^o \\\ \n "%(T1M[i],sT1M[i]))
    outfile.write("\\end{array} \n")
    outfile.write("\\end{equation} \n ")
    
    outfile.write("Por lo tanto, teniendo en cuenta los datos anteriores, y los que proceden de la anterior práctica, tenemos que en este caso el calor peltier será: \n")
    outfile.write("\\begin{equation} \n")
    outfile.write("\\begin{array}{lllllll}\n")
    outfile.write("\\dot{Q}_P & = & %f J & \ \ & s(\\dot{Q})_P & = & %f J \\\ \n"%(QP[i],sQP[i]))
    outfile.write("\\end{array} \n")
    outfile.write("\\end{equation} \n \n \n \n \n")
    outfile.close()
    """
    
    """
    plt.grid(True, linestyle="--")
    plt.plot(t,T2,".",markersize=1,label="%d estacionario"%(i+1))
    plt.xlabel("t (min)")
    plt.ylabel("T ($C^o$)")
    plt.ylim(6,30)
    plt.legend()
    
    """
    
    
    """
    plt.figure()
    plt.grid(True, linestyle="--")
    plt.plot(x,y)
    plt.plot(t,T2,".b",markeredgewidth=1)
    plt.xlabel("t (min)")
    plt.ylabel("T ($C^o$)")
    plt.savefig("plot-peltier%d.png"%(i), dpi=500)
    """
    """
    outfile=open("regresiones.txt", 'a')
    outfile.write("\n\\begin{figure}[h!] \t \centering \n")
    outfile.write("\\includegraphics[scale=0.85]{plot-peltier%d.png} \n"%(i))
    outfile.write("\\caption{representación de $T_2$ frente a $t$ para $V_0 = %d V$ e $I = %.3f A$} \n"%(V0[i],I[i]))
    outfile.write("\\end{figure} \n")
    """
"""
plt.savefig("plot-peltier-todos.png", dpi=500)    
    
"""


I1 = I[0:4]
QP1 = QP[0:4]
sQP1 = sQP[0:4]

I2 = I[4:7]
QP2 = QP[4:7]
sQP2 = sQP[4:7]
    
a1,b1,sa1,sb1=ajustelinealponderado(I1, QP1, sQP1)
a2,b2,sa2,sb2=ajustelinealponderado(I2, QP2, sQP2)

x1 = np.linspace(min(I1),max(I1))
x2 = np.linspace(min(I2),max(I1))

y1 =  a1 + b1*x1
y2 =  a2 + b2*x2


plt.grid(True, linestyle="--")
plt.plot(x1,y1,color="royalblue")
plt.plot(x2,y2,color="sandybrown")
plt.errorbar(I[0:4],QP[0:4],sQP[0:4],color="blue",fmt=".",ecolor="blue",capsize=0.7,label="$V_0 = 120 V$")
plt.errorbar(I[4:7],QP[4:7],sQP[4:7],color="darkorange",fmt=".",ecolor="darkorange",capsize=0.7, label = "$V_0  =150V$")
plt.xlabel("$I  \ (A)$")
plt.ylabel("$\dot{Q}_P$ (J)")
plt.legend()

plt.savefig("plot-coeficiente-peltier.png", dpi=500)        
    


outfile=open("datosregresion1.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$a \ (J)$ & $s(a) \ (J)$ & $\pi_{AB} \ (J/A)$ & $s(\pi_{AB}) \ (J/A)$  \\\ \\hline \n")
outfile.write("%f  & %f &  %f & %f \\\ \n\\hline\n"%(a1,sa1,b1,sb1))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores del ajuste lineal para los pares (I,$\dot{Q}_P$) con voltaje $V_0=120V$} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()
    
    
    
outfile=open("datosregresion2.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$a \ (J)$ & $s(a) \ (J)$ & $\pi_{AB} \ (J/A)$ & $s(\pi_{AB}) \ (J/A)$  \\\ \\hline \n")
outfile.write("%f  & %f &  %f & %f \\\ \n\\hline\n"%(a2,sa2,b2,sb2))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores del ajuste lineal para los pares (I,$\dot{Q}_P$) con voltaje $V_0=150V$} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()
    
    

outfile=open("datosregresion3.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$ $\pi_{AB} \ (J/A)$ & $s(\pi_{AB}) \ (J/A)$  \\\ \\hline \n")
outfile.write("%f & %f \\\ \n\\hline\n"%(mediaponderada2([b1,b2],[sb1,sb2])[0], mediaponderada2([b1,b2],[sb1,sb2])[1]))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{valor medio del coeficiente Peltier} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()
    
        
    
    
    
    