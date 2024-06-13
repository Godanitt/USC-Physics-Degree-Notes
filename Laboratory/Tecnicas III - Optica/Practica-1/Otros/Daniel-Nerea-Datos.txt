# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:32:03 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt

def focal(s,sprima,d) :
    f=[0]*len(s)
    for i in range(len(s)):
        f[i] = -(1/(-sprima[i]+d[i])-1/(d[i]-s[i]))**(-1)
    return np.array(f)

# Primer experimento

s = 0.5                         # En cm, para todos los datos

# Primera distancia
objeto1=np.array([5]*6)          #En cm
imagen1=np.array([101.1,100,101.2,100.3,102.00,100.9])
lente1=np.array([80.5]*6)

focal1=focal(objeto1,imagen1,lente1)



# Segunda distancia
objeto2=np.array([5]*6)          #En cm
imagen2=np.array([105.0,105.9,104.5,105.9,104.9,105.8])
lente2=np.array([85.0]*6)


focal2=focal(objeto2,imagen2,lente2)

# Terce distancia
objeto3=np.array([5]*6)          #En cm
imagen3=np.array([110.5,109.6,110.8,109.6,110.5,109.6])
lente3=np.array([90]*6)

focal3=focal(objeto3,imagen3,lente3)


# Cuarta distancia
objeto4=np.array([5]*6)          #En cm
imagen4=np.array([114.9,113.9,114.7,113.7,115.0,113.9])
lente4=np.array([95]*6)

focal4=focal(objeto4,imagen4,lente4)

# Quinta distancia
objeto5=np.array([5]*6)          #En cm
imagen5=np.array([119.0,119.9,118.9,119.9,118.9,119.7])
lente5=np.array([100]*6)

focal5=focal(objeto5,imagen5,lente5)

# Sexta distancia

objeto6=np.array([5]*6)          #En cm
imagen6=np.array([124.5,123.9,124.6,123.6,124.5,123.8])
lente6=np.array([105]*6)

focal6=focal(objeto6,imagen6,lente6)

focala=np.average([focal1,focal2,focal3,focal4,focal5,focal6])
print("focal1= %.2f"%focala)


# Segundo experimento

imagen=np.array([33.4,19.9,35.7,59.8,24.4,15.0,27.6,39,46,31.4])
lente=np.array([50,36.5,52,75.3,40.2,32.0,44.6,56.2,62.9,48.5])

focal=lente-imagen
print('focal= %.2f'%np.average(focal))

# Tercer experimento 

def focalbessel(a,e):    
    f=((np.average(a)**2)-(np.average(e))**2)/(4*np.average(a))
    return f

# Primera medida

a1 = np.array([105,105,105,105,105])
a2 = np.array([5,5,5,5,5])
a = a1-a2
e1 = np.array([85,84,85.2,84.7])
e2 = np.array([25.5,25.5,26.2,24.9])
e = e1-e2

f=focalbessel(a,e)
print("f= %.2f"%f)

# Segunda medida

a1 = np.array([100]*5)
a2 = np.array([5]*5)
a = a1-a2
e1 = np.array([25.2,26.4,25.2,26.4,25.0])
e2 = np.array([78.8,80.0,78.6,79.7,78.9])
e = e1-e2

f=focalbessel(a,e)
print("f= %.2f"%f)

# Tercera medida


a1 = np.array([95]*5)
a2 = np.array([5]*5)
a = a1-a2
e1 = np.array([26.5,26.8,25.6,26.9,27.2])
e2 = np.array([73.4,74.6,73.0,74.9,75.0])
e = e1-e2

f=focalbessel(a,e)
print("f= %.2f"%f)


# Cuarta medida

a1 = np.array([90]*5)
a2 = np.array([5]*5)
a = a1-a2
e1 = np.array([28.0,26.1,27.6,26.6,27.3])
e2 = np.array([69.0,68.4,68.8,67.9,69.2])
e = e1-e2

f=focalbessel(a,e)
print("f= %.2f"%f)


# Quinta medida

a1 = np.array([85]*5)
a2 = np.array([5]*5)
a = a1-a2
e1 = np.array([28.6,27,28.4,27.1,28.1])
e2 = np.array([63.5,61.9,63.2,62.4,62.7])
e = e1-e2

f=focalbessel(a,e)
print("f= %.2f"%f)

# Cuarto experimento

def focal(s,sprima,d) :
    f=[0]*len(s)
    for i in range(len(s)):
        f[i] = -(1/(-sprima[i]+d[i])-1/(d[i]-s[i]))**(-1)
    return np.array(f)

# Medida 1

di = np.array([13.0,13.5,13.4]) # Posicion objeto con lente divergente
dl = np.array([27.7,27.7,27.7]) # Posicion lente divergente (enfocada)

si = np.array([18.7,18.6,18.9]) # Posición objeto sin lente divergente
sl = np.array([27.7,27.7,27.7]) # Posición lente divergente (desenfocada)

focalita=focal(di,si,dl)
print(np.average(focalita))

# Medida 2


di = np.array([23.4,22.8,23.4]) # Posicion objeto con lente divergente
dl = np.array([40.9]*3) # Posicion lente divergente (enfocada)

si = np.array([31.2,30.5,31.1]) # Posición objeto sin lente divergente
sl = np.array([40.9]*3) # Posición lente divergente (desenfocada)

focalita=focal(di,si,dl)

print(np.average(focalita))

# Medida 3

di = np.array([25.2,26.4,24.3]) # Posicion objeto con lente divergente
dl = np.array([39.6]*3) # Posicion lente divergente (enfocada)

si = np.array([30.9,30.9,31.1]) # Posición objeto sin lente divergente
sl = np.array([39.6,]*3) # Posición lente divergente (desenfocada)

focalita=focal(di,si,dl)

print(np.average(focalita))

# Medida 4

di = np.array([29.4,28.7,30.4]) # Posicion objeto con lente divergente
dl = np.array([53]*3) # Posicion lente divergente (enfocada)

si = np.array([42.6,42.3,42.6]) # Posición objeto sin lente divergente
sl = np.array([53]*3) # Posición lente divergente (desenfocada)

focalita=focal(di,si,dl)

print(np.average(focalita))

# Medida 5

di = np.array([18.7,19.3,18.9]) # Posicion objeto con lente divergente
dl = np.array([35.5]*3) # Posicion lente divergente (enfocada)

si = np.array([26.4,26.2,26.4]) # Posición objeto sin lente divergente
sl = np.array([35.5]*3) # Posición lente divergente (desenfocada)

focalita=focal(di,si,dl)

print(np.average(focalita))







