subroutine Sub_Corr_Energia(vx,vy,vz,Ecin,Epot)

      
      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface
      
      implicit none
      

      real(kind=doblep),dimension(:) :: vx,vy,vz
      real(kind=doblep) :: px,py,pz,pt,pt1,Eaux
      real(kind=doblep), intent(in) :: Epot
      real(kind=doblep), intent(out) :: Ecin
      
      
      
      Ecin=Et-Epot
      print*,'Et=',Et
      print*,'Ecin=',Ecin
      print*,'Epot=',Epot

      px=Dot_Product(vx,vx)
      py=Dot_Product(vy,vy)
      pz=Dot_Product(vz,vz) !funciona exactamente igual con sum(vz*vz)

      pt=sqrt(px+py+pz)
      
      pt1=1/pt
          
      Eaux=sqrt(2.d00*Ecin)
      
      vx=vx*Eaux*pt1
      vy=vy*Eaux*pt1
      vz=vz*Eaux*pt1
      
      
      px=Dot_Product(vx,vx)
      py=Dot_Product(vy,vy)
      pz=Dot_Product(vz,vz)
      !print*,'sum(px)=',(px)
      !print*,'sum(py)=',(py)
      !print*,'sum(pz)=',(pz)

      Ecin=(px+py+pz)/2      
      print*,'*************'
      print*,'Et=',Et
      print*,'Ecin=',Ecin
      print*,'Epot=',Epot
      print*,'*************'


end subroutine