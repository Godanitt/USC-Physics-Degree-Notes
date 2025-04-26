# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 18:22:57 2023

@author: danie
"""


import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
from math import e
import scipy.optimize as so





def ajustelinealponderado(x,y,sig): # Aquí metemos los dos valores y la incertidumbre de y(sig)

    H=np.array([[sum(1./sig**2),sum(x/sig**2)],[sum(x/sig**2),sum(x**2/sig**2)]])
    Delta=lng.det(H)
    Z=np.array([sum(y/sig**2),sum((x*y)/sig**2)])
    
    ([a,b])=np.matmul(lng.inv(H),Z)
    
    siga=np.sqrt(sum(x**2/sig**2)/Delta)
    sigb=np.sqrt(sum(1./sig**2)/Delta)
    
    r = np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))
    
    return a,b,siga,sigb



def mediaponderada(u,sigu):
    w=np.zeros([len(sigu)])
    for i in range(len(sigu)):
        w[i]=1/sigu[i]**2
    k=sum(w)
    media=np.dot(u,w)/k
    s = 1/np.sqrt(k)
    
    return [media, s]



def mediaponderada2(u,sigu):
    w=np.zeros([len(sigu)])
    for i in range(len(sigu)):
        w[i]=1/(sigu[i]**2)
    k=sum(w)
    media=np.dot(u,w)/k
    
    s1 = np.sqrt((sum((u-media)**2))/(len(u)*(len(u)-1)))
    s2 = 1/np.sqrt(k)
    
    s =np.sqrt(s1**2 + s2**2)
    
    return [media, s]


#______________________________________________________________________________
    
Datos1 = np.array([[0.049,100.7],[0.107,92.5],[0.155,86.2],[0.189,81.9],[0.237,75.9],
                   [0.285,70.1],[0.323,65.3],[0.354,61.4],[0.382,58.0],[0.406,55.1],
                   [0.447,50.0]])

V1=Datos1[:,0]
I1=Datos1[:,1]/1000

sV1 = np.array([0.001]*len(V1))

valores1 = ajustelinealponderado(I1, V1, sV1)


E21 = valores1[0]
sE21 = valores1[2]
r1 = valores1[1]
sr1 = valores1[3]

#------------------------------------------------------------------------------

Datos2=np.array([[0.089,140.5],[0.184,125.1],[0.258,118.1],[0.315,111.0],[0.362,104.9],
                 [0.418,98.4],[0.439,94.7],[0.487,89.2],[0.528,84.3],[0.581,77.8],
                 [0.630,71.5],[0.677,65.6]])


V2=Datos2[:,0]
I2=Datos2[:,1]/1000

sV2 = np.array([0.001]*len(V2))

valores2 = ajustelinealponderado(I2, V2, sV2)


E22 = valores2[0]
sE22 = valores2[2]
r2 = valores2[1]
sr2 = valores2[3]

# --------


E11=0.855   
E12 = 1.195

sE1 = 0.001 

# --------


E1,sE1 = mediaponderada([E11,E21],[sE1,sE21])
E2,sE2 = mediaponderada([E12,E22],[sE1,sE22])

ri = mediaponderada([r1,r2],[sr1,sr2])

#______________________________________________________________________________




V1 = 125
sV1 = 1

V2 =150 
sV2 = 1

T1 = np.array([[16.6,12.0,0],[17.1,12.0,120],[18.4,12.1,240],[19.5,12.0,360],
               [20.7,12.1,420],[21.6,12.2,480],[22.0,12.2,600],[22.7,12.0,660],
               [23.3,12.0,900],[23.6,12.3,960],[23.9,12.4,1020],[24.2,12.4,1080],
               [24.6,12.4,1140],[24.9,12.5,1200],[25.1,12.4,1260],[25.4,12.4,1320],
               [25.6,12.4,1380],[25.8,12.4,1440],[26.0,12.5,1500],[26.2,12.5,1560],
               [26.3,12.5,1620],[26.5,12.5,1680],[26.7,12.5,1740],[26.8,12.5,1800],
               [27.0,12.6,1860],[27.2,12.6,1920],[27.3,12.7,1980],[27.4,12.7,2040],
               [27.6,12.7,2100],[27.7,12.6,2160],[27.7,12.6,2220],[27.8,12.5,2280],
               [27.9,12.6,2340],[28.0,12.6,2400],[28.1,12.6,2460],[28.1,12.7,2520],
               [28.2,12.7,2580],[28.3,12.7,2640],[28.4,12.7,2700],[28.4,12.9,2760],
               [28.5,12.9,2820],[28.5,12.7,2880],[28.6,12.7,2940],[28.6,12.7,3000],
               [28.6,12.9,3060],[28.6,12.9,3120]])


T2 = np.array([[28.8,13.0,0],[29.1,13.1,1],[29.5,13.1,2],[29.9,13.2,3],[30.4,13.2,4],
               [30.8,13.3,5],[31.2,13.4,6],[31.5,13.4,7],[31.9,13.5,8],[32.1,13.5,9],
               [32.4,13.5,10],[32.7,13.5,11],[32.9,13.5,12],[33.2,13.6,13],[33.4,13.6,14],
               [33.6,13.6,15],[33.8,13.5,16],[34.0,13.5,17],[34.1,13.5,18],[34.2,13.5,19],
               [34.3,13.5,20],[34.4,13.6,21],[34.5,13.5,22],[34.6,13.5,23],[34.7,13.5,24],
               [34.8,13.5,25],[34.9,13.5,26],[34.9,13.5,27],[34.9,13.5,28],[35.0,13.5,29],
               [35.1,13.5,30],[35.2,13.5,31],[35.2,13.5,32],[35.3,13.5,33],[35.3,13.5,34],
               [35.4,13.5,35],[35.4,13.5,36],[35.5,13.5,37],[35.5,13.5,38],[35.6,13.6,39],
               [35.6,13.6,40],[35.7,13.7,41],[35.7,13.7,42],[35.8,13.7,43],[35.8,13.6,45],
               [35.8,13.5,46]])

T12 = T1[:,0]
t1  = T1[:,2]/60

T22 = T2[:,0]
t2  = T2[:,2]

sT=np.array(46*[0.1])




#Regresiones

def f(t,A,B,C):
    y = A + B*(np.exp(-(C*t)))
    return y

par1 = [29.5,13.3,0.05]
par2 = [37.0,24.0,0.05]
sol1 = so.curve_fit(f,t1,T12,p0=(par1))
sol2 = so.curve_fit(f,t2,T22,p0=(par2))

svalores1 = np.diag(sol1[1])
svalores2 = np.diag(sol2[1])



#______________________________________________________________________________

R = np.array([1023.6942059937179, 4.448932990758463])

valores2 = sol2[0]
valores1 = sol1[0]


T11 = np.array(T1[:,1])
T21 = np.array(T2[:,1])


u1 = [0.1]*len(T11)
u2 = [0.1]*len(T21)

T1 = mediaponderada2(T11,u1)
T2 = mediaponderada2(T21,u2)




# -- Calculo de Delta T

DT1 = valores1[0]-T1[0]
DT2 = valores2[0]-T2[0]

sDT1 = np.sqrt(svalores1[0]**2+T1[1]**2)
sDT2 = np.sqrt(svalores2[0]**2+T2[1]**2)

# -- Calculo de W


W1 = (V1**2)/R[0]
W2 = (V2**2)/R[0]


sW1 = np.sqrt((2*V1*sV1/R[0])**2+(R[1]*(V1/R[0])**2)**2)
sW2 = np.sqrt((2*V2*sV2/R[0])**2+(R[1]*(V2/R[0])**2)**2)



# -- Calculo de lambda


lambda1 = W1/DT1
lambda2 = W2/DT2

slambda1 =  np.sqrt((sW1/DT1)**2+(W1*sDT1/((DT1)**2))**2)
slambda2 =  np.sqrt((sW2/DT2)**2+(W2*sDT2/((DT2)**2))**2)

lambdaM,slambdaM = mediaponderada([lambda1,lambda2], [slambda1,slambda2])



# -- Calculo de Ca

Ca1 = 60*lambda1/valores1[2]
Ca2 = 60*lambda2/valores2[2]

sCa1 = 60*np.sqrt((slambda1/valores1[2])**2+(lambda1*svalores1[2]/((valores1[2])**2))**2)
sCa2 = 60*np.sqrt((slambda2/valores2[2])**2+(lambda2*svalores2[2]/((valores2[2])**2))**2)

# -- Calculo de S

S1 = E1/DT1
S2 = E2/DT2


sS1 =  np.sqrt((sE1/DT1)**2+(E1*sDT1/((DT1)**2))**2)
sS2 =  np.sqrt((sE2/DT2)**2+(E2*sDT2/((DT2)**2))**2)

# -- Tablas de datos ----------------------------------------------------------



outfile=open("tabla1.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\\Delta T_1  \ (C^o)$ & $s(\Delta T_1) \ (C^o)$  & $\Delta T_2  \ (C^o)$ & $s(\Delta T_2) \ (C^o) $ \\\ \hline  \n ")
outfile.write("%f &  %f &  %f & %f \\\ \hline \n"%(DT1, sDT1, DT2, sDT2))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores de las diferencias de temperaturas para $V_0 = 125 \ V$ ($\Delta T_1$) y $V_0 = 150 \ V$ ($\Delta T_2$)} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()



outfile=open("tabla2.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c||c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$ T_1^1  \ (C^o)$ & $s( T_1) \ (C^o)$  & $ T_1^2  \ (C^o)$ & $s( T_1) \ (C^o) $ \\\ \hline  \n ")
outfile.write("%f &  %f &  %f & %f \\\ \hline \n"%(T1[0], T1[1], T2[0], T2[1]))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores de la temperatura unión fría para $V_0 = 125 \ V$ ($ T_1^1$) y $V_0 = 150 \ V$ ($ T_1^2$)} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()


outfile=open("tabla3.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c||c|c|} \n")
outfile.write("\\hline \n")
outfile.write(" $W_{R_c}^1 \ (J)$ & $s(W_{R_c}^2) \ (J)$  & $W_{R_c}^2 \ (J)$  & $s(W_{R_c}^2) \ (J) $ & $W_{R_c} \ (J)$ & $s(W_{R_c}) \ (J)$ \\\ \hline \n")
outfile.write(" %f & %f & %f & %f & %f & %f \\\ \n\hline\n"%(W1,sW1,W2,sW2,mediaponderada([W1,W2],[sW1,sW2])[0],mediaponderada([W1,W2],[sW1,sW2])[1]))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores de $W_{R_c}$ para $V_0 = 125 \ V$ ($W_{R_c}^1$) y $V_0 = 150 \ V$ ($W_{R_c}^2$} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()



outfile=open("tabla4.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c||c|c|} \n")
outfile.write("\\hline \n")
outfile.write(" $\lambda_T^1 \ (W/C^o)$ & $s(\lambda_T^1 ) \ (W/C^o)$  & $\lambda_T^2 \ (W/C^o)$  & $s(\lambda_T^2) \ (W/C^o) $ & $\lambda_T \ (W/C^o)$ & $s(\lambda_T) \ (W/C^o)$ \\\ \hline \n")
outfile.write(" %f & %f & %f & %f & %f & %f \\\ \n\hline\n"%(lambda1,slambda1,lambda2,slambda2,mediaponderada([lambda1,lambda2],[slambda1,slambda2])[0],mediaponderada([lambda1,lambda2],[slambda1,slambda2])[1]))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores de $\lambda_T$ para $V_0 = 125 \ V$ ($\lambda_T^1$) y $V_0 = 150 \ V$ ($\lambda_T^2$)} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()



outfile=open("tabla5.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c||c|c|} \n")
outfile.write("\\hline \n")
outfile.write(" $C_a^1 \ (J/C^o)$ & $s(C_a^1 ) \ (J/C^o)$  & $C_a^2 \ (J/C^o)$  & $s(C_a^2) \ (J/C^o) $ & $C_a \ (J/C^o)$ & $s(C_a) \ (J/C^o)$ \\\ \hline \n")
outfile.write(" %f & %f & %f & %f & %f & %f \\\ \n\hline\n"%(Ca1,sCa1,Ca2,sCa2,mediaponderada([Ca1,Ca2],[sCa1,sCa2])[0],mediaponderada([Ca1,Ca2],[sCa1,sCa2])[1]))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores de $C_a$ para $V_0 = 125 \ V$ ($C_a^1$) y $V_0 = 150 \ V$ ($C_a^2$)} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()



outfile=open("tabla6.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c||c|c|} \n")
outfile.write("\\hline \n")
outfile.write(" $S^1 \ (V/C^o)$ & $s(S^1 ) \ (V/C^o)$  & $S^2 \ (V/C^o)$  & $s(S^2) \ (V/C^o) $ & $S \ (V/C^o)$ & $s(S) \ (V/C^o)$ \\\ \hline \n")
outfile.write(" %f & %f & %f & %f & %f & %f \\\ \n\hline\n"%(S1,sS1,S2,sS2,mediaponderada([S1,S2],[sS1,sS2])[0],mediaponderada([S1,S2],[sS1,sS2])[1]))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores de $S$ para $V_0 = 125 \ V$ ($S^1) y $V_0 = 150 \ V$ ($S^2$)} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()




outfile=open("tabla7.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\\varepsilon_1  \ (V)$ & $s(\\varepsilon^1) \ (V)$  & $\\varepsilon^2  \ (V)$ & $s(\\varepsilon^2) \ (V) $ \\\ \hline  \n ")
outfile.write("%f &  %f &  %f & %f \\\ \hline \n"%(E1, sE1, E2, sE2))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores de $\\varepsilon$ para $V_0 = 125 \ V$ ($\\varepsilon^1$) y $V_0 = 150 \ V$ ($\\\\varepsilon^2$)} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()



outfile=open("tabla8.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c| \n")
outfile.write("\\hline \n")
outfile.write("$\\varepsilon_1  \ (V)$ & $s(\\varepsilon^1) \ (V)$ \\\ \hline  \n ")
outfile.write("%f &  %f  \\\ \hline \n"%(mediaponderada([r1,r2],[sr1,sr2])[0], mediaponderada([r1,r2],[sr1,sr2])[1]))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores de $r_i$ definitivos tras hacer la media ponderada")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()


