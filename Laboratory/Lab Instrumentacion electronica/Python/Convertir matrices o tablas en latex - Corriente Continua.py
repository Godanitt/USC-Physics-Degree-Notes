# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:10:17 2022

@author: PC
"""


#==================================================================================#
#Importamos módulos:
from numpy import loadtxt, savetxt,array

#==================================================================================#
#Programa:
infile=open("CorrienteContinua.tsv", 'r')
tabla = []
lines = infile.readlines()
for i in lines:
    print(i)
    tabla.append(i.split("\t"))
infile.close
tabla = array(tabla)
outfile=open("Datos1-latex.txt", 'w')
for i in range(len(tabla)):
    for j in range(len(tabla[i])):
        if(j==len(tabla[i])-1):
            outfile.write("%s  "%tabla[i][j])
        else:   
            outfile.write("%s & "%tabla[i][j])
    outfile.write("\\\ \n")


outfile.close



