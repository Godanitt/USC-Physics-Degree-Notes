!
!
! Para que salten los errores si algo va mal
!
!


module Mod_03_Interface

      use Mod_01_Def_prec
      use Mod_02_Variables_Comunes

      interface 
          subroutine Sub_Poltj(np,rx,ry,rz,ax,ay,az,epot,dfiv,d2fiv) 
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

end module 