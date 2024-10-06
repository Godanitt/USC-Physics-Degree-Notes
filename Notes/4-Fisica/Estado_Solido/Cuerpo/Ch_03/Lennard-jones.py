
# EN ESTE PROGRAMA VAMOS A REPRESENTAR EL POTENCIAL DE LENNARD-JONES

import numpy as np
import matplotlib.pyplot as plt

# Parámetros de Lennard-Jones
epsilon = 1.0  # Profundidad del pozo
sigma = 1.0    # Distancia en la que el potencial es cero

# Función de Lennard-Jones
def lennard_jones(r, epsilon, sigma):
    return 4 * epsilon * ((sigma / r)**12 - (sigma / r)**6)

# Rango de distancias (r) para graficar
r = np.linspace(0.8, 3.0, 500)  # Evitamos r = 0 para evitar singularidades

# Calcular el potencial para cada valor de r
V = lennard_jones(r, epsilon, sigma)

# Crear la gráfica
plt.figure(figsize=(6, 4))
plt.plot(r, V,linewidth=2.0  ,color='blue', label=r'$V(r) = 4\epsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right]$')
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(sigma, color='red', linestyle='--', label=r'$r = \sigma$')
plt.title('Potencial de Lennard-Jones')
plt.xlabel('Distancia entre partículas $r$')
plt.ylabel('Potencial $V(r)$')
plt.ylim(-1.5,2)
plt.legend()
plt.grid(True)
plt.savefig("Lennard-jones.pdf",dpi=300.0,bbox_inches="tight")
 # Añadir 4-Fisica\Estado_Solido\Cuerpo\Ch_03\ si se ejecuta desde Vscode
plt.show()

"""
n=25
m=11

for i in range(n):
    i+=1
    print("\\begin{figure}[h!] \centering")
    print("\includegraphics[scale=0.5]{Cuerpo/Ch_%0.2i/Fotos libro %i.pdf}"%(m,i))
    print("\caption{}")
    print("\label{Fig:%0.2i-%0.2i}"%(m,i))
    print("\end{figure}")
          
"""