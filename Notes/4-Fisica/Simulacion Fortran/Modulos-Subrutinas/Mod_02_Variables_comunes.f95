module Mod_02_Variables_comunes

      use Mod_01_Def_prec
      
      implicit none      

      integer (kind=entero), parameter ::npmax=500,numk=5,rv=8*6*npmax+8 !npmax
      real (kind=doblep), parameter :: pi=3.1415926535898d00,Et=575
      real (kind=doblep) :: pl,pli,vol,dens,rc,rc2,dt,dt12,dt2
      real (kind=doblep) :: corr_ener=0.d00,corr_sum_rvp=0.d00,corr_sum_r2vpp=0.d00


end module Mod_02_Variables_comunes