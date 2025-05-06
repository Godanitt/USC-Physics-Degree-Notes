import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def Bandas_Energias(file_path,alphas=1.0):
    # Leer el archivo línea por línea
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Inicializar listas
    datasets = []
    current_data = []

    # Recorrer las líneas del archivo
    for line in lines:
        line = line.strip()
        
        # Detectar el separador entre bloques de datos
        if line.startswith("------------------------------------------------------------"):
            if current_data:  # Si ya hay datos, guardar en la lista de datasets
                datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Energy (eV)"]))
                current_data = []
            continue  # Saltar esta línea

        # Intentar leer los datos (evitando la cabecera)
        if line and not line.startswith("Position"):
            try:
                pos, energy = map(float, line.split(","))
                current_data.append([pos, energy])
            except ValueError:
                continue  # En caso de que haya líneas no numéricas

    # Guardar el último bloque de datos si hay alguno
    if current_data:
        datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Energy (eV)"]))

    # Mostrar el número de conjuntos extraídos
 #   print(f"Se encontraron {len(datasets)} conjuntos de datos.")
    # Mostrar el primer conjunto de datos
    labels=["$E_{F0}$","$E_{i0}$","$E_{c0}$","$E_{v0}$","nose","nose","nose"]
    labels2=["$E_{Fn}$","$E_{Fp}$","$E_i$","$E_c$","$E_v$","nose","nose","nose"]
    colors=["black","green","red","blue","white","white"]
    colors2=["purple","black","green","red","blue","white","white"]
  
    if alphas>0.99:
        m=2
        labels=labels2
        colors=colors2
    else:      
        m=3    
        
    for i in range(len(datasets)-m):
        #print(datasets[i].head())  # Imprime los primeros valores del primer bloque
        j=i+m
        x = datasets[j]
        if i==0:
           x = datasets[j-2]  # Selecciona el primer conjunto de datos

        posiciones = x["Position (um)"].values
        energias = x["Energy (eV)"].values

       # print(posiciones)  # Imprime el array de posiciones
       # print(energias)    # Imprime el array de energías

        plt.plot(posiciones-10, energias,color=colors[i], linestyle='-',alpha=alphas,label=labels[i])#markeredgecolor="black",markeredgewidth=0.05, 
        
    plt.xlabel("x ($\\mu$m)")
    plt.ylabel("E (eV)")
    plt.grid(linestyle="--")
    

def Campo_Electrico(file_path,color2,Va=0):
    # Leer el archivo línea por línea
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Inicializar listas
    datasets = []
    current_data = []

    # Recorrer las líneas del archivo
    for line in lines:
        line = line.strip()
        
        # Detectar el separador entre bloques de datos
        if line.startswith("------------------------------------------------------------"):
            if current_data:  # Si ya hay datos, guardar en la lista de datasets
                datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Electric field (V/cm)"]))
                current_data = []
            continue  # Saltar esta línea

        # Intentar leer los datos (evitando la cabecera)
        if line and not line.startswith("Position"):
            try:
                pos, energy = map(float, line.split(","))
                current_data.append([pos, energy])
            except ValueError:
                continue  # En caso de que haya líneas no numéricas

    # Guardar el último bloque de datos si hay alguno
    if current_data:
        datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Electric field (V/cm)"]))

    # Mostrar el número de conjuntos extraídos
    print(f"Se encontraron {len(datasets)} conjuntos de datos.")
    # Mostrar el primer conjunto de datos
    labels=["$V_A=%.2f$"%Va,"nose","nose","nose","nose"]
        
    for i in [0]:
        #print(datasets[i].head())  # Imprime los primeros valores del primer bloque
        x = datasets[i]

        posiciones = x["Position (um)"].values
        energias = x["Electric field (V/cm)"].values

       # print(posiciones)  # Imprime el array de posiciones
       # print(energias)    # Imprime el array de energías

        linestyles="-"
        if (Va==0.0):
            linestyles="--"
        plt.plot(posiciones-10, energias,color=color2, linestyle=linestyles,label=labels[i])#markeredgecolor="black",markeredgewidth=0.05, 
        
    plt.xlabel("x ($\\mu$m)")
    plt.ylabel("$\\mathcal{E}$ (V/cm)")
    plt.grid(linestyle="--")
    

def Potencial_Electrico(file_path,color2,Va=0):
    # Leer el archivo línea por línea
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Inicializar listas
    datasets = []
    current_data = []

    # Recorrer las líneas del archivo
    for line in lines:
        line = line.strip()
        
        # Detectar el separador entre bloques de datos
        if line.startswith("------------------------------------------------------------"):
            if current_data:  # Si ya hay datos, guardar en la lista de datasets
                datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Potential (V)"]))
                current_data = []
            continue  # Saltar esta línea

        # Intentar leer los datos (evitando la cabecera)
        if line and not line.startswith("Position"):
            try:
                pos, energy = map(float, line.split(","))
                current_data.append([pos, energy])
            except ValueError:
                continue  # En caso de que haya líneas no numéricas

    # Guardar el último bloque de datos si hay alguno
    if current_data:
        datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Potential (V)"]))

    # Mostrar el número de conjuntos extraídos
    print(f"Se encontraron {len(datasets)} conjuntos de datos.")
    # Mostrar el primer conjunto de datos
    labels=["$V_A=%.2f$"%Va,"nose","nose","nose","nose"]
        
    for i in [0]:
        #print(datasets[i].head())  # Imprime los primeros valores del primer bloque
        x = datasets[i]

        posiciones = x["Position (um)"].values
        energias = x["Potential (V)"].values

       # print(posiciones)  # Imprime el array de posiciones
       # print(energias)    # Imprime el array de energías
        linestyles="-"
        if (Va==0.0):
            linestyles="--"
        plt.plot(posiciones-10, energias,color=color2, linestyle=linestyles,label=labels[i])#markeredgecolor="black",markeredgewidth=0.05, 
        
    plt.xlabel("x ($\\mu$m)")
    plt.ylabel("V (V/cm)")
    plt.grid(linestyle="--")
    
def Densidad_carga(file_path,color2,Va=0):
    # Leer el archivo línea por línea
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Inicializar listas
    datasets = []
    current_data = []

    # Recorrer las líneas del archivo
    for line in lines:
        line = line.strip()
        
        # Detectar el separador entre bloques de datos
        if line.startswith("------------------------------------------------------------"):
            if current_data:  # Si ya hay datos, guardar en la lista de datasets
                datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Potential (V)"]))
                current_data = []
            continue  # Saltar esta línea

        # Intentar leer los datos (evitando la cabecera)
        if line and not line.startswith("Position"):
            try:
                pos, energy = map(float, line.split(","))
                current_data.append([pos, energy])
            except ValueError:
                continue  # En caso de que haya líneas no numéricas

    # Guardar el último bloque de datos si hay alguno
    if current_data:
        datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Potential (V)"]))

    # Mostrar el número de conjuntos extraídos
    print(f"Se encontraron {len(datasets)} conjuntos de datos.")
    # Mostrar el primer conjunto de datos
    labels=["$V_A=%.2f$"%Va,"nose","nose","nose","nose"]
        
    for i in [0]:
        #print(datasets[i].head())  # Imprime los primeros valores del primer bloque
        x = datasets[i]

        posiciones = x["Position (um)"].values
        energias = x["Potential (V)"].values

       # print(posiciones)  # Imprime el array de posiciones
       # print(energias)    # Imprime el array de energías

        linestyles="-"
        if (Va==0.0):
            linestyles="--"
        plt.plot(posiciones-10, energias,color=color2, linestyle=linestyles,label=labels[i])#markeredgecolor="black",markeredgewidth=0.05, 
        
    plt.xlabel("x ($\\mu$m)")
    plt.ylabel("$\\rho$ (V/cm)")
    plt.grid(linestyle="--")
    
def Portadores(file_path,color2,Va=0):
    # Leer el archivo línea por línea
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Inicializar listas
    datasets = []
    current_data = []

    # Recorrer las líneas del archivo
    for line in lines:
        line = line.strip()
        
        # Detectar el separador entre bloques de datos
        if line.startswith("------------------------------------------------------------"):
            if current_data:  # Si ya hay datos, guardar en la lista de datasets
                datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Potential (V)"]))
                current_data = []
            continue  # Saltar esta línea

        # Intentar leer los datos (evitando la cabecera)
        if line and not line.startswith("Position"):
            try:
                pos, energy = map(float, line.split(","))
                current_data.append([pos, energy])
            except ValueError:
                continue  # En caso de que haya líneas no numéricas

    # Guardar el último bloque de datos si hay alguno
    if current_data:
        datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Potential (V)"]))

    # Mostrar el número de conjuntos extraídos
    print(f"Se encontraron {len(datasets)} conjuntos de datos.")
    # Mostrar el primer conjunto de datos
    labels=["n","p","Dopado","nose","nose"]
    colors=["blue","red","green"]
        
    for i in [0,1,2]:
        #print(datasets[i].head())  # Imprime los primeros valores del primer bloque
        x = datasets[i]

        posiciones = x["Position (um)"].values
        energias = x["Potential (V)"].values

       # print(posiciones)  # Imprime el array de posiciones
       # print(energias)    # Imprime el array de energías

        plt.plot(posiciones-10, energias,color=colors[i], linestyle='-',label=labels[i])#markeredgecolor="black",markeredgewidth=0.05, 
        
    plt.xlabel("x ($\\mu$m)")
    plt.ylabel("Densidad (cm$^{-3}$)")
    plt.grid(linestyle="--")
    plt.yscale("log")
    
def Intensidad(file_path,color2,Va=0):
    # Leer el archivo línea por línea
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Inicializar listas
    datasets = []
    current_data = []

    # Recorrer las líneas del archivo
    for line in lines:
        line = line.strip()
        
        # Detectar el separador entre bloques de datos
        if line.startswith("------------------------------------------------------------"):
            if current_data:  # Si ya hay datos, guardar en la lista de datasets
                datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Potential (V)"]))
                current_data = []
            continue  # Saltar esta línea

        # Intentar leer los datos (evitando la cabecera)
        if line and not line.startswith("Position"):
            try:
                pos, energy = map(float, line.split(","))
                current_data.append([pos, energy])
            except ValueError:
                continue  # En caso de que haya líneas no numéricas

    # Guardar el último bloque de datos si hay alguno
    if current_data:
        datasets.append(pd.DataFrame(current_data, columns=["Position (um)", "Potential (V)"]))

    # Mostrar el número de conjuntos extraídos
    print(f"Se encontraron {len(datasets)} conjuntos de datos.")
    # Mostrar el primer conjunto de datos
  #  labels=["$V_A=%.2f$"%Va,"nose","nose","nose","nose"]
        
    for i in [0]:
        #print(datasets[i].head())  # Imprime los primeros valores del primer bloque
        x = datasets[i]

        posiciones = x["Position (um)"].values
        energias = x["Potential (V)"].values

       # print(posiciones)  # Imprime el array de posiciones
       # print(energias)    # Imprime el array de energías

        plt.plot(posiciones, energias,color=color2, linestyle='-')#markeredgecolor="black",markeredgewidth=0.05, 
        
    plt.ylabel("I (A/cm$^{2}$)")
    plt.xlabel("$V_A$ (V)")
    plt.grid(linestyle="--")
    
nombrespdfs=["Bandas_Energia-Directa.pdf","Campo_Electrico-Directa.pdf","Potencial_Electrico-Directa.pdf","Densidad_Carga-Directa.pdf","Bandas_Minoritarios-Directa.pdf","Intensidades-Directa.pdf"]    
    
    
nombrespdfs2=["Bandas_Energia-Inversa.pdf","Campo_Electrico-Inversa.pdf","Potencial_Electrico-Inversa.pdf","Densidad_Carga-Inversa.pdf","Bandas_Minoritarios-Inversa.pdf","Intensidades-Inversa.pdf"]    

# Nombre del archivo de texto
file_path = "Simetrica_Equilibrio/EnergyBandDiagramatequilibrium.txt"
file_path2 = "Simetrica_0-25/EnergyBandDiagramatappliedbias2.txt"

plt.figure()
plt.tight_layout()
Bandas_Energias(file_path,0.5)
Bandas_Energias(file_path2,1.0)
plt.title("Bandas de Energía Simétrica Simulación")
plt.legend()
plt.savefig(nombrespdfs[0], bbox_inches='tight')

# Nombre del archivo de texto
file_path = "No_Simetrica/EnergyBandDiagramatequilibrium.txt"
file_path2 = "No_Simetrica_0-2/EnergyBandDiagramatappliedbias.txt"

plt.figure()
plt.tight_layout()
Bandas_Energias(file_path,0.5)
Bandas_Energias(file_path2,1.0)
plt.title("Bandas de Energía no Simétrica Simulación")
plt.legend()
plt.savefig(nombrespdfs2[0], bbox_inches='tight')

# Campo eléctrico

file_path = "Simetrica_Equilibrio/ElectricFieldatequilibrium.txt"
file_path2 = "Simetrica_0-25/ElectricFieldatappliedbias.txt"

plt.figure()
plt.tight_layout()
Campo_Electrico(file_path,"red",0.0)
Campo_Electrico(file_path2,"blue",0.25)
plt.title("Campo eléctrico union Simétrica Simulación")
plt.legend()
plt.xlim(-0.2,0.3)    
plt.savefig(nombrespdfs[1], bbox_inches='tight')

# Nombre del archivo de texto
file_path = "No_Simetrica/ElectricFieldatequilibrium.txt"
file_path2 = "No_Simetrica_0-2/ElectricFieldatappliedbias.txt"

plt.figure()
plt.tight_layout()
Campo_Electrico(file_path,"red",0.0)
Campo_Electrico(file_path2,"blue",-0.2)
plt.title("Campo eléctrico union no Simétrica Simulación")
plt.legend()
plt.xlim(-0.2,0.3)  
plt.savefig(nombrespdfs2[1], bbox_inches='tight')

# Potencial eléctrico

file_path = "Simetrica_Equilibrio/ElectrostaticPotentialatequilibrium.txt"
file_path2 = "Simetrica_0-25/ElectrostaticPotentialatappliedbias3.txt"

plt.figure()
plt.tight_layout()
Potencial_Electrico(file_path,"red",0.0)
Potencial_Electrico(file_path2,"blue",0.25)
plt.title("Potencial eléctrico union Simétrica Simulación")
plt.legend()
plt.xlim(-0.2,0.3)    
plt.savefig(nombrespdfs[2], bbox_inches='tight')

# Nombre del archivo de texto
file_path = "No_Simetrica/ElectrostaticPotentialatequilibrium.txt"
file_path2 = "No_Simetrica_0-2/ElectrostaticPotentialatappliedbias.txt"

plt.figure()
plt.tight_layout()
Potencial_Electrico(file_path,"red",0.0)
Potencial_Electrico(file_path2,"blue",-0.2)
plt.title("Potencial union no Simétrica Simulación")
plt.legend()
plt.xlim(-0.2,0.3)  
plt.savefig(nombrespdfs2[2], bbox_inches='tight')

#  Densidad carga

file_path = "Simetrica_Equilibrio/NetChargeDensityatequilibrium.txt"
file_path2 = "Simetrica_0-25/NetChargeDensityatappliedbias.txt"

plt.figure()
plt.tight_layout()
Densidad_carga(file_path,"red",0.0)
Densidad_carga(file_path2,"blue",0.25)
plt.title("Densidad de carga union Simétrica Simulación")
plt.legend()
plt.xlim(-0.3,0.3)    
plt.savefig(nombrespdfs[3], bbox_inches='tight')

# Nombre del archivo de texto
file_path = "No_Simetrica/NetChargeDensityatequilibrium.txt"
file_path2 = "No_Simetrica_0-2/NetChargeDensityatappliedbias.txt"

plt.figure()
plt.tight_layout()
Densidad_carga(file_path,"red",0.0)
Densidad_carga(file_path2,"blue",-0.2)
plt.title("Densidad de carga no Simétrica Simulación")
plt.legend()
plt.xlim(-0.3,0.3)  
plt.savefig(nombrespdfs2[3], bbox_inches='tight')

#  Densidad portadores

file_path2 = "Simetrica_0-25/DopingElectronandHoleDensityatappliedbias.txt"

plt.figure()
plt.tight_layout()
Portadores(file_path2,"blue",0.25)
plt.title("Densidad de portadores union Simétrica Simulación")
plt.legend()
plt.xlim(-10,10)    
plt.ylim(10**3,10**18)
plt.savefig(nombrespdfs[4], bbox_inches='tight')

# Nombre del archivo de texto
file_path2 = "No_Simetrica_0-2/DopingElectronandHoleDensityatappliedbias.txt"

plt.figure()
plt.tight_layout()
Portadores(file_path2,"blue",-0.2)
plt.title("Densidad de portadores no Simétrica Simulación")
plt.legend()
plt.xlim(-10,10)  
plt.ylim(0.1,10**18)
plt.savefig(nombrespdfs2[4], bbox_inches='tight')

#  Intensidad

file_path2 = "Simetrica_Equilibrio/IVCharacteristics.txt"
plt.figure()
plt.tight_layout()
Intensidad(file_path2,"blue",0.25)
plt.title("Relacion IV union Simétrica Simulación")
#plt.legend()
#plt.xlim(-10,10)    
#plt.ylim(10**3,10**18)
plt.savefig(nombrespdfs[5], bbox_inches='tight')

# Nombre del archivo de texto
file_path2 =  "No_Simetrica/IVCharacteristics.txt"

plt.figure()
plt.tight_layout()
Intensidad(file_path2,"blue",-0.2)
plt.title("Relacion IV no Simétrica Simulación")
#plt.legend()
#plt.xlim(-10,10)  
#plt.ylim(1,10**18)
plt.savefig(nombrespdfs2[5], bbox_inches='tight')

#  Densidad portadores (cortado)

file_path2 = "Simetrica_0-25/DopingElectronandHoleDensityatappliedbias.txt"

plt.figure()
plt.tight_layout()
Portadores(file_path2,"blue",0.25)
plt.title("Densidad de portadores union Simétrica Simulación")
plt.legend()
plt.xlim(-0.5,0.5) 
plt.ylim(10**3,10**18)
plt.savefig("Densidad_portadores_directa_cortada.pdf", bbox_inches='tight')

# Nombre del archivo de texto
file_path2 = "No_Simetrica_0-2/DopingElectronandHoleDensityatappliedbias.txt"

plt.figure()
plt.tight_layout()
Portadores(file_path2,"blue",-0.2)
plt.title("Densidad de portadores no Simétrica Simulación")
plt.legend()
plt.xlim(-0.5,0.5)  
plt.ylim(0.1,10**18)
plt.savefig("Densidad_portadores_inversa_cortada.pdf", bbox_inches='tight')