# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 11:41:19 2023

@author: danie
"""



import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
import modulo_1_aproximador as md
from math import e
import scipy.optimize as so



def media(x):
    x=np.array(x)
    media = sum(x)/len(x)
    s = np.sqrt((sum((x-media)**2))/(len(x)-1))
    return [media,s]






def mediaponderada(u,sigu):
    w=np.zeros([len(sigu)])
    for i in range(len(sigu)):
        w[i]=1/(sigu[i]**2)
    k=sum(w)
    media=np.dot(u,w)/k
    
    s1 = np.sqrt((sum((u-media)**2))/(len(u)-1))
    s2 = 1/np.sqrt(k)
    
    s =np.sqrt(s1**2 + s2**2)
    
    return [media, s]




#Datos



T1 = np.array([[16.6,12.0,0],[17.1,12.0,120],[18.4,12.1,240],[19.5,12.0,360],[20.7,12.1,420],[21.6,12.2,480],[22.0,12.2,600],[22.7,12.0,660],[23.3,12.0,900],[23.6,12.3,960],[23.9,12.4,1020],[24.2,12.4,1080],[24.6,12.4,1140],[24.9,12.5,1200],[25.1,12.4,1260],[25.4,12.4,1320],[25.6,12.4,1380],[25.8,12.4,1440],[26.0,12.5,1500],[26.2,12.5,1560],[26.3,12.5,1620],[26.5,12.5,1680],[26.7,12.5,1740],[26.8,12.5,1800],[27.0,12.6,1860],[27.2,12.6,1920],[27.3,12.7,1980],[27.4,12.7,2040],[27.6,12.7,2100],[27.7,12.6,2160],[27.7,12.6,2220],[27.8,12.5,2280],[27.9,12.6,2340],[28.0,12.6,2400],[28.1,12.6,2460],[28.1,12.7,2520],[28.2,12.7,2580],[28.3,12.7,2640],[28.4,12.7,2700],[28.4,12.9,2760],[28.5,12.9,2820],[28.5,12.7,2880],[28.6,12.7,2940],[28.6,12.7,3000],[28.6,12.9,3060],[28.6,12.9,3120]])
T2 = np.array([[28.8,13.0,0],[29.1,13.1,1],[29.5,13.1,2],[29.9,13.2,3],[30.4,13.2,4],[30.8,13.3,5],[31.2,13.4,6],[31.5,13.4,7],[31.9,13.5,8],[32.1,13.5,9],[32.4,13.5,10],[32.7,13.5,11],[32.9,13.5,12],[33.2,13.6,13],[33.4,13.6,14],[33.6,13.6,15],[33.8,13.5,16],[34.0,13.5,17],[34.1,13.5,18],[34.2,13.5,19],[34.3,13.5,20],[34.4,13.6,21],[34.5,13.5,22],[34.6,13.5,23],[34.7,13.5,24],[34.8,13.5,25],[34.9,13.5,26],[34.9,13.5,27],[34.9,13.5,28],[35.0,13.5,29],[35.1,13.5,30],[35.2,13.5,31],[35.2,13.5,32],[35.3,13.5,33],[35.3,13.5,34],[35.4,13.5,35],[35.4,13.5,36],[35.5,13.5,37],[35.5,13.5,38],[35.6,13.6,39],[35.6,13.6,40],[35.7,13.7,41],[35.7,13.7,42],[35.8,13.7,43],[35.8,13.6,45],[35.8,13.5,46]])

T12 = T1[:,0]
t1  = T1[:,2]/60

T22 = T2[:,0]
t2  = T2[:,2]

sT=np.array(46*[0.1])




#Regresiones

def f(t,A,B,C):
    y = A + B*(np.exp(-(C*t)))
    return y

par1 = [29.5,13.3,0.05]
par2 = [37.0,24.0,0.05]
sol1 = so.curve_fit(f,t1,T12,p0=(par1))
sol2 = so.curve_fit(f,t2,T22,p0=(par2))



A1,B1,C1=sol1[0]
sa1,sb1,sc1=np.diag(sol1[1])
A2,B2,C2=sol2[0]
sa2,sb2,sc2=np.diag(sol2[1])

x1 = np.linspace(0,max(t1),100)
y1 = f(x1,A1,B1,C1)

x2 = np.linspace(0,max(t2),100)
y2 = f(x2,A2,B2,C2)



#Plots


plt.figure()
plt.grid(True, linestyle="--")
plt.plot(x1,y1,"r")
plt.plot(t1,T12,".",color="darkred")
plt.xlabel("t (min)")
plt.ylabel("T ($C^o$)")
plt.savefig("T1.png", dpi=500)

plt.figure()
plt.grid(True, linestyle="--")
plt.plot(x2,y2,"r")
plt.plot(t2,T22,".",color="darkred")
plt.xlabel("t (min)")
plt.ylabel("T ($C^o)$")
plt.savefig("T2.png", dpi=500)

#Construcción de tablas


outfile=open("datos12.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$A \ (C^o)$ & $s(A) \\ (C^o)$ & $ B  \ (C^o)$ & $s(B) \ (C^o)$ & $C \ (\mathrm{min}^{-1}) $&  $s(C) \ (\mathrm{min}^{-1}) $ \\\ \\hline \n")
outfile.write("%f  & %f &  %f & %f & %f & %f \\\ \n\\hline\n"%(A1,md.aproximaciondecimales(sa1),B1,md.aproximaciondecimales(sb1),C1,md.aproximaciondecimales(sc1)))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores obtenidos de las regresiones no lineales} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()

outfile=open("datos13.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$A \ (C^o)$ & $s(A) \\ (C^o)$ & $ B  \ (C^o)$ & $s(B) \ (C^o)$ & $C \ (\mathrm{min}^{-1})$ &  $s(C) \ (\mathrm{min}^{-1}) $ \\\ \\hline \n")
outfile.write("%f  & %f &  %f & %f & %f & %f \\\ \n\\hline\n"%(A2,md.aproximaciondecimales(sa2),B2,md.aproximaciondecimales(sb2),C2,md.aproximaciondecimales(sc2)))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores obtenidos de las regresiones no lineales} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()



T11 = np.array(T1[:,1])
T21 = np.array(T2[:,1])


u1 = [0.1]*len(T11)
u2 = [0.1]*len(T21)

T11 = mediaponderada(T11,u1)
T21 = mediaponderada(T21,u2)







