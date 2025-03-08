import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Ejercicios_modulo import *


##################################
# Ejercicio 1 ####################
##################################

KSSi=11.7  # []
taup=10**(-6) # [s]
taun=10**(-6) # [s]
mup=1360 # [cm2/V*s]
mun=460  # [cm2/V*s]
NA=10**(15) # [cm-3]
ND=5*10**(14) # [cm-3]
dP=0.008 # [cm]
dN=0.008 # [cm]
A=10**(-2) # [cm2]

mnSi=1.18 # Masa del hueco en el silicio 300K) en m_e
mpSi= 0.81 

mn=fun_mnp(taun,mun)/me
mp=fun_mnp(taup,mup)/me
NC=fun_NCV(mnSi*me)
NV=fun_NCV(mpSi*me)
ni=fun_ni(NC,NV,EgSi,300)
Vbi=fun_Vbi(NA,ND,ni)
xn=fun_xn(NA,ND,KSSi,Vbi)
xp=fun_xp(NA,ND,KSSi,Vbi)
slopen=fun_slope_lineal(0,ND,KSSi)
slopep=fun_slope_lineal(NA,0,KSSi)

Ei=fun_Ei(ni,NA,ni)
Ec=fun_Ec(mnSi*me,Ei,ni)
Ev=fun_Ev(Ec)

print("Apartado a)")
print("mp_eff=%.5f me"%mp)
print("mp_eff=%.5f me"%mn)
print("NV=%.5e [cm-3]"%NV)
print("NC=%.5e [cm-3]"%NC)
print("ni=%.5e [cm-3]"%ni)
print("pn=%.5e [cm^3]"%(ni**2/ND))
print("Vbi=%.5e [V]"%Vbi)

print("xp=%.5e [cm]"%xp)
print("xn=%.5e [cm]"%xn)

print("Ei=%.2f"%Ei)
print("Ec=%.2f"%Ec)
print("Ev=%.2f"%Ev)

print("slopenp=",slopep)
print("slopenn=",slopen)

fig1=fun_grafica_bandas_pn(Ec,Ev,Vbi,Ei,slopep,slopen,xn,xp)

fig1.savefig("03_01_Bandas.pdf")

print("################")