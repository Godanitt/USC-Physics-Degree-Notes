import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as signal
import scipy.optimize as opt

def gaussiana(x, A, mu, sigma):
    """Función gaussiana estándar."""
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

def ajustar_gaussiana(x, y):
    """Ajusta una gaussiana a los datos (x, y) y devuelve mu y sigma."""
    # Estimaciones iniciales: amplitud, media y sigma
    A_init = max(y)  # Pico máximo
    mu_init = np.sum(x * y) / np.sum(y)  # Centro de masa
    sigma_init = np.sqrt(np.sum(y * (x - mu_init) ** 2) / np.sum(y))  # Aproximación inicial
    
    # Ajuste con curve_fit
    params, _ = opt.curve_fit(gaussiana, x, y, p0=[A_init, mu_init, sigma_init])

    A_fit, mu_fit, sigma_fit = params
    return A_fit,mu_fit, sigma_fit

def lineal(x, m, b):
    """Función lineal: y = m*x + b"""
    return m * x + b

def regresion_lineal_opt(x, y):
    """
    Realiza una regresión lineal usando scipy.optimize.curve_fit.
    
    Parámetros:
        x: Array de valores en el eje x.
        y: Array de valores en el eje y.
    
    Retorna:
        pendiente (m), intersección (b)
    """
    # Estimaciones iniciales para la regresión
    p0 = [1, 0]  # Pendiente inicial = 1, Intersección = 0

    # Ajuste de la función modelo_lineal a los datos
    params, _ = opt.curve_fit(lineal, x, y, p0=p0)

    m, b = params
    return m, b


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



# Vamos a crear una función que nos permite, dado cualquier archivo, leer directamente el LIVE TIME de nuestros datos:

def read_live_time(archivo):

    # Leer el archivo ignorando los bloques <<...>
    with open(archivo, "r") as f:
        lineas = [line.strip() for line in f if not line.startswith("<<")]

    # Convertir a DataFrame
    df = pd.DataFrame([line.split(" - ") for line in lineas if " - " in line], columns=["Clave", "Valor"])

    # Filtrar solo LIVE_TIME
    live_time = df.loc[df["Clave"] == "LIVE_TIME", "Valor"].values[0]
    print(f"LIVE_TIME: {live_time}")

    return live_time


################################################################
# Vamos a empezar dandole nombre a los archivos: 

nombre_fondo="RuidoFondo.txt"
nombre_archivos=["22Na_6-2.mca","207Bi_7.mca","152Eu_7.mca","60Co_7.mca","137Cs_7.txt"]
nombre_titulos=["22Na 6.2 cm","207Bi 7cm","152Eu 7cm","60Co 7cm","137Cs 7cm"]
nombre_pdf1=["Canal/22Na_6-2_canal.pdf","Canal/207Bi_7_canal.pdf","Canal/152Eu_7_canal.pdf","Canal/60Co_7_canal.pdf","Canal/137Cs_7_canal.pdf"]
nombre_pdf2=["Energia/22Na_6-2_energia.pdf","Energia/207Bi_7_energia.pdf","Energia/152Eu_7_energia.pdf","Energia/60Co_7_energia.pdf","Energia/137Cs_7_energia.pdf"]



################################################################################################################################
# Lo primero a tratar es el fondo de radiación externa, por lo que tenemos que evaluar cual es la altura por unidad de tiempo vivo.
# Para esto creamos una función que dado el nombre del archivo nos de una array con el canal y la tasa de lectura por canal 


def Obten_fondo(archivo):
    
    teff=int(read_live_time(archivo))
    
    with open(archivo, "r") as f:
        lineas = f.readlines()
        
    # Extraer datos numéricos (ignorando cabecera)
    datos = np.array([int(linea.strip()) for linea in lineas if linea.strip().isdigit()])
    
    print(teff)
    tasa=datos/teff
    
    canal=np.linspace(0,len(tasa)-1,len(tasa))
    
    fig=plt.figure(figsize=(12,6))
    plt.plot(canal,tasa,linestyle="-",color="blue",linewidth=0.5)
    plt.title("Radiación de fondo")
    plt.xlabel("Canal")
    plt.ylabel("Tasa [$s^{-1}$]")
    
    return tasa,fig


tasa_fondo,fig=Obten_fondo(nombre_fondo)
fig.savefig("Canal/Fondo_Canal.pdf",bbox_inches='tight')
        

#################################################################
# Lo siguiente es calcular cada espectro, primero en tasa de cuentas por unidad de tiempo vivo, 
# Para esto hacemos la función primero que lea para un archivo y un array llamado tasa_fondo que reste el fondo. Devuelve la tasa para dicho array

def Obten_espectroscopia(archivo,fondo,titulo):
    
    teff=int(read_live_time(archivo))
    
    with open(archivo, "r") as f:
        lineas = f.readlines()
        
    # Extraer datos numéricos (ignorando cabecera)
    datos = np.array([int(linea.strip()) for linea in lineas if linea.strip().isdigit()])
    
    print(teff)
    tasa=datos/teff-fondo
    
    canal=np.linspace(0,len(tasa)-1,len(tasa))
    
    fig=plt.figure(figsize=(12,6))
    plt.plot(canal,tasa,linestyle="-",color="blue",linewidth=0.5)
    plt.title("%r"%titulo)
    plt.xlabel("Canal")
    plt.ylabel("Tasa [$s^{-1}$]")
    plt.grid(True, linestyle="--")
    return tasa,fig

Tasas=np.zeros((len(nombre_archivos),len(tasa_fondo)))
for i in range(len(nombre_archivos)):
    Tasas[i,:],fig=Obten_espectroscopia(nombre_archivos[i],tasa_fondo,nombre_titulos[i])
    fig.savefig(nombre_pdf1[i],bbox_inches='tight')

numero_canal=np.linspace(0,len(tasa_fondo)-1,len(tasa_fondo))
    


################################################################
#  Hacemos una función que nos calcula los picos y los relaciona con la energía, obteniendo la función de calibración
# Para esto tenemos que saber cuales son las energías de los diferentes picos

nombre_archivos=["22Na_6-2.mca","207Bi_7.mca","152Eu_7.mca","60Co_7.mca","137Cs_7.txt"]
# Los picos van en el orden siguiente: picos del sodio, picos del bismuto, picos del europio, picos del cobalto y picos del cesio
Picos_Energias=[[511,1274.5],[570,1063],[],[1173,1332],[661.7]]
Energias_picos=np.array([511,1274.5,570,1063,1173,1332,661.7])

# Ajustamos los picos del sodio    
    
A_22Na1, mu_22Na1, sigma_22Na1=ajustar_gaussiana(numero_canal[1800:2200],Tasas[0,1800:2200])
fig=plt.figure()
plt.plot(numero_canal[1700:2200],gaussiana(numero_canal[1700:2200],A_22Na1, mu_22Na1, sigma_22Na1))
plt.plot(numero_canal[1700:2200],Tasas[0,1700:2200],".r")
fig.savefig("Aproximacion_gaussiana/Na22_Pico_1.pdf",bbox_inches='tight')


A_22Na2, mu_22Na2, sigma_22Na2=ajustar_gaussiana(numero_canal[4560:5000],Tasas[0,4560:5000])
fig=plt.figure()
plt.plot(numero_canal[4560:5000],gaussiana(numero_canal[4560:5000],A_22Na2, mu_22Na2, sigma_22Na2))
plt.plot(numero_canal[4560:5000],Tasas[0,4560:5000],".r")
fig.savefig("Aproximacion_gaussiana/Na22_Pico_2.pdf",bbox_inches='tight')

# Ajustamos los picos del bismuto

A_207Bi1, mu_207Bi1, sigma_207Bi1=ajustar_gaussiana(numero_canal[2000:2300],Tasas[1,2000:2300])
fig=plt.figure()
plt.plot(numero_canal[2000:2300],gaussiana(numero_canal[2000:2300],A_207Bi1, mu_207Bi1, sigma_207Bi1))
plt.plot(numero_canal[2000:2300],Tasas[1,2000:2300],".r")
fig.savefig("Aproximacion_gaussiana/Bi207_Pico_1.pdf",bbox_inches='tight')


A_207Bi2, mu_207Bi2, sigma_207Bi2=ajustar_gaussiana(numero_canal[3800:4200],Tasas[1,3800:4200])
fig=plt.figure()
plt.plot(numero_canal[3800:4200],gaussiana(numero_canal[3800:4200],A_207Bi2, mu_207Bi2, sigma_207Bi2))
plt.plot(numero_canal[3800:4200],Tasas[1,3800:4200],".r")
fig.savefig("Aproximacion_gaussiana/Bi207_Pico_2.pdf",bbox_inches='tight')

# Ajustamos los picos del cobalto

A_60Co1, mu_60Co1, sigma_60Co1=ajustar_gaussiana(numero_canal[4000:4700],Tasas[3,4000:4700])
fig=plt.figure()
plt.plot(numero_canal[4000:4700],gaussiana(numero_canal[4000:4700],A_60Co1, mu_60Co1, sigma_60Co1))
plt.plot(numero_canal[4000:4700],Tasas[3,4000:4700],".r")
fig.savefig("Aproximacion_gaussiana/Co60_Pico_1.pdf",bbox_inches='tight')


A_60Co2, mu_60Co2, sigma_60Co2=ajustar_gaussiana(numero_canal[4600:5300],Tasas[3,4600:5300])
fig=plt.figure()
plt.plot(numero_canal[4600:5300],gaussiana(numero_canal[4600:5300],A_60Co2, mu_60Co2, sigma_60Co2))
plt.plot(numero_canal[4600:5300],Tasas[3,4600:5300],".r")
fig.savefig("Aproximacion_gaussiana/Co60_Pico_2.pdf",bbox_inches='tight')


# Ajustamos los picos del cesio


A_137Cs1, mu_137Cs1, sigma_137Cs1=ajustar_gaussiana(numero_canal[2500:2900],Tasas[4,2500:2900])
fig=plt.figure()
plt.plot(numero_canal[2500:2900],gaussiana(numero_canal[2500:2900],A_137Cs1, mu_137Cs1, sigma_137Cs1))
plt.plot(numero_canal[2500:2900],Tasas[4,2500:2900],".r")
fig.savefig("Aproximacion_gaussiana/Cs137_Pico_1.pdf",bbox_inches='tight')

A=np.array([A_22Na1,A_22Na2,A_207Bi1,A_207Bi2,A_60Co1,A_60Co2,A_137Cs1])
mu=np.array([mu_22Na1,mu_22Na2,mu_207Bi1,mu_207Bi2,mu_60Co1,mu_60Co2,mu_137Cs1])
sigma=np.array([sigma_22Na1,sigma_22Na2,sigma_207Bi1,sigma_207Bi2,sigma_60Co1,sigma_60Co2,sigma_137Cs1])



# Ahora con la relación energía-pico podemos relacionar canal-energia (calibracion)

fig=plt.figure()
plt.plot(mu,Energias_picos,".r")
a,b=regresion_lineal_opt(mu,Energias_picos)
plt.plot(mu,lineal(mu,a,b))
plt.grid(True,linestyle="--")
plt.xlabel("Canal")
plt.ylabel("Energía [keV]")
plt.title("Calibración según los picos")
plt.savefig("Recta_calibracion.pdf",bbox_inches='tight')

# Sacamos los datos en forma de .tex


################################################################
#  Luego con los picos obtenidos hacemos una relación de las energías y número de canal con el que poder obtener la calibració y relación entre canal y energía.


def Obten_fondo_2(archivo):
    
    teff=int(read_live_time(archivo))
    
    with open(archivo, "r") as f:
        lineas = f.readlines()
        
    # Extraer datos numéricos (ignorando cabecera)
    datos = np.array([int(linea.strip()) for linea in lineas if linea.strip().isdigit()])
    
    print(teff)
    tasa=datos/teff
    
    canal=lineal(np.linspace(0,len(tasa)-1,len(tasa)),a,b)
    
    fig=plt.figure(figsize=(12,6))
    plt.plot(canal,tasa,linestyle="-",color="blue",linewidth=0.5)
    plt.title("Radiación de fondo")
    plt.xlabel("Energía [keV]")
    plt.ylabel("Tasa [$s^{-1}$]")
    plt.grid(True, linestyle="--")
    
    return tasa,fig

def Obten_espectroscopia_2(archivo,fondo,titulo):
    
    teff=int(read_live_time(archivo))
    
    with open(archivo, "r") as f:
        lineas = f.readlines()
        
    # Extraer datos numéricos (ignorando cabecera)
    datos = np.array([int(linea.strip()) for linea in lineas if linea.strip().isdigit()])
    
    print(teff)
    tasa=datos/teff-fondo
    
    canal=lineal(np.linspace(0,len(tasa)-1,len(tasa)),a,b)
    
    fig=plt.figure(figsize=(12,6))
    plt.plot(canal,tasa,linestyle="-",color="blue",linewidth=0.5)
    plt.title("%r"%titulo)
    plt.xlabel("Energía [keV]")
    plt.ylabel("Tasa [$s^{-1}$]")
    plt.grid(True, linestyle="--")
    return tasa,fig


tasa_fondo,fig=Obten_fondo_2(nombre_fondo)
fig.savefig("Energia/Fondo_Energia.pdf",bbox_inches='tight')

Tasas=np.zeros((len(nombre_archivos),len(tasa_fondo)))
for i in range(len(nombre_archivos)):
    Tasas[i,:],fig=Obten_espectroscopia_2(nombre_archivos[i],tasa_fondo,nombre_titulos[i])
    fig.savefig(nombre_pdf2[i],bbox_inches='tight')




#################################################################
#  Finalmente podemos calcular las anchuras

nombre_pico=["$^{22}$Na","$^{22}$Na","$^{207}$Bi","$^{207}$Bi","$^{60}$Co","$^{60}$Co","$^{137}$Cs"]
generar_tabla_latex(["a (pendiente)","b"],[a],[b],nombre_archivo="Parametro_Calibracion.tex")
generar_tabla_latex(["Pico","A [1/s]"," x_0[keV]"," $\sigma$ [keV]", "FWHM [keV]","FWHM/E"," x_0 [Canal]"],nombre_pico,A,lineal(mu,a,b),-lineal(sigma,a,b),-2.35*lineal(sigma,a,b),-2.35*lineal(sigma,a,b)/Energias_picos,mu,nombre_archivo="Parametros_fotopicos.tex")

fig=plt.figure()
plt.xlabel("E [keV]")
plt.ylabel("FWMH/E")
plt.title("FWHM/E frente a E")
plt.plot(lineal(mu,a,b),-2.35*lineal(sigma,a,b)/lineal(mu,a,b),".r")
plt.grid(True,linestyle="--")
fig.savefig("Dependecia_Anchura.pdf")

###################################################################
# Calculo de las actividades:

nombre=["$^{60}$Co","$^{137}$Cs","$^{207}$Bi","$^{60}$Eu","$^{22}$Na"]
Actividad_inicial=np.array([399000,8417,82510,38973,74000])
Vida_media=np.array([1.93*10**3,30.2*365,30.5*365,13.517*365,2.6*365])
Tiempo_transcurrido=np.array([24*365-(9-2)*30+27,13*365+27,42*365-(4-2)*30+17,18*365-(2-2)*30+27,5*365+8+2*30])
Actividad_acutal=Actividad_inicial*np.exp(-Tiempo_transcurrido/Vida_media)
generar_tabla_latex(["Elemento","Actividad inicial [Bq]","Vida media [dias]","Tiempo trascurrido [dias]", "Actividad actual [Bq]"],nombre,Actividad_inicial,Vida_media,Tiempo_transcurrido,Actividad_acutal,nombre_archivo="Actividad.tex")


#####################################################################
# Calculo de las eficiencia frente a la distancia

nombres_distancias=["Distancias/22Na_6-6cm.mca","Distancias/22Na_7-6cm.mca","Distancias/22Na_8-6cm.mca","Distancias/22Na_11-6cm.mca",
                    "Distancias/22Na_14-6cm.mca","Distancias/22Na_17-6cm.mca","Distancias/22Na_20-6cm.mca","Distancias/22Na_22-6cm.mca"]


nombres_distancias_pdf=["Distancias/22Na_6-6.pdf","Distancias/22Na_7-6.pdf","Distancias/22Na_8-6.pdf","Distancias/22Na_11-6.pdf",
                    "Distancias/22Na_14-6.pdf","Distancias/22Na_17-6.pdf","Distancias/22Na_20-6.pdf","Distancias/22Na_22-6.pdf"]


tasa_fondo,fig=Obten_fondo_2(nombre_fondo)
fig.savefig("Energia/Fondo_Energia.pdf",bbox_inches='tight')

nombre_titulos_distancias=["22Na 6.6 cm","22Na 7.6 cm","22Na 8.6 cm","22Na 11.6 cm","22Na 14.6 cm","22Na 17.6 cm","22Na 20.6 cm","22Na 22.6 cm"]

Tasas=np.zeros((len(nombres_distancias),len(tasa_fondo)))
for i in range(len(nombres_distancias)):
    Tasas[i,:],fig=Obten_espectroscopia_2(nombres_distancias[i],tasa_fondo,nombre_titulos_distancias[i])
    fig.savefig(nombres_distancias_pdf[i],bbox_inches='tight')


A_22Na6_6, mu_22Na6_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[1800:2200],Tasas[0,1800:2200])
A_22Na7_6, mu_22Na7_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[1800:2200],Tasas[1,1800:2200])
A_22Na8_6, mu_22Na8_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[1800:2200],Tasas[2,1800:2200])
A_22Na11_6, mu_22Na11_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[1800:2200],Tasas[3,1800:2200])
A_22Na14_6, mu_22Na14_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[1800:2200],Tasas[4,1800:2200])
A_22Na17_6, mu_22Na17_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[1800:2200],Tasas[5,1800:2200])
A_22Na20_6, mu_22Na20_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[1800:2200],Tasas[6,1800:2200])
A_22Na22_6, mu_22Na22_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[1800:2200],Tasas[7,1800:2200])


distancias=np.array([6.6,7.6,8.6,11.6,14.6,17.6,20.6,22.6])
Tasas_distancias=[A_22Na6_6,A_22Na7_6,A_22Na8_6,A_22Na11_6,A_22Na14_6,A_22Na17_6,A_22Na20_6,A_22Na22_6]
Fotopico_distancias=lineal(np.array([mu_22Na6_6,mu_22Na7_6,mu_22Na8_6,mu_22Na11_6,mu_22Na14_6,mu_22Na17_6,mu_22Na20_6,mu_22Na22_6]),a,b)

fig=plt.figure()
plt.plot(distancias,Tasas_distancias,".r")
plt.xlabel("Distancias [cm]")
plt.ylabel("Tasas [1/s]")
plt.title("Tasas vs distancia Fotopico 511 keV $^{22}$Na")
plt.grid(True)
fig.savefig("Tasa_distancia.pdf")

fig=plt.figure()
plt.plot(distancias,Fotopico_distancias,".r")
plt.xlabel("Distancias [cm]")
plt.ylabel("Energia [keV]")
plt.title("Energias vs distancia Fotopico 511 keV $^{22}$Na")
plt.grid(True)
fig.savefig("Energias_distancias.pdf")


# Vamos a hacer el array con las intensidades:

Actividad_inicial=np.array([399000,399000,74000,74000,82510,82510,8417,38973,38973,38973,38973])
Vida_media=np.array([1.93*10**3,1.93*10**3,2.6*365,2.6*365, 30.15*365,30.15*365,30.02*365,13.517*365,13.517*365,13.517*365,13.517*365])
Tiempo_transcurrido=np.array([24*365-(9-2)*30+27,24*365-(9-2)*30+27,5*365+8+2*30,5*365+8+2*30,42*365-(4-2)*30+17,42*365-(4-2)*30+17,24*365-(9-2)*30+27,18*365-(2-2)*30+27,18*365-(2-2)*30+27,18*365-(2-2)*30+27,18*365-(2-2)*30+27])
Irelativa=np.array([99.88,99.9826,179.91,99.940,97.75,74.5,85.1,26.59,2.237,12.93,1.633])/100

print(len(Actividad_inicial),len(Vida_media),len(Tiempo_transcurrido),len(Irelativa))
Actividad_actual=Irelativa[2]*Actividad_inicial[2]*np.exp(-Tiempo_transcurrido[2]/Vida_media[2])

activiad_sodio=Actividad_actual

def eficiencia_geometrica(d):
    y = 0.5*(1-1/(np.sqrt(1+10*(d/(d**2+1/np.pi**2))**2)))
    return y
def ajustar_eficiencia(x, y):
    # Ajuste con curve_fit
    params, _ = opt.curve_fit(eficiencia_geometrica, x, y, p0=[10**(-6)])

    intrinseca= params
    return intrinseca

fig=plt.figure()
plt.plot(distancias,Tasas_distancias/activiad_sodio,".r")
plt.xlabel("Distancias [cm]")
plt.ylabel("Eficiencia $\\varepsilon$")
plt.title("Eficiencia vs distancia Usando Fotopico 511 keV $^{22}$Na")
plt.grid(True)
fig.savefig("Eficiencia_distancia.pdf")


egeo=eficiencia_geometrica(distancias)
eint=(Tasas_distancias/activiad_sodio)/egeo

fig=plt.figure()
plt.plot(distancias,eint,".r")
plt.xlabel("Distancias [cm]")
plt.ylabel("Eficiencia intríseca $\\varepsilon_{\\text{int}}$")
plt.title("Eficiencia intrínseca vs distancia Usando Fotopico 511 keV $^{22}$Na")
plt.grid(True)
fig.savefig("Eficiencia_intrinseca_distancia.pdf")


generar_tabla_latex(["distancias [cm]","$\\varepsilon_{\\text{tot}}$","$\\varepsilon_{\\text{geo}}$","$\\varepsilon_{\\text{sim}}$"],distancias,Tasas_distancias/activiad_sodio,
                    egeo,eint,nombre_archivo="Eficiencias.tex")

#############3
#### Medimos la eficiencia intrínseca a otra energia
A_22Na6_6, mu_22Na6_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[4500:5200],Tasas[0,4500:5200])
A_22Na7_6, mu_22Na7_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[4500:5000],Tasas[1,4500:5000])
A_22Na8_6, mu_22Na8_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[4560:5000],Tasas[2,4560:5000])
A_22Na11_6, mu_22Na11_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[4560:5000],Tasas[3,4560:5000])
A_22Na14_6, mu_22Na14_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[4560:5000],Tasas[4,4560:5000])
A_22Na17_6, mu_22Na17_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[4560:5000],Tasas[5,4560:5000])
A_22Na20_6, mu_22Na20_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[4560:5000],Tasas[6,4560:5000])
A_22Na22_6, mu_22Na22_6, sigma_22Na6_6=ajustar_gaussiana(numero_canal[4560:5000],Tasas[7,4560:5000])


distancias=np.array([6.6,7.6,8.6,11.6,14.6,17.6,20.6,22.6])
Tasas_distancias=[A_22Na6_6,A_22Na7_6,A_22Na8_6,A_22Na11_6,A_22Na14_6,A_22Na17_6,A_22Na20_6,A_22Na22_6]
Fotopico_distancias=lineal(np.array([mu_22Na6_6,mu_22Na7_6,mu_22Na8_6,mu_22Na11_6,mu_22Na14_6,mu_22Na17_6,mu_22Na20_6,mu_22Na22_6]),a,b)

fig=plt.figure()
plt.plot(distancias,Tasas_distancias,".r")
plt.xlabel("Distancias [cm]")
plt.ylabel("Tasas [1/s]")
plt.title("Tasas vs distancia Fotopico 511 keV $^{22}$Na")
plt.grid(True)
fig.savefig("Tasa_distancia_1000kev.pdf")

fig=plt.figure()
plt.plot(distancias,Fotopico_distancias,".r")
plt.xlabel("Distancias [cm]")
plt.ylabel("Energia [keV]")
plt.title("Energias vs distancia Fotopico 511 keV $^{22}$Na")
plt.grid(True)
fig.savefig("Energias_distancias_1000kev.pdf")


# Vamos a hacer el array con las intensidades:

Actividad_inicial=np.array([399000,399000,74000,74000,82510,82510,8417,38973,38973,38973,38973])
Vida_media=np.array([1.93*10**3,1.93*10**3,2.6*365,2.6*365, 30.15*365,30.15*365,30.02*365,13.517*365,13.517*365,13.517*365,13.517*365])
Tiempo_transcurrido=np.array([24*365-(9-2)*30+27,24*365-(9-2)*30+27,5*365+8+2*30,5*365+8+2*30,42*365-(4-2)*30+17,42*365-(4-2)*30+17,24*365-(9-2)*30+27,18*365-(2-2)*30+27,18*365-(2-2)*30+27,18*365-(2-2)*30+27,18*365-(2-2)*30+27])
Irelativa=np.array([99.88,99.9826,179.91,99.940,97.75,74.5,85.1,26.59,2.237,12.93,1.633])/100

print(len(Actividad_inicial),len(Vida_media),len(Tiempo_transcurrido),len(Irelativa))
Actividad_actual=Irelativa[2]*Actividad_inicial[2]*np.exp(-Tiempo_transcurrido[2]/Vida_media[2])

activiad_sodio=Actividad_actual

def eficiencia_geometrica(d):
    y = 0.5*(1-1/(np.sqrt(1+10*(d/(d**2+1/np.pi**2))**2)))
    return y
def ajustar_eficiencia(x, y):
    # Ajuste con curve_fit
    params, _ = opt.curve_fit(eficiencia_geometrica, x, y, p0=[10**(-6)])

    intrinseca= params
    return intrinseca

fig=plt.figure()
plt.plot(distancias,Tasas_distancias/activiad_sodio,".r")
plt.xlabel("Distancias [cm]")
plt.ylabel("Eficiencia $\\varepsilon$")
plt.title("Eficiencia vs distancia Usando Fotopico 1274 keV $^{22}$Na")
plt.grid(True)
fig.savefig("Eficiencia_distancia1000kev.pdf")


egeo=eficiencia_geometrica(distancias)
eint=(Tasas_distancias/activiad_sodio)/egeo

fig=plt.figure()
plt.plot(distancias,eint,".r")
plt.xlabel("Distancias [cm]")
plt.ylabel("Eficiencia intríseca $\\varepsilon_{\\text{int}}$")
plt.title("Eficiencia intrínseca vs distancia Usando Fotopico 1274 keV $^{22}$Na")
plt.grid(True)
fig.savefig("Eficiencia_intrinseca_distancia_1000kev.pdf")


generar_tabla_latex(["distancias [cm]","$\\varepsilon_{\\text{tot}}$","$\\varepsilon_{\\text{geo}}$","$\\varepsilon_{\\text{sim}}$"],distancias,Tasas_distancias/activiad_sodio,
                    egeo,eint,nombre_archivo="Eficiencias2.tex")


