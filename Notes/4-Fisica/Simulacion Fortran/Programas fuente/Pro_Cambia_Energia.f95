program Pro_Cambia_Energia


      
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

      real(kind=doblep) :: Ecin,Epot,dfiv,d2fiv,E,Ecinaux
      integer(kind=entero) :: iter,i,np,kpasos
      real(kind=doblep) :: rx(Npmax),ry(Npmax),rz(Npmax)
      real(kind=doblep)  :: ax(Npmax),ay(Npmax),az(Npmax)
      real(kind=doblep) :: vx(Npmax),vy(Npmax),vz(Npmax)
      real(kind=doblep) :: pt,pt1,Eaux,px,py,pz,Ecinaux

    
      character(LEN=25) :: gname,fname
      character(LEN=50) :: gname2
      character(LEN=15) :: ruta

      fname='Datos_basicos.dat'
      gname2='Datos_energia_dm.dat'   
      ruta='../../../Datos/'       
      
      open (10,file=ruta//fname, STATUS='OLD', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol,dens
      read (10,9003) E,Ecin,Epot
      read (10,9005) dt,kpasos
      read (10,8000) ruta
      read (10,9000) fname 
      read (10,9000) gname
      close(10)
      
     ! write(*,*) np, gname
      
      open (20,file=ruta//gname,form='unformatted', STATUS='OLD', ACTION='READ')  
      read (20) rx,ry,rz,vx,vy,vz,ax,ay,az
      close(20)
      write(*,*)'Comprobamos bien que la energia cinetica guardada coincide con la energia cinetica real:'
      write(*,*)'Ecin=',Ecin
      Ecin=(Dot_Product(vx,vx)+Dot_Product(vy,vy)+Dot_Product(vz,vz))/2
      write(*,*)'Ecin=',Ecin
      
      write(*,*)'############################'
      
!###########################################################################################################      
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
      
      Ecinaux=Ecin    
    
      Ecin=Et-Epot

      pt=sqrt(Ecinaux*2.d00)
      
      print*,'Ecin2',pt*pt/2.d00
      pt1=1/pt
          
      Eaux=(2.d00*Ecin)**(0.5d00)
      
      vx=vx*Eaux*pt1
      vy=vy*Eaux*pt1
      vz=vz*Eaux*pt1
      
    

      
!####################### ACABAMOS ################################################################ 
 
      write(*,*)'############################'
      
      write(*,*)'Comprobamos bien que la energia total como suma de ambas es 575.00:'
      write(*,*)'Ecin=',Ecin,'Epot',Epot
      write(*,*)'Etot',Ecin+Epot 
      write(*,*)Ecin+Epot+575.d00
      
      open (10,file=ruta//fname, STATUS='OLD', ACTION='WRITE')  
      write (10,9001) np,pl,pli,rc,rc2
      write (10,9002) vol, dens
      write (10,9003) Ecin+Epot,Ecin,Epot
      write (10,9005) dt, kpasos
      write (10,8000) ruta
      write (10,9000) fname 
      write (10,9000) gname
      close(10)

     ! write(*,*) np, gname
      
      open (20,file=ruta//gname,form='unformatted', STATUS='OLD', ACTION='WRITE')  
      write (20) rx,ry,rz,vx,vy,vz,ax,ay,az
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
