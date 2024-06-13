# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 18:35:44 2024

@author: danie
"""


import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as cte
import matplotlib.colors as colors
import matplotlib.animation as animation


t=np.linspace(-5,5,1000)
y=np.cos(t*10*(2*np.pi/5))
plt.plot(t,y,color="red")
plt.xlim(-10,10)
plt.ylim(-1.5,2)
plt.annotate("", (-5.1,1.1), xytext=(5.1, 1.1),
            arrowprops=dict(facecolor='black',arrowstyle="<->"))

plt.annotate("$t_0$", (0,1.2), xytext=(0,1.2))
plt.xlabel("t")
plt.ylabel("E(t)")
plt.grid()
plt.xticks([0],[" "])
plt.yticks([0],[" "])
plt.savefig("02-Achura_espectral.pdf")
#%%
"""
z , x = np.mgrid[-100:100, -500:500]


def E(A0,x,x1,z,z1,k,t):
    E=np.cos(k*((x-x1)**2/(2*(z-z1))+k*z)-t)
    return E

def x(x1,z,z1,k,C):
    x21=x1+np.sqrt(abs((C-k*z)*2*(z-z1)/k))
    x22=x1-np.sqrt(abs((C-k*z)*2*(z-z1)/k))
    return x21,x22


lamb=cte.c/10**7
k=(2*np.pi)/lamb

E1=E(1,x,0,z,-5000,k,0)

fig, ax = plt.subplots(1, 1)

pcm = ax.pcolor(z, x, E1, cmap='twilight_shifted', shading='nearest')

fig.colorbar(pcm, ax=ax, extend='max')

plt.xlabel("z")
plt.ylabel("x")

plt.xticks([],[])
plt.yticks([],[])

plt.savefig("Onda_Paraxial.pdf",dpi=300,bbox_inches="tight")

##############################################################################


fig, ax = plt.subplots()

z = np.linspace(-500, 500, 1000)
x = np.linspace(-500, 500, 1000).reshape(-1, 1)


ims = []
t=0
for i in range(60):
    t += 0.125
    im = ax.imshow(E(10,x,0,z,-1500,k,t), animated=True,cmap='binary')
    if i == 0:
        ax.imshow(E(10,x,0,z,-1500,k,t),cmap='binary')  # show an initial one first
    ims.append([im])
    
ax.set_ylim(-0,1000)
ax.set_xlim(-0,1000)
ax.set_xlabel("z")
ax.set_ylabel("x")

ax.set_xticks([],[])
ax.set_yticks([],[])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)

plt.show()
writer = animation.PillowWriter(fps=25,metadata=dict(artist='Me'),bitrate=3600)
ani.save('scatter.gif', writer=writer,dpi=250)

"""