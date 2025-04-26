# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:24:47 2023

@author: danie
"""


import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
from math import e
import scipy.optimize as so
from mpl_toolkits.mplot3d import Axes3D
import modulo_1_aproximador as md


def ajustelinealponderado(x,y,sig): # Aquí metemos los dos valores y la incertidumbre de y(sig)
    sig=np.array(sig)
    x=np.array(x)
    y=np.array(y)

    H=np.array([[sum(1./sig**2),sum(x/sig**2)],[sum(x/sig**2),sum(x**2/sig**2)]])
    Delta=lng.det(H)
    Z=np.array([sum(y/sig**2),sum((x*y)/sig**2)])
    
    ([a,b])=np.matmul(lng.inv(H),Z)
    
    siga=np.sqrt(sum(x**2/sig**2)/Delta)
    sigb=np.sqrt(sum(1./sig**2)/Delta)
    
    r = np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))
    
    return a,b,siga,sigb


Vdep = 7.41*10**(3)                        # en litros
S =  0.385*0.290                       # en metros
sS = 0.01*np.sqrt(38.5**2+29.0**2)*0.2    # en metros
d = 75                               # en centímetros
sd = 0.2                             # en centímetros


# Calculo para la distancia d=0.75 m

# -- Calculo caudal 152 ml/min 

c1  = 152
sc1 = 1

DT1  = 6.4
sDT1 = 0.1

T31=np.array([[19.06,15],[19.09,30],[19.12,45],[19.14,60],[19.16,75],
              [19.18,90],[19.21,105],[19.20,120],[19.22,135],[19.27,150],[19.30,165],
              [19.34,180],[19.38,195]])


T31=np.array([T31[:,0],T31[:,1]])

sT31 = 0.2

# -- Calcula caudal 124 ml/min


c2  = 124
sc2 = 1

DT2  = 7.9
sDT2 = 0.1

T32 =np.array([[20.66,15],[20.69,30],[20.71,45],[20.74,60],[20.76,75],[20.80,90],
               [20.83,105],[20.86,120],[20.87,135],[20.90,150],[20.93,165],
               [20.96,180],[20.95,195]])



T32=np.array([T32[:,0],T32[:,1]])

# -- Calcula caudal 98

c3 = 98
sc3 = 1

DT3  = 9.7
sDT3 = 0.1

T33 = np.array([[22.41,22.44,22.47,22.50,22.51,22.53,22.56,  22.58,22.60,22.62,22.65,22.68],
                [0,15,30,45,60,75,90,105,120,135,150,165]])


# -- Cauldal 69

c4 = 69
sc4 = 1

DT4  = 13.2
sDT4 = 0.1

T34 = np.array([[23.63,23.66,23.67,23.71,23.72,23.73,23.75,23.77,23.77,23.79,23.80,23.83,23.84],
                [0,15,30,45,60,75,90,105,120,135,150,165,180]])

# -- Caudal 49

c5  = 49
sc5 = 1

DT5  = 17.9
sDT5 = 0.1

T35 = np.array([[24.78,24.82,24.83,24.85,24.86,24.88,24.90,24.91, 24.93,24.95,24.95,24.96],
                [0,15,30,45,60,75,90,105,120,135,150,165]])



c_1 = np.array([c1,c2,c3,c4,c5])


# Calculo para la distancia d=50cm 

# -- Calcula 152 ml/s

c1  = 153
sc1 = 1

DT6  = 9.9
sDT6 = 0.1

T36 = np.array([[20.11,20.13,20.18,20.21,20.24,20.31,20.34,20.37,20.42,20.45,20.56,20.60],
                [0,15,30,45,60,75,90,105,120,135,165,180]]) 


# -- Calculo 120 ml/s

c2  = 127
sc1 = 1

DT7  = 13.3
sDT7 = 0.1

T37 = np.array([[23.52,23.53,23.60,23.61,23.64,23.69,23.74,23.75,23.76,23.82,23.84,23.86,23.91],
               [0,15,30,45,60,75,90,105,120,135,150,165,180]])

# ..

c3 = 100
sc3 = 1

DT8  = 14.9
sDT8 = 0.1

T38 =np.array([[26.12,26.18,26.19,26.20,26.23,26.28,26.30,26.35,26.41,26.43,26.48,26.50],
               [0,15,30,45,60,75,90,105,135,150,165,180]])


# --

c4 = 70
sc4 = 1

DT9  = 18.3
sDT9 = 0.1

T39 = np.array([[27.87,27.94,27.96,27.97,28.0,28.06,28.09,28.10,28.14,28.16,28.19],
                [0,15,30,45,60,75,90,105,120,150,165]])


# -- 

c5 = 44
sc4 = 1

DT10 = 15.6
sDT10= 0.1

T310 = np.array([[29.19,29.19,29.18,29.21,29.22,29.24,29.26,29.27,29.30,29.30,29.32,29.35],
                 [0,15,30,45,60,75,90,105,135,150,165,180]])


# ________________---- DaTos -----_________________________________________

c_2 =  np.array([c1,c2,c3,c4,c5])
c=[0]*10
sce = np.sqrt(1+1/12)
sc=[0]*10

for i in range(10):
    if i<5:
        c[i]=c_1[i]/60
        sc[i]=sce/60
    if i>=5:
        c[i]=c_2[i-5]/60
        sc[i]=sce/60
        
d=[0.75,0.75,0.75,0.75,0.75,0.50,0.50,0.50,0.50,0.50]        
sd=[0.02]*10



DT=[DT1,DT2,DT3,DT4,DT5,DT6,DT7,DT8, DT9,DT10]

sDT=[0]*len(DT)

for i in range(len(DT)):
    sDT[i] = 0.2+DT[i]*0.02

T3=[T31,T32,T33,T34,T35,T36,T37,T38,T39,T310]

Vdep = 7.41                          # en litros
S =  0.385*0.290                       # en metros
sS = np.sqrt(0.385**2+0.290**2)*0.002    # en metro
Mdep= Vdep*1000

I=[0]*len(T3)
sI=[0]*len(T3)

mt=[0]*len(T3)
smt=[0]*len(T3)
E1=[0]*len(T3)
E2=[0]*len(T3)
E3=[0]*len(T3)

sE1=[0]*len(T3)
sE2=[0]*len(T3)
sE3=[0]*len(T3)


eta1=[0]*len(T3)
eta2=[0]*len(T3)
eta3=[0]*len(T3)

seta1=[0]*len(T3)
seta2=[0]*len(T3)
seta3=[0]*len(T3)


Cp = 4.18 #J/g Co


def f(x,a,b):
    y = a + b*x
    return y

Deta1=[0]*10
Deta2=[0]*10
Deta3=[0]*10

for i in range(len(T3)):
    Tt = T3[i]
    T = Tt[0]
    t = Tt[1]
    st = [1]*len(t)
    sT = [0.02]*len(T)
    
    I[i] = 324.2+247.24/(d[i]**2)
    sI[i] = 2*247.24*sd[i]/(d[i]**3)
    
    """
    sol = so.curve_fit(f,t,T,sigma=sT,absolute_sigma=True)
    a,b = sol[0]
    sa,sb = np.diag(sol[1])
    """
    
    a,b,sa,sb = ajustelinealponderado(t, T, sT)
    
    mt[i]=b
    smt[i]=sb
       
    
    E1[i]=I[i]*S
    E2[i]=c[i]*Cp*DT[i]
    E3[i]=Mdep*Cp*mt[i]
    
    sE1[i]=np.sqrt((I[i]*sS)**2+(S*sI[i])**2)
    sE2[i]=np.sqrt((c[i]*Cp*sDT[i])**2+(Cp*DT[i]*sc[i])**2)
    sE3[i]=np.sqrt((Mdep*Cp*smt[i])**2)
    
    
    eta1[i]=E2[i]/E1[i]
    eta2[i]=E3[i]/E2[i]
    eta3[i]=E3[i]/E1[i]
    
    seta1[i]=np.sqrt((E2[i]*sE1[i]/(E1[i]**2))**2+(sE2[i]/E1[i])**2)
    seta2[i]=np.sqrt((E3[i]*sE2[i]/(E2[i]**2))**2+(sE3[i]/E2[i])**2)
    seta3[i]=np.sqrt((E3[i]*sE1[i]/(E1[i]**2))**2+(sE3[i]/E1[i])**2)
    
    
    
    
    """
    x = np.linspace(min(t),max(t),100)
    y = f(x,a,b)
    plt.figure()
    plt.grid("True",linestyle="--")
    plt.errorbar(t,T,yerr=0.9,fmt=".",color="blue",ecolor="cornflowerblue",capsize=2)
    plt.plot(x,y,color="royalblue")
    plt.xlabel("$ t \ (s) $")
    plt.ylabel("$T_3 \ (C^o)$")
    plt.savefig("plotT3%d.png"%i,dpi=500)
    """
    
    

    """
    outfile=open("regresiones.txt", 'a')
    outfile.write("\n\\begin{figure}[h!] \t \centering \n")
    outfile.write("\\includegraphics[scale=1]{plotT3%d.png} \n"%(i))
    outfile.write("\\caption{representación de $T_3$ frente a $t$ para $Q = %.3f \ g/s$ e $d = %d$ cm} \n"%(c[i],100*d[i]))
    outfile.write("\\label{Fig:plot-%d}  \n"%(i+1))
    outfile.write("\\end{figure} \n")
    outfile.close()
    """
    
    if i==4 or i==9:
        plt.grid(True, linestyle="--")
        plt.errorbar(c[i-4:i+1],eta1[i-4:i+1],yerr=seta1[i-4:i+1],fmt=".",color="red",ecolor="red",capsize=2.0,label="$\eta_1$")
        plt.errorbar(c[i-4:i+1],eta2[i-4:i+1],yerr=seta2[i-4:i+1],fmt=".",color="blue",ecolor="blue",capsize=2.0,label="$\eta_2$")
        plt.errorbar(c[i-4:i+1],eta3[i-4:i+1],yerr=seta3[i-4:i+1],fmt=".",color="green",ecolor="green",capsize=2.0,label="$\eta_3$")
        plt.xlabel("$Q \ (g/s)$")
        plt.ylabel("$\eta$")
        plt.legend()
        
    if i==4:
        plt.savefig("etad1.png",dpi=500)
        plt.figure()
    
 
    """
    outfile=open("valoresregresion.txt", 'a')
    outfile.write("\\begin{table}[h!] \t \centering \n")
    outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
    outfile.write("\\hline \n")
    outfile.write("$a \ (C^o)$ & $s(a) \ (C^o)$ & $ b \ (C^o/s)$ & $s(b) \ (C^o/s)$  \\\ \\hline \n")
    outfile.write("%f  & %f &  %.6f & %.6f \\\ \n\\hline\n"%(a,sa,b,sb))
    outfile.write("\\end{tabular} \n")
    outfile.write("\\caption{Valores del ajuste lineal para los pares ($t,T_3$) con $Q=%.3f \ (g/s)$ y $d= %d $ cm} \n"%(c[i],d[i]*100))
    outfile.write("\\label{tab:regresion%i} \n"%(i+1))
    outfile.write("\\end{table} \n \n \n")
    outfile.close()
    """
    
    
    outfile=open("datoscrudos.txt", 'a')
    if i==0:
        outfile.write("\\subsection{Primera distancia}\n \n")
        p = 0
        outfile.write("La primera distancia que tomamos fue: \n \n")
        outfile.write("\\begin{equation} \n")
        outfile.write("\\begin{array}{lllllll}\n")
        outfile.write("d & = & %.2f m &  \ \ &  s(d) & =  & %.2f  m \\\ \n "%(DT[i],md.aproximaciondecimales(sDT[i])))
        outfile.write("I & = & %d W/m^2 &  \ \ &  s(I) & =  & %d W/m^2 \\\ \n "%(I[i],sI[i]))
        outfile.write("S & = & %.3f m^2 &  \ \ &  s(S) & =  & %.3f  m^2 \\\ \n "%(S,md.aproximaciondecimales(sS)))       
        outfile.write("\\end{array} \n")
        outfile.write("\\end{equation} \n \n ")
                      
    if i==5:   
        outfile.write("\\subsection{Segunda distancia}\n")
        p = 5
        outfile.write("La segunda distancia que tomamos fue: \n \n")

        outfile.write("\\begin{equation} \n")
        outfile.write("\\begin{array}{lllllll}\n")
        outfile.write("d & = & %.2f m &  \ \ &  s(d) & =  & %.2f  m \\\ \n "%(DT[i],md.aproximaciondecimales(sDT[i])))
        outfile.write("I & = & %d W/m^2 &  \ \ &  s(I) & =  & %d  W/m^2 \\\ \n "%(I[i],sI[i]))
        outfile.write("S & = & %.5f m^2 &  \ \ &  s(S) & =  & %.5f  m^2 \\\ \n "%(S,md.aproximaciondecimales(sS)))      
        outfile.write("\\end{array} \n")
        outfile.write("\\end{equation} \n \n ")
                    
    
    outfile.write("\\subsubsection{Caudal número %d} \\label{subsec:%i} \n \n"%(i+1-p,i+1))
    outfile.write("Podemos ver el caudal e intensidad en la siguiente ecuación y los pares de valores ($t,T_3$) en la tabla \\ref{tab:datoscrudos%i}: \n \n"%(i))     
 
    outfile.write("\\begin{equation} \n")
    outfile.write("\\begin{array}{lllllll}\n")
    outfile.write("\Delta T & = & %.2f C^o &  \ \ &  s(\Delta T) & =  & %.2f  C^o \\\ \n "%(DT[i],md.aproximaciondecimales(sDT[i])))
    outfile.write("Q & = & %.3f g/s &  \ \ &  s(Q) & =  & %.3f  g/s \\\ \n "%(c[i],md.aproximaciondecimales(sc[i])))
    outfile.write("\\end{array} \n")
    outfile.write("\\end{equation} \n \n ")
    
    outfile.write("\\begin{table}[h!] \t \centering \n")
    outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
    outfile.write("\\hline \n")
    outfile.write("$T_3 \ (C^o)$ & $s(T_3) \ (C^o)$ & $ t \ (s)$ & $s(t) \ (s)$  \\\ \\hline \n")
    for j in range(len(T)):    
        outfile.write("%.2f  & %.2f &  %d & %d \\\ \n\\hline\n"%(T[j],sT[j],t[j],st[j]))
    outfile.write("\\end{tabular} \n")
    outfile.write("\\caption{Valores del ajuste lineal para los pares ($t,T_3$) con $Q=%.3f \ (g/s)$ y $d= %d $ cm} \n"%(c[i],d[i]*100))
    outfile.write("\\label{tab:datoscrudos%i} \n"%(i))
    outfile.write("\\end{table} \n \n \n")   
    outfile.close()  
    
    """
    Deta1[i]=np.array([c[i],d[i],eta1[i]])
    Deta2[i]=np.array([c[i],d[i],eta2[i]])
    Deta3[i]=np.array([c[i],d[i],eta3[i]])
    """
    """
    
    outfile=open("experimental.txt", 'a')
    if i==0:
        outfile.write("\\subsection{Primera distancia}\n \n")
        p = 0       
    if i==5:   
        outfile.write("\\subsection{Segunda distancia}\n")
        p = 5      
    
    
    
    
    outfile.write("\\subsubsection{Caudal número %d} \n \n"%(i+1-p))
    outfile.write("Usando los datos del apartado \\ref{subsec:%d} y los  resultados experimentales de la regreisón lineal (tab \\ref{tab:regresion%d}) (fig \\ref{Fig:plot-%d}), podemos calcular las energías \n \n "%(i+1,i+1,i+1))            
    outfile.write("\\begin{equation} \n")
    outfile.write("\\begin{array}{lllllll}\n")
    outfile.write("E_1 & = & %.1f W &  \ \ &  s(E_1) & =  & %.1f  W \\\ \n "%(E1[i],md.aproximaciondecimales(sE1[i])))
    outfile.write("E_2 & = & %.1f W &  \ \ &  s(E_2) & =  & %.1f  W \\\ \n "%(E2[i],md.aproximaciondecimales(sE2[i])))
    outfile.write("E_3 & = & %.1f W &  \ \ &  s(E_3) & =  & %.1f  W \\\ \n "%(E3[i],md.aproximaciondecimales(sE3[i])))
    outfile.write("\\end{array} \n")
    outfile.write("\\end{equation} \n \n ")
    outfile.write("y podemos calcular los rendimientos \n \n")
    outfile.write("\\begin{equation} \n")
    outfile.write("\\begin{array}{lllllll}\n")
    outfile.write("\eta_1 & = & %.3f  &  \ \ &  s(\eta_1) & =  & %.3f   \\\ \n "%(eta1[i],md.aproximaciondecimales(seta1[i])))
    outfile.write("\eta_2 & = & %.3f  &  \ \ &  s(\eta_2) & =  & %.3f   \\\ \n "%(eta2[i],md.aproximaciondecimales(seta2[i])))
    outfile.write("\eta_3 & = & %.3f  &  \ \ &  s(\eta_3) & =  & %.3f   \\\ \n "%(eta3[i],md.aproximaciondecimales(seta3[i])))
    outfile.write("\\end{array} \n")
    outfile.write("\\end{equation} \n \n ")
    
    outfile.write("\\begin{table}[h!] \t \centering \n")
    outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
    outfile.write("\\hline \n")
    outfile.write("$a \ (C^o)$ & $s(a) \ (C^o)$ & $ b \ (C^o/s)$ & $s(b) \ (C^o/s)$  \\\ \\hline \n")
    outfile.write("%f  & %f &  %.6f & %.6f \\\ \n\\hline\n"%(a,sa,b,sb))
    outfile.write("\\end{tabular} \n")
    outfile.write("\\caption{Valores del ajuste lineal para los pares ($t,T_3$) con $Q=%.3f \ (g/s)$ y $d= %d $ cm} \n"%(c[i],d[i]*100))
    outfile.write("\\label{tab:regresion%i} \n"%(i+1))
    outfile.write("\\end{table} \n \n \n")
    
    outfile.write("\\begin{figure}[h!] \t \centering \n")
    outfile.write("\\includegraphics[scale=1.0]{plotT3%d.png} \n"%(i))
    outfile.write("\\caption{representación de $T_3$ frente a $t$ para $Q = %.3f \ g/s$ e $d = %d$ cm} \n"%(c[i],100*d[i]))
    outfile.write("\\label{Fig:plot-%d}  \n"%(i+1))
    outfile.write("\\end{figure} \n \n")
    outfile.write("\\newpage \n \n \n \n \n")
    
    
    outfile.close()
    
    
    """
    


plt.savefig("etad2.png",dpi=500)
"""
plt.figure()
plt.grid(True, linestyle="--")
plt.errorbar(c[0:5],E2[0:5],yerr=sE2[0:5],fmt=".",color="red",ecolor="red",capsize=2.0,label="$d=75cm$")
plt.errorbar(c[5:10],E2[5:10],yerr=sE2[5:10],fmt=".",color="blue",ecolor="blue",capsize=2.0,label="$d=50cm$")
plt.xlabel("$ Q \ (g/s)")
plt.ylabel("$E_2 \ (W)$")
plt.legend()
plt.savefig("E2-comparacion.png",dpi=500)


plt.figure()
plt.grid(True, linestyle="--")
plt.errorbar(c[0:5],E3[0:5],yerr=sE3[0:5],fmt=".",color="red",ecolor="red",capsize=2.0,label="$d=75cm$")
plt.errorbar(c[5:10],E3[5:10],yerr=sE3[5:10],fmt=".",color="blue",ecolor="blue",capsize=2.0,label="$d=50cm$")
plt.xlabel("$ Q \ (g/s)")
plt.ylabel("$E_3 \ (W)$")
plt.legend()
plt.savefig("E3-comparacion.png",dpi=500)



plt.figure()
plt.grid(True, linestyle="--")
plt.errorbar(c[0:5],eta3[0:5],yerr=seta3[0:5],fmt=".",color="red",ecolor="red",capsize=2.0,label="$d=75cm$")
plt.errorbar(c[5:10],eta3[5:10],yerr=seta3[5:10],fmt=".",color="blue",ecolor="blue",capsize=2.0,label="$d=50cm$")
plt.xlabel("$ Q \ (g/s)")
plt.ylabel("$\eta_3 $")
plt.legend()
plt.savefig("eta3-comparacion.png",dpi=500)
"""




"""
Deta1=np.array(Deta1)
Deta2=np.array(Deta2)
Deta3=np.array(Deta3)



fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(Deta1[:,0],Deta1[:,1],Deta1[:,2],c='b',marker='.')
ax.scatter(Deta2[:,0],Deta2[:,1],Deta2[:,2],c='r',marker='.')
ax.scatter(Deta3[:,0],Deta3[:,1],Deta3[:,2],c='g',marker='.')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.savefig("3D.png",dpi=500)  
"""