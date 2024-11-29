program Pro_DM_NVT

      
      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface

      implicit none

      ! Definimos las variables

      real(kind=doblep) :: Etot,Ecin,Epot,dfiv,d2fiv,Ecin_inv
    
      integer(kind=entero) :: kpasos,i,np,numero
      real(kind=doblep) :: rx(Npmax),ry(Npmax),rz(Npmax)
      real(kind=doblep)  :: ax(Npmax),ay(Npmax),az(Npmax)
      real(kind=doblep) :: vx(Npmax),vy(Npmax),vz(Npmax)
      !real(kind=doblep) :: bx(Npmax),by(Npmax),bz(Npmax)
      !real(kind=doblep) :: cx(Npmax),cy(Npmax),cz(Npmax)
      !real(kind=doblep) :: dx(Npmax),dy(Npmax),dz(Npmax)
      
      real(kind=doblep) :: rxx(500000/100,Npmax),ryy(500000/100,Npmax),rzz(500000/100,Npmax)
      real(kind=doblep) :: vxx(500000/100,Npmax),vyy(500000/100,Npmax),vzz(500000/100,Npmax)
      
      integer(kind=entero) :: j 
      real(kind=doblep) :: Ec_media,Et_media
      real(kind=doblep) :: f,P,CV,gammaB,ks_inv
    
      character(LEN=28) :: gname,fname
      character(LEN=50) :: gname1,gname2,gname3,gname4
      character(LEN=25) :: ruta
      character(LEN=2)  :: Char_val

      ! Vamos a definir cosas exclusivsas de NVT
      
      real(kind=doblep) :: varphi,varphiV,varphiVV,varphi2,varphi2V,varphiV2
      

      ! Vamos a definir los que son exclusivos de gear5

      real(kind=doblep) :: s,vs,as,Q
      real(kind=doblep) :: bx(Npmax),by(Npmax),bz(Npmax)
      real(kind=doblep) :: cx(Npmax),cy(Npmax),cz(Npmax)
      real(kind=doblep) :: dx(Npmax),dy(Npmax),dz(Npmax)

      
      
      
      ! Leemos a teclado la interacción que corresponde (cada interacción 500K pasos, 10 interacciones total)
      ! Recoradmos que aunque se pida a teclado la enviamos con un archivo de lotes (.bat)
      
      !write(*,*) 'Pedimos dato a teclado:'
     ! read(*,8001)j,numero

      ! Aqui incluimos las condiciones de contorno para calcular los valores de la b,c,d en un primer caso.
     
      bx=0.d00
      by=0.d00
      bz=0.d00
      cx=0.d00
      cy=0.d00
      cz=0.d00
      dx=0.d00
      dy=0.d00
      dz=0.d00
      

      ! Damos valores a los pasa timepo, aunque tambien se vayan a leer (esto lo hacemos para que no haya errores)

      dt=0.0001d00
      dt12=dt/2.d00
      dt2=dt*dt/2.d00
      dti=1/dt

!     Inicializamos s,ds,as,Q

      s=1.d00
      vs=0.d00
      as=0.d00
      Q=1.d00    

!     Damos valores a los valores medios, iguales a cero en un principio
            ! grados de libertad

      Ecin=0.d00
      Et_media=0.d00
      Ec_media=0.d00
      Epot=0.d00
      varphi=0.d00
      varphiV=0.d00
      varphiVV=0.d00
      varphi2=0.d00
      varphi2V=0.d00
      varphiV2=0.d00
      
      P=0.d00
      CV=0.d00
      gammaB=0.d00
      ks_inv=0.d00
      
      j=0

      
      ! Definimos los nombres de los archivos y la ruta.
      WRITE(char_val, '(i2.2)') j

      fname='Datos_basicos_DM_NVT.dat'      
      ruta='../../../Datos/Optativo4/' 
      gname='Datos_particulas_DM_NVT.dat'      
      gname1='Datos_Valores_medios_energias_DM_NVT.dat' 
      gname2='Datos_Valores_medios_DM_NVT.dat'
      gname3='Posiciones_DM_NVT_'//Char_val//'.dat'
      gname4='Velocidades_DM_NVT_'//Char_val//'.dat'

      write(*,*)gname3,gname4

      ! Leemos la carpeta donde están los datos más interesantes
      
      open (10,file=ruta//fname, STATUS='old', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol, dens
      read (10,9003) Etot,Ecin,Epot
      read (10,9003) s,vs,as
      read (10,9005) dt,kpasos
      read (10,8000) ruta
      read (10,9000) fname 
      read (10,9000) gname
      close(10)  
      f=dble(np)*3.d00-3.d00   

      ! inicializamos los archivos de datos, ademas damos valores interesantes para calcular posteriores medias    

      if (j.eq.1) then      
         open(50,file=ruta//gname1,status='new')
         write(50,9500)vol,numero
         close(50)
         open(60,file=ruta//gname2,status='new')
         write(60,9500)vol,numero
         close(60)
      endif  
    

      ! Número de pasos (5K si viene de fcc, 500K si no) -> Debería leerse bien en kpasos, pero por si acaso lo volvemos a definir.

      kpasos=500000
      
      ! Leemos la configuración inicial (posiciones, velocidades, aceleraciones) de las 500 partículas

      gname='Datos_particulas_DM_NVT.dat' 
      ruta='../../../Datos/Optativo4/' 

      open (20,file=ruta//gname,form="unformatted", STATUS='old', ACTION='READ')  
      read (20) rx,ry,rz,vx,vy,vz,ax,ay,az,bx,by,bz,cx,cy,cz,dx,dy,dz
      close(20)

      

      ! Comenzamos el lazo. En cada paso avanzamos 0.0001 en el tiempo. Hacemos un número kpasos  de pasos
      
      f=3.d00*dble(np)-3.d00 ! grados de libertad

      open(80,file=ruta//'Energias-Equilibracion.dat',status='old',action='write')
      do i=1,kpasos
            ! Llamamos a la subrutina verlet, recibiendo una configuración de entrada, devolviendo la del insatnte posterior
            call SUB_GEAR5(np,rx,ry,rz,vx,vy,vz,ax,ay,az,bx,by,bz,cx,cy,cz,dx,dy,dz,s,vs,as,Epot,dfiv,d2fiv,Q,f)        
            Ecin=(Dot_Product(vx,vx)+Dot_Product(vy,vy)+Dot_Product(vz,vz))*(s*s)

            Et_media=Et_media+Ecin+2.d00*Epot
            Ec_media=Ec_media+Ecin
              
            varphi=varphi+Epot
            varphiV=varphiV+dfiv
            varphiVV=varphiVV+d2fiv
            varphi2=varphi2+Epot*Epot
            varphi2V=varphi2V+Epot*dfiv
            varphiV2=varphiV2+dfiv*dfiv
            
            ! Guardamos las cosas para el calculo de factores dinámicos (coeficiente de difusion, tensor de viscosidad)
            if (modulo(i,100).eq.0) then
                rxx(i/100,:)=rx
                ryy(i/100,:)=ry
                rzz(i/100,:)=rz
                vxx(i/100,:)=vx*s
                vyy(i/100,:)=vy*s
                vzz(i/100,:)=vz*s
            endif
            ! Guardamos las cosas para la equilibracion
            if (modulo(i,50).eq.0) then
                write(80,9003) Ecin/2.d00+Epot,Ecin/2.d00,Epot
            endif
      enddo
      close(80)
      
      

      ! Calculamos los valores meidos de las energias potenciales, totales y cineticas, asi como otros valores de interes para calcular las propiedades macroscopicas

      Et_media=Et_media/(2.d00*dble(kpasos))
      Ec_media=Ec_media/(2.d00*dble(kpasos))
      varphi=varphi/(dble(kpasos))
      varphiV=varphiV/(dble(kpasos))
      varphiVV=varphiVV/(dble(kpasos))
      varphi2=varphi2/(dble(kpasos))
      varphi2V=varphi2V/(dble(kpasos))
      varphiV2=varphiV2/(dble(kpasos))


      f=3.d00*(np-1) ! Grados de libertad  
      P=Np*T/Vol-varphiV
      CV=f/2.d00 + (varphi2-varphi*varphi)/(T*T)
      gammaB=(Vol/CV)*(np/vol+(varphi*varphiV-varphi2V)/(T*T))
      ks_inv=np*T/vol+Vol*varphiVV-(Vol/T)*(varphiV2-varphiV*varphiV)
      
      fname='Datos_basicos_DM_NVT.dat'      
      ruta='../../../Datos/Optativo4/' 
      gname='Datos_particulas_DM_NVT.dat'      
      gname1='Datos_Valores_medios_energias_DM_NVT.dat' 
      gname2='Datos_Valores_medios_DM_NVT.dat'
      gname3='Posiciones_DM_NVT_'//Char_val//'.dat'
      gname4='Velocidades_DM_NVT_'//Char_val//'.dat'


      open (22,file=ruta//gname1,STATUS='old', ACTION='WRITE')  
      write(22,9007) 'Interaccion 500K pasos Número:',j
      write(22,9006) 'Ec_tot=',Et_media
      write (22,9006) 'varphi=',varphi
      write(22,9006) 'Ec_media=',Ec_media
      write (22,9006) 'varphiV=',varphiV
      write (22,9006) 'varphiVV=',varphiVV
      write (22,9006) 'varphi2=',varphi2
      write (22,9006) 'varphi2V=',varphi2V
      write (22,9006) 'varphiV2=',varphiV2
      write(22,9000) '##############################'
      close(22)
      open (23,file=ruta//gname2,STATUS='old', ACTION='WRITE')  
      write(23,9007) 'Interaccion 500K pasos Número:',j
      write (23,9006) 'P=',P
      write (23,9006) 'CV=',CV
      write (23,9006) 'gammaB=',gammaB
      write (23,9006) 'ks_inv=',ks_inv
      write(23,9000) '##############################'
      close(23)



      
!     Ahora abrimos los archivos para escribir en los mismos que se leyó la nueva configuración. Escribe por encima de los anteriores, 
!     de tal manera que los primeros son irrecuperables.
      
      open (10,file=ruta//fname, STATUS='OLD', ACTION='WRITE')  
      write (10,9001) np,pl,pli,rc,rc2
      write (10,9002) vol, dens
      write (10,9003) Ecin+Epot,Ecin,Epot
      write (10,9003) s,vs,as
      write (10,9005) Dt,kpasos
      write (10,8000) ruta
      write (10,9000) fname 
      write (10,9000) gname
      close(10)
      
      open (20,file=ruta//gname,form='unformatted', STATUS='UNKNOWN', ACTION='WRITE')  
      write(20) rx,ry,rz,vx,vy,vz,ax,ay,az,bx,by,bz,cx,cy,cz,dx,dy,dz
      close(20)

      open (21,file=ruta//gname3,form='unformatted', ACTION='WRITE')  
      write(21)rxx,ryy,rzz
      close(21)
      open (24,file=ruta//gname4,form='unformatted',ACTION='WRITE')  
      write(24)vxx,vyy,vzz
      close(24)

!      Formatos usado para leer/escribir a lo largo de la simulación

 8000 format(a15)
 8001 format(i4,i4)
 9000 format(a25)
 9001 format(i4,2x,1pe19.12,3(2x,e19.12)) ! -> el 19.12 es perfecto para los decimales, mientras que el 1pe ya sabemos que es por la potenciación. Lo ultimo 3(3x,e19.12) quiere decir que 3 veces con el mismo formato 
 9002 format(1pe19.12,2x,e19.12)
 9003 format(1pe19.12,2x,e19.12,2x,e19.12)
 9005 format(1pe19.12,2x,i6)
 9006 format(a15,2x,1pe19.12)
 9007 format(a35,2x,i4)
 9500 format(1pe19.12,2x,i4)
 
      pause

end program