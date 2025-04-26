#-*- coding: utf-8 -*-
#Programa para a realizacion da practica 5
#Autor: Adolfo Otero Fumega
#Mail:adolfo.otero.fumega@usc.es

import numpy as np
import matplotlib as m
import matplotlib.pyplot as plt
import scipy.constants
import random

print("-> Escribe en A a Intensidade (I) que queiras introducir na fonte de alimentación das bobinas Helmholtz e pulsa ENTER:")
I=float(input()) #Intensidade
print("-> Escribe en V a Diferencia de Potencial (V) que queiras introducir para arrincar os electróns e pulsa ENTER:")
V=float(input()) #Diferencia de potencial

#Distintos Parametros, todos eles en unidades do SI
a=0.15 #Raio da Helmholtz
N=130.0 #Numero de espiras da Helmholtz

B=N*scipy.constants.mu_0*I/((5.0/4.0)**(3.0/2.0)*a) #Campo B xerado

r=np.sqrt(2.0*V*scipy.constants.m_e/scipy.constants.e)/B

d=2.0*r

#Grafica:
print(" ")

print(" ")
print("-> Traza que veriamos no experimento:")
print(" ")

# Mesh no que imos a plotear:
p = np.linspace(0, 2*np.pi, 50)
r1 = np.linspace(0, r, 50)
R1, P = np.meshgrid(r1, p)

# Mesh en coordenadas cartesianas:
X_s, Y_s = r*np.cos(P), r*np.sin(P)

fig = plt.figure()
fig.set_size_inches(5.0, 5.0)
plt.style.use('dark_background')
plt.plot(X_s,Y_s, color='cyan', linestyle='-', linewidth=3) 
plt.plot(X_s,Y_s, color='blue', linestyle='-', linewidth=1)
plt.yticks([])	
plt.show()


#Esto inclue desviacions aleatorias de V_1, V_2 e des:

random.seed(a=None, version=2)
d=d+0.0005*random.randint(-11,11)

#Resultados por pantalla das medidas:
print(" ")
print("-> Resultado da medida:")
print(" ")
print("     Diámetro d da traza circular (m): "+str(round(d, 3)))
print(" ")
print(" ")
