import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Ejercicios_modulo import *

VA=0.2
A=2*10**-2
T=300
Eg=1.42
ND=10**14
NA=10**14
mun=9000
mup=450
taup=20*10**(-9)
taun=10*10**(-9)
KS=1.4337*10**-10/cte.epsilon_0
mn=0.4*me
mp=0.3*me

NC=fun_NCV(mp)
NV=fun_NCV(mn)
ni=fun_ni(NC,NV,Eg,T)

print("ni=%.3e"%ni)


Vbi=fun_Vbi(NA,ND,ni,T)

print("Vbi=%.3e"%Vbi)
print("KS=%.2e"%KS)

DP=fun_D(mup,T)
DN=fun_D(mun,T)
LP=fun_L(DP,taup)
LN=fun_L(DN,taun)

print("DN=",DN)
print("DP=",DP)
print("LN=",LN)
print("LP=",LP)

xn=fun_xn(NA,ND,KS,Vbi,VA)
xp=fun_xp(NA,ND,KS,Vbi,VA)

print("xn=%.3e"%xn)
print("xp=%.3e"%xp)

IPxn=-fun_IPxn(A,DP,LP,ni,ND,VA,xn,np.inf,T)
INxp=-fun_INxp(A,DN,LN,ni,ND,VA,xp,np.inf,T)

print("IPxn=%.3e"%IPxn)
print("INxp=%.3e"%INxp)
print("Itot=%.3e"%(IPxn+INxp))
Ei=fun_Ei(ni,NA,ni)
Ec=fun_Ec(mn,Ei,ni,T)
Ev=fun_Ev(Ec,Eg)
Vbi=fun_Vbi(NA,ND,ni,T)

slope_p=fun_slope_lineal(NA,0,KS)
slope_n=fun_slope_lineal(0,ND,KS)

fig1=plt.figure()
fun_grafica_bandas_pn(fig1,Ec,Ev,Vbi,Ei,slope_p,slope_n,xn,xp,VA,T,1,True,LN,LP,"NP")
plt.legend()
plt.savefig("03_06_01.pdf",bbox_inches="tight")

fig1=plt.figure()
fun_grafica_I_pn(fig1,xn,xp,INxp,IPxn,LN,LP,125,300,VA,False,T,"NP")
plt.legend()
plt.savefig("03_06_02.pdf",bbox_inches="tight")