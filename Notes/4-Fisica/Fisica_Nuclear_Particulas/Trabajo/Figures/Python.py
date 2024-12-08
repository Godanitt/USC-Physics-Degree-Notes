# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:11:24 2024

@author: danie
"""
import numpy as np
import matplotlib.pyplot as plt

# Definimos las constantes para la dispersión de Rutherford para 19F
Z1 = 9  # Número atómico del núcleo objetivo (flúor)
Z2 = 1  # Número atómico de la partícula incidente (protón)
e = 1.602e-19  # Carga elemental (C)

# Constante de permitividad del vacío
epsilon_0 = 8.854e-12  # F/m

# Ángulo fijo (por ejemplo, 90 grados en radianes)
theta = np.radians(150)  # Cambiado a 150° para reflejar condiciones experimentales

# Conversión a mili barns
barn_to_m2 = 1e-28
mb_to_m2 = 1e-31

# Expresión de la sección eficaz diferencial de Rutherford
# Ajustada para superponer mejor con la gráfica experimental
def seccion_eficaz(E):
    numerador = (Z1 * Z2 * e**2 / (4 * np.pi * epsilon_0))**2
    denominador = (4 * E * np.sin(theta / 2)**4)
    return numerador / denominador / mb_to_m2  # Convertir a mili barns

# Energías en MeV (sin conversión a Joules para mantener la escala)
E_MeV = np.linspace(0, 10.5, 1000)  # Energías entre 8.5 MeV y 10.5 MeV
E = E_MeV * 1e6 * e  # Conversión a Joules

# Factor de escalamiento para ajustar con los datos experimentales
scaling_factor = 0.6  # Factor ajustado manualmente para la superposición

# Sección eficaz diferencial
sigma = scaling_factor * seccion_eficaz(E)

# Crear la gráfica para superponer
plt.figure(figsize=(8, 6))
plt.plot(E_MeV, sigma, label=f'Sección eficaz de Rutherford ajustada a θ = {np.degrees(theta):.0f}°', color='red')
plt.xlabel('$E_{^{19}F}$ (MeV)')
plt.ylabel('$d\sigma/d\Omega$ (mb/sr)')
plt.title('Dispersión de Rutherford para $^{19}$F en función de la energía')
plt.grid(True, linestyle="--", linewidth=0.5)
plt.legend()

plt.savefig("Rutherford.pdf",dpi=300.0,bbox_inches="tight")
plt.show()



#%% 

# Datos de la tabla
T9 = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0])
present = np.array([2.75e-5, 1.15e-3, 1.60e-2, 1.12e-1, 4.99e-1, 1.62e+0, 9.32e+0, 3.26e+1, 8.68e+1, 2.00e+2, 4.18e+2, 1.94e+3, 6.11e+3])
harss = np.array([2.75e-5, 1.15e-3, 1.60e-2, 1.12e-1, 4.98e-1, 1.62e+0, 9.19e+0, 3.10e+1, 7.73e+1, 1.60e+2, 2.99e+2, 1.11e+3, 3.25e+3])
hahn = np.array([1.89e-5, 7.91e-4, 1.10e-2, 7.70e-2, 3.43e-1, 1.11e+0, 6.38e+0, 2.23e+1, 6.00e+1, 1.43e+2, 3.17e+2, 1.73e+3, 6.12e+3])
wiescher = np.array([6.14e-6, 2.32e-4, 3.03e-3, 2.05e-2, 9.08e-2, 3.03e-1, 2.04e+0, 9.70e+0, 3.74e+1, 1.21e+2, 3.30e+2, 2.35e+3, 9.77e+3])

# Graficar
plt.figure(figsize=(6,4.5))

# Graficar cada conjunto de datos
plt.plot(T9, present, marker='o', label='J. J. He et al.', color='b')
plt.plot(T9, harss, marker='s', label='Harss et al.', color='g')
plt.plot(T9, hahn, marker='^', label='Hahn et al.', color='r')
plt.plot(T9, wiescher, marker='d', label='Wiescher et al.', color='orange')

# Configurar escala logarítmica en el eje y
plt.yscale('log')

# Etiquetas y título
plt.xlabel('Temperatura (GK)')
plt.ylabel('Tasa de reacción (cm³ s⁻¹ mol⁻¹)')
# Configurar leyenda
plt.legend()

# Mostrar la cuadrícula
plt.grid(True, which="both", ls="--")

plt.savefig("Final.pdf",dpi=300.0,bbox_inches="tight")
# Mostrar el gráfico
plt.show()
