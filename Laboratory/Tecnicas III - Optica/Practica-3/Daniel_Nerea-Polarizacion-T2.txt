# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 17:08:56 2024

@author: danie
"""
import numpy as np
import matplotlib.pyplot as plt
import math as mt
#====================Ley Malus:MÁXIMO DE I(theta)================================

cero=0.11  #microW, tuvimos que cambiar la escala porque oscilaba
theta=np.array([0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180])-90#2 grados 
potencia=np.array([0.14,0.18,0.47,0.93,1.50,2.22,2.82,3.35,3.78,3.95,3.85,3.63,3.18,
2.59,1.9,1.27,0.68,0.30,0.13])-0.11
plt.plot(theta,potencia,'.',color='teal')
#a=mt.cos(theta)*mt.cos(theta)
#plt.plot(a,potencia,'.')
#====================LAMINA RETARDADORA===============================

#el polarizador p-8 tiene su orientacion vertical para el angulo -20º
lamina=240  #para este angulo los ejes de la lamina retardadora coinciden el vert-hrizont
#feixe de luz l.pol. 210º se movio 30º para que se vea

Wa=1.75
thetaa=60 # respecto la horizontal

Wb=0.65
thetab=30 # respecto la horizontal referencia el polarizador 2 / el detallado'P1'
#nuestra ref es 150 n0 los  180 que medimos porque movimos la lamina 30º

# Nuestro cero respecto los ejes principales esta en el 150 del polarizdor P1
#ELÍPTICO
theta2=np.array([0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180]) #respecto ejes ppales
W2=np.array([0.66,0.68,0.75,0.91,1.11,1.32,1.48,1.62,1.76,1.81,1.77,1.68,1.56,1.35,
             1.17,0.96,0.78,0.69,0.66])
plt.figure()
plt.title("polarizacion eliptica")
plt.plot(theta2,W2,".",color="blue")
#CIRCULAR
plt.figure()
plt.title("polarizacion circular")
theta3=np.array([140,170,200,230,260,290,320,350,20,50,80,110])-135
W3=np.array([1.13,1.15,1.15,1.12,1.10,1.08,1.13,1.15,1.15,1.12,1.09,1.08])
plt.plot(theta3,W3,".",color="blue")
I=max(W3)/min(W3)
print(I)


#=============================BREWSTER=================================
P1=180  #angulo de polarizacion horizontal POLARIZADOR P1

