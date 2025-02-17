import numpy as np
import matplotlib.pyplot as plt

# Definimos las excentricidades
excentricidades = [0, 0.3, 0.6, 0.9, 1, 1.5]

# Crear figura y subgráficos (3 filas, 2 columnas)
fig, axes = plt.subplots(3, 2, figsize=(10, 12))
fig.suptitle('Órbitas en función de la excentricidad', fontsize=16, fontweight='bold')

# Rango de ángulo para órbitas cerradas (elípticas)
theta = np.linspace(0, 2 * np.pi, 500)

# Semieje mayor (normalizado)
a = 1

for ax, e in zip(axes.flat, excentricidades):
    if e < 1:
        # Órbitas elípticas (e < 1) en coordenadas polares
        r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        ax.plot(x, y, label=f'e = {e}', linewidth=2)

    elif e == 1:
        # Órbita parabólica (e = 1) en coordenadas cartesianas
        x_p = np.linspace(-0.2, 2, 500)  # Dominio en x
        y_p = np.sqrt(4 * a * x_p)  # Parábola y^2 = 4ax
        ax.plot(x_p, y_p, label=f'e = {e} (Parábola)', linewidth=2)
        ax.plot(x_p, -y_p, linewidth=2)  # Parte inferior de la parábola

    else:
        # Órbita hiperbólica (e > 1) en coordenadas cartesianas
        u = np.linspace(-2, 2, 500)  # Rango hiperbólico
        x_h = a * (e**2 - 1) / (1 + e * np.cosh(u))
        y_h = a * np.sqrt(e**2 - 1) * np.sinh(u) / (1 + e * np.cosh(u))
        ax.plot(x_h, y_h, label=f'e = {e} (Hipérbola)', linewidth=2)
        ax.plot(x_h, -y_h, linewidth=2)  # Segunda rama de la hipérbola

    # Añadir el Sol en el foco
    ax.plot(0, 0, 'yo', markersize=10, label='Sol')

    # Configuración del gráfico
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')  # Mantener proporción
    ax.legend(loc='upper right', fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

# Ajustar el diseño
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Mostrar la figura
plt.savefig("02-Orbitas.pdf",dpi=300)
