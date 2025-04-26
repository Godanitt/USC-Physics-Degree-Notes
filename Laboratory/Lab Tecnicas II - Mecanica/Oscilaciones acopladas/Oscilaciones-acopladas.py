# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:50:32 2022

@author: PC
"""

import numpy as np
from numpy.linalg import *
from matplotlib import *
from matplotlib import pyplot as plt
from IPython.display import display, Latex
import pandas as pd

# -- --- --- -- -- --- -- -- - -- - - - - - -- -- - -- - -


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

def incertidumbretipoA(u,medu):
    siga=np.ones([len(u)])
    for i in range(len(u)):
        siga[i] = np.sqrt(((np.dot(u[i],u[i])/len(u[i]))-np.dot(medu[i],medu[i]))/(len(u)-1))
    return siga

def estatico(m,sm,x,sx,x0,sx0):
    k = (9.81*m)/(x-x0)
    sk = np.sqrt(((9.81*sm/(x-x0))**2)+((m*9.81*sx/(x-x0)**2)**2)+((m*9.81*sx0/(x-x0)**2)**2))
    return k,sk

def dinamico(T,sT,m,sm):    
    T = np.array(T,dtype=object)/10
    sT = sT/10
    for i in range(len(T)):
        Tf = media(T)
        sigTfb = sT/np.sqrt(len(T))
        sigTf = np.sqrt(sigTfb**2)
    k = m*(2*np.pi/Tf)**2
    sk = np.sqrt((((1/Tf**3)*4*m*sigTf*np.pi**2)**2)+((1/Tf**2)*sm*4*np.pi**2)**2)
    return k,sk
    
def frecuencias(k1,k2,k3,m1,m2,):
    f1= np.sqrt(((k1+k3)*m2+(k2+k3)*m1+np.sqrt((((k1+k3)*m2-(k2+k3)*m1)**2)+4*m1*m2*k3**2))/((2*m1*m2)))/(2*np.pi)
    f2= np.sqrt(((k1+k3)*m2+(k2+k3)*m1-np.sqrt((((k1+k3)*m2-(k2+k3)*m1)**2)+4*m1*m2*k3**2))/((2*m1*m2)))/(2*np.pi)
    return f1, f2

def amplitudes(k1,k2,k3,m1,m2):
    a1=  -((k2+k3)*m1-(k1+k3)*m2+np.sqrt((((k1+k3)*m2-(k2+k3)*m1)**2)+4*m1*m2*k3**2))/(2*k3*m2)
    a2=  -((k2+k3)*m1-(k1+k3)*m2-np.sqrt((((k1+k3)*m2-(k2+k3)*m1)**2)+4*m1*m2*k3**2))/(2*k3*m2)
    return a1,a2

# -- CALCULO DE CONSTANTES PARA MUELLE 1 -----

m = np.array([17,27,37,47,57])*0.001
sm = 0.001*np.sqrt(2)

x0 = 0.476
sx0 = 0.002

x = np.array([522,555,590,620,650])*0.001
sx = 0.005

T = np.array([[4.95,5.07,5.09,5.12,4.37,4.60,4.76,4.70],[5.64,5.45,5.38,6.10,6.13,6.53,6.25,6.16],[6.19,6.72,6.56,6.70,6.83,6.9,7.14,7.15,7.15],[7.71,7.76,7.87,7.77,7.82,7.78],[8.01,8.09,8.09,8.08,8.65,8.76,8.76,8.75]],dtype=object)
sT=0.25

Tm = np.ones([len(T)])
sTm = np.ones([len(T)])

for i in range(len(T)):
    Tm[i] = (media(T[i])/(10*2*np.pi))**2
    sTm[i]= (sT/(len(T)*np.sqrt(len(T))))*2*Tm[i]

a1,b1,siga1,sigb1,r1 = ajustelinealponderado(m, Tm, sTm)   

plt.figure()
plt.grid(True)
xx = np.linspace(0,max(m),100)
y = a1+b1*xx
plt.plot(xx,y,"c")
plt.errorbar(m,Tm,yerr=sTm,color="blue",fmt=".")
plt.xlabel("m (kg)")
plt.ylabel("$T^2/4\pi^2$  ($s^2$)")
plt.savefig("plot1.png")

kd1 = 1/b1
skd1 = sigb1/((b1)**2)

dx = np.array([])
sdx = np.array([])
for i in range(len(x)):
    dx = np.append(dx, x[i]-x0)
    sdx = np.append(sdx, np.sqrt(sx**2+sx0**2))
    
    
F = m*9.81


a1,b1,siga1,sigb1,r1 = ajustelinealponderado(F, dx, sdx)


plt.figure()
plt.grid(True)
xx = np.linspace(0,max(F),100)
y = a1+b1*xx
plt.plot(xx,y,"c")
plt.errorbar(F,dx,yerr=sdx,color="blue",fmt=".")
plt.xlabel("F (N)")
plt.ylabel("$\Delta x$  (m)")
plt.savefig("plot2.png")
ke1 = 1/b1
ske1 = sigb1/((b1)**2)



k1,sk1 = mediaponderada([ke1,kd1], [ske1,skd1])


"""
ke = np.ones([len(m)]) 
kd = np.ones([len(m)])
sigke = np.ones([len(m)])
sigkd = np.ones([len(m)])

K=np.zeros(len(ke)+len(kd))
sK = np.zeros(len(ke)+len(kd)
for i in range(len(m)):
    ke[i],sigke[i]=estatico(m[i], sm, x[i], sx, x0, sx0)
    kd[i],sigkd[i]=dinamico(np.array(T[i],dtype=object),sT,m[i],sm)
    K[i]=ke[i]
    K[i+len(kd)]=kd[i]
    sK[i]=sigke[i]
    sK[i+len(kd)]=sigkd[i]

k1,sk1 = mediaponderada(K,sK)
"""

k1,sk1 = mediaponderada([ke1,kd1], [ske1,skd1])

# -- CALCULO DE CONSTANTES PARA MUELLE 2 -----


m = np.array([17,27,37,47,57])*0.001
sm = 0.001*np.sqrt(2)

x0 = 0.478
sx0 = 0.002

x = np.array([538,580,625,672,716])*0.001
sx = 0.005

T = np.array([[5.02,5.09,4.90,5.02],[6.60,6.63,6.63,6.58],[7.59,7.52,7.52,7.64],[8.59,8.63,8.50,8.46],[9.46,9.26,9.51,9.38]],dtype=object)
sT=0.25


Tm = np.ones([len(T)])
sTm = np.ones([len(T)])

for i in range(len(T)):
    Tm[i] = (media(T[i])/(10*2*np.pi))**2
    sTm[i]= (sT/(len(T)*np.sqrt(len(T))))*2*Tm[i]

a1,b1,siga1,sigb1,r1 = ajustelinealponderado(m, Tm, sTm)   

plt.figure()
plt.grid(True)
xx = np.linspace(0,max(m),100)
y = a1+b1*xx
plt.plot(xx,y,"r")
plt.errorbar(m,Tm,yerr=sTm,color="brown",fmt=".")
plt.xlabel("m (kg)")
plt.ylabel("$T^2/4\pi^2$  ($s^2$)")
plt.savefig("plot3.png")

kd2 = 1/b1
skd2 = sigb1/((b1)**2)

dx = np.array([])
sdx = np.array([])
for i in range(len(x)):
    dx = np.append(dx, x[i]-x0)
    sdx = np.append(sdx, np.sqrt(sx**2+sx0**2))
    
    
F = m*9.81


a1,b1,siga1,sigb1,r1 = ajustelinealponderado(F, dx, sdx)


plt.figure()
plt.grid(True)
xx = np.linspace(0,max(F),100)
y = a1+b1*xx
plt.plot(xx,y,"r")
plt.errorbar(F,dx,yerr=sdx,color="brown",fmt=".")
plt.xlabel("F (N)")
plt.ylabel("$\Delta x$  (m)")
plt.savefig("plot4.png")
ke2 = 1/b1
ske2 = sigb1/((b1)**2)



k2,sk2 = mediaponderada([ke2,kd2], [ske2,skd2])

"""
ke = np.ones([len(m)]) 
kd = np.ones([len(m)])
sigke = np.ones([len(m)])
sigkd = np.ones([len(m)])

K=np.zeros(len(ke)+len(kd))
sK = np.zeros(len(ke)+len(kd))
for i in range(len(m)):
    ke[i],sigke[i]=estatico(m[i], sm, x[i], sx, x0, sx0)
    kd[i],sigkd[i]=dinamico(np.array(T[i],dtype=object),sT,m[i],sm)
    K[i]=ke[i]
    K[i+len(kd)]=kd[i]
    sK[i]=sigke[i]
    sK[i+len(kd)]=sigkd[i]

k2,sk2 = mediaponderada(K,sK)
"""


# -- CALCULO DE FRECUENCIAS DE RESONANCIA TEORICAS --- 

# Para m1 = m2 y k3 = k1

m=0.100
f11,f12 = frecuencias(k1, k1, k1, m, m)
a11,a12 = amplitudes(k1, k1, k1, m, m)

# Para m1 = m2 y k3 = k2

f21,f22= frecuencias(k1, k1, k2, m, m)
a21,a22= amplitudes(k1, k1, k2, m, m)

# Para m2 = 2m1 y k3 = k1

f31,f32= frecuencias(k1, k1, k1, m, m*2)
a31,a32= amplitudes(k1, k1, k1, m, m*2)

# -- Escribimos datos 
outfile = open("Datos-1.txt",'w')
outfile.write("\\begin{table}[h!] \cetering \n")
outfile.write("\\begin{tabular}{}  \n")
outfile.write("\\hline \n$k_1$ (N/m) \t & s($k_1$) (N/m) \t & $k_2$ (N/m) \t & s($k_2$) (n/m) \hline  \n")
outfile.write("%.3f \t & %.3f  \t & %.3f   \t & %.3f "%(k1,sk1,k2,sk2))
outfile.write("\hline \n\\end{tabular} \n")
outfile.write("\\caption{} \n")
outfile.write("\\label{} \n")
outfile.write("\\end{table}")
outfile.close()

sf11=3*np.sqrt(((sk1/(2*np.sqrt(k1/m)))**2)+((0.001/(2*np.sqrt(k1/m)*m**2))**2))
sf12=np.sqrt(((sk1/(2*np.sqrt(k1/m)))**2)+((0.001/(2*np.sqrt(k1/m)*m**2))**2))


sf21=np.sqrt(((sk1/(2*np.sqrt(k1/m)))**2)+((0.001/(2*np.sqrt(k1/m)*m**2))**2))
sf22=np.sqrt(((sk1/(2*np.sqrt(k1/m)))**2)+((0.001/(2*np.sqrt(k1/m)*m**2))**2)+((2*sk2/(2*np.sqrt(k2/m)))**2)+((2*0.001/(2*np.sqrt(k2/m)*m**2))**2))


sf31=(3+np.sqrt(2))*np.sqrt(((sk1/(2*np.sqrt(k1/m)))**2)+((0.001/(2*np.sqrt(k1/m)*m**2))**2))
sf32=(3-np.sqrt(2))*np.sqrt(((sk1/(2*np.sqrt(k1/m)))**2)+((0.001/(2*np.sqrt(k1/m)*m**2))**2))

outfile = open("Datos-2.txt",'w')
outfile.write("\\begin{table}[h!] \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|}  \n")
outfile.write("\\hline\n \t & Teorica \t & s(Teorica) \t & Experimental \t & s(Experimental) \hline \n")
outfile.write("1) \t & %.6f \t & %.6f  \t & %.3f   \t & %.3f \n"%(f12,sf12,0.909,0.001))
outfile.write("2) \t & %.6f \t & %.6f  \t & %.3f   \t & %.3f \n"%(f11,sf11,1.542,0.001))
outfile.write("3) \t &   -  \t &    -  \t & %.3f   \t & %.3f \n"%(0.7750,0.030))
outfile.write("4) \t &   -  \t &    -  \t & %.3f   \t & %.3f \n"%(1.285,0.083))
outfile.write("\hline \n\\end{tabular} \n")
outfile.write("\\caption{dos masas de 100g y el muelle central de constante $k_1$}\n")
outfile.write("\\label{} \n")
outfile.write("\\end{table}")
outfile.close()


outfile = open("Datos-3.txt",'w')
outfile.write("\\begin{table}[h!] \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|}  \n")
outfile.write("\\hline\n \t & Teorica \t & s(Teorica) \t & Experimental \t & s(Experimental) \\\ \hline \n")
outfile.write("1) \t & %.6f \t & %.6f  \t & %.3f   \t & %.3f \\\ \n "%(f22,sf22,0.935,0.001))
outfile.write("2) \t & %.6f \t & %.6f  \t & %.3f   \t & %.3f \\\ \n "%(f21,sf21,1.427,0.001))
outfile.write("3) \t &   -  \t &    -  \t & %.3f   \t & %.3f \\\ \n"%(0.8563,0.0073))
outfile.write("4) \t &   -  \t &    -  \t & %.3f   \t & %.3f \\\ \n\hline\n"%(1.138,0.013))
outfile.write("\hline \n\\end{tabular} \n")
outfile.write("\\caption{dos masas de 100g y el muelle central de constante $k_2$}\n")
outfile.write("\\label{} \n")
outfile.write("\\end{table}")
outfile.close()


outfile = open("Datos-4.txt",'w')
outfile.write("\\begin{table}[h!] \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|}  \n")
outfile.write("\\hline\n \t & Teorica \t & s(Teorica) \t & Experimental \t & s(Experimental) \hline \n")
outfile.write("1) \t & %.6f \t & %.6f  \t & %.3f   \t & %.3f \\\ \n"%(f32,sf32,0.772,0.001))
outfile.write("2) \t & %.6f \t & %.6f  \t & %.3f   \t & %.3f \\\ \n"%(f31,sf31,1.31,0.001))
outfile.write("\hline \n\\end{tabular} \n")
outfile.write("\\caption{dos masas de 100g y 200g y el muelle central de constante $k_1$}\n")
outfile.write("\\label{} \n")
outfile.write("\\end{table}")
outfile.close()


outfile = open("Datos-5.txt",'w')
outfile.write("\\begin{table}[h!] \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|}  \n")
outfile.write("\\hline\n \t & Teorica  \t & Experimental \t & s(Experimental) \\\ \hline \n")
outfile.write("1) \t & %.6f   \t & %.3f   \t & %.3f \\\ \n "%(a12,70/65,10*np.sqrt(((1/65)**2)+((70**2)/(65**4)))))
outfile.write("2) \t & %.6f   \t & %.3f   \t & %.3f \\\ \n "%(a11,-15/15,5*np.sqrt(((1/15**2)+1/(15**2)))))
outfile.write("\hline \n\\end{tabular} \n")
outfile.write("\\caption{amplitudes relativas para dos masas de 100g y el muelle central $k_2$}\n")
outfile.write("\\label{} \n")
outfile.write("\\end{table}")
outfile.close()


outfile = open("Datos-6.txt",'w')
outfile.write("\\begin{table}[h!] \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|}  \n")
outfile.write("\\hline\n \t & Teorica  \t & Experimental \t & s(Experimental) \\\ \hline \n")
outfile.write("1) \t & %.6f   \t & %.3f   \t & %.3f \\\ \n "%(a22,75/65,10*np.sqrt(((1/65**2)+75**2/(65**4)))))
outfile.write("2) \t & %.6f   \t & %.3f   \t & %.3f \\\ \n "%(a21,-20/25,5*np.sqrt(((1/25**2)+400/(25**4)))))
outfile.write("\hline \n\\end{tabular} \n")
outfile.write("\\caption{amplitudes relativas para dos masas de 100g y el muelle central $k_2$}\n")
outfile.write("\\label{} \n")
outfile.write("\\end{table}")
outfile.close()

"""

outfile = open("Datos-7.txt",'w')
outfile.write("\\begin{table}[h!] \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|}  \n")
outfile.write("\\hline\n \t & Teorica  \t & Experimental \t & s(Experimental) \\\ \hline \n")
outfile.write("1) \t & %.6f   \t & %.3f   \t & %.3f \\\ \n "%(a32,40/25,5*np.sqrt(((1/25**2)+(40**2)/(25**4)))))
outfile.write("2) \t & %.6f   \t & %.3f   \t & %.3f \\\ \n "%(a31,-25/35,10*np.sqrt(((1/35**2)+(25**2/(35**4)))))
outfile.write("\hline \n\\end{tabular} \n")
outfile.write("\\caption{amplitudes relativas para dos masas de 100g y 200g con el muelle $k_2$}\n")
outfile.write("\\label{} \n")
outfile.write("\\end{table}")
outfile.close()



"""




























