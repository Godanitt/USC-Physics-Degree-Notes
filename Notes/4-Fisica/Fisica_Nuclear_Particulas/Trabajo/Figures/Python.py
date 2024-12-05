# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:11:24 2024

@author: danie
"""

import numpy as np
import matplotlib.pyplot as plt

# Definimos las constantes
Z1 = 2  # Número atómico de la partícula incidente (por ejemplo, alfa)
Z2 = 7  # Número atómico del núcleo objetivo (por ejemplo, oro)
e = 1.602e-19  # Carga elemental (C)

# Constante de permitividad del vacío
epsilon_0 = 8.854e-12  # F/m

# Ángulo fijo (por ejemplo, 90 grados en radianes)
theta1 = np.radians(90)
theta2 = np.radians(45)
theta3 = np.radians(30)

# Expresión de la sección eficaz diferencial de Rutherford
def seccion_eficaz(E,theta):
    numerador = (Z1 * Z2 * e**2 / (4 * np.pi * epsilon_0))**2
    denominador = (4 * E * np.sin(theta / 2)**4)
    return numerador / denominador

# Energías en MeV (convertidas a Joules)
E_MeV = np.linspace(0.0, 10, 1000)  # Energías entre 1 MeV y 10 MeV
E = E_MeV * 1e6 * e  # Conversión a Joules

# Sección eficaz diferencial
sigma1 = seccion_eficaz(E,theta1)
sigma2 = seccion_eficaz(E,theta2)
sigma3 = seccion_eficaz(E,theta3)

# Crear la gráfica
plt.figure(figsize=(6, 4.5))
plt.plot(E_MeV, sigma1*10**34, label=f'Sección eficaz a \u03B8 = {np.degrees(theta1):.0f}°',color="blue")
plt.plot(E_MeV, sigma2*10**34, label=f'Sección eficaz a \u03B8 = {np.degrees(theta2):.0f}°',color="red")
plt.plot(E_MeV, sigma3*10**34, label=f'Sección eficaz a \u03B8 = {np.degrees(theta3):.0f}°',color="green")
plt.yscale('log')  # Escala logarítmica para una mejor visualización
plt.xlabel('Energía cinética (MeV)')
plt.ylabel('Sección eficaz diferencial (b/$\mu$sr)')
#plt.title('Sección eficaz de Rutherford en función de la energía')
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.savefig("Rutherford.pdf",dpi=300.0,bbox_inches="tight")
plt.show()

#%%

# Definimos las constantes para la dispersión 14N(p,p)14N
Z1 = 1  # Número atómico del protón incidente
Z2 = 7  # Número atómico del núcleo objetivo (nitrógeno)
e = 1.602e-19  # Carga elemental (C)

# Constante de permitividad del vacío
epsilon_0 = 8.854e-12  # F/m

# Ángulo fijo (por ejemplo, 90 grados en radianes)
theta = np.radians(180)

# Función para la sección eficaz diferencial de Rutherford con resonancia
def seccion_eficaz_con_resonancia(E):
    # Parámetros de la resonancia
    E_resonancia = 1.06e6 * e  # Energía de la resonancia en Joules
    gamma =  e *((6.62607*10**(-34))/(2*np.pi))/10**(-15) # Ancho de la resonancia en Joules
    factor_resonancia = 1 + (gamma**2 / ((E - E_resonancia)**2 + gamma**2))

    # Parte de Rutherford
    numerador = (Z1 * Z2 * e**2 / (4 * np.pi * epsilon_0))**2
    denominador = (4 * E * np.sin(theta / 2)**4)
    rutherford = numerador / denominador

    return rutherford * factor_resonancia

# Energías en MeV (convertidas a Joules)
E_MeV = np.linspace(0.5, 1.1, 10000)  # Energías entre 0.5 MeV y 2 MeV
E = E_MeV * 1e6 * e  # Conversión a Joules

# Sección eficaz diferencial con resonancia
sigma = seccion_eficaz_con_resonancia(E)

# Crear la gráfica
plt.figure(figsize=(8, 6))
plt.plot(E_MeV, sigma*10**30, label=f'Sección eficaz con resonancia a \u03B8 = {np.degrees(theta):.0f}°')
plt.yscale('log')  # Escala logarítmica para una mejor visualización
plt.xlabel('Energía cinética (MeV)')
plt.ylabel('Sección eficaz diferencial (mb/sr)')
plt.title('Dispersión de Rutherford en función de la energía\n14N(p,p)14N con resonancia')
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.show()

#%%

# Definimos las constantes para la dispersión de Rutherford para 19F
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
E_MeV = np.linspace(8.5, 10.5, 1000)  # Energías entre 8.5 MeV y 10.5 MeV
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
