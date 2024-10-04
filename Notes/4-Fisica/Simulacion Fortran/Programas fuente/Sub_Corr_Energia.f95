subroutine Sub_Corr_Energia(vx,vy,vz,Epot,pt)

      
      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface
      
      implicit none
      

      real(kind=doblep),dimension(:) :: vx,vy,vz
      real(kind=doblep) :: pt1,Eaux
      real(kind=doblep), intent(in) :: Epot,pt
      real(kind=doblep):: Ecin
      
      
      
      Ecin=Et-Epot
      print*,'Et=',Et
      print*,'Ecin=',Ecin
      print*,'Epot=',Epot



      print*,'Ecin2',pt/2.d00
      pt1=1/pt
          
      Eaux=(2.d00*Ecin)**(0.5d00)
      
      vx=vx*Eaux*pt1
      vy=vy*Eaux*pt1
      vz=vz*Eaux*pt1
      
      pt=(Dot_Product(vx,vx)+Dot_Product(vy,vy)+Dot_Product(vz,vz))
      
      !print*,'sum(px)=',(px)
      !print*,'sum(py)=',(py)
      !print*,'sum(pz)=',(pz)

      Ecin=pt/2.d00      
      print*,'*************'
      print*,'Et=',Et
      print*,'Ecin=',Ecin
      print*,'Epot=',Epot
      print*,'*************'


end subroutine