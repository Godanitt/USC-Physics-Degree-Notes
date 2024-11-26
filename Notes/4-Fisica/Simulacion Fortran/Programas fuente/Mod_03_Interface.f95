module Mod_03_Interface

      use Mod_01_Def_prec
      !use Mod_02_Variables_Comunes


!##############################################################################################################################################
!
! En este modulo aplicamos el comando interface a todas las subrutinas usadas a lo largo de la asignatura. 
!
! De esta manera podremos controlar adecuadamente la entrada y salida de datos (por ejemplo, nos permitiría saber si estamos modificando
! una variable de entrada en la subrutina, ya que saltaría un error claro y evidente). También nos facilita saber si estamos introducien-
! do variables de salida o entrada no definidas adecuadamente (sacarla como real pero que esté definida como entera).
!
!##############################################################################################################################################



      interface 
          subroutine Sub_Potlj(np,rx,ry,rz,ax,ay,az,epot,dfiv,d2fiv) 
            integer (kind=entero), intent(in) :: np
            real(kind=doblep), dimension(:), intent(in):: rx,ry,rz
            real(kind=doblep),intent(out) :: Epot,dfiv,d2fiv
            real(kind=doblep),dimension(:) ::  ax,ay,az
          end subroutine
      end interface

      interface 
          subroutine SUB_VERLET(np,rx,ry,rz,vx,vy,vz,ax,ay,az,epot,dfiv,d2fiv)     
            integer (kind=entero), intent(in) :: np
            !real(kind=doblep),intent(in)::dt,dt12,dt2
            real(kind=doblep), dimension(:) :: rx,ry,rz
            real(kind=doblep),dimension(:) ::  vx,vy,vz
            real(kind=doblep),dimension(:) ::  ax,ay,az  
            real(kind=doblep),intent(out) :: Epot,dfiv,d2fiv
          end subroutine
      end interface
      
      interface 
          subroutine Sub_Corr_Energia(vx,vy,vz,Epot,Ecinaux)
            integer(kind=entero) :: i
            real(kind=doblep),dimension(:) :: vx,vy,vz
            real(kind=doblep) ::px,py,pz,pt,pt1
            real(kind=doblep), intent(in) :: Epot, Ecinaux
            real(kind=doblep) :: Ecin
          end subroutine
      end interface

      interface
          subroutine SUB_POTLJ_NVT_MONTECARLO(np,part,rx,ry,rz,rxnew,rynew,rznew,Eaux_2,Eaux,pl,pli,rc,rc2,vol)  
            integer(kind=entero), intent(in) :: np,part
            real(kind=doblep), dimension(:) :: rx,ry,rz
            real(kind=doblep), intent(in) :: rxnew,rynew,rznew
            real(kind=doblep), intent(in) :: vol,pl,pli,rc,rc2
            real(kind=doblep),intent(out) :: Eaux,Eaux_2
          end subroutine
      end interface


      interface
          subroutine SUB_POTLJ_2(np,rx,ry,rz,epot,dfiv,d2fiv,pl,pli,rc,rc2,vol)  
            integer(kind=entero), intent(in) :: np,part
            real(kind=doblep), dimension(:) :: rx,ry,rz
            real(kind=doblep), intent(in) :: rxnew,rynew,rznew
            real(kind=doblep), intent(in) :: vol,pl,pli,rc,rc2
            real(kind=doblep),intent(out) :: Epot,dfiv,d2fiv
          end subroutine
      end interface
end module 