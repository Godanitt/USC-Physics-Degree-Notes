# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 16:40:45 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

############################ DEFLEXION MAGNETICA ##############################

V=np.array([2.0,2.5,3.0,3.5,4.0,4.5,5.0]) # La incertidumbre asociada será 0.1 (precision) en KV

# El campo magnetico viene dado por B=k*I donde k=4.2mT/A, cuando la distancia entre las
# bobinas es la misma que los radios (radio=68mm)
# Al o mejor hay que sumarle 1 mm o 0.5 mm para que de bien ya que no se donde es el cuadrado bien

d1=[2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4,3.6] # Incertidumbre de 2 mm (ojo+escala)
I1=[0.37,0.41,0.45,0.49,0.53,0.57,0.61,0.66,0.70] # Incertidumbre de 0.01 A (polimetro escala + baile del polimetro)

plt.plot(d1,I1,".",label="V=2.0")

d2=[1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4] # Incertidumbre de 2 mm (ojo+escala)
I2=[0.23,0.26,0.32,0.36,0.41,0.46,0.51,0.55,0.60,0.64,0.68,0.72] # Incertidumbre de 0.01 A (polimetro escala + baile del polimetro)

plt.plot(d2,I2,".",label="V=2.5")

d3=[1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4] # Incertidumbre de 2 mm (ojo+escala)
I3=[0.35,0.40,0.46,0.51,0.56,0.61,0.66,0.71,0.76,0.82] # Incertidumbre de 0.01 A (polimetro escala + baile del polimetro)

plt.plot(d3,I3,".",label="V=3.0")

d4=[1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4] # Incertidumbre de 2 mm (ojo+escala)
I4=[0.33,0.38,0.43,0.49,0.54,0.60,0.66,0.71,0.76,0.83,0.89] # Incertidumbre de 0.01 A (polimetro escala + baile del polimetro)

plt.plot(d4,I4,".",label="V=3.5")

d5=[1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4] # Incertidumbre de 2 mm (ojo+escala)
I5=[0.36,0.42,0.48,0.53,0.59,0.64,0.70,0.77,0.81,0.88,0.94] # Incertidumbre de 0.01 A (polimetro escala + baile del polimetro)

plt.plot(d5,I5,".",label="V=4.0")

d6=[1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4] # Incertidumbre de 2 mm (ojo+escala)
I6=[0.39,0.45,0.51,0.56,0.63,0.69,0.75,0.81,0.87,0.95,1.01] # Incertidumbre de 0.01 A (polimetro escala + baile del polimetro)

plt.plot(d6,I6,".",label="V=4.5")                                                                                                                         

d7=[1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4] # Incertidumbre de 2 mm (ojo+escala)
I7=[0.42,0.47,0.54,0.60,0.67,0.73,0.79,0.86,0.93,0.99,1.06] # Incertidumbre de 0.01 A (polimetro escala + baile del polimetro)

plt.plot(d7,I7,".",label="V=5.0")
plt.legend()

########################### DEFLEXION ELECTRICA ###############################
plt.figure()

d1=[0.8,1.0,1.2,1.4,1.6] # Incertidumbre de 2 mm (ojo+escala)
V1=[192,238,297,367,463] # Incertidumbre de 10 V (es en el rango que visualmente se puede ver la raya por la zona negra + 1V precision)

d2=[0.8,1.0,1.2,1.4] # Incertidumbre de 2 mm (ojo+escala)
V2=[226,292,362,454] # Incertidumbre de 10 V (es en el rango que visualmente se puede ver la raya por la zona negra + 1V precision)

d3=[0.8,1.0,1.2] # Incertidumbre de 2 mm (ojo+escala)
V3=[282,353,444] # Incertidumbre de 10 V (es en el rango que visualmente se puede ver la raya por la zona negra + 1V precision)


d4=[0.8,1.0,1.2] # Incertidumbre de 2 mm (ojo+escala)
V4=[320,392,496] # Incertidumbre de 10 V (es en el rango que visualmente se puede ver la raya por la zona negra + 1V precision)

d5=[0.8,1.0,1.2] # Incertidumbre de 2 mm (ojo+escala)
V5=[320,392,496] # Incertidumbre de 10 V (es en el rango que visualmente se puede ver la raya por la zona negra + 1V precision)

d6=[0.8,1.0] # Incertidumbre de 2 mm (ojo+escala)
V6=[366,470] # Incertidumbre de 10 V (es en el rango que visualmente se puede ver la raya por la zona negra + 1V precision)

d7=[0.8] # Incertidumbre de 2 mm (ojo+escala)
V7=[455] # Incertidumbre de 10 V (es en el rango que visualmente se puede ver la raya por la zona negra + 1V precision)



plt.plot(d1,V1,".",label="V=2.0")
plt.plot(d2,V2,".",label="V=2.5")
plt.plot(d3,V3,".",label="V=3.0")
plt.plot(d4,V4,".",label="V=3.5")
plt.plot(d5,V5,".",label="V=4.0")
plt.plot(d6,V6,".",label="V=4.5")
plt.plot(d7,V7,".",label="V=5.0")

plt.legend()

########################### COMPENSACION CAMPOS ###############################

plt.figure()

Vg=np.array([2,2.5,3,3.5,4,4.5,5])*10**3

V1 = [50,100,150,200,250,300,350]                                                                                               
I1 = [0.11,0.24,0.38,0.52,0.67,0.82,0.98]           

V2 = [50,100,150,200,250,300,350]                                                                                               
I2 = [0.07,0.20,0.33,0.47,0.60,0.72,0.86]                                                                               
                                                     
V3 = [50,100,150,200,250,300,350]                                                                                               
I3 = [0.05,0.17,0.29,0.42,0.53,0.65,0.77]            


V4 = [50,100,150,200,250,300,350]                                                                                               
I4 = [0.04,0.15,0.27,0.37,0.49,0.60,0.72]                                                                               
                                            
V5 = [50,100,150,200,250,300,350]                                                                                               
I5 = [0.04,0.14,0.24,0.35,0.46,0.55,0.66]                                                                               
                                                                    
               
V6 = [50,100,150,200,250,300,350]                                                                                               
I6 = [0.03,0.12,0.21,0.33,0.42,0.52,0.62]                                                                               
                                                                    
               
V7 = [50,100,150,200,250,300,350]                                                                                               
I7 = [0.01,0.11,0.20,0.29,0.39,0.48,0.58]                                                                               
                                                                    
def E(V,d):
    V=np.array(V)
    E=V/d
    return E

def B(I,k):
    I=np.array(I)
    B = k*I
    return B
                                 
                                                                                 
def f(x,a,b):
    y = a + b*x
    return y

k=0.0042
d=0.008

I=np.array([I1,I2,I3,I4,I5,I6,I7])
V=np.array([V1,V2,V3,V4,V5,V6,V7])

E=E(V,d)
B=B(I,k)
m = np.array([])

for i in range(len(E)):
    a,b=curve_fit(f,B[i],E[i],maxfev=30000)[0]
    m = np.append(m,b)

m2=m**2

p0=[1,1]
for i in [0,1,2,3]:
    a,cargamasa=curve_fit(f,Vg*2*10**(11),m2,p0=p0,maxfev=30000)[0]
    p0=[a,cargamasa]

#plt.figure(figsize=(5,3))
#plt.plot(Vg*2*10**(11),m2)

print("La carga masa es %.2f *10**(11)"%(p0[1]))
