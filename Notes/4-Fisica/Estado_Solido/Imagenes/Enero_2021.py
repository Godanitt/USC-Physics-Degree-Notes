# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 12:35:11 2024

@author: danie
"""

import matplotlib.pyplot as plt
import numpy as np

# Configuración del gráfico
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xticks([],[])
ax.set_yticks([],[])
ax.set_aspect('equal', 'box')

# Coordenadas de los puntos exteriores (esquinas del diamante)
diamond_points = np.array([
    [0, 1],   # Arriba
    [1, 0],   # Derecha
    [0, -1],  # Abajo
    [-1, 0],  # Izquierda
    [0, 1]    # Volver al punto inicial
])

# Coordenadas de los puntos azules alrededor
blue_points = np.array([
    [0,0],
    [1, 1],
    [1, -1],
    [-1, -1],
    [-1, 1]
])

# Flechas F1 y F2
F1 = [1, 0]  # Flecha en x positiva
F2 = [0.5, 0.5]  # Flecha diagonal

# Dibujar el diamante en rojo
ax.plot(diamond_points[:, 0], diamond_points[:, 1], 'r-', linewidth=1.5,label="PZB")

# Dibujar los puntos azules

# Dibujar las flechas
ax.quiver(0, 0, F1[0], F1[1], angles='xy', scale_units='xy', scale=1, color='black')#, label=r'$\vec{F_1}$')
ax.quiver(0, 0, F2[0], F2[1], angles='xy', scale_units='xy', scale=1, color='black')#, label=r'$\vec{F_2}$')

# Etiquetas
ax.text(1.6, 0, r"$\hat{x}$", fontsize=12, ha='center')
ax.text(0, 1.6, r"$\hat{y}$", fontsize=12, va='center')
ax.text(1.1, 0.1, r"$k_{\max}^{PZB}$", fontsize=12, color='black')
ax.text(0.6, 0.6, r"$k_{\min}^{PZB}$", fontsize=12, color='black')


ax.scatter(blue_points[:, 0], blue_points[:, 1], color='blue',label="Puntos red recíproca", s=50)
ax.legend()

# Ocultar bordes del gráfico
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

plt.grid(False)
plt.savefig("2021_Enero_03_1.pdf",dpi=300.0,bbox_inches="tight")
plt.show()

#%%

def parabola_from_points(p1, p2):
    """
    Calcula la ecuación de una parábola y = ax^2 + bx + c dado un punto genérico (p1)
    y el vértice de la parábola (p2).

    Parámetros:
        p1: tuple, coordenadas del primer punto (x1, y1).
        p2: tuple, coordenadas del vértice (x2, y2).

    Retorna:
        Una función que representa la parábola y = ax^2 + bx + c.
        También devuelve los coeficientes (a, b, c).
    """
    x1, y1 = p1
    x2, y2 = p2

    # La fórmula para el vértice nos dice que b = -2 * a * x2
    # Usaremos este conocimiento para resolver el sistema de ecuaciones:
    # y1 = a * x1^2 + b * x1 + c
    # y2 = a * x2^2 + b * x2 + c (pero sabemos que b = -2 * a * x2)

    # Resolver el sistema de ecuaciones para encontrar "a" y "c":
    # De y2 = a * x2^2 + b * x2 + c y sabiendo que en el vértice la derivada es 0:
    # y2 = c (en el vértice, la parábola toma su valor máximo o mínimo)
    c = y2

    # Sustituyendo c en la ecuación de y1:
    # y1 = a * x1^2 + b * x1 + c
    # y1 = a * x1^2 + (-2 * a * x2) * x1 + c
    # y1 - c = a * x1^2 - 2 * a * x2 * x1
    # a * (x1^2 - 2 * x2 * x1) = y1 - c
    a = (y1 - c) / (x1**2 - 2 * x2 * x1)

    # Calcular b usando la relación b = -2 * a * x2
    b = -2 * a * x2

    # Retornar la función de la parábola y los coeficientes
    def parabola(x):
        return a * x**2 + b * x + c

    return parabola, (a, b, c)

# Ejemplo de uso:
p1 = (1, 2)
p2 = (0, 1)  # Vértice
parabola, coeficientes = parabola_from_points(p1, p2)
print("Coeficientes de la parábola:", coeficientes)
print("Valor de la parábola en x=2:", parabola(2))

# Crear la gráfica de la nueva imagen
x = np.linspace(0, 2, 500)
y = x**2  # Curva cuadrática como ejemplo de energía

# Puntos específicos (ε1, ε2)
x1, x2 = 0.8, 1.1
y1, y2 = x1**2, x2**2

fig, ax = plt.subplots(figsize=(6, 6))




ax.set_xlim(0, 1.5)
ax.set_ylim(0, 2)
ax.set_xlabel('$k$', fontsize=14)
ax.set_ylabel('$\epsilon$', fontsize=14)

plt.grid(False)
plt.savefig("2021_Enero_03_2.pdf",dpi=300.0,bbox_inches="tight")
plt.show()
