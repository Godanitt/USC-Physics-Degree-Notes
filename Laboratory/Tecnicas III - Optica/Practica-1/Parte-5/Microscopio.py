# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 10:38:46 2024

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


def aumetoteorico(d0,d,f,lp,l,sd,sf,sl,slp):
    bt=(lp/l)*(1+(d0-d)/f)
    sbt=np.sqrt(2*(lp/l)*(sd/f)**2+(sf*(lp/l)*(d0-d)/f**2)**2+(slp*bt/lp)**2+(sl*bt/l)**2)
    return bt,sbt

# Uso de la lupa

def di(f,do,sf,sdo):
    di=(f*do)/(do-f)
    sdi=np.sqrt((sf*do**2/(do-f)**2)**2+((sdo*f**2/(do-f)**2))**2)
    return di,sdi

d0=40 # cm
sd=0.1/np.sqrt(6)


dt=np.array([])
lt=np.array([])

cuadradosog=4 # Los cuadrados grandes, 8 de los pequeños
tamañoog=[258.3,253.1,259.2] # Tamaño original
tamañogm=np.average(tamañoog)
stamañoog=np.array(incertidumbre(tamañoog),incertidumbrepropagadan(np.array([sd]*3)))



cuadrados1=(1/5)*0.5
tamañolupa11=np.array([46,44])
d=46.1-40.1 #cm lupa1-camara
l=18.0-8.8 #lente2-objeto

dt=np.append(dt,d)
lt=np.append(lt,l)

    #medida2 micro
cuadrados=(1/5)*0.5
tamañolupa12=np.array([46.0,47.0,42.0])

 #medida3 micro
cuadrados=(1/5)*0.5
tamañolupa13=np.array([46,44,45])

tamañolupa1=np.array([46,44,46,47,42,46,44,45])

lupa1=np.average(tamañolupa1)
slupa1=combinada(incertidumbre(tamañolupa1),incertidumbrepropagadan(np.array([d/np.sqrt(12)]*len(tamañolupa1))))

# Distancia 2
    #medida1 micro

cuadrados2=(1/5)*0.5
tamañolupa21=np.array([61,60])
d=46.1-40.1 #cm lupa1-camara
l=15.3-7.3 #lente2-objeto


dt=np.append(dt,d)
lt=np.append(lt,l)

    #medida2 micro
cuadrados=(1/5)*0.5
tamañolupa22=np.array([62,61])

 #medida3 micro
cuadrados=(1/5)*0.5
tamañolupa23=np.array([60,60])


tamañolupa2=np.array([61,60,62,61,60,60])

lupa2=np.average(tamañolupa2)
slupa2=combinada(incertidumbre(tamañolupa2),incertidumbrepropagadan(np.array([d/np.sqrt(12)]*len(tamañolupa2))))


# Distancia 3
    #medida1 micro

cuadrados3=(4/5)*0.5
tamañolupa31=np.array([99.0,99.0,100.0])
d=46.1-40.1 #cm lupa1-camara
l=21.1-9.8#lente2-objeto

dt=np.append(dt,d)
lt=np.append(lt,l)

    #medida2 micro
cuadrados=(4/5)*0.5
tamañolupa32=np.array([100.0,100.0,99.0])


 #medida3 micro
cuadrados=(4/5)*0.5
tamañolupa33=np.array([98.0,100.0,99.0])

tamañolupa3=np.array([99,99,100,100,100,99,98,100,99])


lupa3=np.average(tamañolupa3)
slupa3=combinada(incertidumbre(tamañolupa3),incertidumbrepropagadan(np.array([d/np.sqrt(12)]*len(tamañolupa3))))


# Distancia 4
    #medida1 micro

cuadrados4=0.5#un medio cuadrado grande uno pequerrechiño
tamañolupa41=np.array([63,61,61])
d=46.1-40.1 #cm lupa1-camara
l=24-7.1 #lente2-objeto

lt=np.append(lt,l)
dt=np.append(dt,d)

    #medida2 micro
cuadrados=0.5
tamañolupa42=np.array([61,61,61])


 #medida3 micro
cuadrados=0.5
tamañolupa43=np.array([62,62,61])


tamañolupa4=np.array([63,61,61,61,61,61,62,62,61])


lupa4=np.average(tamañolupa4)
slupa4=combinada(incertidumbre(tamañolupa4),incertidumbrepropagadan(np.array([d/np.sqrt(12)]*len(tamañolupa4))))



# Distancia 5
    #medida1 micro

cuadrados5=1#un  cuadrado grande
tamañolupa51=np.array([85,85,84])
d=46.1-40.1 #cm lupa1-camara
l=25-3.2 #lente2-objeto cuanto mayor sea menor es el error entre exp y teo

dt=np.append(dt,d)
lt=np.append(lt,l)

    #medida2 micro
cuadrados=1
tamañolupa52=np.array([86,86,84])

 #medida3 micro
cuadrados=1
tamañolupa53=np.array([87,86,85])


tamañolupa5=np.array([85,85,84,86,86,84,87,86,85])

lupa5=np.average(tamañolupa5)
slupa5=combinada(incertidumbre(tamañolupa5),incertidumbrepropagadan(np.array([d/np.sqrt(12)]*len(tamañolupa5))))


# DATOS CALCULAR

cuadrados=np.array([cuadrados1,cuadrados2,cuadrados3,cuadrados4,cuadrados5])
lupa=np.array([lupa1,lupa2,lupa3,lupa4,lupa5])
slupa=np.array([slupa1,slupa2,slupa3,slupa4,slupa5])
dt=dt
d0=d0
lt=lt
lp,slp=di(f2, lt, sf2, sd)

bt,sbt=aumetoteorico(d0, dt, f1, lp, lt, sd, sf1, slp, slp)

bexp=(lupa/np.average(tamañoog))*(cuadradosog/cuadrados)
sbexp=np.sqrt((slupa*(1/np.average(tamañoog))*(cuadradosog/cuadrados))**2+(stamañoog*bexp/np.average(tamañoog))**2)



tabla=concatenarbueno((bt,sbt,bexp,sbexp))
header=["$  beta_t $", "$s(  beta_t)$","$ beta_{exp}$", "$s( beta_{exp})$"]
hola=tabulate(tabla, header,tablefmt="latex",floatfmt=(".3f", ".3f",".3f", ".3f"))
outfile=open("Microscopio-Aumentos.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write(hola)
outfile.write("\\caption{Valores de los aumentos angulares experimentales y teóricos} \n")
outfile.write("\\label{tab:datos-parte-2.1.%d} \n"%(1))
outfile.write("\\end{table} \n \n \n")
outfile.close()
