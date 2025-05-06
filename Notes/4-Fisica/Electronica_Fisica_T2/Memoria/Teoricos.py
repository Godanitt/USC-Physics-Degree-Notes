import numpy as np
import matplotlib.pyplot as plt


import numpy as np
import scipy.constants as cte

# Constantes físicas

q = 1.602e-19           # Carga elemental (C)
epsilon_0 = 8.854e-14   # Permisividad del vacío en F/cm
k=8.617333262*10**(-5)

def calcular_alpha(Ks, Kox, x0, NA):
    fraccion = Ks * x0 / (Kox )
    raiz = np.sqrt((2 * q * NA) / (Ks * epsilon_0))
    alpha = fraccion * raiz
    return alpha

def calcular_phi_s(alpha, VG):
    phi_s = ((-alpha + np.sqrt(alpha**2 + 4 * abs(VG))) / 2)**2
    return phi_s

def calcular_W(phiS, KS, NA_cm3):
    """Calcula la anchura W (en cm) de la zona de carga espacial."""
    return np.sqrt((2*phiS * KS * epsilon_0) / (q * NA_cm3))

def campo_electrico_en_0(W_cm, KS, NA_cm3):
    """Calcula el campo eléctrico E_S(x) en x = 0 (en V/cm)."""
    return (q * NA_cm3 / (KS * epsilon_0)) * W_cm

def calcular_VG(phiS, KS, K0, x0_cm, NA_cm3):
    """Calcula la tensión de compuerta VG (en V)."""
    raiz = np.sqrt((2 * q * NA_cm3 * phiS) / (KS * epsilon_0))
    return phiS + (KS / K0) * x0_cm * raiz

def calcular_VG(phiS, KS, K0, x0_cm, NA_cm3):
    """Calcula la tensión de compuerta VG (en V)."""
    raiz = np.sqrt((2 * q * NA_cm3 * phiS) / (KS * epsilon_0))
    return phiS + (KS / K0) * x0_cm * raiz


def formato_si(valor, unidades=""):
    """Formatea el número en notación científica estilo siunitx."""
    return "$" + r"\SI{{{:.2e}}}{{{}}}".format(valor, unidades) + "$"

    
    
T=300
x0=0.1*10**(-4)
ni=10**(10)
NA=3.5*10**(14)
K0=3.9
KS=11.7
Eg=1.12
mnSi=1.18    
mpSi= 0.81 

phiF=(cte.k/cte.e)*T*np.log(NA/ni)
alpha=calcular_alpha(KS,K0,x0,NA)
phiS=0.579894
VFB=calcular_VG(phiS,KS,K0, x0, NA)
print("phiF=",phiF)
print("V_FB=",VFB)
print("alpha=",alpha)
alpha=calcular_alpha(KS,K0,x0,NA)


######################################################

print("******** Polarizacion 0 ****************")

VG=0+VFB
phiS=calcular_phi_s(alpha,VG)
W=calcular_W(phiS,KS,NA)
Eox=(KS/K0)*campo_electrico_en_0(W,KS,NA)
Esil=campo_electrico_en_0(W,KS,NA)

print("phiS (0)=",formato_si(phiS))
print("W=",formato_si(W))
print("Eox=",formato_si(Eox))
print("Esil=",formato_si(Esil))
print("pp (sustrato)=",formato_si(NA))
print("np (sustrato)=",formato_si((ni**2)/NA))

print("pp (interfaz)=",formato_si((ni)*np.exp(-(-phiF+phiS)/(k*T))))
print("np (interfaz)=",formato_si(ni*np.exp((-phiF+phiS)/(k*T))))

print("Ec (sustrato)=",formato_si(Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF))
print("Ev (sustrato)=",formato_si(-Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF))
print("Ec (interfaz)=",formato_si(Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF-phiS))
print("Ev (interfaz)=",formato_si(-Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF-phiS))


######################################################

print("******** Polarizacion 2 ****************")

VG=2+VFB
phiS=calcular_phi_s(alpha,VG)
W=calcular_W(phiS,KS,NA)
Eox=(KS/K0)*campo_electrico_en_0(W,KS,NA)
Esil=campo_electrico_en_0(W,KS,NA)

print("phiS (2)=",formato_si(phiS))
print("W=",formato_si(W))
print("Eox=",formato_si(Eox))
print("Esil=",formato_si(Esil))
print("pp (sustrato)=",formato_si(NA))
print("np (sustrato)=",formato_si((ni**2)/NA))

print("pp (interfaz)=",formato_si((ni)*np.exp(-(-phiF+phiS)/(k*T))))
print("np (interfaz)=",formato_si(ni*np.exp((-phiF+phiS)/(k*T))))

print("Ec (sustrato)=",formato_si(Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF))
print("Ev (sustrato)=",formato_si(-Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF))
print("Ec (interfaz)=",formato_si(Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF-phiS))
print("Ev (interfaz)=",formato_si(-Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF-phiS))

######################################################

print("******** Polarizacion -2 ****************")

VG=-2+VFB
phiS=calcular_phi_s(alpha,VG)
W=calcular_W(phiS,KS,NA)
Eox=(KS/K0)*campo_electrico_en_0(W,KS,NA)
Esil=campo_electrico_en_0(W,KS,NA)


print("phiS (-2)=",formato_si(phiS))
print("W=",formato_si(W))
print("Eox=",formato_si(Eox))
print("Esil=",formato_si(Esil))
print("pp (sustrato)=",formato_si(NA))
print("np (sustrato)=",formato_si((ni**2)/NA))

print("pp (interfaz)=",formato_si((ni)*np.exp(-(-phiF-phiS)/(k*T))))
print("np (interfaz)=",formato_si(ni*np.exp((-phiF-phiS)/(k*T))))

print("Ec (sustrato)=",formato_si(Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF))
print("Ev (sustrato)=",formato_si(-Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF))
print("Ec (interfaz)=",formato_si(Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF+phiS))
print("Ev (interfaz)=",formato_si(-Eg/2+3*k*T*np.log(mpSi/mnSi)/4+phiF+phiS))