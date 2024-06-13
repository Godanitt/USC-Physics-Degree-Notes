# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 16:05:06 2024

@author: danie
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte

def f(x,a,b):
    y=a+b*x
    return y

def longitud_onda(theta,zero,d):
    a=np.pi/180
    l_o=np.array([])
    l_oi=np.array([])
    l_od=np.array([])
    phi=abs(theta-zero)
    if len(phi)%2==0:
        n=len(phi)/2
        for i in range(int(n)):
            #print(i,"-",len(phi)-1-i)
            l_oi=np.append(l_oi,(d/(n-i))*np.sin(phi[len(phi)-1-i]*a))
            l_od=np.append(l_od,(d/(n-i))*np.sin(phi[i]*a))
            l_o=np.append(l_o,(d/(n-i))*np.sin(phi[i]*a))
            l_o=np.append(l_o,(d/(n-i))*np.sin(phi[len(phi)-1-i]*a))
    
    else:
        l_o=np.append(l_o,(d/(3))*np.sin(phi[0]*a))
        l_od=np.append(l_od,(d/(3))*np.sin(phi[0]*a))
        phi=phi[1:]
        n=(len(phi))/2
        for i in range(int(n)):
            l_oi=np.append(l_oi,(d/(n-i))*np.sin(phi[len(phi)-1-i]*a))
            l_od=np.append(l_od,(d/(n-i))*np.sin(phi[i]*a))
            l_o=np.append(l_o,(d/(n-i))*np.sin(phi[i]*a))
            l_o=np.append(l_o,(d/(n-i))*np.sin(phi[len(phi)-1-i]*a))
    
    l_0=np.average(l_o)   
    l_0d=np.average(l_od)   
    l_0i=np.average(l_oi)        
    return np.array([l_0,l_0i,l_0d])
        
d=10**(-3)/600
 
zero1=53+27.5/60

rojo1=np.array([0+40.5/60,30+6/60,76+56/60,16.5/60])
turquesa1=np.array([-8-33.5/60,17+26/60,36+20/60,70+40/60,89,115+46.5/60])
azul1=np.array([1+26.5/60,22+44.5/60,38+15/60,68+46.5/60,85+19/60])

zero2=53+33.5/60

rojo2=np.array([0+53/60,30+7.5/60,77,106.20/60])
turquesa2=np.array([-8-33.5/60,17+26/60,36+20/60,70+40/60,89+40/60,115+46.5/60])
azul2=np.array([1+26.5/60,22+46.5/60,38+15/60,68+46.5/60,85+19/60])

zero3=53+34/60
rojo3=np.array([0+48/60,30+7/60,77,106+14/60])
turquesa3=np.array([-8-39.5/60,17+25/60,36+25.5/60,70+43.5/60,89+49.5/60,115+28.5/60])
azul3=np.array([1+29.5/60,22+46/60,38+18.5/60,68+49.5/60,85+25/50])

zero4=53+36.5/60
rojo4=np.array([49.5/60,30+9.5/60,77+1/60,106+13.5/60])
turquesa4=np.array([-4-43.5/60,17+27.5/60,36+26.5/60,70+43.5/60,89+40.5/60,115+39.5/60])
azul4=np.array([3+42/60,21+49.5/60,38+18/60,68+47.5/60,85+15/60])
zero=np.array([zero1,zero2,zero3,zero4])

rojo=np.array([rojo1,rojo2,rojo3,rojo4])
azul=np.array([azul1,azul2,azul3,azul4])
turquesa=np.array([turquesa1,turquesa2,turquesa3,turquesa4])

lrojo=np.array([])
lrojo_d=np.array([])
lrojo_i=np.array([])
lazul=np.array([])
lazul_d=np.array([])
lazul_i=np.array([])
lturquesa=np.array([])
lturquesa_d=np.array([])
lturquesa_i=np.array([])

for i in range(len(zero)):
    lrojo=np.append(lrojo,longitud_onda(rojo[i], zero[i], d)[0]*10**9)
    lrojo_d=np.append(lrojo_d,longitud_onda(rojo[i], zero[i], d)[2]*10**9)
    lrojo_i=np.append(lrojo_i,longitud_onda(rojo[i], zero[i], d)[1]*10**9)
    lazul=np.append(lazul,longitud_onda(azul[i], zero[i], d)[0]*10**9)
    lazul_d=np.append(lazul_d,longitud_onda(azul[i], zero[i], d)[2]*10**9)
    lazul_i=np.append(lazul_i,longitud_onda(azul[i], zero[i], d)[1]*10**9)
    lturquesa=np.append(lturquesa,longitud_onda(turquesa[i], zero[i], d)[0]*10**9)
    lturquesa_d=np.append(lturquesa_d,longitud_onda(turquesa[i], zero[i], d)[2]*10**9)
    lturquesa_i=np.append(lturquesa_i,longitud_onda(turquesa[i], zero[i], d)[1]*10**9)

print("lrojo=",lrojo)
print("lturquesa",lturquesa)
print("lazul=",lazul)

print("-"*40)  

print("lrojo_d=",lrojo_d)
print("lturquesa_d",lturquesa_d)
print("lazul_d=",lazul_d)

print("-"*40)  
print("lrojo_i=",lrojo_i)
print("lturquesa_i",lturquesa_i)
print("lazul_i=",lazul_i)

def R(lrojo, lazul, lturquesa,nombre):  
    a=np.array([])
    b=np.array([])
    for i in range(len(lrojo)):        
        n=2
        m=np.array([5,4,3])
        plt.figure()
        plt.title(nombre+" "+"%d"%(i+1))
        l=np.array([lrojo[i],lturquesa[i],lazul[i]])
        x=(1/(n**2)+1/(m**2))
        #print(l,x)
        y=1/l
        a0,b0=curve_fit(f,x,y,maxfev=3000)[0]
        u=np.linspace(min(x),max(x),20)
        v=f(u,a0,b0)
        plt.plot(u,v,color="blue")
        plt.plot(x,y,".",color="red")
        a=np.append(a,a0)
        b=np.append(b,b0*10**2)
    return b

print("-"*40)  
R_m=R(lrojo,lazul,lturquesa,"Media")
for i in range(len(R_m)):
    print("R = %.3f *10^7"%R_m[i])
    
print("-"*40)  

R_d=R(lrojo_d,lazul_d,lturquesa_d,"Derecha")

for i in range(len(R_d)):
    print("R_d = %.3f *10^7"%R_d[i])
print("-"*40)  
R_i=R(lrojo_i,lazul_i,lturquesa_i,"Izquierda")
for i in range(len(R_i)):
    print("R_i = %.3f *10^7"%R_i[i])
print("-"*40)  