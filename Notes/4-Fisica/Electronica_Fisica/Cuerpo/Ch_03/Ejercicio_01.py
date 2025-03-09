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
Va=0
fig1=plt.figure()
fun_grafica_bandas_pn(fig1,Ec,Ev,Vbi,Ei,slopep,slopen,xn,xp,Va)
plt.ylim(-1.3,1.0)
fig1.savefig("03_01_Bandas.pdf")

xn_aux=xn
xp_aux=xp

print("################")


print("Apartado b)")

Va=-0.2

xn=fun_xn(NA,ND,KSSi,Vbi,Va)
xp=fun_xp(NA,ND,KSSi,Vbi,Va)

print("xp=%.5e [cm]"%xp)
print("xn=%.5e [cm]"%xn)

fig2=plt.figure()
fun_grafica_bandas_pn(fig2,Ec,Ev,Vbi,Ei,slopep,slopen,xn,xp,Va)
plt.ylim(-1.3,1.0)
fig2.savefig("03_02_Bandas.pdf")
print("################")
print("Apartado c)")

Va=0.2

xn=fun_xn(NA,ND,KSSi,Vbi,Va)
xp=fun_xp(NA,ND,KSSi,Vbi,Va)

print("xp=%.5e [cm]"%xp)
print("xn=%.5e [cm]"%xn)

fig3=plt.figure()
fun_grafica_bandas_pn(fig3,Ec,Ev,Vbi,Ei,slopep,slopen,xn,xp,Va)
plt.ylim(-1.3,1.0)
fig3.savefig("03_03_Bandas.pdf")

print("################")
print("Apartado c)")
fig4=plt.figure()
fun_grafica_E_pn(fig4,NA,ND,KSSi,xn,xp,0.2,"blue","-")
fun_grafica_E_pn(fig4,NA,ND,KSSi,xn_aux,xp_aux,0.0,"red","--")
plt.legend()
fig4.savefig("03_04_E.pdf")

fig5=plt.figure()
fun_grafica_V_pn(fig4,Vbi,slopen,slopep,xn,xp,0.2,"blue","-")
fun_grafica_V_pn(fig4,Vbi,slopen,slopep,xn_aux,xp_aux,0.0,"red","--")
plt.legend()
fig5.savefig("03_05_V.pdf")

fig6=plt.figure()
fun_grafica_rho_pn(fig4,xn_aux,xp_aux,NA,ND,0.0,"grey","-")
fun_grafica_rho_pn(fig4,xn,xp,NA,ND,0.2,"black","--")
plt.legend()
fig6.savefig("03_06_rho.pdf")