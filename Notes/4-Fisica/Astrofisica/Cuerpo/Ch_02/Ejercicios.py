import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as cte


Msol=1.989*10**(30)

def Masa(a1,T1,a2,T2,M):
    m=((a1/a2)**3)*((T2/T1)**2)*M
    return m

print("Ejercicio 3")
print("La masa de marte es:", Masa(9400000,0.319033*24*3600,227.946*10**9,686.96*24*3600,Msol))
print(cte.gravitational_constant,686.96*24*3600)