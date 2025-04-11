import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Ejercicios_modulo import *

Va1=0.0
Va2=-0.0
A=2*10**-2
T=300
Eg=1.42
ND=5*10**15
NA1=10**16
NA2=10**15
ni=2.25*10**6


mun=9000
mup=450
taup=20*10**(-9)
taun=10*10**(-9)

KS=1.4337*10**-10/cte.epsilon_0
mn=0.066*me
mp=0.52*me                      
print("******************* Bandas de Energia *************************")
print("*********************** Apartado a) ***************************")
fig=plt.figure(figsize=(8,6))
fun_bandasPNP(fig,NA1,NA2,ND,ni,0,0,KS,Eg,mp,mp,T,prop=1,nombre_pdf="04_Ejercicio-2-01.pdf")
print("*********************** Apartado b) ***************************")
fig=plt.figure(figsize=(8,6))
fun_bandasPNP(fig,NA1,NA2,ND,ni,0.8,-1.5,KS,Eg,mp,mp,T,prop=1,nombre_pdf="04_Ejercicio-2-02.pdf")
print("********************* Campo Electrico *************************")
print("*********************** Apartado a) ***************************")
fig=plt.figure(figsize=(8,6))
fun_PNPCampoElectrico(fig,NA1,NA2,ND,ni,0,0,KS,T,prop=1.0,nombre_pdf="04_Ejercicio-2-03.pdf")
fig=plt.figure(figsize=(8,6))
print("*********************** Apartado b) ***************************")
fun_PNPCampoElectrico(fig,NA1,NA2,ND,ni,0.8,-1.5,KS,T,prop=1.0,nombre_pdf="04_Ejercicio-2-04.pdf")