subroutine Verlet(np,rx,ry,rz,vx,vy,vz,ax,ay,az,epot,dfiv,d2fiv)     
   
      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface
       
      integer (kind=entero), intent(in) :: np
      !real(kind=doblep),intent(in)::dt,dt12,dt2
      real(kind=doblep), dimension(:) :: rx,ry,rz
      real(kind=doblep),dimension(:) ::  vx,vy,vz
      real(kind=doblep),dimension(:) ::  ax,ay,az
      real(kind=doblep) :: Epot,dfiv,d2fiv
          
      rx=rx+vx*dt+ax*dt12*dt  
      ry=ry+vy*dt+ay*dt12*dt  
      rz=rz+vz*dt+az*dt12*dt  

      vx=vx+ax*dt12
      vy=vy+ax*dt12
      vz=vz+ax*dt12
    
      call SUB_POLTJ(np,rx,ry,rz,ax,ay,az,epot,dfiv,d2fiv)     

      vx=vx+ax*dt12
      vy=vy+ax*dt12
      vz=vz+ax*dt12
    
end subroutine