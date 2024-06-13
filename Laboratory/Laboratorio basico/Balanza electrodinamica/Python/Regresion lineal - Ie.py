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
x1 = array(tabla[54:74,1])
for i in range(len(x1)):
    if "," in x1[i]:
        x1[i]=x1[i].replace(",", ".")
    if "\n" in x1[i]:
        x1[i]=x1[i].replace("\n","")
x1=array(x1,'float')
t1=linspace(0, max(x1), 100)


y1=array(tabla[54:74,3])
for i in range(len(y1)):
    if "," in y1[i]:
        y1[i]=y1[i].replace(",", ".")
    if "\n" in y1[i]:
        y1[i]=y1[i].replace("\n","")
y1=array(y1,'float')

b1=(sum(x1*y1))/(sum(x1**2))


#------------------------------------------------------------------------------------#

x2 = array(tabla[108:128,1])
for i in range(len(x2)):
    if "," in x2[i]:
        x2[i]=x2[i].replace(",", ".")
    if "\n" in x2[i]:
        x2[i]=x2[i].replace("\n","")
x2=array(x2,'float')
t2=linspace(0,max(x2),100)

y2=array(tabla[108:128,3])
for i in range(len(y2)):
    if "," in y2[i]:
        y2[i]=y2[i].replace(",", ".")
    if "\n" in y2[i]:
        y2[i]=y2[i].replace("\n","")
y2=array(y2,'float')


b2=(sum(x2*y2))/(sum(x2**2))


#------------------------------------------------------------------------------------#

x3 = array(tabla[108:128,1])
for i in range(len(x3)):
    if "," in x3[i]:
        x3[i]=x3[i].replace(",", ".")
    if "\n" in x3[i]:
        x3[i]=x3[i].replace("\n","")
x3=array(x3,'float')
t3=linspace(0,max(x3), 100)

y3=array(tabla[162:182,3])
for i in range(len(y3)):
    if "," in y3[i]:
        y3[i]=y3[i].replace(",", ".")
    if "\n" in y3[i]:
        y3[i]=y3[i].replace("\n","")
y3=array(y3,'float')

b3=(sum(x3*y3))/(sum(x3**2))


#------------------------------------------------------------------------------------#

x4 = x3
t4 = t3

y4=array(tabla[216:236,3])
for i in range(len(y4)):
    if "," in y4[i]:
        y4[i]=y4[i].replace(",", ".")
    if "\n" in y4[i]:
        y4[i]=y4[i].replace("\n","")
y4=array(y4,'float')

b4=(sum(x1*y4))/(sum(x1**2))


#==================================================================================#    
#Programa:
grid(True)
plot(x1, y1, ".b")
p1=polyfit(x1, y1,1)
p1=(b1,0)
h=polyval(p1,t1)
plot(t1,h, "b",label="l=12,5mm")
xlabel("T (Cº)")
ylabel("$\\gamma$  N/m")
xlim(0,max(x1)*1.1)
ylim(min(y1)*0.9,max(y1)*1.1)

grid(True)
plot(x2, y2, ".r")
p2=polyfit(x2, y2,1)
p2=(b2,0)
h=polyval(p2,t2)
plot(t2,h, "r",label="l=25mm")
xlabel("% etanol")
ylabel("$\\gamma$  N/m")
xlim(0,max(x2)*1.1)
ylim(0,max(y2)*1.1)

grid(True)
plot(x3, y3, ".y")
p2=polyfit(x2, y3,1)
p2=(b3,0)
h=polyval(p2,t2)
plot(t2,h, "y",label="l=50mm")
xlabel("% etanol")
ylabel("$\\gamma$  N/m")
xlim(0,max(x2)*1.1)
ylim(0,max(y2)*1.1)

grid(True)
plot(x2, y4, ".g")
p2=polyfit(x2, y4,1)
p2=(b4,0)
h=polyval(p2,t2)
plot(t2,h, "g", label="l=100mm")
xlabel("$I_e$    A")
ylabel("$F_{mag}$    mN")
xlim(0,max(x2)*1.1)
ylim(0,max(y4)*1.1)

legend()

savefig("plot1-balanzaelectrodinamica.png")



















