#-*- coding: utf-8 -*-
#Animacion do campo electrico como funcion da frecuencia para a practica de propagacion de ondas electromagneticas en condutores.
#Autor: Adolfo Otero Fumega

import numpy as np
import matplotlib as m
import matplotlib.pyplot as plt
import scipy.constants
#import time

print("~~~~~~~~ ANIMACIÓN DA PRÁCTICA DE PROPAGACIÓN DE ONDAS ELECTROMAGNETICAS EN CONDUTORES ~~~~~~~~")
print("Mostrarase unha vista superior do solenoide de campo (circunferencia de fora) e do cilindro condutor no seu interior (circunferencias con liñas quebradas).")
print("Aparecerá unha animación para que visualices o campo. Tamén che calculará o desfase entre o campo antes de entrar e despois de saír do cilindro condutor, así como a relacion entre as amplitudes máximas do campo dentro e fóra. Como vistes, todo esto dependerá da frecuencia do campo Electromagnético. Esta será a variable que podes modificar.")
print(" ")
print("Escribe a frecuencia que queiras do Campo E en Hz e pulsa ENTER (Procura que sexa menor a 1GHz, senón as aproximacións que se fan para calcular os campos non son válidas e o programa peta!!!):")
nu=float(input()) #Frecuencia

#Distintos Parametros, todos eles en unidades do SI
L=0.10 #Lonxitude do solenoide de campo
N=200 #Numero de voltas do solenoide de campo
om=nu*2.0*np.pi #Frecuencia angular
R_s=0.016 #Radio do solenoide de campo
R_i=0.0065 #Radio interior do cilindro condutor
R_f=0.0075 #Radio exterior do cilindro condutor
d=R_f-R_i # Anchura do cilindro condutor
sigma=59600000 #Codutividade do cilindro condutor
T_p=2.0*np.pi/om #Periodo
B=np.sqrt(scipy.constants.mu_0*sigma*om/2.0) #Coeficiente de Atenuacion

#Cantidades auxiliares que se empregan no loop temporal, para aforrar tempo de calculo:
aux_1=-scipy.constants.mu_0*N*om/L*0.5
aux_2=-B*N/L*np.sqrt(2.0)/sigma/(np.sinh(B*d)**2*np.cos(B*d)**2+np.cosh(B*d)**2*np.sin(B*d)**2)
aux_3=np.abs((aux_2*np.cos(B*d)*np.sin(B*d)+aux_2*np.cosh(B*d)*np.sinh(B*d))*R_s/R_f/np.sqrt(2))


des=int(B*d*180/np.pi) #Desfase
at=np.exp(-B*d) #Atenuacion

# Mesh no que imos a plotear:
p = np.linspace(0, 2*np.pi, 50)
r1 = np.linspace(0, R_i, 50)
R1, P = np.meshgrid(r1, p)
r2 = np.linspace(R_i, R_f, 50)
R2, P = np.meshgrid(r2, p)
r3 = np.linspace(R_f, R_s, 50)
R3, P = np.meshgrid(r3, p)

# Mesh en coordenadas cartesianas:
X_s, Y_s = R_s*np.cos(P), R_s*np.sin(P)
X_i, Y_i = R_i*np.cos(P), R_i*np.sin(P)
X_f, Y_f = R_f*np.cos(P), R_f*np.sin(P)
X1, Y1 = R1*np.cos(P), R1*np.sin(P)
X2, Y2 = R2*np.cos(P), R2*np.sin(P) 
X3, Y3 = R3*np.cos(P), R3*np.sin(P)



fig = plt.figure()
plt.ion()
plt.plot(X_s,Y_s, color='black', linestyle='dashed') 
plt.plot(X_i,Y_i, color='black', linestyle='dashed') 
plt.plot(X_f,Y_f, color='black', linestyle='dashed') 

plt.gcf().text(0.1, 0.93, "Desfase $\phi =$"+ str(des) +"$^\circ$"+ ", $E(d)_{max}/E(0)_{max}$=" + str(round(at, 2)), fontsize=20)

#Inializamos o ploteado:
Z1=aux_2*(np.cos(om*0-np.pi/4.0)*np.sin(B*d)*np.cosh(B*d)+np.cos(om*0+np.pi/4.0)*np.cos(B*d)*np.sinh(B*d))*R1/R_i
Z2=aux_2*(np.cos(om*0-np.pi/4.0)*np.cos(B*(R_i-R2))*np.cosh(B*(R_i-R2))*np.sin(B*d)*np.cosh(B*d)+np.sin(B*(R_i-R2))*np.sinh(B*(R_i-R2))*np.cos(B*d)*np.sinh(B*d))
Z2=Z2+aux_2*(np.cos(om*0+np.pi/4.0)*np.cos(B*(R_i-R2))*np.cosh(B*(R_i-R2))*np.cos(B*d)*np.sinh(B*d)+np.sin(B*(R_i-R2))*np.sinh(B*(R_i-R2))*np.sin(B*d)*np.cosh(B*d))
Z3=aux_2*(np.cos(om*0-np.pi/4.0)*np.cos(B*d)*np.sin(B*d)+np.cos(om*0+np.pi/4.0)*np.cosh(B*d)*np.sinh(B*d))*R3/R_f
plt.pcolor(X1, Y1, Z1, cmap=plt.cm.seismic, vmin=(-aux_3), vmax=(aux_3))
plt.pcolor(X2, Y2, Z2, cmap=plt.cm.seismic, vmin=(-aux_3), vmax=(aux_3))
plt.pcolor(X3, Y3, Z3, cmap=plt.cm.seismic, vmin=(-aux_3), vmax=(aux_3))
plt.xlim(-0.017,0.017)
plt.ylim(-0.017,0.017)
clb = plt.colorbar()
clb.set_label('$E$ $(V/m)$', labelpad=30, y=0.5, rotation=-90, fontsize=20)	

#Loop temporal:
for t in np.linspace(0,2*T_p,100): #Recorremos 2 periodos
	#Calculo do campo en cada rexion do espazo:
	Z1=aux_2*(np.cos(om*t-np.pi/4.0)*np.sin(B*d)*np.cosh(B*d)+np.cos(om*t+np.pi/4.0)*np.cos(B*d)*np.sinh(B*d))*R1/R_i
	Z2=aux_2*(np.cos(om*t-np.pi/4.0)*np.cos(B*(R_i-R2))*np.cosh(B*(R_i-R2))*np.sin(B*d)*np.cosh(B*d)+np.sin(B*(R_i-R2))*np.sinh(B*(R_i-R2))*np.cos(B*d)*np.sinh(B*d))
	Z2=Z2+aux_2*(np.cos(om*t+np.pi/4.0)*np.cos(B*(R_i-R2))*np.cosh(B*(R_i-R2))*np.cos(B*d)*np.sinh(B*d)+np.sin(B*(R_i-R2))*np.sinh(B*(R_i-R2))*np.sin(B*d)*np.cosh(B*d))
	Z3=aux_2*(np.cos(om*t-np.pi/4.0)*np.cos(B*d)*np.sin(B*d)+np.cos(om*t+np.pi/4.0)*np.cosh(B*d)*np.sinh(B*d))*R3/R_f
	#Ploteado do campo en cada rexion.
	plt.pcolor(X1, Y1, Z1, cmap=plt.cm.seismic, vmin=(-aux_3), vmax=(aux_3)) #Rexion interior
	plt.pcolor(X2, Y2, Z2, cmap=plt.cm.seismic, vmin=(-aux_3), vmax=(aux_3)) #Rexion do condutor
	plt.pcolor(X3, Y3, Z3, cmap=plt.cm.seismic, vmin=(-aux_3), vmax=(aux_3)) #Rexion exterior
	plt.pause(0.0001)

	
plt.ioff() 
plt.show()	
























