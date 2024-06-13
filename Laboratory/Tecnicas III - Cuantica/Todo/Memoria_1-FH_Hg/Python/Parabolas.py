# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:14:50 2024

@author: danie
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
import scipy.constants as cte
import scipy.optimize as so
from Funciones import parabola, sacavalores, aproximaparabolas, energia, Emedia, longitud_onda, concatenarbueno
from FH_analysis import dfs, colors, labels
from tabulate import tabulate
l=0.95

extremosn=np.array([[[13.837-l,13.837+l],[18.518-l,18.518+l],[23.253-l,23.253+l],[28.167-l,28.167+l],[33.147-l,33.147+l]],
[[13.863-l,13.863+l],[18.561-l,18.561+l],[23.297-l,23.297+l],[28.225-l,28.225+l],[33.204-l,33.204+l]],
[[13.925-l,13.925+l],[18.618-l,18.618+l],[23.352-l,23.352+l],[28.246-l,28.246+l],[33.223-l,33.223+l]],
[[14.051-l,14.051+l],[18.754-l,18.754+l],[23.486-l,23.486+l],[28.407-l,28.407+l],[33.391-l,33.391+l]],
[[14.326-l,14.326+l],[18.870-l,18.870+l],[23.710-l,23.710+l],[28.710-l,28.710+l],[33.573-l,33.573+l]],
[[14.482-l,14.482+l],[19.144-l,19.144+l],[23.909-l,23.909+l],[28.806-l,28.806+l],[33.779-l,33.779+l]]])
j=0

extremosp=np.array([[[12.015-l,12.015+l],[16.383-l,16.383+l],[21.053-l,21.053+l],[25.881-l,25.881+l],[30.81-l,30.81+l]],
[[12.038-l,12.038+l],[16.415-l,16.415+l],[21.084-l,21.084+l],[25.933-l,25.933+l],[30.854-l,30.854+l]],        
[[12.043-l,12.043+l],[16.447-l,16.447+l],[21.111-l,21.111+l],[25.933-l,25.933+l],[30.864-l,30.864+l]],                    
[[12.176-l,12.176+l],[16.567-l,16.567+l],[21.224-l,21.224+l],[26.045-l,26.045+l],[30.967-l,30.967+l]],        
[[12.239-l,12.239+l],[16.683-l,16.683+l],[21.339-l,21.339+l],[26.171-l,26.171+l],[31.094-l,31.094+l]],    
[[12.434-l,12.434+l],[16.838-l,16.838+l],[21.473-l,21.473+l],[26.313-l,26.313+l],[31.229-l,31.229+l]]])


an=np.zeros([6,5])
san=np.zeros([6,5])
ap=np.zeros([6,5])
sap=np.zeros([6,5])

for df, color, label in zip(dfs, colors, labels):
    plt.figure(figsize=[10,8])
    plt.plot(df["U1/V"], df["IA/nA"], ".r", label=label,markersize="0.5" )
    x=df["U1/V"]
    y=df["IA/nA"]
    maxy=max(y.to_numpy())
    for i in range(len(extremosn[j])):
        up,vp=sacavalores(extremosp[j,i],x.to_numpy(),y.to_numpy())
        un,vn=sacavalores(extremosn[j,i], x.to_numpy(), y.to_numpy())
        ap0,sap0=aproximaparabolas(parabola, up, vp,maxy)
        an0,san0=aproximaparabolas(parabola, un, vn,maxy)
        ap[j,i]=ap0
        sap[j,i]=sap0
        an[j,i]=an0
        san[j,i]=san0  
    plt.ylim(-0.18,maxy+0.15*np.sqrt(maxy*1.4))    
    plt.savefig("Parabola-%d.pdf"%(j+1),bbox_inches="tight")
    j+=1

V2=[0.4,0.5,0.6,1,1.5,2]
outfile=open("Extremos-Parabolas.txt", 'w')
for i in range(len(an)):
    tabla=concatenarbueno(([1,2,3,4,5],ap[i],sap[i],an[i],san[i]))
    hola=tabulate(tabla,tablefmt="latex",floatfmt=(".0f",".2f",".2f",".2f",".2f"))
    outfile.write("\\begin{table}[h!] \t \centering \n") 
    outfile.write(hola)
    outfile.write("\\caption{Extremos para $U_2=%.2f$ V usando la aproximación-parabólica.} \n"%(V2[i]))
    outfile.write("\\label{Tab:parabolas-%d} \n"%(i+1))
    outfile.write("\\end{table} \n \n \n")
outfile.close()
