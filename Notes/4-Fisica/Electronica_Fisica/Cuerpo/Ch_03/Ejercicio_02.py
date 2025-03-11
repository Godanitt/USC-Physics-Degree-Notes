import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Ejercicios_modulo import *

Eg=0.66
mn=0.5
mp=0.37
ND=10**16
NA=10**15
A=0.01
KS=(1.4337*10**(-10))/cte.epsilon_0
ni=2*10**13
mun=3900
mup=1900
taun=10**(-6)
taup=10**(-6)
xp1=0.002
xn1=0.003

Vbi=fun_Vbi(NA,ND,ni,)

# Apartado a)
NC=fun_NCV(mn*me)
NV=fun_NCV(mp*me)
ni=fun_ni(NC,NV,Eg,300)
Vbi=fun_Vbi(NA,ND,ni)
xn=fun_xn(NA,ND,KS,Vbi)
xp=fun_xp(NA,ND,KS,Vbi)
slopen=fun_slope_lineal(0,ND,KS)
slopep=fun_slope_lineal(NA,0,KS)

Ei=fun_Ei(ni,NA,ni)
Ec=fun_Ec(mn*me,Ei,ni)
Ev=fun_Ev(Ec)
Va=0


print("Ejercicio 2-2")
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

fig1=plt.figure(figsize=(7,5))
fun_grafica_bandas_pn(fig1,Ec,Ev,Vbi,Ei,slopep,slopen,xn,xp,Va,300,True)
fig1.savefig("03_08_Bandas.pdf")

print("\Ecal_{\max}=%.5e"%fun_Efield_max(NA,xp,KS))

print("##########")


print("Apartado b)")
DN=fun_D(mun)
DP=fun_D(mup)
LN=fun_L(DN,taun)
LP=fun_L(DP,taup)
print("Dn=%.5e"%DN)
print("Dp=%.5e"%DP)
print("Ln=%.5e"%LN)
print("Lp=%.5e"%LP)


xn=fun_xn(NA,ND,KS,Vbi+0.1)
xp=fun_xp(NA,ND,KS,Vbi+0.1)
fig2=plt.figure()

print("Va=%.5e [V]"%-0.1)
print("\SI{x_p=%.5e }{[cm]}"%xp)
print("\SI{x_n=%.5e}{[cm]}"%xn)

fun_grafica_minoritarios(fig2,NA,ND,ni,LP,LN,-0.1,xn,xp,xn1,xp1,300,True,"red","-.")
xn=fun_xn(NA,ND,KS,Vbi-0.1)
xp=fun_xp(NA,ND,KS,Vbi-0.1)

print("Va=%.5e [V]"%0.1)
print("x_p=\SI{%.5e }{[cm]}"%xp)
print("x_n=\SI{%.5e}{[cm]}"%xn)
fun_grafica_minoritarios(fig2,NA,ND,ni,LP,LN,+0.1,xn,xp,xn1,xp1,300,True,"green","-.")
plt.legend()
fig2.savefig("03_09_portadores.pdf")

print("##########")
print("Apartado c)")

fig3=plt.figure()
Va=0.1

xn=fun_xn(NA,ND,KS,Vbi-Va)
xp=fun_xp(NA,ND,KS,Vbi-Va)
IPxn=fun_IPxn(A,DP,LP,ni,ND,Va,xn,xn1,300)
INxp=fun_INxp(A,DN,LN,ni,NA,Va,xp,xp1,300)
print("V_a=\\SI{%.5e}{[V]}"%Va)
print("I_N(x_p)=\SI{%.5e}{[A]}"%INxp)
print("I_P(x_n)=\SI{%.5e}{[A]}"%IPxn)
fun_grafica_I_pn(fig1,xn,xp,INxp,IPxn,LN,LP,xn1,xp1,Va,300,True)
plt.legend()
fig3.savefig("03_10_corrientes.pdf")


fig3=plt.figure()
Va=-0.1
xn=fun_xn(NA,ND,KS,Vbi-Va)
xp=fun_xp(NA,ND,KS,Vbi-Va)
IPxn=fun_IPxn(A,DP,LP,ni,ND,Va,xn,xn1,300)
INxp=fun_INxp(A,DN,LN,ni,NA,Va,xp,xp1,300)
print("V_a=\\SI{%.5e}{[V]}"%Va)
print("I_N(x_p)=\SI{%.5e}{[A]}"%INxp)
print("I_P(x_n)=\SI{%.5e}{[A]}"%IPxn)
fun_grafica_I_pn(fig1,xn,xp,INxp,IPxn,LN,LP,xn1,xp1,Va,300,True)
plt.legend()
fig3.savefig("03_11_corrientes.pdf")
