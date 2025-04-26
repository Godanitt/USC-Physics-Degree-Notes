# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:55:52 2022

@author: PC
"""

"""
Created on Fri Mar 18 14:55:52 2022

@author: PC
"""
#==============================================================================#
#Importamos los módulos:
from math import sqrt, log10
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
x1 = array(tabla[1:21,0], 'float')
t=linspace(0, max(x1), 10)


y2=array(tabla[1:21,6])
for i in range(len(y2)):
    if "," in y2[i]:
        y2[i]=y2[i].replace(",", ".")
    if "\n" in y2[i]:
        y2[i]=y2[i].replace("\n","")
y2=array(y2,'float')
##################################################    
#Programa:
grid(True)
plot(x1, y2, ".b")
p=polyfit(x1, y2,1)
h=polyval(p,t)
plot(t,h, "c")
xlabel("f (Hz)")
ylabel("Vmr/Vmc")
xlim(0,max(x1)*1.1)
ylim(0,3)
plot((1-p[1])/p[0],1, "k.")
xticks([0,500,1000,(1-p[1])/p[0],2000,2500,3000,3500,4000]) 

savefig("Plot1.png")