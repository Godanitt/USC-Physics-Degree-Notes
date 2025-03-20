import sys
import os

# Get the absolute path of the parent directory
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Add the folder2 path to sys.path
sys.path.append(module_dir)

# Now you can import script2.py
from Ejercicios_modulo import *

JN=0.025 # A/cm^2
JP=0.007 # A/cm2
DN=21 # cm2/s
DP=10 # cm2/s
taun=5*10**(-7) # s
taup=5*10**(-7) # s
VA=0.5 # V 
KS=11.7 

LN=fun_L(DN,taun)
LP=fun_L(DP,taup)

print("LN=",LN)
print("LP=",LP)

np0=(JN/e)*(LN/DN)*(1/(np.e**(VA/(300*k))-1)) 
pn0=(JP/e)*(LP/DP)*(1/(np.e**(VA/(300*k))-1))

print("np0=",np0)
print("pn0=",pn0)

ni=10**(10)

NA=(ni**2)/np0
ND=(ni**2)/pn0

print("NA=%.3e"%NA)
print("ND=%.3e"%ND)

Ei=fun_Ei(ni,NA,ni)
Ec=fun_Ec(mnSi,Ei,ni,300)
Ev=fun_Ev(Ec,EgSi)
Vbi=fun_Vbi(NA,ND,ni,300)

slope_p=fun_slope_lineal(NA,0,KS)
slope_n=fun_slope_lineal(0,ND,KS)

print("Vbi=",Vbi)

xn=fun_xn(NA,ND,KS,Vbi,VA)
xp=fun_xp(NA,ND,KS,Vbi,VA)
print("xn=",xn)
print("xp=",xp)

fig1=plt.figure()
fun_grafica_bandas_pn(fig1,Ec,Ev,Vbi,Ei,slope_p,slope_n,xn,xp,VA,300,1,True,LN,LP)
plt.legend()
plt.savefig("03_05_01.pdf",bbox_inches="tight")

fig2=plt.figure()
fun_grafica_minoritarios(fig2,NA,ND,ni,LP,LN,VA,xn,xp,1,1,300,Flag=False)
plt.legend()
plt.savefig("03_05_02.pdf",bbox_inches="tight")