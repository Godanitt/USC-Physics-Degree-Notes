import numpy as np
import matplotlib.pyplot as plt
import imageio
import os


def plot_orbit(e, a=1):
    theta = np.linspace(0, 2 * np.pi, 1000)
    
    if e < 1:
        r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
    elif e == 1:
        theta = np.linspace(-np.pi / 2, np.pi / 2, 500)
        r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
    else:
        theta = np.linspace(-np.pi, np.pi, 1000)
        r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, label=f'e = {e}')
    plt.scatter([0], [0], color='red', label='Foco')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Órbita para una excentricidad dada")
    plt.legend()
    plt.grid()
    plt.axis('equal')
    plt.savefig(f'frame_{int(e*100)}.png')
    plt.close()
