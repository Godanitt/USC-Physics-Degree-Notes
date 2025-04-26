# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:55:52 2022

@author: PC
"""
#==============================================================================#
#Importamos los módulos:
from math import sqrt, log10, pi
from numpy import array, linspace, dtype
from matplotlib.pyplot import plot, grid, ylabel, xlabel, title, xlim, ylim, savefig, xticks, yticks
from pylab import polyfit, polyval
from numpy import loadtxt, savetxt, array

#==================================================================================#
#Datos:
infile=open("CorrienteAlterna.txt.tsv", 'r')
tabla = []
lines = infile.readlines()
for i in lines:
    print(i)
    tabla.append(i.split("\t"))
infile.close
tabla = array(tabla)
x1 = array(tabla[23:43,1])
for i in range(len(x1)):
    if "," in x1[i]:
        x1[i]=x1[i].replace(",", ".")
    if "\n" in x1[i]:
        x1[i]=x1[i].replace("\n","")
x1=array(x1,'float')
t=linspace(min(x1), max(x1), 100)


y1=array(tabla[23:43,3])
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
p=polyfit(x1, y1,2)
h=polyval(p,t)
plot(t,h, "c")
xlabel("f (Hz)        (escala logarítimica)")
ylabel("Desfase (-º)")
xlim(min(x1)*0.9,max(x1)*1.1)
ylim(0,max(y1)*1.1)
f1=(-p[1]-sqrt(p[1]**2-4*(p[2]-45)*p[0]))/(2*p[0])
plot(f1,45,"k.")

xticks=([2,2.25,2.5,2.75,3.00,f1])

savefig("Regresión1.png")






