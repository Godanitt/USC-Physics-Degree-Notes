# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 16:20:52 2023

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
    
    r1 = np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))
    
    r2 = (sum(1./sig**2)*sum(x*y/sig**2)-sum(x/sig**2)*sum(y/sig**2))/(np.sqrt((sum(1/sig**2)*sum(x**2/sig**2)-(sum(x/sig**2))**2)*(sum(1/sig**2)*sum(y**2/sig**2)-(sum(y/sig**2))**2)))
    
    return a,b,siga,sigb,r2



# Calculo de la superficie

r=130 #milimetros

S = np.pi*r**2  #milimetros cuadrados


CM = 220 #nF
sCM= 220*0.2

# Primera parte

VC1 = 1.5 #kV
sVC1 = VC1*0.06 #kV

d1= np.array([0.20,0.22,0.24,0.26,0.28,0.30])*10 # mm
VM1 = np.array([1.842,1.645,1.55,1.46,1.42,1.27]) # V

sd1=np.ones(len(d1))*0.1
sVM1=np.sqrt((VM1*0.005)**2+0.02**2)

# Segunda parte

d2 = 2.5 #mm
sd2 = 0.1

VC2=np.array([0.5,1,1.5,2,2.5,3]) # kV
sVC2=VC2*0.06

VM2=np.array([0.55,1.125,1.677,2.13,2.84,3.67]) #V
sVM2 = np.sqrt((VM2*0.005)**2+0.02**2)

#Tecera parte

d3=9.9  #mm
sd3=0.1

VC3=np.array([1,2,3,4,5]) #kV
sVC3=VC3*0.06
VM3=[[0.98,2.03,3.15,4.00,5.04],[0.37,0.63,1.02,1.35,1.60]] 
VM3=np.array(VM3)
print(VM3)
sVM3=np.sqrt((VM3*0.005)**2+0.02**2)
sVM3=np.array(sVM3)


# -- Analisis de datos -------------------

# Parte 1 ------------

Q1=np.ones(len(VM1))
sQ1=np.ones(len(VM1))
for i in range(len(Q1)):
    Q1[i]=VM1[i]*CM
    sQ1[i]=np.sqrt((CM*sVM1[i])**2+(sCM*VM1[i])**2)
    
    
CP1=Q1/(VC1)*0.001
sCP1 = np.ones(len(CP1))    
for i in range(len(sCP1)):
    sCP1[i]=np.sqrt((sQ1[i]/VC1)**2+((Q1[i]*sVC1)/(VC1**2))**2)*0.001
    
dm1=1/d1    
sdm1=np.ones(len(dm1))
for i in range(len(sdm1)):
    sdm1[i]=sd1[i]/(d1[i]**2)



outfile=open("datos1a.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$d \ (mm)$ & $s(d) \ (mm)$ & $ V_M \ (V)$ & $s(V_M) \ (V)$ & $Q_0 \ (nC)  $ &  $s(Q_0) \ (nC)$ \\\ \\hline \n")
for i in range(len(d1)):
    outfile.write("%.1f  & %.1f &  %.3f & %.3f & %d & %d \\\ \n"%(d1[i],sd1[i],VM1[i],sVM1[i],Q1[i],sQ1[i]))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{datos de las medidas directas y las carga almacenada en $Q_0$} \n")
outfile.write("\\label{tab:datos1} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()


outfile=open("datos1b.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$1/d \ (mm^{-1})$ & $s(1/d) \ (mm^{-1})$ & $ C_P \ (nF)$ & $s(C_P) \ (nF)$ \\\ \\hline \n")
for i in range(len(d1)):
    outfile.write("%.3f  & %.3f &  %.3f & %.3f \\\ \n"%(dm1[i],sdm1[i], CP1[i],sCP1[i]))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{pares de valores($1/d,C_p$) para la regresión lineal \\ref{regresion1}} \n")
outfile.write("\\label{tab:datos2} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()

a1,b1,sa1,sb1,r1 = ajustelinealponderado(dm1, CP1, sCP1)


epsilon1=b1/S
sepsilon1=sb1/S




x = np.linspace(min(dm1),max(dm1),20)
y = a1+b1*x

plt.figure(dpi=500)
plt.grid(True,linestyle="--")
plt.plot(x,y,color="cornflowerblue")
plt.errorbar(dm1, CP1, yerr=sCP1, fmt=".",capsize=2.0,color="royalblue")
plt.xlabel("$1/d \ (mm^{-1})$")
plt.ylabel("$C_p \ (nF)$")
plt.savefig("plot1.png",dpi=500)


outfile=open("regresion1.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$a \ (nF)$ & $s(a) \ (nF)$ & $ b \ (pF |cdot mm)$ & $s(b) \ (pF \cdot mm) $ & r  \\\ \\hline \n")
outfile.write("%.2f  & %.2f &  %.2f & %.2f & %.3f \\\ \n"%(a1,sa1,b1,sb1,r1))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{pares de valores($1/d,C_p$) para la regresión lineal \\ref{Fig:regresion1}} \n")
outfile.write("\\label{tab:datos2} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()


# Parte 2 -----------




Q2=np.ones(len(VM2))
sQ2=np.ones(len(VM2))
for i in range(len(Q2)):
    Q2[i]=VM2[i]*CM
    sQ2[i]=np.sqrt((CM*sVM2[i])**2+(sCM*VM2[i])**2)
   

outfile=open("datos2a.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$V_0\ (kV)$ & $s(V_0) \ (kV)$ & $ V_M \ (V)$ & $s(V_M) \ (V)$ & $Q_0 \ (nC)  $ &  $s(Q_0) \ (nC)$ \\\ \\hline \n")
for i in range(len(d1)):
    outfile.write("%.3f  & %.3f &  %.3f & %.3f & %d & %d \\\ \n"%(VC2[i],sVC2[i],VM2[i],sVM2[i],Q2[i],sQ2[i]))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{datos de las medidas directas y las carga almacenada en $Q_0$} \n")
outfile.write("\\label{tab:datos2} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()


a2,b2,sa2,sb2,r2 = ajustelinealponderado(VC2, Q2, sQ2)




x = np.linspace(min(VC2),max(VC2),20)
y = a2+b2*x

plt.figure(dpi=500)
plt.grid(True,linestyle="--")
plt.plot(x,y,color="cornflowerblue")
plt.errorbar(VC2, Q2, yerr=sQ2, fmt=".",capsize=2.0,color="royalblue")
plt.xlabel("$V \ (kV)$")
plt.ylabel("$Q \ (nC)$")
plt.savefig("plot2.png",dpi=500)


outfile=open("regresion2.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$a \ (nC)$ & $s(a) \ (nC)$ & $ b \ (pF)$ & $s(b) \ (pF) $ & r  \\\ \\hline \n")
outfile.write("%.2f  & %.2f &  %d & %d & %.5f \\\ \n"%(a2,sa2,b2,sb2,r2))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{pares de valores($1/d,C_p$) para la regresión lineal \\ref{Fig:regresion1}} \n")
outfile.write("\\label{tab:datos2} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()

epsilon2 = b2*d2/S*1000
sepsilon2=np.sqrt((sb2*d2)**2+(sd2*b2))/S*1000



# Parte 3 -----------------




Q3 = [[1,1,1,1,1],[1,1,1,1,1]]
sQ3 =[[1,1,1,1,1],[1,1,1,1,1]]
for i in range(len(Q3)):
    for j in range(len(Q3[i])):
        Q3[i][j]=VM3[i][j]*CM
        sQ3[i][j]=np.sqrt((CM*sVM3[i][j])**2+(sCM*VM3[i][j])**2)
Q3=np.array(Q3)
sQ3=np.array(sQ3)

a=[0,0]
b=[0,0]
sa=[0,0]
sb=[0,0]
r=[0,0]
C=["Con dieléctrico","Sin dieléctrico"]
colores=np.array([["tomato","salmon"],["royalblue","cornflowerblue"]])


plt.figure(dpi=500)

for i in range(len(Q3)):
    
    outfile=open("datos3-%d.txt"%(i), 'w')
    outfile.write("\\begin{table}[h!] \t \centering \n")
    outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
    outfile.write("\\hline \n")
    outfile.write("$V_0\ (kV)$ & $s(V_0) \ (kV)$ & $ V_M \ (V)$ & $s(V_M) \ (V)$ & $Q_0 \ (nC)  $ &  $s(Q_0) \ (nC)$ \\\ \\hline \n")
    for j in range(len(VC3)):
        outfile.write("%.3f  & %.3f &  %.3f & %.3f & %d & %d \\\ \n"%(VC3[j],sVC3[j],VM3[i,j],sVM3[i,j],Q3[i,j],sQ3[i,j]))
    outfile.write("\\hline\n\\end{tabular} \n")
    outfile.write("\\caption{datos de las medidas directas y las carga almacenada en $Q_0$} \n")
    outfile.write("\\label{tab:datos%d} \n"%(i+2))
    outfile.write("\\end{table} \n \n \n")
    outfile.close()
    
    
    a[i],b[i],sa[i],sb[i],r[i] = ajustelinealponderado(VC3, Q3[i], sQ3[i])
    
    x = np.linspace(min(VC3),max(VC3),20)
    y = a[i]+b[i]*x
    
    plt.grid(True,linestyle="--")
    plt.plot(x,y,color="%s"%(colores[i,1]))
    plt.errorbar(VC3, Q3[i], yerr=sQ3[i], fmt=".",capsize=2.0,color="%s"%(colores[i,0]),label="%s"%(C[i]))
    plt.xlabel("$V \ (kV)$")
    plt.ylabel("$Q \ (nC)$")
    plt.legend()
    plt.savefig("plot3.png",dpi=500)
    
    
    epsilon03= b[1]*d3/S*1000
    sepsilon3=np.sqrt((sb[1]*d3)**2+(sd3*b[1]))/S*1000
    


    
    


outfile=open("regresion3.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("i & $a \ (nC)$ & $s(a) \ (nC)$ & $ C_i \ (pF)$ & $s(C_i) \ (pF) $ & r  \\\ \\hline \n")
outfile.write("1 & %d  & %d &  %d & %d & %.4f \\\ \n\\hline\n"%(a[0],sa[0],b[0],sb[0],r[0]))
outfile.write("2 & %d  & %d &  %d & %d & %.4f \\\ \n"%(a[1],sa[1],b[1],sb[1],r[1]))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{pares de valores  para la regresión lineal \\ref{Fig:regresion1}} \n")
outfile.write("\\label{tab:datos2} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()
  






epsilon3 = b[0]/b[1]
sepsilon3 = np.sqrt((sb[0]/b[1])**2+(b[0]*sb[1]/b[1]**2)**2)


print("\\varepsilon_r = %.2f \\quad \\quad s(\\varepsilon_r) = %.2f "%(epsilon3,sepsilon3))

