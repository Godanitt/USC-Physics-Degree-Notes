# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:55:52 2022

@author: PC
"""
#==============================================================================#
#Importamos los módulos:
from math import sqrt, log10, pi
from numpy import array, linspace, dtype
from matplotlib.pyplot import plot, grid, ylabel, xlabel, xlim, ylim, savefig, xticks, yticks, clf
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
x1 = array(tabla[32:57,1])
for i in range(len(x1)):
    if "," in x1[i]:
        x1[i]=x1[i].replace(",", ".")
    if "\n" in x1[i]:
        x1[i]=x1[i].replace("\n","")
x1=array(x1,'float')
t1=linspace(0, max(x1), 100)


y1=array(tabla[32:57,3])
for i in range(len(y1)):
    if "," in y1[i]:
        y1[i]=y1[i].replace(",", ".")
    if "\n" in y1[i]:
        y1[i]=y1[i].replace("\n","")
y1=array(y1,'float')

#------------------------------------------------------------------------------------#

x2 = array(tabla[62:72,1])
for i in range(len(x2)):
    if "," in x2[i]:
        x2[i]=x2[i].replace(",", ".")
    if "\n" in x2[i]:
        x2[i]=x2[i].replace("\n","")
x2=array(x2,'float')
t2=linspace(min(x2)*0.9,max(x2), 100)

y2=array(tabla[62:72,3])
for i in range(len(y2)):
    if "," in y2[i]:
        y2[i]=y2[i].replace(",", ".")
    if "\n" in y2[i]:
        y2[i]=y2[i].replace("\n","")
y2=array(y2,'float')

#==================================================================================#    
#Programa:
grid(True)
plot(x1, y1, ".b")
p1=polyfit(x1, y1,1)
h=polyval(p1,t1)
plot(t1,h, "c")
xlabel("T (Cº)")
ylabel("$\\gamma$  N/m")
xlim(0,max(x1)*1.1)
ylim(min(y1)*0.9,max(y1)*1.1)
savefig("plot1-tensionsuperficial.png")

clf()

grid(True)
plot(x2, y2, ".b")
p2=polyfit(x2, y2,2)
h=polyval(p2,t2)
plot(t2,h, "c")
xlabel("% etanol")
ylabel("$\\gamma$  N/m")
xlim(0,max(x2)*1.1)
ylim(0.015,0.08)

savefig("plot2-tensionsuperficial.png")









