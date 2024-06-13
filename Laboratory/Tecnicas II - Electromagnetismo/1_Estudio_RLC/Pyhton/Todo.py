2# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 10:39:44 2023

@author: danie
"""


import sys
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as lng
import pylab as py
from math import e
import scipy.optimize as so
from mpl_toolkits.mplot3d import Axes3D
import modulo_1_aproximador as md


def media(x):
    y = sum(x)/len(x)
    return y


def incertidumbre(x):
    x = np.array(x)
    u = np.sqrt(sum((x-media(x))**2)/(len(x)-1))
    return u


R = 328  + 17.8
sR = np.sqrt((2+328*0.005)**2+(0.02+17.8*0.005)**2)

L = 33*10**(-3)
sL = 0.05*L

C = 22*10**(-9)
sC = 0.05*C


w0 =  1/np.sqrt(L*C)
sw0 = (np.sqrt((sC/np.sqrt(L*C**3))**2+((sL/np.sqrt(C*L**3))**2)))/2

Q = w0*L/R
sQ = np.sqrt((sw0*L/R)**2+(sL*w0/R)**2+(sR*L*w0/(R**2))**2)

B = w0/(2*np.pi*Q)
sB = np.sqrt((sQ*w0/(2*np.pi*(Q**2)))**2+(sw0/(2*np.pi*Q))**2)


# ---------------------------------------

f = np.array([100000, 51350, 17900, 12970, 9810, 8900, 8170, 7620, 7270, 6990, 6830, 6660, 6500, 6410, 6280, 6200, 6100,
              6000, 5930, 5820, 5760, 5690, 5620, 5520, 5450, 5340, 5260, 5160, 5030, 4910, 4700, 4510, 4250, 3770,
              3200, 2600, 1800, 500.5, 200, 101.1])

Vin = np.array([0.15876, 0.3340, 1.04, 1.62, 2.5, 3.06, 3.84, 4.56, 5.12, 5.68, 6.08, 6.56, 6.88, 7.20, 7.52, 7.60, 7.84, 8.00,
                8.00, 8.00, 8.00, 8.00, 7.84, 7.60, 7.36, 7.12, 6.80, 6.56, 6.08, 5.52, 4.88, 4.32, 3.68, 2.74, 2.04, 1.50,
                0.9360, 0.2480, 0.1090, 0.0645])

Vr = np.array([10.80, 10.16, 10.08, 10.08, 9.92, 9.84, 9.76, 9.68, 9.60, 9.52, 9.36, 9.28, 9.20, 9.12, 9.12, 9.04, 8.96, 8.88,
               8.88, 8.88, 8.96, 8.96, 9.04, 9.12, 9.2, 9.2, 9.24, 9.28, 9.44, 9.60, 9.68, 9.76, 9.76, 9.92, 10.00, 10.06, 10.08,
               10.08, 10.16, 10.48])

Theta = [[86, 92], [88.4, 91.71], [84.0, 85.7], [79.4, 80.5], [73.5, 75.3], [70.08, 71.34], [65.0, 65.9], [59.3, 60.8],
         [54.6, 55.14], [49.1, 50.10], [44.81, 45.41], [
             39.9, 40.41], [34.12, 35.4], [29.3, 32.0, ], [24.6, 25.6],
         [18.5, 22.0], [14.3, 16.8], [9.3, 10.7], [5.3, 6.2],
         [0, 0], [353.1, 355.6], [349.5, 350.5], [346.1, 344.6], [
    340.6, 338.7], [334.6, 335.6], [329.3, 330.4],
    [325.0, 324.9], [319.3, 322.0], [314.4, 315.9], [
        310.7, 309.7], [305.8, 305.4], [299.2, 300.4], [296, 295.6],
    [289, 290], [284.9, 285.7], [280.9, 280.0], [274.6, 276], [267.2, 268.5], [262.0, 272.0], [257, 263]]

N = np.array([0.001, 0.005, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025,
              0.025, 0.025, 0.025, 0.025, 0.05, 0.05, 0.05, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025,
              0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.025, 0.05, 0.05, 0.1, 0.250, 1, 2.5])

sf = np.zeros(40)
sVin = np.zeros(40)
sVr = np.zeros(40)
phi = np.zeros(40)
sphi = np.zeros(40)

for i in range(len(f)):
    sf[i] = 10

    sVr[i] = 0.1+0.05*Vr[i]

    if(Vin[i] < 1):
        sVin = 0.05*Vin+0.002

    if(Vin[i] > 10):
        sVin[i] = 0.1+0.05*Vin[i]

    if(media(Theta[i]) > 100):
        phi[i] = media(Theta[i])-360
        sphi[i] = np.sqrt((incertidumbre(Theta[i]))**2 +
                          (f[i]*2*np.pi*15*N[i]/1000000)**2)

    if(media(Theta[i]) < 100):
        phi[i] = media(Theta[i])
        sphi[i] = np.sqrt((incertidumbre(Theta[i]))**2 +
                          (f[i]*2*np.pi*15*N[i]/1000000)**2)


# ---------------------------------------

Z = np.zeros(40)
sZ = np.zeros(40)
w = 2*np.pi*f
sw = 2*np.pi*sf

for i in range(len(Z)):
    Z[i] = (R*Vr[i]/Vin[i])
    sZ[i] = np.sqrt((sR*Vr[i]/Vin[i])**2+(sVr[i]*R/Vin[i])
                    ** 2+(sVin[i]*R*Vr[i]/(Vin[i]**2))**2)


# ------------------------------------

def fun(x, a, b, c):
    y = a/(x**2)+b+c*x**2
    return y


Z2 = Z**2
sZ2 = 2*Z*sZ

par1 = [2088500354683100, -2901477.1175187863,0.001112242408117156]
sol1 = so.curve_fit(fun, w[1:38], Z2[1:38], sigma=sZ2[1:38],absolute_sigma=True, p0=(par1))

a, b, c = sol1[0]
sa,sb,sc = np.diag(sol1[1])
print("a", a,sa)
sa,sb,sc = 0.033*a,0.0178*b,0.0289*c
print(a,sa, "\n", b, sb, "\n",c, sc)


t=np.linspace(min(w[1:38]),max(w[1:38]),1000) 

plt.figure(dpi=300,figsize=(16,8))
plt.grid(True,linestyle="--")
plt.plot(t,fun(t,a,b,c),color="red")
plt.errorbar(w[1:38], Z2[1:38], yerr=sZ2[1:38], fmt=".",capsize=2.0,ecolor="blue",color="blue")
plt.xlabel("w  (rad/s)")
plt.ylabel("$|Z|^2 \ (\Omega^2)$")
plt.xscale("log")
plt.savefig("plot1.png")


C1=np.sqrt(1/a)
L1 = np.sqrt(c)
R1=np.sqrt(b+2*L1/C1)

sC1 = sa*(1/(2*np.sqrt(a**3)))
sL1 = sc*(1/(2*np.sqrt(c)))
sR1 = np.sqrt(sb**2+(sL1*2/C1)**2+(2*sC*L1/(C1**2)))/(2*R1)

print(" C %e \n L %f \n R1 %f"%(C1,L1,R1))
print(" C %e \n L %f \n R1 %f"%(C,L,R))


# ---------------------------------------

z = 1/Z
sz = sZ/(Z**2)


t=np.linspace(min(w[2:37]),max(w[2:37]),1000) 
p = 1/np.sqrt(fun(t,a,b,c))

plt.figure(dpi=300,figsize=(12,5))
plt.grid(True,linestyle="--")
plt.plot(t,p,"red")
plt.errorbar(w[2:37], z[2:37], yerr=sz[2:37], fmt=".",capsize=2.0,ecolor="cornflowerblue",color="blue")
plt.plot(t,p,"red")
plt.plot(w[2:37], z[2:37],"b.")
plt.xscale("log")
plt.xlabel("w  (rad/s)")
plt.ylabel("$|Z|^{-1} \ (\Omega^{-1})$")
plt.savefig("plot2.png")

# ----------------------------------------


tanphi = np.tan(2*np.pi*phi/(360))
stanphi = 2*np.pi*sphi*(1+tanphi**2)/360


def fun2(x, a, b):
    y = a/x + b*x
    return y

for j in range(len(tanphi)):
    print("%.3f"%(stanphi[j]/tanphi[j]))

par2 = [L/R, 1/(R*C)]
sol2 = so.curve_fit(fun2, w[2:38], tanphi[2:38],sigma=stanphi[2:38], p0=(par2))

a2, b2 = sol2[0]
sa2,sb2 = np.diag(sol2[1])
sa2=0.17*a2
sb2=0.14*b2


t=np.linspace(min(w[2:37])*0.9,max(w[2:37]),1000) 


plt.figure(dpi=300,figsize=(16,8))
plt.grid(True,linestyle="--")
plt.plot(t,fun2(t,a2,b2),color="red")
plt.errorbar(w[2:37], tanphi[2:37],yerr=stanphi[2:37], fmt=".",capsize=2.0,ecolor="blue",color="blue")
plt.xlabel("w  (rad/s)")
plt.ylabel("$\\tan (\phi) $")
plt.xscale("log")
plt.savefig("plot3.png")

# ----------------------------------


plt.figure(dpi=300,figsize=(16,8))

t=np.linspace(min(f),max(f),5000)

p=np.arctan(2*np.pi*t*a2+b2/(2*np.pi*t))*360/(2*np.pi)
plt.grid(True,linestyle="--")
plt.plot(t,p,"red")
plt.errorbar(f[1:39],phi[1:39],yerr=sphi[1:39],fmt=".",color="blue")
plt.ylabel("$\phi (^o)$")
plt.xlabel("f (Hz)")
plt.xscale("log")
plt.savefig("plot4.png")

# ------------------------------------------------

t = np.linspace(min(f), max(f), 1000)
p = 1/np.sqrt(fun((2*np.pi)*t, a , b, c))
plt.figure(dpi=300, figsize=(12, 5))
plt.grid(True, linestyle="--")
plt.plot(t, p, "red")
plt.errorbar(f, z, fmt=".", capsize=0.5, ecolor="cornflowerblue", color="blue")
plt.plot(t, p, "red")
plt.plot(f, z, "b.")
plt.xscale("log")
plt.xlabel("f  (Hz)")
plt.ylabel("$|Z|^{-1} \ (\Omega^{-1})$")
plt.savefig("plot5.png")

# ----------------------------------------------(



outfile=open("Regresion1.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$a_0 \ (F^{-2}) $  & $s(a_0) \ (F^{-2})$ & $ a_1 \ (\Omega^2)$ & $s(a_1) \ (\Omega^2)$ & $a_2 \ (H^2)  $ &  $s(a_2) \ (H^2)$ \\\ \\hline \n")
outfile.write("$%.2f \cdot 10^{14}$  & $%.2f \cdot 10^{14}$ & $ %.2f \cdot 10^5$ & $%.2f \cdot 10^5 $& $%.2f \cdot 10^{-4} $ & $%.2f \cdot 10^{-4}$ \\\ \n"%(a/(10**14),sa/(10**14),b/(10**5),sb/(10**5),c*10**4,sc*10**4))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{valores del ajuste \\ref{Ec:ajuste1}} \n")
outfile.write("\\label{Tab:regresion1} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()


 
outfile=open("Valores1.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$C \ (nF) $  & $s(C) \ (nF)$ & $ L \ (mH)$ & $s(L) \ (mH)$ & $R_T \ (\Omega)  $ &  $s(R_T) \ (\Omega)$ \\\ \\hline \n")
outfile.write("$%.2f $  & $%.2f $ & $ %.2f$ & $%.2f  $& $%d  $ & $%d $ \\\ \n"%(C1*10**9,sC1*10**9,L1*10**3,sL1*10**3,R1,sR1))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{parámetros intrínsecos del circuito \n")
outfile.write("\\label{Tab:valores1} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()



w01 = 1/np.sqrt(L1*C1)
Q1 = w01*L1/R1    
B1 = w01/(2*np.pi*Q1)    

sw01 = w01*(np.sqrt((sL1/L1)**2+(sC1/C1)**2))
sQ1  = np.sqrt((sw01*L1/R1)**2+(sL1*w01/R1)**2+(sR1*w01*L1/(R1**2))**2)
sB1 = (np.sqrt((w01*sQ1/(Q1**2))**2+(sw01/Q1)**2))/(2*np.pi)
f01=w01/(2*np.pi*1000)
sf01=sw01/(2*np.pi*1000)


outfile=open("Valores2.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$Q \  $  & $s(Q) \ $ & $ B \ (k \Hz)$ & $s(B) \ (k \Hz)$ & $w_0 \ (\mathrm{rad}/s)  $ &  $s(w_0) \ (\mathrm{rad}/s)$  & $f_0 \ (k$Hz) & $s(f_0) \ (k$Hz) \\\ \\hline \n")
outfile.write("$%.2f $  & $%.2f $ & $ %.2f $ & $%.2f$ & $%d  $ & $%d $ & %.2f & %.2f \\\ \n"%(Q1,sQ1,B1/10**3,sB1/10**3,w01,sw01,f01,sf01))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{parámetros intrínsecos del circuito} \n")
outfile.write("\\label{Tab:valores2} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()



outfile=open("Regresion2.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$b_0 \ (\Omega^{-1} F^{-1}) $  & $s(b_0) \ (\Omega^{-1} F^{-1})$ & $ b_1 \ (H/\Omega)$ & $s(b_1) \ (H/\Omega)$    \\\ \\hline \n")
outfile.write("$%.1f \cdot 10^{4}$  & $%.1f \cdot 10^{4}$ & $ %.1f \cdot 10^{-5} $ & $%.1f \cdot 10^{-5} $ \\\ \n"%(a2/10**4,sa2/10**4,b2*10**5,sb2*10**5))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{valores del ajuste \\ref{Ec:ajuste2}} \n")
outfile.write("\\label{Tab:regresion2} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()

w02=np.sqrt(-a2/b2)
Q2=w02*b2

sw02 = np.sqrt((sa2*np.sqrt(1/(-a2*b2))/2)**2+(sb2*np.sqrt(-a2/b2**3)/2)**2)
sQ2 = np.sqrt((sw02*b2)**2+(sb2*w02)**2)

f02=w02/(np.pi*2*1000)
sf02=sw02/(np.pi*2*1000)

B2 = w02/(2*np.pi*Q2)    
sB2 = (np.sqrt((w02*sQ2/(Q2**2))**2+(sw02/Q2)**2))/(2*np.pi)


outfile=open("Valores3.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$Q \  $  & $s(Q) \ $ & $ B \ (k \Hz)$ & $s(B) \ (k \Hz)$ & $w_0 \ (\mathrm{rad}/s)  $ &  $s(w_0) \ (\mathrm{rad}/s)$  & $f_0 \ (k$Hz) & $s(f_0) \ (k$Hz) \\\ \\hline \n")
outfile.write("$%.2f $  & $%.2f $ & $ %.2f $ & $%.2f$ & $%d  $ & $%d $ & %.2f & %.2f \\\ \n"%(Q2,sQ2,B2/10**3,sB2/10**3,w02,sw02,f02,sf02))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{parámetros intrínsecos del circuito} \n")
outfile.write("\\label{Tab:valores3} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()


outfile=open("Datos1.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$f  \ (\Hz) $  & $s(f) \ (\Hz)$ & $ w \ (\\mathrm{rad}/s)$ & $s(w) \ (\\mathrm{rad}/s)$ & $V_1 \ (V)  $ &  $s(V_1) \ (V)$ & $V_2 \ (V)$ & $ s(V_2) \ (V)$ \\\ \\hline \n")
for i in range(len(f)):
    if(sVin[i]<0.010):
        outfile.write("%d  & %d &  %d & %d & %.4f & %.4f & %.2f & %.2f \\\ \n"%(f[i],sf[i],w[i],63,Vin[i],md.aproximaciondecimales(sVin[i]),Vr[i],md.aproximaciondecimales(sVr[i])))
    if(sVin[i]<0.10 and sVin[i]>0.010):
        outfile.write("%d  & %d &  %d & %d & %.3f & %.3f & %.2f & %.2f \\\ \n"%(f[i],sf[i],w[i],63,Vin[i],md.aproximaciondecimales(sVin[i]),Vr[i],md.aproximaciondecimales(sVr[i])))
    if(sVin[i]>0.0999):
        outfile.write("%d  & %d &  %d & %d & %.2f & %.2f & %.2f & %.2f \\\ \n"%(f[i],sf[i],w[i],63,Vin[i],md.aproximaciondecimales(sVin[i]),Vr[i],md.aproximaciondecimales(sVr[i])))

outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{datos de la práctica} \n")
outfile.write("\\label{Tab:datos1} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()


outfile=open("Datos2.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$f  \ (\Hz) $  & $s(f) \ (\Hz)$ & $ \\phi \ (^o)$ & $s(\phi) \ (^o)$ & $Z \ (k \Omega)  $ &  $s(Z) \ (k \Omega)$ \\\ \\hline \n")

for i in range(len(f)):
    if(sphi[i]>0.099):
        if (sZ[i]/1000<0.1):
            outfile.write("%d  & %d &  %.2f & %.2f & %.3f & %.3f \\\ \n"%(f[i],sf[i],phi[i],sphi[i],Z[i]/1000,sZ[i]/1000))
        if (sZ[i]/1000>0.099 and sZ[i]/1000<1):
            outfile.write("%d  & %d &  %.2f & %.2f & %.2f & %.2f \\\ \n"%(f[i],sf[i],phi[i],sphi[i],Z[i]/1000,sZ[i]/1000))
        if sZ[i]/1000>1:
            outfile.write("%d  & %d &  %.2f & %.2f & %.1f & %.1f \\\ \n"%(f[i],sf[i],phi[i],sphi[i],Z[i]/1000,sZ[i]/1000))
            
    if(sphi[i]<0.10):
        if sZ[i]/1000<0.1:
            outfile.write("%d  & %d &  %.2f & %.2f & %.3f & %.3f \\\ \n"%(f[i],sf[i],phi[i],sphi[i],Z[i]/1000,sZ[i]/1000))
        if (sZ[i]/1000>0.099 and sZ[i]/1000<1):
            outfile.write("%d  & %d &  %.2f & %.2f & %.2f & %.2f \\\ \n"%(f[i],sf[i],phi[i],sphi[i],Z[i]/1000,sZ[i]/1000))
        if sZ[i]/1000>1:
            outfile.write("%d  & %d &  %.2f & %.2f & %.1f & %.1f \\\ \n"%(f[i],sf[i],phi[i],sphi[i],Z[i]/1000,sZ[i]/1000))
   
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{datos de la práctica} \n")
outfile.write("\\label{Tab:datos2} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()



outfile=open("Conclusion1color.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{c|c|c|c|c|c|c|} \n")
outfile.write("\n")
outfile.write("  & \cellcolor{color1} $ R \  (\Omega) $  &  \cellcolor{color1}  $s(R) \ (\Omega) $  &  \cellcolor{color1} $ C \ (nF)  $ & \cellcolor{color1}  $s(C) \ (nF)$  & \cellcolor{color1} $L \ (mH)$ & \cellcolor{color1} $s(L) \ (mH)$ \\\ \\hline \n")
outfile.write(" \cellcolor{color1} Parte 1 & \cellcolor{color2} $ %d $  &  \cellcolor{color2} $%d $  &  \cellcolor{color2} $%.2f  $ &  \cellcolor{color2} $ %.2f $ &   \cellcolor{color2}%.2f &  \cellcolor{color2} %.2f  \\\ \\hline  \n"%(R,sR,C*10**9,sC*10**9,L*10**3,sL*10**3))
outfile.write(" \cellcolor{color1} Parte 2.1 &  \cellcolor{color2} $ %d $  &  \cellcolor{color2} $%d $  &  \cellcolor{color2} $ %.2f  $ &  \cellcolor{color2} $ %.2f $ &  \cellcolor{color2}  %.2f &  \cellcolor{color2} %.2f  \\\ \\hline  \n"%(R1,sR1,C1*10**9,sC1*10**9,L1*10**3,sL1*10**3))
outfile.write(" \cellcolor{color1} Parte 2.2 2&  \cellcolor{color2} - & \cellcolor{color2} - & \cellcolor{color2} - &  \cellcolor{color2} - & \cellcolor{color2} - & \cellcolor{color2} - \\\ \\hline  \n")
outfile.write(" \cellcolor{color1} Experimentales &  \cellcolor{color2} - & \cellcolor{color2} - & \cellcolor{color2} - &  \cellcolor{color2} - & \cellcolor{color2} - & \cellcolor{color2} - \\\ \n")
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{parámetros intrínsecos del circuito} \n")
outfile.write("\\label{Tab:conclusion1} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()




outfile=open("Conclusion1.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("  &  $ R \  (\Omega) $  &    $s(R) \ (\Omega) $  &   $ C \ (nF)  $ &   $s(C) \ (nF)$   $L \ (mH)$ &  $s(L) \ (mH)$ \\\ \\hline \n")
outfile.write("  Teóricos & $ %d $  & $%d $  & $%.2f  $ & $ %.2f $ & %.2f & %.2f  \\\ \\hline  \n"%(R,sR,C*10**9,sC*10**9,L*10**3,sL*10**3))
outfile.write("  Regresion 1 & $ %d $  & $%d $  & $ %.2f  $ & $ %.2f $ & %.2f & %.2f  \\\ \\hline  \n"%(R1,sR1,C1*10**9,sC1*10**9,L1*10**3,sL1*10**3))
outfile.write("  Regresion 2 & - & - & - & - & - & -  \\\ \\hline  \n")
outfile.write("  Experimentales  & - & - & - & - & - & -  \\\ \n")
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{parámetros intrínsecos del circuito} \n")
outfile.write("\\label{Tab:conclusion1} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()



def interpolacionlineal(x1,sx1,x2,sx2,y1,sy1,y2,sy2,p):
    a = y1 
    z = p - x1
    b = (y2-y1)/(x2-x1)
    
    sa = sy1
    sb = np.sqrt( (1/(x2-x1)) * sy2**2 +  (1/(x2-x1)) * sy1**2 + ((y2-y1)/(x2-x1)**2)**2 * sx2**2 + ((y2-y1)/(x2-x1)**2)**2 * sx1**2)
    
    valor = a + b * z
    svalor = np.sqrt(sa**2 + sb**2 * z**2)
    return valor, svalor

valor1,svalor1=interpolacionlineal(40.16,0.36,45.11,0.42,6660,10,6830,10,45)
valor2,svalor2=interpolacionlineal(44.85,1.06,49.80,0.71,5039,10,4910,10,45)

B1T = valor1-5820
B2T = -valor2+ 5820

sB1T = np.sqrt(svalor1**2+10**2)
sB2T = np.sqrt(svalor2**2+10**2)

BT = (B1T+B2T)

sBT = np.sqrt(sB1T**2+sB2T**2)

QT = 5820/BT

sQT = np.sqrt((sBT*5820/BT**2)**2+(63/BT)**2)


outfile=open("Conclusion2color.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c|c|c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("  & \cellcolor{color3} $ Q \   $  & \cellcolor{color3}   $s(Q)  $  & \cellcolor{color3}  $ B \ (\Hz)  $ & \cellcolor{color3}  $s(B) \ (\Hz)$  & \cellcolor{color3} $ w_0 \ (\\mathrm{rad}/s)$ &  \cellcolor{color3} $s(w_0) \ (\\mathrm{rad}/s)$ \\\ \\hline \n")
outfile.write("  \cellcolor{color3} Parte 1 &  \cellcolor{color4} $ %.2f $  & \cellcolor{color4} $%.2f $  & \cellcolor{color4} $%d  $  & \cellcolor{color4} $ %d $ &  \cellcolor{color4} %d & \cellcolor{color4} %d  \\\ \\hline \n"%(Q,sQ,B,sB,w0,sw0))
outfile.write(" \cellcolor{color3} Parte 2.1 & \cellcolor{color4} $ %.2f $  & \cellcolor{color4} $%.2f $  & \cellcolor{color4} $%d  $ & \cellcolor{color4}$ %d $ & \cellcolor{color4} %d &  \cellcolor{color4} %d  \\\ \\hline \n"%(Q1,sQ1,B1,sB1,w01,sw01))
outfile.write(" \cellcolor{color3} Parte 2.2 & \cellcolor{color4} $ %.2f $  & \cellcolor{color4} $%.2f $  & \cellcolor{color4} $%d  $ & \cellcolor{color4}$ %d $ & \cellcolor{color4} %d &\cellcolor{color4} %d  \\\ \\hline  \n"%(Q2,sQ2,B2,sB2,w02,sw02))
outfile.write(" \cellcolor{color3} Experimentales & \cellcolor{color4} $ %.3f $  & \cellcolor{color4} $%.3f $  & \cellcolor{color4} $ %d  $ & \cellcolor{color4} $ %d $ & \cellcolor{color4} %d & \cellcolor{color4} %d  \\\  \n"%(QT,sQT,BT,sBT,36568,63))
outfile.write("\\hline\n\\end{tabular} \n")
outfile.write("\\caption{parámetros intrínsecos del circuito} \n")
outfile.write("\\label{Tab:conclusion2} \n")
outfile.write("\\end{table} \n \n \n")
outfile.close()

