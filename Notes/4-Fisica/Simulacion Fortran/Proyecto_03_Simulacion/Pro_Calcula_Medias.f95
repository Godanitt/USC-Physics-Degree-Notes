program Pro_Calcula_Medias

      implicit none
      
      integer, parameter::entero=SELECTED_INT_KIND(9)
      integer, parameter::doblep=SELECTED_REAL_KIND(15,307)


!     Variables que necesitamos      
      
      integer(kind=entero) :: i,j,kpasos

      real(kind=doblep) :: kpasos2,vol
      real(kind=doblep) :: Ec(10),Ecinv(10),dfiv(10),d2fiv(10),dfivEcInv(10),dfiv2EcInv(10),Et(10),Ep(10)
      real(kind=doblep) :: T(10),P(10),Cv(10),alphaE(10),gammaB(10),ks_inv(10),factor2(10)
      
      character(LEN=9) :: ruta
      character(LEN=25) :: aux
      character(LEN=15) :: aux2
      character(LEN=50) :: gname1,gname2,gname3,gname4
      
!     Medias de las variables
      real(kind=doblep) :: Ecm,Etm,Epm
      real(kind=doblep) :: Tm,Pm,Cvm,alphaEm,gammaBm,ks_invm,ksm
      real(kind=doblep) :: alphapm,alphasm,alphaE_invm,kt_invm,Cpm,ktm,alphaE2m
      
!     Incertidumbres de las variables
      real(kind=doblep) :: Ecs,Ets,Eps
      real(kind=doblep) :: Ts,Ps,Cvs,alphaEs,gammaBs,ks_invs,kss
      real(kind=doblep) :: alphaps,alphass,alphaE_invs,kt_invs,Cps,kts,alphaE2s

      ruta='../Datos/' 
      gname1='Datos_Valores_medios_energias.dat' 
      gname2='Datos_valores_medios.dat'
      gname3='Datos_DM_NVE_medias.dat'
      gname4='Datos_DM_NVE.dat'
      
      kpasos=10 ! le damos un valor prueba
      vol=1000.d00 ! le damos valor prueba, que debe ser exactamente igual que este
        
      ! inicializamos las variables
      
      Et=0.d00 
      Ec=0.d00
      Ep=0.d00
      
      T=0.d00
      P=0.d00
      CV=0.d00
      gammaB=0.d00
      alphaE=0.d00
      ks_inv=0.d00

      
      open(50,file=ruta//gname1,status="old")
      read(50,9001) vol,kpasos
      do i=1,int(kpasos)
        read(50,9007) aux,j
        read(50,9006) aux2,Et(i)
        read(50,9006) aux2,Ep(i)
        read(50,9006) aux2,Ec(i)
        read(50,9006) aux2,Ecinv(i)
        read(50,9006) aux2,dfiv(i)
        read(50,9006) aux2,d2fiv(i)
        read(50,9006) aux2,dfivEcInv(i)
        read(50,9006) aux2,dfiv2EcInv(i)
        read(50,9000) aux
       enddo
      close(50)
      
      open(60,file=ruta//gname2,status="old")
      read(60,9001) vol,kpasos
      kpasos2=dble(kpasos)
      do i=1,int(kpasos)
        read(60,9007) aux,j
        read(60,9006) aux2,T(i)
        read(60,9006) aux2,P(i)
        read(60,9006) aux2,CV(i)
        read(60,9006) aux2,alphaE(i)
        read(60,9006) aux2,gammaB(i)
        read(60,9006) aux2,ks_inv(i)
        read(60,9000) aux
      enddo
      close(60)

!     Calculamos las medias de los arrays
      
      write(*,*)kpasos2

      Ecm=sum(Ec)/kpasos2
      Epm=sum(Ep)/kpasos2
      Etm=sum(Et)/kpasos2
      Tm=sum(T)/kpasos2
      Pm=sum(P)/kpasos2
      CVm=sum(CV)/kpasos2
      alphaEm=sum(alphaE)/kpasos2
      gammaBm=sum(gammaB)/kpasos2
      ks_invm=sum(ks_inv)/kpasos2
      ksm=1/ks_invm

!     Calculamos las propiedades restantes a partir de las anteriores
      
      vol=1000.d00 ! le damos valor prueba, que debe ser exactamente igual que este
      kt_invm=ks_invm-Tm*CVm*gammaBm*gammaBm/Vol
      ktm=1/kt_invm
      alphapm=CVm*gammaBm*kTm/vol
      alphasm=-1/(gammaBm*Tm)
      alphaE_invm=Pm*Vol/CVm-gammaBm*Tm
      alphaE2m=1/alphaE_invm
      Cpm=CVm*ks_invm/kt_invm
      
!     Calculamos las incertidumbres de las medias (las incertidumrbes no nos sirven, ahora mismo, de nada)

      Ecs=sqrt(Dot_Product(Ec-Ecm,Ec-Ecm)/((kpasos2-1)*kpasos2))
      Eps=sqrt(Dot_Product(Ep-Epm,Ep-Epm)/((kpasos2-1)*kpasos2))
      Ets=sqrt(Dot_Product(Et-Etm,Et-Etm)/((kpasos2-1)*kpasos2))
      Ts=sqrt(Dot_Product(T-Tm,T-Tm)/((kpasos2-1)*kpasos2))
      Ps=sqrt(Dot_Product(P-Pm,P-Pm)/((kpasos2-1)*kpasos2))
      CVs=sqrt(Dot_Product(CV-CVm,CV-CVm)/((kpasos2-1)*kpasos2))
!      write(*,*)Dot_Product(CV-CVm,CV-CVm)/(10*9)
      alphaEs=sqrt(Dot_Product(alphaE-alphaEm,alphaE-alphaEm)/((kpasos2-1)*kpasos2))
      gammaBs=sqrt(Dot_Product(gammaB-gammaBm,gammaB-gammaBm)/((kpasos2-1)*kpasos2))
      ks_invs=sqrt(Dot_Product(ks_inv-ks_invm,ks_inv-ks_invm)/((kpasos2-1)*kpasos2))
      kss=ks_invs/(ks_invm*ks_invm)

      
!     Calculamos las incertidumbres restantes a partir de las anteriores
       
      kt_invs=sqrt((kss/ksm)**2+(CVm*gammaBm**2*Ts/Vol)**2+(Tm*gammaBm**2*CVs/Vol)**2+(2*CVm*gammaBm*Tm*gammaBs/Vol)**2)
      kts=kt_invs/(kt_invm*kt_invm)
      alphaPs=(1/Vol)*sqrt((CVm*gammaBm*kts)**2+(gammaBm*ktm*CVs)**2+(CVm*ktm*gammaBs)**2)
      alphass=sqrt((Ts/(gammaBm*Tm**2))**2+(gammaBs/(Tm*gammaBm**2))**2)
      alphaE_invs=sqrt((Vol*Ps/CVm)**2+(Vol*Pm*CVs/(CVm**2))**2+(Tm*gammaBs)**2+(gammaBm*Ts)**2)
      alphaE2s=alphaE_invs/(alphaE_invm*alphaE_invm)
      Cps=sqrt((CVs*ktm/ksm)**2+(kts*CVm/ksm)**2+(kss*Cvm*ktm/(ksm**2))**2)
     


      open(70,file=ruta//gname3)
      write(70,9008)'$E_c^*$',Ecm,Ecs*2
      write(70,9008)'$E_p^*$',Epm,Eps*2
      write(70,9008)'$E_t^*$',Etm,Ets*2
      
      write(70,9008)'$T^*$',Tm,Ts*2      
      write(70,9008)'$P^*$',Pm,Ps*2
      write(70,9008)'$C_V^*$',CVm,Cvs*2
      write(70,9008)'$\alpha_E^*$',alphaEm,alphaEs*2
      write(70,9008)'$\gamma^*$',gammaBm,gammaBs*2
      write(70,9008)'$1/k_s^*$',ks_invm,ks_invs*2
      write(70,9008)'$k_s^*$',ksm,kss*2
      
      write(70,9008)'$\alpha_P^*$',alphaPm,alphaPs*2
      write(70,9008)'$\alpha_S^*$',alphasm,alphass*2
      write(70,9008)'$1/\alpha_{E2}^*$',alphaE_invm,alphaE_invs*2
      write(70,9008)'$\alpha_{E2}^*$',alphaE2m,alphaE2s*2
      write(70,9008)'$1/k_T^*$',kt_invm,kt_invs*2
      write(70,9008)'$k_T^*$',ktm,kts*2
      
      close(70)

      open(80,file=ruta//gname4)
     ! write(80,8000)'$E_c^*$','$E_p^*$','$E_t^*$','$T^*$','$P^*$','$C_V^*$','$\alpha_E^*$','$\gamma^*$','$1/k_s^*$'
      do i=1,int(kpasos)   
          write(80,8001) Ec(i),Ep(i),Et(i),T(i),P(i),CV(i),alphaE(i),gammaB(i),ks_inv(i)
      enddo  
      close(80)

      pause

 8000 format(9(a12,2x))
 8001 format(1pe19.12,8(2x,1e19.12))
 9000 format(a25)
 9001 format(1pe19.12,2x,i4)
 9006 format(a15,2x,1pe19.12)
 9007 format(a35,2x,i4)
 9008 format(a25,2x,1pe19.12,2x,1e19.12)

end program
      
