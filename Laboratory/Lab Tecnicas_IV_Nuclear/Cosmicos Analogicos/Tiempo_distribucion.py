import numpy as np
import matplotlib.pyplot as plt 

x1=np.array([1.89,2.46,2.79,1.73,1.39,1.39,1.15,1.30,1.52,1.4,1.42,1.34,0.95,1.15,1.92,1.27,1.28,1.67,1.57,1.35])
x2=np.array([2,2.6,3.03,1.84,1.64,1.44,1.58,1.53,1.51,1.5,1.52,1.57,1.19,1.35,1.99,1.54,1.47,1.69,1.65,1.34])

deltat=x2-x1


# Histograma de la diferencia (centrado respecto a x1)
plt.figure(figsize=(8,5))
plt.hist(deltat, bins='auto', edgecolor='white', alpha=0.7)
plt.title("Histograma de $\\Delta t = x_1 - x_2$")
plt.xlabel("$\\Delta t$ [s]")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.savefig("Tiempo.pdf")