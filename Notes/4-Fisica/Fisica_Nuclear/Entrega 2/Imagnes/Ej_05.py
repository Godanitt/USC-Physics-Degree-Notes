import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 

# Reimportar librerías tras reinicio

import re

# Ruta del archivo (tras resubida necesaria)
file_path = "MassGod.txt"

# Leer el archivo de texto
with open(file_path, "r") as file:
    lines = file.readlines()

# Lista para almacenar datos
data = []

for line in lines:
    parts = re.split(r"\s+", line.strip())
    #print(parts)
    if len(parts) < 6:
        continue

    try:
        A_code = parts[0]
        if not A_code.isdigit():
            continue
        A = int(A_code) 
        Z_code = parts[1]
        Z_code = Z_code.replace("W", "")  # 
        if not Z_code.isdigit():
            continue
        Z = int(Z_code)//10
        N = A - Z
    

        mass_str = parts[3].replace("#", "")
        mass = float(mass_str) 

        # Buscar vida media o "stbl"
        lifetime = "unknown"
        for i in range(len(parts)):
            if any(unit in parts[i] for unit in ['stbl', 's', 'ms', 'us', 'ns', 'ps', 'm', 'h', 'd', 'y']):
                lifetime = " ".join(parts[i:i+3])
                break

        data.append({
            "Z": Z,
            "N": N,
            "A": A,
            "Exceso_masa_keV": mass,
            "Lifetime": lifetime
        })

    except:
        continue

# Convertir a DataFrame
df = pd.DataFrame(data)
print(df)
# Cargar el archivo CSV directamente, tal como está, sin manipular encabezados ni columnas
#df = pd.read_csv("Ej5.csv")

# Mostrar el DataFrame crudo tal cual
#print(df)


Z = df["Z"].to_numpy()
N = df["N"].to_numpy()
mass = df["Exceso_masa_keV"].to_numpy()
lifetime=df["Lifetime"].to_numpy()

Q=np.zeros((max(Z)+1,max(N)+1))

for i in range(len(Z)):
    #if ('stbl' in lifetime[i] ):
    print("Z",Z[i],"N",N[i])
    try: 
        # Z par, N par        
        Q[Z[i],N[i]]=mass[i]

        #print(mass[i])
        if (Z[i]%2==0 and N[i]%2==0):
            j=0
            while not(Z[i]/2==Z[j] and N[i]/2==N[j]):
                j+=1
                
            Q[Z[i],N[i]]+=-2*mass[j]
            #print(i)
            
        elif (Z[i]%2!=0 and N[i]%2==0):    
            j=0
            while not(Z[i]//2+1==Z[j] and N[i]/2==N[j]):
                j+=1                
            Q[Z[i],N[i]]+=-mass[j]
            j=0
            while not(Z[i]//2==Z[j] and N[i]/2==N[j]):
                j+=1                
            Q[Z[i],N[i]]+=-mass[j]
            
        # Z par, N impar    
        elif (Z[i]%2!=0 and N[i]%2==0):    
            j=0
            while not(Z[i]//2==Z[j] and N[i]//2+1==N[j]):
                j+=1                
            Q[Z[i],N[i]]+=-mass[j]
            j=0
            while not(Z[i]//2==Z[j] and N[i]/2==N[j]):
                j+=1                
            Q[Z[i],N[i]]+=-mass[j]
        # Z impar, N impar    
        else: 
            j=0
            while not(Z[i]//2+1==Z[j] and N[i]//2+1==N[j]):
                j+=1                
            Q[Z[i],N[i]]+=-mass[j]/2
            j=0
            while not(Z[i]//2==Z[j] and N[i]//2==N[j]):
                j+=1                
            Q[Z[i],N[i]]+=-mass[j]/2
            j=0
            while not(Z[i]//2+1==Z[j] and N[i]//2==N[j]):
                j+=1                
            Q[Z[i],N[i]]+=-mass[j]/2
            j=0
            while not(Z[i]//2==Z[j] and N[i]//2+1==N[j]):
                j+=1                
            Q[Z[i],N[i]]+=-mass[j]/2
            
            
            
            
            
    except IndexError:
        continue
        
plt.figure(figsize=(6, 6))
plt.imshow(Q, cmap='hsv')
cbar = plt.colorbar(shrink=0.6)  # reduce la barra al 60% del alto del gráfico
plt.xlabel("N")
plt.ylabel("Z")
plt.gca().invert_yaxis()
plt.title('Mapa de calor de $Q_{gs}$')
plt.tight_layout()
plt.grid()
plt.savefig("Qcolormap_nudat.pdf", dpi=300, bbox_inches='tight')