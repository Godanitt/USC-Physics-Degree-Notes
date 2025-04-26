# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:19:00 2022

@author: PC
"""

#==================================================================================#
#Importamos módulos:
from numpy import loadtxt, savetxt,array

#==================================================================================#
#Programa:
infile=open("Tensión superficial.tsv", 'r')
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
            if(tabla[i][j]=='' or tabla[i][j]=='\n'):
                k=0
            else:
                outfile.write("%s  \t"%tabla[i][j])
        else:   
            if(tabla[i][j]=='' or tabla[i][j]=='\n'):
                k=0
            else:
                 if(tabla[i][j+1]=='' or tabla[i][j+1]=='\n'):   
                    outfile.write("%s "%tabla[i][j])
                 else:
                     outfile.write("%s & \t "%tabla[i][j])
    outfile.write("\\\ \n")


outfile.close



