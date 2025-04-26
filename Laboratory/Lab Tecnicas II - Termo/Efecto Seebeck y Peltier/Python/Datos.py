# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from matplotlib import pyplot as plt
import numpy as np

#Calculamos la resistencia tomando pares de valores (V,I):
    
    
R = np.array([[20,0.022],[40,0.042],[60,0.062],[80,0.082],[100,0.102],[120,0.121],[140,0.140],[160,0.159],[180,0.176],[200,0.195]])


#De manera directa obtenemos:
    
RD = 1.01  #En K Ohmnios


#El voltaje es de 125.0 V
#Tomamos valores de la tempeartura cada min. T = [T2,T1]. (la diferencia entre cada valor sera de 2 min)


T1 =  np.array([[16.6,12.0,0],[17.1,12.0,120],[18.4,12.1,240],[19.5,12.0,360],[20.7,12.1,420],[21.6,12.2,480],[22.0,12.2,600],[22.7,12.0,660],[23.3,12.0,900],[23.6,12.3,960],[23.9,12.4,1020],[24.2,12.4,1080],[24.6,12.4,1140],[24.9,12.5,1200],[25.1,12.4,1260],[25.4,12.4,1320],[25.6,12.4,1380],[25.8,12.4,1440],[26.0,12.5,1500],[26.2,12.5,1560],[26.3,12.5,1620],[26.5,12.5,1680],[26.7,12.5,1740],[26.8,12.5,1800],[27.0,12.6,1860],[27.2,12.6,1920],[27.3,12.7,1980],[27.4,12.7,2040],[27.6,12.7,2100],[27.7,12.6,2160],[27.7,12.6,2220],[27.8,12.5,2280],[27.9,12.6,2340],[28.0,12.6,2400],[28.1,12.6,2460],[28.1,12.7,2520],[28.2,12.7,2580],[28.3,12.7,2640],[28.4,12.7,2700],[28.4,12.9,2760],[28.5,12.9,2820],[28.5,12.7,2880],[28.6,12.7,2940],[28.6,12.7,3000],[28.6,12.9,3060],[28.7,12.9,3120]])

#Medimos el voltaje de manera directa

E1=0.855

#Medimos de manera indirecta (V,I (mA)):
    
Datos = np.array([[0.049,100.7],[0.107,92.5],[0.155,86.2],[0.189,81.9],[0.237,75.9],[0.285,70.1],[0.323,65.3],[0.354,61.4],[0.382,58.0],[0.406,55.1],[0.447,50.0],["-","-"]])


#El voltaje es de 150.0
#Tomamos valores cada minuto (un minuto es el 3er valor):
    
T2=np.array([[28.8,13.0,0],[29.1,13.1,1],[29.5,13.1,2],[29.9,13.2,3],[30.4,13.2,4],[30.8,13.3,5],[31.2,13.4,6],[31.5,13.4,7],[31.9,13.5,8],[32.1,13.5,9],[32.4,13.5,10],[32.7,13.5,11],[32.9,13.5,12],[33.2,13.6,13],[33.4,13.6,14],[33.6,13.6,15],[33.8,13.5,16],[34.0,13.5,17],[34.1,13.5,18],[34.2,13.5,19],[34.3,13.5,20],[34.4,13.6,21],[34.5,13.5,22],[34.6,13.5,23],[34.7,13.5,24],[34.8,13.5,25],[34.9,13.5,26],[34.9,13.5,27],[34.9,13.5,28],[35.0,13.5,29],[35.1,13.5,30],[35.2,13.5,31],[35.2,13.5,32],[35.3,13.5,33],[35.3,13.5,34],[35.4,13.5,35],[35.4,13.5,36],[35.5,13.5,37],[35.5,13.5,38],[35.6,13.6,39],[35.6,13.6,40],[35.7,13.7,41],[35.7,13.7,42],[35.8,13.7,43],[35.8,13.6,45],[35.8,13.5,46]])


#Medimos el voltaje de manera directa:
    
E2 = 1.195

#Medimmos de manera indirecta V(V, I (mA)):

Datos2=np.array([[0.089,140.5],[0.184,125.1],[0.258,118.1],[0.315,111.0],[0.362,104.9],[0.418,98.4],[0.439,94.7],[0.487,89.2],[0.528,84.3],[0.581,77.8],[0.630,71.5],[0.677,65.6]])



outfile=open("datos3.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\\varepsilon \ (V)$ & $s(\\varepsilon) \(V) $ \\\ \\hline \n")
outfile.write("%f  & %f \\\ \n\hline\n"%(E1,0.001))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores para la fuerza electromotriz V=125V de manera directa} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()



outfile=open("datos4.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\\varepsilon \ (V)$ & $s(\\varepsilon) \ (V) $ \\\ \\hline \n")
outfile.write("%f  & %f \\\ \n\hline\n"%(E2,0.001))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valores para la fuerza electromotriz  V=150V de manera directa} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()



outfile=open("datos5.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c||c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\\Delta V_{R_X} \ (V)$ & $I \ (mA) $ & $\\Delta V_{R_X} \ (V)$ & $I \ (mA) $  \\\ \\hline \n")
for i in range(int(len(Datos)/2)):
    outfile.write("%s &  %s & %s & %s \\\ \n"%(str(Datos[i,0]),str(Datos[i,1]),str(Datos[i+6,0]),str(Datos[i+6,1])))
outfile.write("\\hline \n\\end{tabular} \n")
outfile.write("\\caption{Valores de los pares ($\Delta V_{R_X},I$) para V = 125V} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()

outfile=open("datos6.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c||c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\\Delta V_{R_X} \ (V)$ & $I \ (mA) $ & $\\Delta V_{R_X} \ (V)$ & $I \ (mA) $  \\\ \\hline \n")
for i in range(int(len(Datos)/2)):
    outfile.write("%s &  %s & %s & %s \\\ \n"%(str(Datos2[i,0]),str(Datos2[i,1]),str(Datos2[i+6,0]),str(Datos2[i+6,1])))
outfile.write("\\hline \n\\end{tabular} \n")
outfile.write("\\caption{Valores de los pares ($\Delta V_{R_X},I$) para V = 150V} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()


outfile=open("datos7.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c||c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$\\Delta V_{R_X} \ (V)$ & $I \ (A) $ & $\\Delta V_{R_X} \ (V)$ & $I \ (A) $  \\\ \\hline \n")
for i in range(int(len(R)/2)):
    outfile.write("%s &  %s & %s & %s \\\ \n"%(str(R[i,0]),str(R[i,1]),str(R[i+5,0]),str(R[i+5,1])))
outfile.write("\\hline \n\\end{tabular} \n")
outfile.write("\\caption{Valores para ($V,I$) para el cálculo de la  resistencia $R_c$} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()

outfile=open("datos9.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$ R_{C1} \ (\\Omega)$ & $s(R_{C1}) \ (\\Omega) $ & $R_{C2} \ (\\Omega)$ & $ s(R_{C2}) \ (||Omega) $ \\\ \\hline \n")
outfile.write("%d  & %d & %d &  %d \\\ \n\hline\n"%(RD*1000,10,989,10))
outfile.write("\\end{tabular} \n")
outfile.write("\\caption{Valor para la resistencia $R_C$ calculada de manera directa} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()



outfile=open("datos10.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c||c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$T_2 \ (C^o)$ & $T_1 \ (C^o) $ & $t \ (min)$ & $T_2 \ (C^o)$ & $T_1 \ (C^o) $ & $t \ (min)$ \\\ \\hline \n")
for i in range(int(len(T1)/2)):
    outfile.write("%.1f &  %.1f & %d & %.1f & %1.f & %d \\\ \n"%(T1[i,0],T1[i,1],T1[i,2]/60,T1[i+23,0],T1[i+23,1],T1[i+23,2]/60))
outfile.write("\\hline \n\\end{tabular} \n")
outfile.write("\\caption{Valores ($T_2,T_1,t$) tomados en el laboratorio para voltaje 125$V$} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()

outfile=open("datos11.txt", 'w')
outfile.write("\\begin{table}[h!] \t \centering \n")
outfile.write("\\begin{tabular}{|c|c|c||c|c|c|} \n")
outfile.write("\\hline \n")
outfile.write("$T_2 \ (C^o)$ & $T_1 \ (C^o) $ & $t \ (min)$ & $T_2 \ (C^o)$ & $T_1 \ (C^o) $ & $t \ (min)$ \\\ \\hline \n")
for i in range(int(len(T1)/2)):
    outfile.write("%.1f &  %.1f & %d & %.1f & %.1f & %d \\\ \n"%(T2[i,0],T2[i,1],T2[i,2],T2[i+23,0],T2[i+23,1],T2[i+23,2]))
outfile.write("\\hline \n\\end{tabular} \n")
outfile.write("\\caption{Valores ($T_2,T_1,t$) tomados en el laboratorio para voltaje 150$V$} \n")
outfile.write("\\label{tab:} \n")
outfile.write("\\end{table} \n")
outfile.close()




