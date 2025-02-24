import numpy as np
import matplotlib.pyplot as plt 
import numpy as np
from scipy.special import erf
from scipy.optimize import fsolve

############################
##### EJERCICIO 8 ##########
############################

# Creación de nuestro colocador de bandas:

Energias=np.array([0,6.2,9.8,16.2,19.8,21.4,26.4,31.8,34.4,36.6,39.2,49.8,52.2,55.2,57.6,59.6,72.2,75.0,77.8,79.6,81.6])
Degeneracion=np.array([2,4,2,6,2,4,8,4,6,2,10,8,6,4,2,12,10,8,6,4,2])
Nombre=["1s1/2  [0MeV]","1p3/2 [6.2MeV]","1p1/2 [9.8MeV]","1d5/2 [16.2MeV]",    "2s1/2 [19.8MeV]",  "1d3/2 [21.4MeV]",    "1f7/2 [26.4MeV]",    "2p3/2 [31.8MeV]",   "1f5/2 [34.4MeV]",    "2p1/2 [36.6MeV]",
    "1g9/2 [39.2MeV]",    "1g7/2 [49.8 MeV]",    "2d5/2 [52.2MeV]",    "2d3/2 [55.2MeV]",    "3s1/2 [57.6MeV]",    "1h11/2 [59.6MeV]",    "1h9/2 [72.2MeV]",    "2f7/2 [75.0MeV]",    "2f5/2[77.8MeV]",   
    "3p3/2 [79.6MeV]",    "3p1/2 [81.6 MeV]"]



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


# Resolución del ejercicio:


def f(x,gamma,Ei):
    return (x-Ei)/np.sqrt(gamma) 
def g(E,Ei,gamma):
    return (np.exp(-(f(E,gamma,Ei)**2)))/np.sqrt(np.pi*gamma)



E=np.linspace(-10,90,10000)

plt.figure()

def ge(gamma,Area):
    y=np.zeros(len(E), dtype=float)
    z=np.zeros(len(E), dtype=float)

    for i in range(len(Degeneracion)):
        for j in range(len(E)):
            y[j]=Degeneracion[i]*g(E[j],Energias[i],gamma)
            z[j]+=Degeneracion[i]*g(E[j],Energias[i],gamma)
            #plt.plot(E,y)  
        
    area = np.trapezoid(z, E)    
    #print(area)
    if Area<42:
        plt.plot(E,z,label="$\gamma=%.2f $"%gamma)
        plt.legend()
        plt.xlabel("E [MeV]")
        plt.ylabel("g(E)")

    x=E
    y=z

    # Área objetivo que queremos alcanzar
    area_objetivo = Area

    # Calculamos las diferencias entre los puntos de x
    dx = np.diff(x)

    # Calculamos las áreas de cada intervalo usando la regla del trapecio:
    # area_i = (x[i+1] - x[i]) * (y[i] + y[i+1]) / 2
    areas = dx * (y[:-1] + y[1:]) / 2

    # Calculamos el área acumulada sumando las áreas de cada intervalo
    area_acumulada = np.concatenate(([0], np.cumsum(areas)))

    # Encontramos el índice donde el área acumulada es mayor o igual al área objetivo
    idx = np.where(area_acumulada >= area_objetivo)[0][0]

    # Interpolamos linealmente para obtener un valor más exacto de x
    if idx == 0:
        x_target = x[0]
    else:
        x0, x1 = x[idx-1], x[idx]
        area0, area1 = area_acumulada[idx-1], area_acumulada[idx]
        # Interpolación lineal
        x_target = x0 + (area_objetivo - area0) * (x1 - x0) / (area1 - area0)

   # print("El valor de x hasta el cual se debe integrar para obtener un área de", area_objetivo, "es:", x_target)
    
    return x_target
    
gamma=[1,2,10,20]
Area=[50,82,40,68]

energia=np.zeros((len(gamma),len(Area)))

for i in range(len(gamma)):
    for j in range(len(Area)):
        energia[i,j]=ge(gamma[i],Area[j])
    
print(energia)    

Eshell=np.zeros((len(Area)))
Eshell2=np.zeros((len(gamma),len(Area)))

for i in range(len(Area)):
    j=0
    aux=0
    while j<len(Degeneracion) and sum(Degeneracion[0:j])<Area[i]:
        if sum(Degeneracion[0:j+1])>Area[i]:
            aux=Area[i]-sum(Degeneracion[0:j])-Degeneracion[j]
        Eshell[i]+=Energias[j]*(Degeneracion[j]+aux)
        
        j+=1


for i in range(len(Area)):
    for j in range(len(gamma)):
        for k in range(len(Energias)):
            Eshell2[j,i]+=-np.sqrt(gamma[j]/(4*np.pi))*(Degeneracion[k]*np.exp(-((energia[j,i]-Energias[k])/np.sqrt(gamma[j]))**2))
            Eshell2[j,i]+=(1/2)*(Degeneracion[k]*Energias[k]*(erf((energia[j,i]-Energias[k])/np.sqrt(gamma[j]))+1))


print("energia lambda_F",energia)
print(Eshell)
print(Eshell2)


plt.savefig("ge.pdf")





























