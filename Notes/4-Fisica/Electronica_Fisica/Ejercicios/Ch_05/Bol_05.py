import numpy as np
import scipy.constants as cte

# Constantes físicas
q = 1.602e-19        # Carga elemental (C)
epsilon_0 = 8.854e-14  # Permisividad del vacío en F/cm

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

def formato_si(valor, unidades):
    """Formatea el número en notación científica estilo siunitx."""
    return r"\SI{{{:.2e}}}{{{}}}".format(valor, unidades)

def calcula(phiS,NA,x0,KS,K0):
    # Cálculos
    W = calcular_W(phiS, KS, NA)
    E0 = campo_electrico_en_0(W, KS, NA)
    VG = calcular_VG(phiS, KS, K0, x0, NA)

    # Resultados formateados
    print("\\phi_{S} =", formato_si(phiS, "V"))
    print("W =", formato_si(W, "cm"))
    print("E(0) =", formato_si(E0, "V/cm"))
    print("V_G =", formato_si(VG, "V"))
    
T=300
x0=0.1*10**(-4)
ni=10**(10)
NA=10**(15)
K0=3.9
KS=11.7
phiF=(cte.k/cte.e)*T*np.log(NA/ni)
phiS=phiF

print("Ejercicio 2")
calcula(phiS,NA,x0,KS,K0)


print("*************************")
T=300
x0=5*10**(-7)
ni=10**(10)
NA=10**(17)
K0=3.9
KS=11.7
phiF=(cte.k/cte.e)*T*np.log(NA/ni)
phiS=phiF
print("Ejercicio 4")
calcula(phiS,NA,x0,KS,K0)