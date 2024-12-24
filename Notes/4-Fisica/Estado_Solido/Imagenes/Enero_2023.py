# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 18:26:20 2024

@author: danie
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import plotly.graph_objects as go



# Función para generar una red FCC
def generate_fcc_lattice(a, n_cells):
    """
    Genera una red cúbica centrada en las caras (FCC).
    Args:
        a: Parámetro de red (distancia entre átomos).
        n_cells: Número de celdas unitarias en cada dirección.
    Returns:
        coords: Coordenadas de los átomos en la red FCC.
    """
    # Posiciones relativas dentro de una celda FCC
    fcc_basis = np.array([
        [0, 0, 0],
        [0.5, 0.5, 0],
        [0.5, 0, 0.5],
        [0, 0.5, 0.5]
    ])
    
    fcc_basis2 = np.array([
        [0.5, 0, 0],
        [0, 0.5, 0],
        [0, 0, 0.5],
        [0.5, 0.5, 0.5]
    ])
    
    coords = []
    coords2 = []
    for i in range(n_cells):
        for j in range(n_cells):
            for k in range(n_cells):
                for basis in fcc_basis:
                    if not(i+basis[0]>1.0 or j+basis[1]>1.0 or k+basis[2]>1.0):
                        coords.append((np.array([i, j, k]) + basis) * a)
                for basis2 in fcc_basis2:
                    if not(i+basis2[0]>1.0 or j+basis2[1]>1.0 or k+basis2[2]>1.0):
                        coords2.append((np.array([i, j, k]) + basis2) * a)
    return np.array(coords),np.array(coords2)


def crear_cubo(x0, y0, z0, lado):
    return [
        (x0, y0, z0),  # Vértice 0
        (x0 + lado, y0, z0),  # Vértice 1
        (x0, y0 + lado, z0),  # Vértice 2
        (x0, y0, z0 + lado),  # Vértice 3
        (x0 + lado, y0 + lado, z0),  # Vértice 4
        (x0 + lado, y0, z0 + lado),  # Vértice 5
        (x0, y0 + lado, z0 + lado),  # Vértice 6
        (x0 + lado, y0 + lado, z0 + lado)  # Vértice 7
    ]


# Parámetros de la red FCC
a = 1.0  # Parámetro de red (en unidades arbitrarias)
n_cells = 3  # Número de celdas unitarias

# Generar las coordenadas
fcc_coords,fcc_coords2 = generate_fcc_lattice(a, n_cells)


# Graficar la red FCC
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
azul_clarito = (0.85, 0.85, 1)  # Equivalente al color definido en LaTeX
fig.patch.set_facecolor(azul_clarito)  # Fondo de la figura
ax.set_facecolor(azul_clarito)        # Fondo de los ejes



# Dibujamos las líneas

# Crear los 8 mini cubos
lado = 0.5
mini_cubos = [
    crear_cubo(0, 0, 0, lado),       # Cubo 1 (octante inferior-frontal-izquierdo)
    crear_cubo(0.5, 0, 0, lado),    # Cubo 2 (octante inferior-frontal-derecho)
    crear_cubo(0, 0.5, 0, lado),    # Cubo 3 (octante inferior-trasero-izquierdo)
    crear_cubo(0.5, 0.5, 0, lado),  # Cubo 4 (octante inferior-trasero-derecho)
    crear_cubo(0, 0, 0.5, lado),    # Cubo 5 (octante superior-frontal-izquierdo)
    crear_cubo(0.5, 0, 0.5, lado),  # Cubo 6 (octante superior-frontal-derecho)
    crear_cubo(0, 0.5, 0.5, lado),  # Cubo 7 (octante superior-trasero-izquierdo)
    crear_cubo(0.5, 0.5, 0.5, lado) # Cubo 8 (octante superior-trasero-derecho)
]

# Conexiones entre los vértices (aristas de un cubo)
aristas = [
    (0, 1), (0, 2), (0, 3),  # Conexiones desde el vértice 0
    (1, 4), (1, 5),          # Conexiones desde el vértice 1
    (2, 4), (2, 6),          # Conexiones desde el vértice 2
    (3, 5), (3, 6),          # Conexiones desde el vértice 3
    (4, 7),                  # Conexiones desde el vértice 4
    (5, 7),                  # Conexiones desde el vértice 5
    (6, 7)                   # Conexión desde el vértice 6
]


# Dibujar cada mini cubo
for cubo in mini_cubos:
    # Separar coordenadas X, Y, Z
    x = [v[0] for v in cubo]
    y = [v[1] for v in cubo]
    z = [v[2] for v in cubo]
    
    # Dibujar las aristas del cubo
    for arista in aristas:
        p1, p2 = arista
        ax.plot(
            [x[p1], x[p2]],
            [y[p1], y[p2]],
            [z[p1], z[p2]],
            color='k'
        )

# Dibujar átomos
ax.scatter(fcc_coords[:, 0], fcc_coords[:, 1], fcc_coords[:, 2], c='blue',alpha=1.0, s=1000)

ax.scatter(fcc_coords2[:, 0], fcc_coords2[:, 1], fcc_coords2[:, 2], c='orange',alpha=1.0,  s=1000)


# Opciones de gráfica
ax.set_xlabel('X (Å)')
ax.set_ylabel('Y (Å)')
ax.set_zlabel('Z (Å)')
#ax.set_title('Red FCC')

# Ajustar límites
ax.set_xlim(0, n_cells * a)
ax.set_ylim(0, n_cells * a)
ax.set_zlim(0, n_cells * a)

ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_zlim(0,2)

ax.view_init(elev=6.5, azim=12)


plt.savefig("2023-Enero-01.pdf",dpi=300.0,bbox_inches="tight")
plt.show()
