# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:55:52 2022

@author: PC
"""
#==============================================================================#
#Importamos los módulos:
from math import sqrt, log10, pi
from numpy import array, linspace, dtype
from matplotlib.pyplot import plot, grid, ylabel, xlabel, xlim, ylim, savefig, xticks, yticks, clf, legend
from pylab import polyfit, polyval
from numpy import loadtxt, savetxt, array

#==================================================================================#
#Datos:
infile=open("Tensión superficial.tsv", 'r')
tabla = []
lines = infile.readlines()
for i in lines:
    print(i)
    tabla.append(i.split("\t"))
infile.close
tabla = array(tabla)
x1 = array(tabla[15:25,2])
for i in range(len(x1)):
    if "," in x1[i]:
        x1[i]=x1[i].replace(",", ".")
    if "\n" in x1[i]:
        x1[i]=x1[i].replace("\n","")
x1=array(x1,'float')
t1=linspace(min(x1), max(x1), 100)


y1=array(tabla[15:25,0])
for i in range(len(y1)):
    if "," in y1[i]:
        y1[i]=y1[i].replace(",", ".")
    if "\n" in y1[i]:
        y1[i]=y1[i].replace("\n","")
y1=array(y1,'float')


#==================================================================================#    
#Programa:
grid(True)
plot(x1, y1, ".b",label="puntos exprimentales")
p1=polyfit(x1, y1,1)
p1=array([0.217,0])
h=polyval(p1,t1)
plot(t1,h, "r", label="regresión lineal")
xlabel("$T_1^2h_1-T^2_2h_2 \ \ (s^2m) $")
ylabel("$h_1^2-h_2^2  \ \ (m^2)$")
xlim(-4,3.5)
ylim(-0.9,0.9)

p2=(0.248,0)
h2=polyval(p2,t1)
plot(t1,h2,"g", label="linea para g=9,81")

legend()

savefig("Plot2-Kater.png")







