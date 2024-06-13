# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 16:58:35 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as cte
from tabulate import tabulate
from Focales import f_1,sf_1,f2,sf2

f1=f_1
sf1=sf_1

def incertidumbre(x):
    sx=np.sqrt(sum((x-(np.average(x)))**2)/((len(x)-1)*len(x)))
    return sx


def incertidumbrepropagadan(s):
    for i in range(len(s)):
        b=sum(s**2)/len(s)
    a=np.sqrt(b)
    return a


def concatenarbueno(lista):
    a=np.zeros([len(lista[0]),len(lista)])
    for i in range(len(lista)):
        for j in range(len(lista[0])):
            a[j,i]=lista[i][j]
    return a

    
def combinada(sx,sy):
    sz=np.sqrt(sx**2+sy**2)
    return sz


# Uso de la lupa

d0=40 # cm
sd=0.1/np.sqrt(6)

cuadradosog=4 # Los cuadrados grandes, 8 de los pequeños
tamañoog=[258.3,253.1,259.2] # Tamaño original
tamañogm=np.average(tamañoog)
stamañoog=np.array(incertidumbre(tamañoog),incertidumbrepropagadan(np.array([sd]*3)))



def aumetoteorico(d0,d,f,sd,sf):
    bt=(1+(d0-d)/f)
    sbt=np.sqrt(2*(sd/f)**2+(sf*(d0-d)/f**2)**2)
    return bt,sbt
    

# Incertidumbre de la medida de los cuadrados es 0.1 por la medida

dt=np.array([])

# Primera medida

d=46.1-39.5 # cm, distancia lupa-camara (entre las bases)
tamañolupa1=[1033.0,1030.0,1024.0] # Tamaño original

cuadrados1=4
dt=np.append(dt,d)


# Segunda medida

d=46.1-36.5 # cm, distancia lupa-camara (entre las bases)
tamañolupa2=[1030.4,1022.4,1021.4] # Tamaño original
cuadrados2=4
dt=np.append(dt,d)

# Tercera medida

cuadrados3=2 # 2 grandes, 4 pques
d=46.1-33.1 # cm, distancia lupa-camara (entre las bases)
tamañolupa3=np.array([471.1,465.1,468.1]) # Tamaño original

dt=np.append(dt,d)


# Cuarta medida

cuadrados4=2 # 2 grandes, 4 p2ques
d=46.1-25 # cm, distancia lupa-camara (entre las bases)
tamañolupa4=np.array([379.0,382.0,378.0]) # Tamaño original

dt=np.append(dt,d)


#Quinta medida
cuadrados5=0.5 # 0.5 grandes, 1 p2ques
d=46.1-20.9 # cm, distancia lupa-camara (entre las bases)
tamañolupa5=np.array([94,92,93]) # Tamaño original
dt=np.append(dt,d)

cuadrados=np.array([cuadrados1,cuadrados2,cuadrados3,cuadrados4,cuadrados5])
tamañolupa=np.array([tamañolupa1,tamañolupa2,tamañolupa3,tamañolupa4,tamañolupa5])


# CALCULO
bt=np.array([])
sbt=np.array([])
for i in range(len(dt)):
    b1,sb1=aumetoteorico(d0, dt[i], f1, sd, sf1)
    bt=np.append(bt,b1)
    sbt=np.append(sbt,sb1)
    
bexp=np.zeros([len(tamañolupa),len(tamañolupa[0])])
sbexp=np.zeros([len(tamañolupa),len(tamañolupa[0])])
bexpm=np.zeros([len(tamañolupa)])
sbexpm=np.zeros([len(tamañolupa)])
for i in range(len(tamañolupa)):
    for j in range(len(tamañolupa[0])):
        bexp[i,j]=(tamañolupa[i,j])*(cuadradosog/cuadrados[i])/tamañogm
        sbexp[i,j]=np.sqrt((sd*(cuadradosog/cuadrados[i])/tamañogm)**2+(stamañoog*tamañolupa[i,j]*(cuadradosog/cuadrados[i])/tamañogm**2)**2)
    bexpm[i]=np.average(bexp[i])
    sbexpm[i]=combinada(incertidumbre(bexp[i]), incertidumbrepropagadan(sbexp[i]))



tabla=concatenarbueno((bt,sbt,bexpm,sbexpm))
header=["$  beta_t $", "$s(  beta_t)$","$ beta_{exp}$", "$s( beta_{exp})$"]
hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".3f", ".3f",".3f", ".3f"))
outfile=open("Lupa-Aumentos.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write(hola)
outfile.write("\\caption{Valores de los aumentos angulares experimentales y teóricos} \n")
outfile.write("\\label{tab:datos-parte-2.1.%d} \n"%(1))
outfile.write("\\end{table} \n \n \n")
outfile.close()


# -- Doble lupa es decir microsocopio --

"""
def di(f,do):
    di=(1/f-1/do)**(-1)
    return di

def bteo(l,lp,d0,d,f):
    bteo=(lp/l)*(1-(d0-d)/(fl1))
    return bteo

# Distancia 1
    #medida1 micro

cuadrados=(1/5)*0.5
tamañolupa=np.array([46,44])
d=46.1-40.1 #cm lupa1-camara
l=18.0-8.8 #lente2-objeto
lp=di(fl2,l) #cm lente2-imagen (calculado con la focal)

bexp11=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)
bt1=bteo(l,lp,d0,d,fl1)

    #medida2 micro
cuadrados=(1/5)*0.5
tamañolupa=np.array([46,47,42])

bexp12=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)

 #medida3 micro
cuadrados=(1/5)*0.5
tamañolupa=np.array([46,44,45])

bexp13=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)

# Distancia 2
    #medida1 micro

cuadrados=(1/5)*0.5
tamañolupa=np.array([61,60])
d=46.1-40.1 #cm lupa1-camara
l=15.3-7.3 #lente2-objeto
lp=di(fl2,l) #cm lente2-imagen (calculado con la focal)

bexp21=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)
bt2=bteo(l,lp,d0,d,fl1)

    #medida2 micro
cuadrados=(1/5)*0.5
tamañolupa=np.array([62,61])

bexp22=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)

 #medida3 micro
cuadrados=(1/5)*0.5
tamañolupa=np.array([60,60])

bexp23=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)


# Distancia 3
    #medida1 micro

cuadrados=(4/5)*0.5
tamañolupa=np.array([99.0,99.0,100.0])
d=46.1-40.1 #cm lupa1-camara
l= 21.1-9.8#lente2-objeto
lp=di(fl2,l) #cm lente2-imagen (calculado con la focal)

bexp31=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)
bt3=bteo(l,lp,d0,d,fl1)

    #medida2 micro
cuadrados=(4/5)*0.5
tamañolupa=np.array([100.0,100.0,99.0])

bexp32=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)

 #medida3 micro
cuadrados=(4/5)*0.5
tamañolupa=np.array([98.0,100.0,99.0])

bexp33=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)

# Distancia 4
    #medida1 micro

cuadrados=0.5#un medio cuadrado grande uno pequerrechiño
tamañolupa=np.array([63,61,61])
d=46.1-40.1 #cm lupa1-camara
l=24-7.1 #lente2-objeto
lp=di(fl2,l) #cm lente2-imagen (calculado con la focal)

bexp41=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)
bt4=bteo(l,lp,d0,d,fl1)

    #medida2 micro
cuadrados=0.5
tamañolupa=np.array([61,61,61])

bexp42=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)

 #medida3 micro
cuadrados=0.5
tamañolupa=np.array([62,62,61])

bexp43=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)

# Distancia 5
    #medida1 micro

cuadrados=1#un  cuadrado grande
tamañolupa=np.array([85,85,84])
d=46.1-40.1 #cm lupa1-camara
l=25-3.2 #lente2-objeto cuanto mayor sea menor es el error entre exp y teo
lp=di(fl2,l) #cm lente2-imagen (calculado con la focal)

bexp51=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)
bt5=bteo(l,lp,d0,d,fl1)

    #medida2 micro
cuadrados=1
tamañolupa=np.array([86,86,84])

bexp52=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)

 #medida3 micro
cuadrados=1
tamañolupa=np.array([87,86,85])

bexp53=bexp(tamañolupa*(cuadradosog/cuadrados),tamañoog)
"""