module Mod_02_Variables_comunes

      use Mod_01_Def_prec

      
!################################################ VARIABLES  ##########################################################################################
!
!   npmax   -> Número de partículas que vamos a tener en cuenta para la simulacion (coincide con n, el número de particulas de la simulacion)
!   numk    -> Entero que nos permite calcular el numero N para crear una fcc perfecta, tal que Npmax=4*k*k*k
!   pi      -> Número pi
!   pl      -> Lado de la caja, pl=vol**(1/3)
!   pli     -> Lado inverso de la caja pli=1/pl
!   vol     -> Volumen
!   rc      -> Radio de corte, rc=pl/2.d00
!   rc2     -> Radio de corte al cuadrado rc2=rc*rc
!   dt      -> Paso del tiempo
!   dt12    -> Paso del tiempo mitad dt12=dt/2
!   dt2     -> Paso del tiempo cuadrado mitad dt2=dt*dt/2
!   Et      -> Energía total, dato del ejercicio, por eso está definida aquí  
!   corr_ener       -> Correción a la energía, le damos un valor cero para no tener problemas si después la llamamos y no esta definida
!   corr_sum_rvp    -> Correción a diferencial potencial de volumen , le damos un valor cero para no tener problemas si después la llamamos y no esta definida
!   corr_ener_r2vpp -> Correción a diferencial potencial de voluemn (2o orde), le damos un valor cero para no tener problemas si después la llamamos y no esta definida
!
!##############################################################################################################################################

      
      implicit none      

      integer (kind=entero), parameter ::npmax=500,numk=5,rv=8*6*npmax+8 !npmax
      real (kind=doblep), parameter :: pi=3.1415926535898d00,T=1.461
      real (kind=doblep) :: pl,pli,vol,dens,rc,rc2,dt,dt12,dt2,dti,Et=-575.d00
      real (kind=doblep) :: corr_ener=0.d00,corr_sum_rvp=0.d00,corr_sum_r2vpp=0.d00


end module Mod_02_Variables_comunes