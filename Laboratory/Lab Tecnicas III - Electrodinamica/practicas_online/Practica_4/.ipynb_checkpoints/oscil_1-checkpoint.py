#-*- coding: utf-8 -*-
#Programa para a realizacion da practica 4
#Autor: Adolfo Otero Fumega
#Mail:adolfo.otero.fumega@usc.es

import numpy as np
import matplotlib as m
import matplotlib.pyplot as plt
import scipy.constants
import random

print("-> Escribe en Hz a frecuencia (f) que queiras introducir no xerador de sinal e pulsa ENTER:")
nu=float(input()) #Frecuencia

#Distintos Parametros, todos eles en unidades do SI
om=nu*2.0*np.pi #Frecuencia angular
R_2=0.0075 #Raio do solenoide interior ao cilindro condutor
R_1=0.0100 #Raio do solenoide exterior ao cilindro condutor
N_2=200.0 #Numero de espiras do solenoide interior ao cilindro condutor
N_1=100.0 #Numero de espiras do solenoide exterior ao cilindro condutor
d=0.001 # Anchura do cilindro condutor
sigma=59600000 #Codutividade do cilindro condutor
T_p=2.0*np.pi/om #Periodo
B=np.sqrt(scipy.constants.mu_0*sigma*om/2.0) #Coeficiente de Atenuacion

des=int(B*d*180/np.pi) #Desfase
at=(R_2*N_2/(R_1*N_1))/np.sqrt((np.sinh(B*d)**2*np.sin(B*d)**2+np.cosh(B*d)**2*np.cos(B*d)**2)) #Atenuacion

V_1=1.00
V_2=at*V_1



#Grafica no osciloscopio:
print(" ")

print(" ")
print("-> Imaxe que veriamos no osciloscopio, a liña contínua vermella é V_1 e a liña a trazos azul é V_2:")
print(" ")

x = np.arange(-2*np.pi,2*np.pi,0.1)   # start,stop,step
y1 = V_1*np.sin(x)
y2 = V_2*np.sin(x+B*d)
plt.plot(x,y1, color='r', linestyle='-')
plt.plot(x,y2, color='b', linestyle='--')
plt.xlabel('Escala axustada no osciloscopio para observar 2 períodos')
plt.ylabel('V (V)')
plt.grid(True)
plt.show()


#Esto inclue desviacions aleatorias de V_1, V_2 e des:

random.seed(a=None, version=2)
V_1=V_1+0.0005*random.randint(-101,101)
V_2=V_2+0.0005*random.randint(-101,101)
des=des+0.01*random.randint(-101,101)

#Resultados por pantalla das medidas:
print(" ")
print("-> Resultados das medidas:")
print(" ")
print("     Forza electromotriz inducida V_1 (V): "+str(round(V_1, 2)))
print("     Forza electromotriz inducida V_2 (V): "+str(round(V_2, 2)))
print("     Desfase (º): "+str(round(des, 1)))
print(" ")
print(" ")
