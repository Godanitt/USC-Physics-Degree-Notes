import numpy as np
import matplotlib.pyplot as plt 
import numpy as np
from scipy.special import erf
import pandas as pd 



def generar_tabla_latex(nombres_columnas, *arrays, nombre_archivo="tabla.tex"):
    """
    Genera una tabla en formato LaTeX a partir de arrays usando pandas.

    Parámetros:
        nombres_columnas (list): Lista con los nombres de las columnas.
        *arrays (list): Listas o arrays con los datos de cada columna.
        nombre_archivo (str): Nombre del archivo donde se guardará la tabla (por defecto "tabla.tex").
    
    Retorna:
        str: Código LaTeX de la tabla.
    """
    # Verificar que todos los arrays tienen la misma longitud
    longitud = len(arrays[0])
    if not all(len(arr) == longitud for arr in arrays):
        raise ValueError("Todos los arrays deben tener la misma longitud")

    # Crear DataFrame
    df = pd.DataFrame({nombre: arr for nombre, arr in zip(nombres_columnas, arrays)})

    # Generar código LaTeX
    tabla_latex = df.to_latex(index=False, caption="Tabla generada con Python y pandas", label="tab:datos")

    # Guardar en un archivo
    with open(nombre_archivo, "w") as f:
        f.write(tabla_latex)

    return tabla_latex

# Creación de nuestro colocador de bandas, para dados N y Z nos diga cuales son sus bandas

Energias=np.array([0,6.2,9.8,16.2,19.8,21.4,26.4,31.8,34.4,36.6,39.2,49.8,52.2,55.2,57.6,59.6,72.2,75.0,77.8,79.6,81.6])
Degeneracion=np.array([2,4,2,6,2,4,8,4,6,2,10,8,6,4,2,12,10,8,6,4,2])
Nombre=["1s1/2  [0MeV]","1p3/2 [6.2MeV]","1p1/2 [9.8MeV]","1d5/2 [16.2MeV]",    "2s1/2 [19.8MeV]",  "1d3/2 [21.4MeV]",    "1f7/2 [26.4MeV]", 
        "2p3/2 [31.8MeV]",   "1f5/2 [34.4MeV]",    "2p1/2 [36.6MeV]",   "1g9/2 [39.2MeV]",    "1g7/2 [49.8 MeV]", 
        "2d5/2 [52.2MeV]",    "2d3/2 [55.2MeV]",    "3s1/2 [57.6MeV]",    "1h11/2 [59.6MeV]",    "1h9/2 [72.2MeV]",  
        "2f7/2 [75.0MeV]",    "2f5/2[77.8MeV]",     "3p3/2 [79.6MeV]",    "3p1/2 [81.6 MeV]"]



def Crea_Bandas(Z,N):
    sumando=0
    aux2=0
    aux3=0
    plt.figure(figsize=(7,7))
    i=0
    flag=True

    while (i<len(Energias) and flag):   
        if (Z<sum(Degeneracion[0:i+1])):
            aux2=Z-sum(Degeneracion[0:i])+Degeneracion[i]
            flag=False
            
        entero_aux=Degeneracion[i]
        
        aux01=np.array((entero_aux-aux2)*[Energias[i]])
        
        minimo=1+(12-Degeneracion[i])*(4/24)
        maximo=5-(12-Degeneracion[i])*(4/24)

        
        plt.scatter(np.linspace(minimo,maximo,Degeneracion[i]-aux2),aux01,color="blue",marker="x")
        i+=1
    flag=True    
    i=0
    while (i<len(Energias) and flag):   
        if (N<sum(Degeneracion[0:i+1])):
            aux3=N-sum(Degeneracion[0:i])+Degeneracion[i]
            flag=False
            
        entero_aux=Degeneracion[i]
        aux02=np.array((entero_aux-aux3)*[Energias[i]])
        
        minimo=1+(12-Degeneracion[i])*(4/24)
        maximo=5-(12-Degeneracion[i])*(4/24)

        plt.scatter(np.linspace(5+minimo,5+maximo,Degeneracion[i]-aux3),aux02,color="red",marker="x",)

        i+=1
        
    plt.ylabel("E [MeV]")
    plt.xticks([3,8],["Protones","Neutrones"])
    plt.yticks(Energias,Nombre)
    plt.ylim(-10,max(Energias))
    plt.ylim(-10,max(Energias))
    plt.title("N=%i Z=%d  "%(N,Z))
    plt.savefig("N%s_Z%s_Bandas.pdf"%(N,Z), bbox_inches='tight')
    
Crea_Bandas(50,82)
Crea_Bandas(40,68)    

# Funcinoes auxiliares para resolver el ejercicio. Contienen la exponencial y el interior de la exponencial:
def f(x,gamma,Ei):
    return (x-Ei)/(gamma) 
def g(E,Ei,gamma):
    return (np.exp(-(f(E,gamma,Ei))**2))/(np.sqrt(np.pi)*gamma)

# Array de energías
E=np.linspace(-12,93,50000)
plt.figure()

# Función que guarda una gráfica y nos dice cual es lambda shift (energía de Fermi modificada)
# Para esto lo que vamos a hacer es sumar las áreas hasta que llege a un valor buscado

from scipy.integrate import simpson

def ge(gamma,Area):
    y=np.zeros(len(E), dtype=float)
    z=np.zeros(len(E), dtype=float)
    
    # Aquí estamos dando valor g(E)

    for i in range(len(Degeneracion)):
        z+=g(E,Energias[i],gamma)*Degeneracion[i]
            
    if Area<42:
        plt.plot(E,z,label="$\gamma=%.2f $"%gamma)
        plt.legend()
        plt.xlabel("E [MeV]")
        plt.ylabel("g(E)")
    suma=0
    flag=True
  #  h = E[1]-E[0]
    j=int(2300*(len(E)/5000))
    while(flag):
        suma += simpson(z[:j],E[:j]) 
      #  suma += (h / 2) * (z[0] + 2 * np.sum(z[1:j-1]) + z[j-1])
        if (suma>Area):
            flag=False
        else:
            j+=1
            suma=0
   # print(j)        
    return E[j]
# Gamma que queremos probar, en las areas ponemos Z y N     
    
gamma=np.array([0.8,1,1.3,1.8,2,3])
Area=np.array([50,82,40,68])

energia=np.zeros((len(gamma),len(Area)))

for k in range(len(Area)):
    for i in range(len(gamma)):
        energia[i,k]=ge(gamma[i],Area[k])
        
print(gamma,energia[:,1])
print(gamma,energia[:,2])
print(gamma,energia[:,3])

generar_tabla_latex(["$\\gamma$","Z=50","N=82","Z=40","N=60"],gamma,energia[:,0],
                    energia[:,1],energia[:,2],energia[:,3],nombre_archivo="lambda.tex")


        
plt.savefig("ge.pdf")
        
    # # Valores de lambda shift:
print(energia)    

# En Eshell las no modificadas, en Eshell2 las modificadas por las gaussianas
Eshell=np.zeros((len(Area)))
Eshell2=np.zeros((len(gamma),len(Area)))

# Calculamos las energías no modificadas
# Esto lo podemos hacer así solo porque las capas están llenas:

gamma=[0.8,1,1.3,1.8,2,3]
Area=[50,82,40,68]
E=np.linspace(-12,93,50000)
print("E",E)    
for i in range(len(Area)):
    flag=True
    j=1
    while(flag):
        if (Area[i]==sum(Degeneracion[:j])):
            flag=False
        else:
            j+=1
    Eshell[i]=np.dot(Energias[:j],Degeneracion[:j]) 
    #Eshell[i]=sum(Energias[:j]) 
    
for i in range(len(Area)):
    for j in range(len(gamma)):
        E=np.linspace(-10,energia[j,i],100001)
        for k in range(len(Energias)):
            y =  E*g(E,Energias[k],gamma[j])*Degeneracion[k]  # Valores de la función en esos puntos 
            Eshell2 [j,i]+= simpson(y,E)
            #n=len(E)
            #h = E[1]-E[0]
            #Eshell2[j,i] += (h / 2) * (y[0] + 2 * np.sum(y[1:n-1]) + y[n-1])
                                       
print("Eshel=",Eshell)
print("Eshel2=",Eshell2)  
for i in range(len(Eshell2)):
    print("*******************************")
    print("gamma=",gamma[i])
    for j in range(len(Eshell2[0])):
        print("Para el Z=%i tenemos un valor de deltaE = %.5f"%(Area[j],Eshell[j]-Eshell2[i,j]))
              

delta1=np.zeros((len(gamma)))  
delta2=np.zeros((len(gamma)))    
delta3=np.zeros((len(gamma)))    
delta4=np.zeros((len(gamma)))      
            
for i in range(len(gamma)):            
    delta1[i]=Eshell[0]-Eshell2[i,0]
    delta2[i]=Eshell[1]-Eshell2[i,1]
    delta3[i]=Eshell[2]-Eshell2[i,2]
    delta4[i]=Eshell[3]-Eshell2[i,3]
    
print(delta1)
print(gamma)

generar_tabla_latex(["$\\gamma$","Z=50","N=82","Z=40","N=60"],gamma,delta1,delta2,delta3,delta4,nombre_archivo="Gamma.tex")

























