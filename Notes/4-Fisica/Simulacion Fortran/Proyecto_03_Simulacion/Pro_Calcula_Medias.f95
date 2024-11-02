program Pro_Calcula_Medias

      implicit none
      
      integer, parameter::entero=SELECTED_INT_KIND(9)
      integer, parameter::doblep=SELECTED_REAL_KIND(15,307)

!     Variables del modulo de valores comunes

      integer (kind=entero), parameter ::npmax=500,numk=5,rv=8*6*npmax+8 !npmax
      real (kind=doblep), parameter :: pi=3.1415926535898d00
      real (kind=doblep) :: pl,pli,vol,dens,rc,rc2,dt,dt12,dt2,Et=-575.d00
      real (kind=doblep) :: corr_ener=0.d00,corr_sum_rvp=0.d00,corr_sum_r2vpp=0.d00

!     Variables que necesitamos      


      open(50,file=ruta//gname1)
      read(50,9007) 'Interaccion 500K pasos Número:',j
      read(50,9006) 'Ec_tot=',Et_media
      read(50,9006) 'Ec_media=',Ec_media
      read(50,9006) 'Ecinv_media=',Ecinv_media
      read(50,9006) 'dfiv_media=',dfiv_media
      read(50,9006) 'd2fiv_media=',d2fiv_media
      read(50,9006) 'dfivEcinInv_media=',dfivEcinInv_media
      read(50,9006) 'd2fivEcinInv_media=',dfiv2EcinInv_media
      read(50,9000) '##############################'
      close(50)
      open(60,file=ruta//gname2)
      
      read(60,9007) 'Interaccion 500K pasos Número:',j
      read(60,9006) 'T=',T
      read(60,9006) 'P=',P
      read(60,9006) 'CV=',CV
      read(60,9006) 'alphaE=',alphaE
      read(60,9006) 'gamma=',gammaB
      read(60,9006) '1/ks=',ks_inv
      read(60,9000) '##############################'
      close(60)


 9000 format(a25)
 9006 format(a15,2x,1pe19.12)
 9007 format(a35,2x,i4)

end program
      