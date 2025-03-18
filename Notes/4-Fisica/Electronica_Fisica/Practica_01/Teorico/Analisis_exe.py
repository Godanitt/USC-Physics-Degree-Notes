
from Analisis import *


KSSi=11.7  # []
KS=KSSi
taup=10**(-10) # [s]
taun=10**(-10) # [s]
mup=460 # [cm2/V*s]
mun=1360  # [cm2/V*s]
xn1=0.001 # [cm]
xp1=0.001 # [cm]


mnSi=1.18 # Masa del hueco en el silicio 300K) en m_e
mpSi= 0.81 

NC=fun_NCV(mnSi*me)
NV=fun_NCV(mpSi*me)


DN=fun_D(mun)
DP=fun_D(mup)
LN=fun_L(DN,taun)
LP=fun_L(DP,taup)
print("Dn=%.5e"%DN)
print("Dp=%.5e"%DP)
print("Ln=%.5e"%LN)
print("Lp=%.5e"%LP)

def main(NA,ND,Va,nombrepdfs):

    ni=fun_ni(NC,NV,EgSi,300)
    ni=1*10**(10)
    Vbi=fun_Vbi(NA,ND,ni)
    xn_aux=fun_xn(NA,ND,KSSi,Vbi)
    xp_aux=fun_xp(NA,ND,KSSi,Vbi)
    xn=fun_xn(NA,ND,KSSi,Vbi,Va)
    xp=fun_xp(NA,ND,KSSi,Vbi,Va)
    I0=cte.e*((DN*ni**2/(LN*NA))+(DP*ni**2/(LP*ND)))
    slopen=fun_slope_lineal(0,ND,KSSi)
    slopep=fun_slope_lineal(NA,0,KSSi)

    Ei=fun_Ei(ni,NA,ni)
    Ec=fun_Ec(mnSi*me,Ei,ni)
    Ev=fun_Ev(Ec)
    ni=1*10**(10)

    print("Apartado a)")
    print("NV=%.5e [cm-3]"%NV)
    print("NC=%.5e [cm-3]"%NC)
    print("ni=%.5e [cm-3]"%ni)
    print("pn=%.5e [cm^3]"%(ni**2/ND))
    print("Vbi=%.5e [V]"%Vbi)
    print("-------------------------------")
    print("-------------------------------")
    print("-------------------------------")
    print("xp pol=%.5e [cm]"%xp)
    print("xn pol=%.5e [cm]"%xn)
    print("xp eq=%.5e [cm]"%xp_aux)
    print("xn eq=%.5e [cm]"%xn_aux)
    
    print("PRIMERA TABLA")

    print("Equlibrio")
    print("Region P")
    print("Ei=%.3f"%Ei)
    print("Ec=%.3f"%Ec)
    print("Ev=%.3f"%Ev) 
    print("Region N")
    print("Ei=%.3f"%(Ei-Vbi))
    print("Ec=%.3f"%(Ec-Vbi))
    print("Ev=%.3f"%(Ev-Vbi))
    print("********")   
    print("Polarizada")
    print("Region P")
    print("Ei=%.3f"%(Ei-Va))
    print("Ec=%.3f"%(Ec-Va))
    print("Ev=%.3f"%(Ev-Va))
    print("Region N")
    print("Ei=%.3f"%(Ei-Vbi))
    print("Ec=%.3f"%(Ec-Vbi))
    print("Ev=%.3f"%(Ev-Vbi))
    print("-------------------------------")
    print("SEGUNDA TABLA")
    print("Emax0=",-(e*NA/(KS*cte.epsilon_0*10**(-2)))*(xp_aux))
    print("Emax=",-(e*NA/(KS*cte.epsilon_0*10**(-2)))*(xp))
    print("-------------------------------")
    print("TERCERA TABLA")
    print("VJ0=",Vbi)
    print("VJ=",Vbi-Va)
    print("-------------------------------")
    print("CUARTA TABLA")
    print("rhopmax0=",e*NA)
    print("rhonmax0=",e*ND)
    print("rhopmax=",e*NA)
    print("rhonmax=",e*ND)   
    print("-------------------------------")
    print("QUINTA TABLA")
    print("np0=",(ni**2)/NA)
    print("pn0=",(ni**2)/ND)
    print("Dnp=",((ni**2)/NA)*(np.exp(Va/(k*300))-1.00))
    print("Dpn=",((ni**2)/ND)*(np.exp(Va/(k*300))-1.00))
    print("-------------------------------")
    print("SEXTA TABLA")
    print("I0=",I0)
    print("I=",I0*(np.exp(Va/(k*300))-1))
    
    print("##############################")
    
    # Bandas de energía
    
    fig1=plt.figure()
    fun_grafica_bandas_pn(fig1,Ec,Ev,Vbi,Ei,slopep,slopen,xn_aux,xp_aux,LN,LP,0.0,alpha1=0.4)
    fun_grafica_bandas_pn(fig1,Ec,Ev,Vbi,Ei,slopep,slopen,xn,xp,LN,LP,Va,alpha1=1.0)
    fig1.savefig(nombrepdfs[0],bbox_inches='tight')
        
    fig2=plt.figure()
    fun_grafica_E_pn(fig2,NA,ND,KSSi,xn,xp,Va,"blue","-")
    fun_grafica_E_pn(fig2,NA,ND,KSSi,xn_aux,xp_aux,0.0,"red","--")
    plt.legend()
    plt.xlim(-0.00002,0.00003)
    fig2.savefig(nombrepdfs[1],bbox_inches='tight')

    fig3=plt.figure()
    fun_grafica_V_pn(fig3,Vbi,slopen,slopep,xn_aux,xp_aux,0.0,"red","--")
    fun_grafica_V_pn(fig3,Vbi,slopen,slopep,xn,xp,Va,"blue","-")
    plt.legend()
    plt.xlim(-0.00002,0.00003)
    fig3.savefig(nombrepdfs[2],bbox_inches='tight')

    fig4=plt.figure()
    fun_grafica_rho_pn(fig4,xn_aux,xp_aux,NA,ND,0.0,"red","--")
    fun_grafica_rho_pn(fig4,xn,xp,NA,ND,Va,"blue","-")
    plt.legend()
    plt.xlim(-0.00003,0.00003)
    fig4.savefig(nombrepdfs[3],bbox_inches='tight')
        
    fig5=plt.figure() 
    fun_grafica_minoritarios(fig2,NA,ND,ni,LP,LN,Va,xn,xp,100,100,300,True,True,"green","-.")
    plt.legend()
    #plt.xlim(-0.5*10**-4,0.5*10**-4)
    fig5.savefig(nombrepdfs[4],bbox_inches='tight')
        
    fig5=plt.figure() 
    fun_grafica_minoritarios(fig2,NA,ND,ni,LP,LN,Va,xn,xp,100,100,300,True,False,"green","-.")
    plt.legend()
    plt.xlim(-0.5*10**-4,0.5*10**-4)
    fig5.savefig(nombrepdfs[6],bbox_inches='tight')
    
    fig6=plt.figure() 
    fun_grafica_IV(fig6,I0,Va,300)
    #plt.legend()
    fig6.savefig(nombrepdfs[5],bbox_inches='tight')
    
    

    
    
nombrespdfs=["Bandas_Energia-Directa.pdf","Campo_Electrico-Directa.pdf","Potencial_Electrico-Directa.pdf","Densidad_Carga-Directa.pdf","Bandas_Minoritarios-Directa.pdf","Intensidades-Directa.pdf","Densidad_portadores_directa_cortada.pdf"]    
    
    
nombrespdfs2=["Bandas_Energia-Inversa.pdf","Campo_Electrico-Inversa.pdf","Potencial_Electrico-Inversa.pdf","Densidad_Carga-Inversa.pdf","Bandas_Minoritarios-Inversa.pdf","Intensidades-Inversa.pdf","Densidad_portadores_inversa_cortada.pdf"]    

NA=3.5*10**(16) # [cm-3]
ND=3.5*10**(16) # [cm-3]
main(NA,ND,0.25,nombrespdfs)
NA=3.5*10**(17) # [cm-3]
ND=3.5*10**(16) # [cm-3]
main(NA,ND,-0.2,nombrespdfs2)