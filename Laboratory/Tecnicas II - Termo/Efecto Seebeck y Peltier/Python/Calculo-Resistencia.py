# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 13:32:25 2023

@author: danie
"""


import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
import modulo_1_aproximador as md





def mediaponderada(u,sigu):
    w=np.zeros([len(sigu)])
    for i in range(len(sigu)):
        w[i]=1/sigu[i]**2
    k=sum(w)
    media=np.dot(u,w)/k
    s = 1/np.sqrt(k)
    return [media, s]

def ajustelinealponderado(x,y,sig): # Aquí metemos los dos valores y la incertidumbre de y(sig)

    H=np.array([[sum(1./sig**2),sum(x/sig**2)],[sum(x/sig**2),sum(x**2/sig**2)]])
    Delta=lng.det(H)
    Z=np.array([sum(y/sig**2),sum((x*y)/sig**2)])
    
    ([a,b])=np.matmul(lng.inv(H),Z)
    
    siga=np.sqrt(sum(x**2/sig**2)/Delta)
    sigb=np.sqrt(sum(1./sig**2)/Delta)
    
    r = np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))
    
    return a,b,siga,sigb


R = np.array([[20,0.022],[40,0.042],[60,0.062],[80,0.082],[100,0.102],[120,0.121],[140,0.140],[160,0.159],[180,0.176],[200,0.195]])


#Calculo de los valores de la resistencia


V = R[:,0]
I = R[:,1]

sV = np.array([1]*len(V))

valores=ajustelinealponderado(I,V,sV)



#Plots

x = np.linspace(0,max(I),100)
y = valores[0]+valores[1]*x

plt.figure()
plt.grid(True, linestyle="--")
plt.plot(x, y, color="limegreen")
plt.errorbar(I,V,fmt=".",color="darkgreen")
plt.xlabel("I (A)")
plt.ylabel(" V (V)")
plt.xlim(0, max(I)*1.1)
plt.savefig("R.png", dpi=500)


#Creacion de tablas


outfile=open("datos8.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\ a \ (V)$ & $s(a) \ (V)$ & $R_C \ (\Omega)$ & $R_C \ (\Omega)$  \\\ \\hline \n")
outfile.write("%f  & %f &  %f & %f \\\ \n\\hline\n"%(valores[0],md.aproximaciondecimales(valores[2]),valores[1],md.aproximaciondecimales(valores[3])))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{valor de la resistencia y ordenada en el origen} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()


R = np.array([1010,989,valores[1]])
sR = np.array([10,10,valores[3]])

otros = mediaponderada(R, sR)


outfile=open("datos14.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|} \n")
outfile.write("\\hline \n")
outfile.write(" $R_C \ (\Omega)$ & $R_C \ (\Omega)$  \\\ \\hline \n")
outfile.write("%f  & %f  \\\ \n\\hline\n"%(otros[0],md.aproximaciondecimales(otros[1])))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{valor de la resistencia finales} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()




