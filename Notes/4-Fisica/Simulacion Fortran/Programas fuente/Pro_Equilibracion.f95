program Pro_Equilibracion

      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface

      implicit none

      real(kind=doblep) :: E,Ecin,Epot,dfiv,d2fiv
      integer(kind=entero) :: kpasos,i,np
      real(kind=doblep) :: rx(Npmax),ry(Npmax),rz(Npmax)
      real(kind=doblep)  :: ax(Npmax),ay(Npmax),az(Npmax)
      real(kind=doblep) :: vx(Npmax),vy(Npmax),vz(Npmax)
    
      character(LEN=25) :: gname,fname,vname1,vname2,vname3
      character(LEN=50) :: gname1
      character(LEN=15) :: ruta


      dt=0.0001d00
      dt12=dt/2.d00
      dt2=dt*dt/2.d00
      
      fname='Datos_basicos.dat'      
      gname1='Datos_energia_equilibracion.dat'      
      vname1='Datos_vx.dat'    
      vname2='Datos_vy.dat'    
      vname3='Datos_vz.dat'    
      ruta='../../../Datos/'  

      open (10,file=ruta//fname, STATUS='OLD', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol, dens
      read (10,9003) E,Ecin,Epot
      read (10,9005) Dt,kpasos
      read (10,8000) ruta
      read (10,9000) fname 
      read (10,9000) gname
      close(10)
    
      kpasos=500000 
      
      open (20,file=ruta//gname,form="unformatted", STATUS='OLD', ACTION='READ')  
      read (20) rx,ry,rz,vx,vy,vz,ax,ay,az
      close(20)

    
      
      open (30,file=ruta//gname1,STATUS='UNKNOWN')
      open (41,file=ruta//vname1,form="unformatted")
      open (42,file=ruta//vname2,form="unformatted")
      open (43,file=ruta//vname3,form="unformatted")
      do i=0,kpasos
            call SUB_VERLET(np,rx,ry,rz,vx,vy,vz,ax,ay,az,epot,dfiv,d2fiv)         
            Ecin=(Dot_Product(vx,vx)+Dot_Product(vy,vy)+Dot_Product(vz,vz))/2
            
            if (modulo(i,100).eq.0) then
                 write(30,9004) Ecin+Epot,Ecin,Epot
                 write(41)vx 
                 write(42)vy
                 write(43)vz
                 if (modulo(i,10000).eq.0) then
                   write(*,*)i
                 endif  
            endif       
      enddo
      
      close(30)
      close(41)
      close(42)
      close(43)
      
      
      open (10,file=ruta//fname, STATUS='OLD', ACTION='WRITE')  
      write (10,9001) np,pl,pli,rc,rc2
      write (10,9002) vol, dens
      write (10,9003) Ecin+Epot,Ecin,Epot
      write (10,9005) Dt,kpasos
      write (10,8000) ruta
      write (10,9000) fname 
      write (10,9000) gname
      close(10)
      
      open (20,file=ruta//gname,form='unformatted', STATUS='OLD', ACTION='WRITE')  
      write(20) rx,ry,rz,vx,vy,vz,ax,ay,az
      close(20)


 8000 format(a15)
 9000 format(a25)
 9001 format(i4,2x,1pe19.12,3(2x,e19.12)) ! -> el 19.12 es perfecto para los decimales, mientras que el 1pe ya sabemos que es por la potenciación. Lo ultimo 3(3x,e19.12) quiere decir que 3 veces con el mismo formato 
 9002 format(1pe19.12,2x,e19.12)
 9003 format(1pe19.12,2x,e19.12,2x,e19.12)
 9004 format(1pe19.12,2x,e19.12,2x,e19.12)
 9005 format(1pe19.12,2x,i6)
 
      pause 
      
        

end program