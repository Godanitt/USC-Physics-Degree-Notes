# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from math import sqrt
from numpy import array, linspace
from matplotlib.pyplot import plot, grid, ylabel, xlabel, title, xlim, ylim
from pylab import polyfit, polyval
##############################

R1=22*10**4         #Valor de la resistencia r1 teoricamente
R2=39*10**4         #Valor de la resistencia r2 teoricamente
SR1=R1*5/100        #Valor de la incertidumbre de la resistencia r1 teoricamente
SR2=R2*5/100        #Valor de la incertidumbre de la resistencia r2 teoricamente

""" 
#1: corriente continua
    #1.1 Ahora vamos a calcular los valores de la resistencia de la resistencia equivalente, 
    su incertidumbre.
    #1.2 Hacemos la regresión lineal de los valores calculados experimentalmente para así 
    calcular la resi
#1.2stencia total del circuito.   
"""

#1.1
RE1=R1+R2
SRE1=sqrt(SR1**2+SR2**2)

V=[]
for i in range(10):
    V.append(float(i+1))
SRV=0.1

I=[7.5E-6,14.7E-6,21.7E-6,28.9E-6,35.9E-6,43.2E-6,50.5E-6,57.5E-6,64.5E-6,72.0E-6]
I=array(I,'float')

t=linspace(0,72.0E-6)
plot(I,V,'b.',)
grid(True)
ylabel("V (V)")
xlabel("I (A)")
p=polyfit(I,V,1)
p[1]=0
p[0]=138971
h=polyval(p,t)
v=polyval(p,I)
plot(I,v,'r')
xlim(0,0.00008)
ylim(0,11)
plot(t,h,'r')
