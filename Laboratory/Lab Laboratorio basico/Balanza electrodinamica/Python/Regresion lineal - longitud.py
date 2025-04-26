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
x1 = array(tabla[405:409,0])
for i in range(len(x1)):
    if "," in x1[i]:
        x1[i]=x1[i].replace(",", ".")
    if "\n" in x1[i]:
        x1[i]=x1[i].replace("\n","")
x1=array(x1,'float')
t1=linspace(0, max(x1), 100)


y1=array(tabla[405:409,3])
for i in range(len(y1)):
    if "," in y1[i]:
        y1[i]=y1[i].replace(",", ".")
    if "\n" in y1[i]:
        y1[i]=y1[i].replace("\n","")
y1=array(y1,'float')

b1=(sum(x1*y1))/(sum(x1**2))


#------------------------------------------------------------------------------------#

x2 = array(tabla[405:409,0])
for i in range(len(x2)):
    if "," in x2[i]:
        x2[i]=x2[i].replace(",", ".")
    if "\n" in x2[i]:
        x2[i]=x2[i].replace("\n","")
x2=array(x2,'float')
t2=linspace(0,max(x2),100)

y2=array(tabla[415:419,3])
for i in range(len(y2)):
    if "," in y2[i]:
        y2[i]=y2[i].replace(",", ".")
    if "\n" in y2[i]:
        y2[i]=y2[i].replace("\n","")
y2=array(y2,'float')

b2=(sum(x1*y2))/(sum(x1**2))


#------------------------------------------------------------------------------------#

x3 = array(tabla[405:409,0])
for i in range(len(x3)):
    if "," in x3[i]:
        x3[i]=x3[i].replace(",", ".")
    if "\n" in x3[i]:
        x3[i]=x3[i].replace("\n","")
x3=array(x3,'float')
t3=linspace(0,max(x3), 100)

y3=array(tabla[425:429,3])
for i in range(len(y3)):
    if "," in y3[i]:
        y3[i]=y3[i].replace(",", ".")
    if "\n" in y3[i]:
        y3[i]=y3[i].replace("\n","")
y3=array(y3,'float')

b3=(sum(x1*y3))/(sum(x1**2))


#------------------------------------------------------------------------------------#

x4 = x3
t4 = t3

y4=array(tabla[435:439,3])
for i in range(len(y4)):
    if "," in y4[i]:
        y4[i]=y4[i].replace(",", ".")
    if "\n" in y4[i]:
        y4[i]=y4[i].replace("\n","")
y4=array(y4,'float')

b4=(sum(x1*y4))/(sum(x1**2))


#------------------------------------------------------------------------------------#


x5 = x3
t5 = t3

y5=array(tabla[445:449,3])
for i in range(len(y5)):
    if "," in y5[i]:
        y5[i]=y5[i].replace(",", ".")
    if "\n" in y5[i]:
        y5[i]=y5[i].replace("\n","")
y5=array(y5,'float')

b5=(sum(x1*y5))/(sum(x1**2))


#==================================================================================#    
#Programa:
grid(True)
plot(x1, y1, ".b")
p1=polyfit(x1, y1,1)
p1=(b1,0)
h=polyval(p1,t1)
plot(t1,h, "b",label="$I_e = 0,8$ A")
xlabel("T (Cº)")
ylabel("$\\gamma$  N/m")
xlim(0,max(x1)*1.1)
ylim(min(y1)*0.9,max(y1)*1.1)

grid(True)
plot(x2, y2, ".r")
p2=polyfit(x2, y2,1)
p2=(b2,0)
h=polyval(p2,t2)
plot(t2,h, "r",label="$I_e = 1,6$ A")
xlabel("% etanol")
ylabel("$\\gamma$  N/m")
xlim(0,max(x2)*1.1)
ylim(0,max(y2)*1.1)

grid(True)
plot(x3, y3, ".y")
p2=polyfit(x2, y3,1)
p2=(b3,0)
h=polyval(p2,t2)
plot(t2,h, "y",label="$I_e = 2,4$ A")
xlabel("% etanol")
ylabel("$\\gamma$  N/m")
xlim(0,max(x2)*1.1)
ylim(0,max(y2)*1.1)


grid(True)
plot(x2, y4, ".g")
p2=polyfit(x2, y4,1)
p2=(b4,0)
h=polyval(p2,t2)
plot(t2,h, "g", label="$I_e = 3,2$ A")
xlabel("$I_b$    A")
ylabel("$F_{mag}$    mN")
xlim(0,max(x3)*1.1)
ylim(0,max(y4)*1.1)


grid(True)
plot(x2, y5, ".m")
p2=polyfit(x2, y5,1)
p2=(b5,0)
h=polyval(p2,t2)
plot(t2,h, "m", label="$I_e = 4$ A")
xlabel("L    mm")
ylabel("$F_{mag}$    mN")
xlim(0,max(x4)*1.1)
ylim(0,max(y5)*1.1)

xticks([12.5,25,50,75,100])

legend()

savefig("plot2-balanzaelectrodinamica.png")