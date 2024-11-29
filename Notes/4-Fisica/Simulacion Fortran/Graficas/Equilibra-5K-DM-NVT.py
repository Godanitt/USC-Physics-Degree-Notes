import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from matplotlib.gridspec import GridSpec

# Función para leer el archivo .dat
def leer_datos(archivo):
    Etot, Ecin, Epot = [], [], []
    
    with open(archivo, 'r') as file:
        for linea in file:
            # Separar los valores basados en 2 espacios
            datos = linea.split('  ')  # Usa split con 2 espacios
            if len(datos) == 3:
                Etot.append(float(datos[0].strip()))
                Ecin.append(float(datos[1].strip()))
                Epot.append(float(datos[2].strip()))
    
    return Etot, Ecin, Epot

# Ejemplo de uso

# Función para graficar los datos
def graficar_datos(Etot, Ecin, Epot):
    gs = GridSpec(2, 3)
    x = range(len(Etot))  # Índices en el eje x
    x=np.array(x)
    x=x*20/10000
    
    E=np.array([Etot,Ecin,Epot])
    nombres=np.array(["Et-equilibra-DM-NVT.pdf","Ecin-equilibra-DM-NVT-500K.pdf","Epot-equilibra-DM-NVT.pdf"])
    limites=np.array([-575.6,-574.95])
    nombre=np.array(["$E_{tot}$","$E_{cin}$","$E_{pot}$"])
    color=np.array(["red","blue","green"])
    
    fig=plt.figure(figsize=(13, 6))
    ax1=fig.add_subplot(gs[:,:-1])
    ax2=fig.add_subplot(gs[0,-1])
    ax3=fig.add_subplot(gs[-1,-1])
    
    
    for i, ax in enumerate(fig.axes):
    # Graficar las energías
        
        ax.plot(x, E[i], label='%s'%nombre[i], color=color[i], marker='.',linewidth=1,markersize=1)    
    # Configuración de la gráfica
        ax.legend()
        ax.grid(True)
        if i==0:
          #  ax.set_ylim(-575.6,-574.95)
            ax.set_ylabel('Energía')
            ax.set_xlabel('Tiempo')
        elif i==2:            
            ax.set_xlabel('Tiempo')
    # Mostrar gráfica
    plt.savefig("Et-equilibra-DM-NVT-500K.pdf",dpi=300.0,bbox_inches="tight")
    
    
    
    

# Ejemplo de uso
archivo = os.path.join('..', 'Datos','Optativo4','Energias-Equilibracion.dat')
Etot, Ecin, Epot = leer_datos(archivo)
graficar_datos(Etot, Ecin, Epot)