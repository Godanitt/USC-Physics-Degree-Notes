# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:09:54 2022

@author: PC
"""


#==============================================================================#
#Importamos los módulos:
from math import sqrt, log10, pi
from numpy import array, linspace, dtype
from matplotlib.pyplot import plot, grid, ylabel, xlabel, xlim, ylim, savefig, xticks, yticks
from pylab import polyfit, polyval
from numpy import loadtxt, savetxt, array

#==================================================================================#
#Datos:
infile=open("CorrienteContinua.tsv", 'r')
tabla = []
lines = infile.readlines()
for i in lines:
    print(i)
    tabla.append(i.split("\t"))
infile.close
tabla = array(tabla)
x1 = array(tabla[1:11,2])
for i in range(len(x1)):
    if "," in x1[i]:
        x1[i]=x1[i].replace(",", ".")
    if "\n" in x1[i]:
        x1[i]=x1[i].replace("\n","")
x1=array(x1,'float')
t=linspace(0, max(x1), 100)


y1=array(tabla[1:11,1])
for i in range(len(y1)):
    if "," in y1[i]:
        y1[i]=y1[i].replace(",", ".")
    if "\n" in y1[i]:
        y1[i]=y1[i].replace("\n","")
y1=array(y1,'float')
#==================================================================================#    
#Programa:
grid(True)
plot(x1, y1, ".b")
p=polyfit(x1, y1,1)
h=polyval(p,t)
plot(t,h, "c")
xlabel("I (A)")
ylabel("V (V)")
xlim(0,max(x1)*1.1)
ylim(0,max(y1)*1.1)







