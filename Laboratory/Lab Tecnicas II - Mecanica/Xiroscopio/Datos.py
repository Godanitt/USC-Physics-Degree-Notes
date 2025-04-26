# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 09:36:42 2022

@author: PC
""" 

"""

import numpy as np
import math as mth
import matplotlib.pyplot as plt
import pylab as py

distancia = np.linspace(3,60,20)
tiempo =  [2-0.2, 2-0.25, 2-0.3, 2-0.45, 2-0.5,2-0.6, 2-0.7,2-0.8, 2-0.9,2-0.95, 2-1.05, 2-1.15, 2-1.2, 2-1.3, 2-1.4, 2-1.5, 2-1.6, 2-1.7, 2-1.8, 2-1.9]

tiempos=[0]*20

for i in range(len(tiempo)):
    tiempos[i] = tiempo[len(tiempo)-i-1]
 [2-0.2, 2-0.25, 2-0.3, 2-0.45, 2-0.5,2-0.6, 2-0.7,2-0.8, 2-0.9,2-0.95, 2-1.05, 2-1.15, 2-1.2, 2-1.3, 2-1.4, 2-1.5, 2-1.6, 2-1.7, 2-1.8, 2-1.9]
plt.grid(True)
p = py.polyfit(tiempos, distancia,1)
h = py.polyval(p,tiempos)
plt.plot(tiempos,distancia, "r.")
plt.plot(tiempos,h)

"""

import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
from IPython.display import display, Latex
import pandas as pd
pd.set_option('precision', 2)


def media(xlist):
    return sum(xlist)/len(xlist)

def sigma(xlist):
    return np.sqrt(sum((xlist-media(xlist))**2)/(1.*len(xlist)*(len(xlist)-1.)))

def sigmab(xlist):
    return np.sqrt(sum((xlist-media(xlist))**2)/(1.*len(xlist)*(len(xlist)-1)))

def utotal(ua,ub):
    return np.sqrt(ua**2+ub**2)

#ajuste lineal y=a+bx
def ajustelinealponderado(x,y,sig): # Aquí metemos los dos valores y el peso estadístico (sig)

    H=np.array([[sum(1./sig**2),sum(x/sig**2)],[sum(x/sig**2),sum(x**2/sig**2)]])
    Delta=det(H)
    Z=np.array([sum(y/sig**2),sum((x*y)/sig**2)])
    
    ([a,b])=np.matmul(inv(H),Z)
    
    siga=np.sqrt(sum(x**2/sig**2)/Delta)
    sigb=np.sqrt(sum(1./sig**2)/Delta)
    
    r = np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))
    
    return a,b,siga,sigb,r

def ajustelineal(x,y):
    HX=len(x)*(np.dot(x,x))-sum(x)**2
    HY=len(y)*(np.dot(y,y))-sum(y)**2
    a = (sum(y)*sum(x**2)-sum(x)*sum(x*y))/(HX)
    b = (len(x)*sum(x*y)-sum(x)*sum(y))/(HX)
    s=np.sqrt(sum((y-a-b*x)**2)/(len(x)-2))
    siga=s*np.sqrt((sum(x**2))/HX)
    sigb=s*np.sqrt(len(x)/HX)
    r=(len(x)*sum(x*y)-sum(x)*sum(y))/(np.sqrt(HX*HY))
    return a,b,siga,sigb,r

def mediaponderada(u,sigu):
    w=np.zeros([len(sigu)])
    for i in range(len(sigu)):
        w[i]=1/sigu[i]**2
    k=sum(w)
    media=np.dot(u,w)/k
    s = 1/np.sqrt(k)
    return media, s

"""

y=np.array(np.linspace(3,60,20))

n=len(y)

tiempo =  [2-0.2, 2-0.25, 2-0.3, 2-0.45, 2-0.5,2-0.6, 2-0.7,2-0.8, 2-0.9,2-0.95, 2-1.05, 2-1.15, 2-1.2, 2-1.3, 2-1.4, 2-1.5, 2-1.6, 2-1.7, 2-1.8, 2-1.9]

x=[0]*20

for i in range(n):
    x[i] = tiempo[n-i-1]


x=np.array(x)
y=np.array(y)

datos = pd.DataFrame({'x': x, 'y': y},index=np.arange(n)+1)
display(datos)

cadena  = '\\begin{array}{|r|r|} \hline x & y \\\\ \hline'
for i in range(10):
    cadena += '%3.2f & %3.2f \\\\' % (x[i],y[i])
cadena += '\hline \end{array}'

display(Latex(cadena))

ymed=media(y)
display(Latex(r'$ \bar{y} =%i $' % ymed))


sigbar=sigmab(y)
display(Latex(r'$\sigma(\bar y)=%i $' % sigbar))

sigi=np.sqrt(y)

uy=np.array([0.2]*len(y))

datossig = pd.DataFrame({'x': x,'y': y ,'sig': uy},index=np.arange(n)+1)
display(datossig)

a,b,siga,sigb,r = ajustelinealponderado(x,y,uy)

display(Latex('$a$=%3.2f , $\sigma_{a}$=%3.2f' % (a,siga) ))
display(Latex('$b$=%3.2f , $\sigma_{b}$=%3.2f' % (b,sigb) ))


outfile=open("datos1.txt", 'w')
outfile.write(" a \t & s(a) \t & b \t & s(b) \t & r \\\ \n")
outfile.write("%f \t & %2f \t & %f \t & %2f \t & %f"%(a,siga,b,sigb,r))
outfile.close()

#___________________________________________________________________________________________________#

Y= a + b*x


plt.figure(figsize=(7,6))
plt.plot(x,y, '.')
plt.plot(x,Y)
plt.grid()
plt.show()

plt.figure(figsize=(7,6))

plt.grid(True)
plt.errorbar(x, y, fmt= '.', yerr=uy, label=("f = 65,7 hz"))
plt.xlabel("t (ms)")
plt.ylabel("l (cm)")
plt.xlim(0, max(x)*1.1)
plt.ylim(-5, max(y)*1.1)
x[0]=0
Y= a + b*x
plt.plot(x,Y)

plt.savefig("regresiónlineal.png")

#-------------------Parte 2 --------------------Parte 2-------------------Parte 2------------------#

#Ahora vamos a calcular las frecuencias de onda:

#semiabierto

T = np.array([2.7*2*10**-3,1.2*0.002,2.8*0.0005,2*0.0005,1.6*0.0005])
sT  =np.array([0.4,0.4,0.1,0.1,0.1])

n=len(T)

v = b*10
sigv = sigb*10

def function(T,sT,v,sigv,n):
    sigT = np.zeros([5])
    
    for i in range(len(T)):
        sigT[i]=sT[i]*10**-3

    f = np.zeros([5])

    for i in range(len(T)):
        f[i] = T[i]**(-1)

    sigf = np.zeros([n])

    for i in range(n):
        sigf[i]=(sigT[i]/T[i]**2)
    
    lamb=np.zeros([n])
    siglamb=np.zeros([n])

    for i in range(n):
        lamb[i] = v/f[i]

    for i in range(n):
        siglamb[i] = np.sqrt((sigv/f[i])**2+(v*sigf[i]/f[i]**2)**2)
        
    return(f,sigf,lamb,siglamb)

f,sigf,lamb,siglamb = function(T,sT, v, sigv,n)

outfile=open("datos2.txt", 'w')
outfile.write("\\hline \n")
outfile.write(" modo \t & $f_i \ (Hz)$ \t &  $s(f_i) \ (Hz) $ \t & $\lambda_i \(m)$ \t & $s(\lambda_i) \ (m) $  \\\ \\hline \n")
for i in range(n):
     outfile.write("%d \t & %f \t & %f \t & %f \t & %f  \\\ \n "%(i+1,f[i],sigf[i],lamb[i],siglamb[i]))
outfile.close()

#abierto

T1=np.array([4.6*10**-3,2.5*10**-3, 1.6*10**-3, 1.2*10**-3,0.95*10**-3])
sT1=np.array([0.2,0.1,0.1,0.1,0.1])

f1,sigf1,lamb1,siglamb1 = function(T1,sT1, v, sigv,n)

outfile=open("datos3.txt", 'w')
outfile.write("\\hline \n")
outfile.write(" modo \t & $f_i \ (Hz)$ \t &  $s(f_i) \ (Hz) $ \t & $\lambda_i \(m)$ \t & $s(\lambda_i) \ (m) $  \\\ \\hline \n")
for i in range(n):
     outfile.write("%d \t & %f \t & %f \t & %f \t & %f  \\\ \n "%(i+1,f1[i],sigf1[i],lamb1[i],siglamb1[i]))
outfile.close()

#funciones

def funcion(lambn,L,n):
    fun=np.zeros([5])
    for i in range(n):
        fun[i]=(L*4/lambn[i])
    return(fun)

#semiabierto


fun=funcion(lamb,0.6,n)


outfile=open("datos4.txt", 'w')
outfile.write("\hline  \n $f_1$ \t & $f_2$ \t & $f_3$ \t & $f_4$ \t & $f_5$ \\\ \hline \n")
outfile.write("%f \t & %f \t & %f \t & %f \t & %f \t  t \n \\hline "%(fun[0],fun[1],fun[2],fun[3],fun[4]))
outfile.close()

#abierto

fun1=funcion(lamb1,0.8,n)


outfile=open("datos5.txt", 'w')
outfile.write("\hline  \n $f_1$ \t & $f_2$ \t & $f_3$ \t & $f_4$ \t & $f_5$ \\\ \hline \n")
outfile.write("%f \t & %f \t & %f \t & %f \t & %f \t  \n \\hline "%(fun1[0],fun1[1],fun1[2],fun1[3],fun1[4]))
outfile.close()
"""

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#+++++++++++++++++++++++++++++++++++++++ GIROSCOPIO +++++++++++++++++++++++++++++++++++++++++++++++++#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#





# -- OBTENCION DIRECTA Y TEORICA DEL I3 ---------------------------------------------------

g=9.81
sigr=0.002
sigm1=0.001
sigh=0.2/100
sigt0=0.25

m1=0.060
r=0.025

h=np.array([94.8,63.5,50.2,32.7,108.0])/100
t0=[7.69, 5.86,5.26,3.88,7.94]

t = np.zeros([5])

for i in range(len(t0)):
    t[i]=t0[i]**2

sigt = np.zeros([5])

for i in range(len(t0)):
    sigt[i]=np.sqrt(2*t[i]*sigt0**2)


a,b,siga,sigb,r=ajustelinealponderado(h, t, sigt)


plt.grid(True)
plt.errorbar(h, t, fmt= '.', yerr=sigt, color="k")
plt.xlabel("h (m)")
plt.ylabel("$t^2$ $(s^2)$")
plt.xlim(0, max(h)*1.1)
plt.ylim(-10, max(t)*1.5)
x=np.linspace(0,max(h),100)
Y= a + b*x
plt.plot(x,Y,"r")

plt.savefig("plot-aceleracion.png")

print(b)
I3T = (b*0.060*9.81*(0.025)**2)/2

sigI3T = np.sqrt((0.025**2*m1*g*sigb/2)**2+(2*0.025*b*m1*g*0.002/2)**2+(0.025**2*b*g*sigm1/2)**2)

print(I3T)
print(sigI3T)



outfile=open("datos3.txt", 'w')
outfile.write("\\begin{table}[h!] \\centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c||c|c|} \n")
outfile.write("\hline $ a $ \t & s(a) \t & b \t & s(b) \t & r \t & $I_3$ \t & s($I_3$) \t \\\ \hline ")
outfile.write("\n %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f & %.5f \t & %.5f\\\ "%(a,siga,b,sigb,r,I3T, sigI3T))
outfile.write("\hline \n \\end{tabular} \n")
outfile.write("\\caption{resultados de la regresión lineal y el momento de incercia $I_3$} \n")
outfile.write("\\end{table} \n")
outfile.close()




# -- OBTENCIÓN DIRECTA Y TEORICA DE I1 -------------------------------------------------------------------------


#Calculo de la constante k:


m2=99/1000
sigm2=1/100
sigT10=0.25
T10=4.37

T = T10/10
sigT = sigT10/10

k = (2*np.pi)**2*m2/T**2

sigk = np.sqrt((sigm2/T**2)**2+((m2/T**3)*(sigT)*2)**2)*(2*np.pi)**2
# Calculo de I1
D = 28.5/100
sigD=0.1/100
sigT10=0.25
T10=np.array([8.81,8.49,8.58,8.27,9.04])
TM=T10/10
sigTM=sigT10/10




sigTM = sigTM/np.sqrt(len(TM))
TM = sum(TM)/len(TM)

print("Tm %.5f sig %.5f"%(TM, sigTM))

I1T = (2*k)*(TM**2)*(D**2)/(2*np.pi)**2

print(I1T)

sigI1T =np.sqrt(((2)*(TM**2)*(D**2)/(2*np.pi)**2*(sigk))**2+((2*k)*(TM*2)*(D**2)/(2*np.pi)**2*(sigTM))**2+((2*k)*(TM**2)*(D*2)/(2*np.pi)**2*(sigD))**2)

print(sigI1T)


outfile=open("datos4.txt", 'w')
outfile.write("\\begin{table}[h!] \\centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c||c|c|} \n")
outfile.write("\hline $ k $ \t & s(k) \t & D \t & s(D) \t & w \t & s(w) \t & $I_3$ \t & s($I_3$) \t \\\ \hline ")
outfile.write("\n %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f & %.5f \t & %.5f \t & %.5f \\\ "%(k, sigk,D,sigD,TM,sigTM,I1T, sigI1T))
outfile.write("\hline \n \\end{tabular} \n")
outfile.write("\\caption{resultados de la regresión lineal y el momento de incercia $I_3$} \n")
outfile.write("\\end{table} \n")
outfile.close()


# -- OBTENCIÓN DE I3 A PARTIR DEL MOVIMIENTO DE PRECESION --------------------------------------------------------------------------------------------------

sigw=np.pi*0.4
sigT=0.25       
d=(50-28.5)/100
sigd=np.sqrt(0.002)
#Serie1:

w1=np.pi*np.array([12.3,11.1,19.1,14.6,10.9])
T1=np.array([14.8,13.1,21.4,17.22,12.99])

#Serie2:

w2=np.pi*np.array([20.3,13.5,25.1,19.8,16.8])
T2=np.array([24.08,15.65,28.43,23.51,19.00])
    
#Serie3: 

w3=np.pi*np.array([26.2,22.2,17.9,13.9,13.4])
T3=np.array([30.48,24.83,20.89,17.41,17.05])


n=len(T1)
f1=np.zeros([5])
f2=np.zeros([5])
f3=np.zeros([5])

for i in range(n):
    f1[i]=T1[i]**(-1)
    f2[i]=T2[i]**(-1)
    f3[i]=T3[i]**(-1)

sigf1=np.zeros([5])
sigf2=np.zeros([5])
sigf3=np.zeros([5])

for i in range(n):
    sigf1[i]=sigT/T1[i]
    sigf2[i]=sigT/T2[i]
    sigf3[i]=sigT/T3[i]
    

v1=1/w1
v2=1/w2
v3=1/w3

sigv1=np.zeros([5])
sigv2=np.zeros([5])
sigv3=np.zeros([5])

for i in range(n):
    sigv1[i]=sigw*v1[i]
    sigv2[i]=sigw*v2[i]
    sigv3[i]=sigw*v3[i]


a1,b1,siga1,sigb1,r1=ajustelineal(w1, T1)
a2,b2,siga2,sigb2,r2=ajustelineal(w2, T2)
a3,b3,siga3,sigb3,r3=ajustelineal(w3, T3)

plt.figure()

plt.grid(True)
plt.errorbar(w1, T1, fmt= '.', yerr=sigT, label=("serie 1"), color="red")
plt.xlabel("$w_1$ $(s^{-1})$)")
plt.ylabel("$T_p$ (s)")
plt.xlim(0, max(w1)*1.1)
plt.ylim(0, max(T1)*1.5)
x=np.linspace(0,max(w3),100)
Y= a1 + b1*x
plt.plot(x,Y,"r")

plt.errorbar(w2, T2, fmt= '.', yerr=sigT, label=("serie 2"), color="blue")
plt.xlabel("$w_1$ $(s^{-1})$)")
plt.ylabel("$\Omega_p$ (s)")
plt.xlim(0, max(w2)*1.1)
plt.ylim(0, max(T2)*1.5)
x=np.linspace(0,max(w3),100)
Y= a2 + b2*x
plt.plot(x,Y,"b")

plt.errorbar(w3, T3, fmt= '.', yerr=sigT, label=("serie 3"), color="green")
plt.xlabel("w $(s^{-1})$")
plt.ylabel("$T_p$ (s)")
plt.xlim(0, max(w3)*1.1)
plt.ylim(0, max(T3)*1.5)
x=np.linspace(0,max(w3),100)
Y= a3 + b3*x
plt.legend()
plt.plot(x,Y,"g")

plt.savefig("regresionlineal-precesion.png")


plt.figure()


plt.grid(True)
plt.grid(True)
plt.errorbar(w1, T1, fmt= '.', yerr=sigT, label=("serie 1"), color="red")
plt.xlabel("$w_1$ $(s^{-1})$)")
plt.ylabel("$T_p$ (s)")
plt.xlim(0, max(w1)*1.1)
plt.ylim(0, max(T1)*1.5)
x=np.linspace(0,max(w1),100)
Y= a1 + b1*x

plt.legend()
plt.plot(x,Y,"r")


plt.savefig("regresionlineal-precesion1.png")

plt.figure()


plt.grid(True)
plt.errorbar(w2, T2, fmt= '.', yerr=sigT, label=("serie 2"), color="blue")
plt.xlabel("$w_1$ $(s^{-1})$)")
plt.ylabel("$\Omega_p$ (s)")
plt.xlim(0, max(w2)*1.1)
plt.ylim(0, max(T2)*1.5)
x=np.linspace(0,max(w2),100)
Y= a2 + b2*x
plt.legend()
plt.plot(x,Y,"b")


plt.savefig("regresionlineal-precesion2.png")


plt.figure()


plt.grid(True)
plt.errorbar(w3, T3, fmt= '.', yerr=sigT, label=("serie 3"), color="green")
plt.xlabel("w $(rad \cdot s^{-1})$")
plt.ylabel("$T_p$ (s)")
plt.xlim(0, max(w3)*1.1)
plt.ylim(0, max(T3)*1.5)
x=np.linspace(0,max(w3),100)
Y= a3 + b3*x
plt.legend()
plt.plot(x,Y,"g")


plt.savefig("regresionlineal-precesion3.png")



outfile=open("datos1.txt", 'w')
outfile.write("\\begin{table} \\centering \n")
outfile.write("\\begin{tabular}{} \n")
outfile.write("\hline $ w_1 $ \t & $ \Omega_p $ \t & $s(\Omega_p)$ \t & $w_2$ \t & $\Omega_p$ \t & $s(\Omega_p)$ \t & $w_3$ \t & $\Omega_p$ \t &  $s(\Omega_p)$ \\\ \hline \n")
for i in range(n):
    outfile.write("%.1f \t & %.5f \t & %.5f \t & %.1f \t & %.5f \t & %.5f \t & %.1f \t & %.5f \t & %.5f  \\\ \n"%(w1[i],f1[i],sigf1[i],w2[i],f2[i],sigf2[i],w3[i], f3[i], sigf3[i]))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{} \n")
outfile.write("\\end{table} \n")
outfile.close()

I31 = b1 * m1 * 9.81 * d / (2*np.pi)
sigI31 = np.sqrt(( m1 * 9.81 * d * sigb1 / (2*np.pi))**2 + (sigm1 * b1  * 9.81 * d / (2*np.pi))**2+( b1 * m1 * 9.81 * sigd / (2*np.pi))**2)
I32 = b2 * m1 * 9.81 * d / (2*np.pi)
sigI32 = np.sqrt(( m1 * 9.81 * d * sigb2 / (2*np.pi))**2 + (sigm1 * b2  * 9.81 * d / (2*np.pi))**2+( b2 * m1 * 9.81 * sigd / (2*np.pi))**2)
I33 = b3 * m1 * 9.81 * d / (2*np.pi)
sigI33 = np.sqrt(( m1 * 9.81 * d * sigb3 / (2*np.pi))**2 + (sigm1 * b3  * 9.81 * d / (2*np.pi))**2+( b3 * m1 * 9.81 * sigd / (2*np.pi))**2)

todos = [I31,I32,I33]
incertidumbres = [sigI31,sigI32,sigI33]

I3M, sigI3M  = mediaponderada(todos, incertidumbres)

print("I3M =", I3M, sigI3M)

outfile=open("datos5.txt", 'w')
outfile.write("\\begin{table}[h!] \\centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c||c|c|} \n")
outfile.write("\hline  \t & $ a $ \t & s(a) \t & b \t & s(b) \t & r \t & $I_3$ \t & s($I_3$) \t \\\ \n \hline ")
outfile.write("serie 1 \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \\\ \n"%(a1,siga1,b1,sigb1,r1,I31, sigI31))
outfile.write("serie 2 \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \\\ \n"%(a2,siga2,b2,sigb2,r2,I32, sigI32))
outfile.write("serie 3 \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \\\ \n"%(a3,siga3,b3,sigb3,r3,I33, sigI33))
outfile.write("media \t & - \t & - \t & - \t & - \t & - \t & %.5f \t & %.5f \\\ \n"%(I3M, sigI3M))
outfile.write("\hline \n \\end{tabular} \n")
outfile.write("\\caption{resultados de la regresión lineal y el momento de incercia $I_3$} \n")
outfile.write("\\end{table} \n")
outfile.close()


print(b1, b2, b3)

# -- CALCULO DE I1 A PARTIR DE NUTACION E I3 -----------------------------------------------------------------------------------------

#Serie1:
    
sigw=0.4    
sigt=0.25
nut=4
    
t1=np.array([2.86,3.22,3.08,5.10])/4
w11=[21.8,17.5,13.9,9.45]
w12=[21.3,17.2,13.2,9.20] 

wm1=np.zeros([4])   

for i in range(len(t1)):
    wm1[i] = np.pi*(w11[i]+w12[i])/2
    

sigwm1=np.zeros([4])

for i in range(len(t1)):
    sigwm1[i] = np.pi*sigw
    

#Serie2:

t2=np.array([2.73,2.24,2.56,3.43,3.51])/4
w21=[17.1,21.0,19.0,16.3,14.0]
w22=[16.9, 20.8,18.8,16.1,13.8]

wm2=np.zeros([5])   

for i in range(len(t2)):
    wm2[i] = np.pi*(w21[i]+w22[i])/2
    

sigwm2=np.zeros([5])

for i in range(len(t2)):
    sigwm2[i] =  np.pi*sigw
    
    
#Serie3:
    
t3=np.array([2.61,3.51,3.72,2.34,5.73])/4
w31=[20.3,15.2,14.0,23.7,10.9]
w32=[20.0,14.9,13.7,23.4,10.6]


wm3=np.zeros([5])   

for i in range(len(t3)):
    wm3[i] = np.pi*(w31[i]+w32[i])/2
    

sigwm3=np.zeros([5])

for i in range(len(t3)):
    sigwm3[i] =  np.pi*sigw
    


n=len(T1)
f1=np.zeros([4])
f2=np.zeros([5])
f3=np.zeros([5])

for i in range(n):
    f3[i]=t3[i]**(-1)
    f2[i]=t2[i]**(-1)

for i in range(4):
    f1[i]=t1[i]**(-1)
    
f1 = f1*2*np.pi
f2 = f2*2*np.pi
f3 = f3*2*np.pi

sigf1=np.zeros([4])
sigf2=np.zeros([5])
sigf3=np.zeros([5])

for i in range(n):
    if i==4:
        sigf2[i]=sigt/t2[i]*2*np.pi
        sigf3[i]=sigt/t3[i]*2*np.pi
    else:
        sigf1[i]=sigt/t1[i]*2*np.pi
        sigf2[i]=sigt/t2[i]*2*np.pi
        sigf3[i]=sigt/t3[i]*2*np.pi


"""
outfile=open("datos2.txt", 'w')
outfile.write("\\begin{table}[h!] \\centering \n")
outfile.write("\\begin{tabular}{} \n")
outfile.write("\hline $ w_1 $ \t & $ \Omega_n $ \t & $s(\Omega_n)$ \t & $w_2$ \t & $\Omega_n$ \t & $s(\Omega_n)$ \t & $w_3$ \t & $\Omega_n$ \t &  $s(\Omega_n)$ \\\ \hline ")
for i in range(n):
    outfile.write("\n %.1f \t & %.5f \t & %.5f \t & %.1f \t & %.5f \t & %.5f \t & %.1f \t & %.5f \t & %.5f  \\\ "%(wm1[i],f1[i],sigf1[i],wm2[i],f2[i],sigf2[i],wm3[i], f3[i], sigf3[i]))
outfile.write("\hline \n \\end{tabular} \n")
outfile.write("\\caption{} \n")
outfile.write("\\end{table} \n")
outfile.close()
"""

a1,b1,siga1,sigb1,r1=ajustelinealponderado(wm1, f1, sigf1)
a2,b2,siga2,sigb2,r2=ajustelinealponderado(wm2, f2, sigf2)
a3,b3,siga3,sigb3,r3=ajustelinealponderado(wm3, f3, sigf3)


plt.figure()
plt.grid(True)
plt.errorbar(wm1, f1, fmt= '.', yerr=sigf1, label=("serie 1"), color="red")
plt.xlabel("w $(s^{-1})$")
plt.ylabel("$\Omega_n$ ($s^{-1}$)")
plt.xlim(0, max(wm1)*1.1)
plt.ylim(-2.5, max(f1)*1.5)
x=np.linspace(0,max(wm1),100)
Y= a1 + b1*x
plt.legend()
plt.plot(x,Y,"r")


plt.savefig("regresionlineal-nutacion1.png")

plt.figure()

plt.grid(True)
plt.errorbar(wm2, f2, fmt= '.', yerr=sigf2, label=("serie 2"), color="blue")
plt.xlabel("w $(s^{-1})$")
plt.ylabel("$\Omega_n$ ($s^{-1}$)")
plt.xlim(0, max(wm2)*1.1)
plt.ylim(-2.5, max(f2)*1.5)
x=np.linspace(0,max(wm2),100)
Y= a2 + b2*x
plt.legend()
plt.plot(x,Y,"b")


plt.savefig("regresionlineal-nutacion2.png")


plt.figure()
plt.grid(True)
plt.errorbar(wm3, f3, fmt= '.', yerr=sigf3, label=("serie 3"), color="green")
plt.xlabel("w $(s^{-1})$")
plt.ylabel("$\Omega_n$ ($s^{-1}$)")
plt.xlim(0, max(wm3)*1.1)
plt.ylim(-2.5, max(f3)*1.5)
x=np.linspace(0,max(wm3),100)
Y= a3 + b3*x
plt.legend()
plt.plot(x,Y,"g")


plt.savefig("regresionlineal-nutacion3.png")



plt.figure()

plt.grid(True)
plt.errorbar(wm1, f1, fmt= '.', yerr=sigf1, label=("serie 1"), color="red")
plt.xlabel("w $(s^{-1})$")
plt.ylabel("$\Omega_n$ ($s^{-1}$)")
plt.xlim(0, max(wm1)*1.1)
plt.ylim(-0.5, max(f1)*1.5)
x=np.linspace(0,max(wm1),100)
Y= a1 + b1*x
plt.plot(x,Y,"r")

plt.errorbar(wm2, f2, fmt= '.', yerr=sigf2, label=("serie 2"), color="blue")
plt.xlabel("w $(s^{-1})$")
plt.ylabel("$\Omega_n$ ($s^{-1}$)")
plt.xlim(0, max(wm2)*1.1)
plt.ylim(-0.5, max(f2)*1.5)
x=np.linspace(0,max(wm2),100)
Y= a2 + b2*x
plt.plot(x,Y,"b")

plt.errorbar(wm3, f3, fmt= '.', yerr=sigf3, label=("serie 3"), color="green")
plt.xlabel("w $(rad \cdot s^{-1})$")
plt.ylabel("$\Omega_n$ ($rad \cdot s^{-1}$)")
plt.xlim(0, max(wm3)*1.1)
plt.ylim(-2.5, max(f3)*1.5)
x=np.linspace(0,max(wm3),100)
Y= a3 + b3*x
plt.legend(loc="upper left")
plt.plot(x,Y,"g")



plt.savefig("regresionlineal-nutacion.png")


b=np.array([b1,b2,b3])
sigb=np.array([sigb1,sigb2,sigb3])
a=np.array([a1,a2,a3])
siga=np.array([siga1,siga2,siga3])

bm, sigbm = mediaponderada(b, sigb)
am, sigam = mediaponderada(a, siga)

outfile=open("datos6.txt", 'w')
outfile.write("\\begin{table}[h!] \\centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c||c|c|} \n")
outfile.write("\hline  \t & $ a $ \t & s(a) \t & b \t & s(b) \t & r \t       \\\ \n \hline ")
outfile.write("serie 1 \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t  \\\ \n"%(a1,siga1,b1,sigb1,r1))
outfile.write("serie 2 \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t  \\\ \n"%(a2,siga2,b2,sigb2,r2))
outfile.write("serie 3 \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t  \\\ \n"%(a3,siga3,b3,sigb3,r3))
outfile.write("media   \t & %.5f \t & %.5f \t & %.5f \t & %.5f \t & - \t  \\\ \n"%(am,sigam,bm,sigbm))
outfile.write("\hline \n \\end{tabular} \n")
outfile.write("\\caption{resultados de la regresión lineal y el momento de incercia $I_3$} \n")
outfile.write("\\end{table} \n")
outfile.close()



I1=I3T/bm
sigI1 = np.sqrt((sigI3T/bm)**2+(I3T*sigbm/bm**2)**2)

print("I_1 \ = \ %.5f \\pm %.5f"%(I1,sigI1))

I1=I3M/bm
sigI1 = np.sqrt((sigI3M/bm)**2+(I3M*sigbm/bm**2)**2)

print("I_1 \ = \ %.5f \\pm %.5f"%(I1,sigI1))