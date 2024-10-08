subroutine Sub_Corr_Energia(vx,vy,vz,Epot,Ecinaux)

      
      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface
      
      implicit none
       
!################################## VARIABLES #####################################################
!
! vx,vy,vz  -> Velocidades de las partículas
! px,py,pz  -> Variables auxiiliares que nos permiten corregir los valores de las velocidades para hacer que el momento total sea cero
! pt        -> Variable auxiliar que nos ayuda a corregir los modulos de las velocidades para que coincida con la energía que queremos
! pt1       -> Inverso de pt
! i         -> Variable auxiliar, nos permite hacer el bucle para conseguir el momento total nulo
! Epot      -> Variable de entrada, es la energía potencial del sistema 
! Ecinaux   -> Variable de entrada, nos da el valor erróneo de la energía cinética
! Ecin      -> Variable auxiliar, que nos da el valor que queremos conseguir para que se verifque T=E-V
!
!#######################################################################################

      integer(kind=entero) :: i
      real(kind=doblep),dimension(:) :: vx,vy,vz
      real(kind=doblep) :: pt,pt1,Eaux,px,py,pz
      real(kind=doblep), intent(in) :: Epot, Ecinaux
      real(kind=doblep):: Ecin

!####################### MOMENTO TOTAL NULO ################################################################
      
      
      px=sum(vx)/dble(npmax)
      py=sum(vy)/dble(npmax)
      pz=sum(vz)/dble(npmax)

      DO i=1,Npmax
          vx(i)=vx(i)-px
          vy(i)=vy(i)-py
          vz(i)=vz(i)-pz
      ENDDO

      
!####################### ENERGIA CINÉTICA E-V ################################################################      
      
      Ecin=Et-Epot


      pt=sqrt(Ecinaux*2.d00)
      print*,'Ecin2',pt*pt/2.d00
      pt1=1/pt
          
      Eaux=(2.d00*Ecin)**(0.5d00)
      
      vx=vx*Eaux*pt1
      vy=vy*Eaux*pt1
      vz=vz*Eaux*pt1
      
      pt=(Dot_Product(vx,vx)+Dot_Product(vy,vy)+Dot_Product(vz,vz))
      
      Ecin=pt/2.d00      


end subroutine