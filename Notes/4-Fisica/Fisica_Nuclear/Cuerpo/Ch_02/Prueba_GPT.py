import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gamma as sp_gamma
import matplotlib.pyplot as plt

def smoothing_function(x, M=6):
    """
    Función de suavizado con corrección de curvatura.
    Se define como:
      f(x) = (1/√π) exp(-x^2) * P_M(x)
    donde P_M(x) es un polinomio de corrección de orden M.
    """
    poly = 0.0
    for k in range(M + 1):
        poly += ((-x**2)**k / np.math.factorial(k)) * (sp_gamma(M + 1.5) / sp_gamma(M - k + 1.5))
    return np.exp(-x**2) / np.sqrt(np.pi) * poly

def smoothed_density(e, levels, gamma, M=6):
    """
    Calcula la densidad de niveles suavizada:
      ˜g(e) = (1/γ) ∑ (2j_i+1) f((e - e_i)/γ)
    """
    density = 0.0
    for energy, degeneracy in levels:
        x = (e - energy) / gamma
        density += degeneracy * smoothing_function(x, M)
    return density / gamma

def particle_number(lambda_val, levels, gamma, M=6):
    """
    Calcula el número de partículas integrando la densidad suavizada desde -∞ hasta lambda_val.
    """
    N, _ = quad(lambda e: smoothed_density(e, levels, gamma, M), -100, lambda_val)
    return N

def smoothed_energy(lambda_val, levels, gamma, M=6):
    """
    Calcula la energía suave ˜E:
      ˜E = ∫ (e * ˜g(e)) de, de -∞ hasta lambda_val.
    """
    E, _ = quad(lambda e: e * smoothed_density(e, levels, gamma, M), -100, lambda_val)
    return E

def shell_correction(levels, N_particles, gamma, M=6):
    """
    Calcula la corrección de capas:
      δE_shell = E_total - ˜E
    donde:
      E_total = suma de energías de los niveles ocupados (incluyendo degeneración)
      ˜E     = energía suave obtenida de la densidad de niveles suavizada.
      
    Retorna:
      delta_E: corrección de capas
      E_total: energía discreta acumulada
      E_tilde: energía suave
      lambda_F: energía de Fermi suavizada (λ̃)
    """
    # Sumar energías de niveles ocupados (considerando degeneración)
    N_accum = 0
    E_total = 0.0
    for energy, degeneracy in levels:
        if N_accum + degeneracy <= N_particles:
            E_total += degeneracy * energy
            N_accum += degeneracy
        else:
            remaining = N_particles - N_accum
            E_total += remaining * energy
            N_accum = N_particles
            break

    # Determinar lambda_F tal que ∫(-∞,lambda_F) ˜g(e) de = N_particles
    lambda_low = min(lvl[0] for lvl in levels) - 10
    lambda_high = max(lvl[0] for lvl in levels) + 10
    lambda_F = brentq(lambda lam: particle_number(lam, levels, gamma, M) - N_particles, lambda_low, lambda_high)
    E_tilde = smoothed_energy(lambda_F, levels, gamma, M)
    delta_E = E_total - E_tilde
    return delta_E, E_total, E_tilde, lambda_F

# Tabla de niveles (energía en MeV, degeneración = 2j+1)
# Se consideran los niveles hasta "3p1/2".
levels_table = [
    (0.0,   2),   # 1s1/2
    (6.2,   4),   # 1p3/2
    (9.8,   2),   # 1p1/2
    (16.2,  6),   # 1d5/2
    (19.8,  2),   # 2s1/2
    (21.4,  4),   # 1d3/2
    (26.4,  8),   # 1f7/2
    (31.8,  4),   # 2p3/2
    (34.4,  6),   # 1f5/2
    (36.6,  2),   # 2p1/2
    (39.2,  10),  # 1g9/2
    (49.8,  8),   # 1g7/2
    (52.2,  6),   # 2d5/2
    (55.2,  4),   # 2d3/2
    (57.6,  2),   # 3s1/2
    (59.6,  12),  # 1h11/2
    (72.2,  10),  # 1h9/2
    (75.0,  8),   # 2f7/2
    (77.8,  6),   # 2f5/2
    (79.6,  4),   # 3p3/2
    (81.6,  2)    # 3p1/2 (última capa)
]

# Parámetros de entrada: número de partículas y gamma (en MeV)
N_example = 50    # Ejemplo: para protones (Z = 50) o neutrones (N = 82)
gamma_val = 1.2   # Parámetro de suavizado en MeV
M_order = 6       # Orden del polinomio de corrección

delta_E, E_total, E_tilde, lambda_F = shell_correction(levels_table, N_example, gamma_val, M_order)

print("Número de partículas =", N_example)
print("E_total (suma discreta) =", E_total, "MeV")
print("E_tilde (energía suave) =", E_tilde, "MeV")
print("Corrección de capas (delta E) =", delta_E, "MeV")
print("Energía de Fermi suavizada =", lambda_F, "MeV")

# Gráfica opcional: densidad de niveles suavizada
e_vals = np.linspace(-20, 100, 500)
density_vals = [smoothed_density(e, levels_table, gamma_val, M_order) for e in e_vals]

plt.plot(e_vals, density_vals, label="Densidad suavizada")
plt.axvline(lambda_F, color='r', linestyle='--', label=f"λ̃ = {lambda_F:.2f} MeV")
plt.xlabel("Energía (MeV)")
plt.ylabel("Densidad de niveles suavizada")
plt.title("Método de Corrección de Strutinsky")
plt.legend()
plt.grid(True)
plt.savefig("densidad_suavizada.png", dpi=300, bbox_inches="tight")
plt.show()
