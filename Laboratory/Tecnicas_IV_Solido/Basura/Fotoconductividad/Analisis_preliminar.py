import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

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



# Calculo de G0

V0=[6041,
5497,
5060,
4501,
3995,
3505,
3004,
2507,
1999,
1513,
1021,
498,
0
]

I0=[0.65,
0.59,
0.55,
0.49,
0.44,
0.39,
0.33,
0.27,
0.22,
0.17,
0.12,
0.07,
0.01
]

V0=np.array(V0)
I0=np.array(I0)


G0,a=regresion_lineal_opt(V0,I0)

fig=plt.figure()
plt.plot(V0,I0,".r")
plt.plot(V0,lineal(V0,G0,a))
fig.savefig("G0.pdf")

print("El valor de G0=%.7f mA/V"%G0)

# Caclulo de m y b
# Para calcular m y b necesitamos conocer Delta G cuando luminosidad ambiental es cero, asi pues

V0=np.array(V0)

theta=[#90,
85,
80,
75,
70,
65,
60,
55,
50,
45,
40,
35,
30,
25,
20,
15,
10,
5,
0]
Vphia=6.34
Iphia0=[#0.6,
1.3,
1.9,
2.9,
3.9,
5,
6,
7,
8.1,
9.2,
10.3,
11.1,
11.9,
12.8,
13.2,
13.7,
14,
14.1,
14.1
]

theta=np.array(theta)*np.pi/180
Iphia0=np.array(Iphia0)
Gphia0=Iphia0/Vphia

DGphia0=Gphia0-G0

#print(theta)

logDGphia0=np.log(DGphia0)
costheta=np.log(np.cos(theta))



fig=plt.figure()
plt.plot(costheta,logDGphia0,".r")
plt.xlabel("$\log \cos(\\theta)$ ")
plt.ylabel("$\log \\Delta G (\\theta)$ ")
fig.savefig("logphia0.pdf")

m,b0=regresion_lineal_opt(costheta,logDGphia0)

print("m=%.5f"%m)
b=np.exp(2*b0/m)
print("b=%.5f"%b)


fig=plt.figure()
plt.plot(np.cos(theta),DGphia0,".r")
plt.plot(np.cos(theta),(b**(m/2))*(np.cos(theta))**m,color="blue",linestyle="-")
plt.xlabel("$\cos (\\theta)$")
plt.ylabel("$\Delta G $")
plt.title("$\Delta G$ frente a $\\theta$ sin luminosidad natural")
fig.savefig("DG.pdf")

# Una vezz tenemos b y m ahora podems calcular a, con los datos de la radiación natural 
V=np.array([
#6.34,
6.34,
6.34,
6.28,
6.34,
6.34,
6.34,
6.34,
6.34,
6.34,
6.33,
6.33,
6.33,
6.33,
6.33,
6.33,
6.33,
6.33,
6.34])

I=np.array([
#6.7,
6.9,
7.6,
8.5,
9.3,
10,
11,
12,
12.9,
13.6,
14.4,
15.4,
15.9,
16.3,
16.7,
17.3,
17.3,
17.6,
17.8
])

DG=I/V-G0

def funcion_1(theta,a):
    y=np.sqrt((a+b*(np.cos(theta))**2)**m)
    return y
def funcion_2(theta,a):
    y=np.sqrt((a)**m)+np.sqrt((b*(np.cos(theta))**2)**m)
    return y

fig=plt.figure()

params1, _ = opt.curve_fit(funcion_1, theta, DG, p0=5)
print(params1)
params2, _ = opt.curve_fit(funcion_2, theta, DG, p0=params1[0])

plt.plot(theta,funcion_1(theta,params1[0]),color="green",label="Funcion 8")


plt.plot(theta,funcion_2(theta,params2[0]),color="blue",label="Funcion 11")



plt.plot(theta,DG,".r",label="Valroes experimentales")
plt.xlabel("$\\theta$ (rad)")
plt.ylabel("$\\Delta G$")
plt.title("$\Delta G$ frente a $\\theta$ con luminosidad natural")
plt.legend()
fig.savefig("DG22.pdf")