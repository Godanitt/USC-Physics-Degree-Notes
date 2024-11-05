program Pro_DM

      
      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface

!################################################ VARIABLES  ##########################################################################################
!
!   VARIABLES definias en el modulo VARIABLES_COMUNES
!
!   npmax   -> Número de partículas que vamos a tener en cuenta para la simulacion (coincide con n, el número de particulas de la simulacion)
!   numk    -> Entero que nos permite calcular el numero N para crear una fcc perfecta, tal que Npmax=4*k*k*k
!   pi      -> Número pi
!   pl      -> Lado de la caja, pl=vol**(1/3)
!   pli     -> Lado inverso de la caja pli=1/pl
!   vol     -> Volumen
!   rc      -> Radio de corte, rc=pl/2.d00
!   rc2     -> Radio de corte al cuadrado rc2=rc*rc
!   dt      -> Paso del tiempo
!   dt12    -> Paso del tiempo mitad dt12=dt/2
!   dt2     -> Paso del tiempo cuadrado mitad dt2=dt*dt/2
!   Et      -> Energía total, dato del ejercicio, por eso está definida aquí  
!   corr_ener       -> Correción a la energía, le damos un valor cero para no tener problemas si después la llamamos y no esta definida
!   corr_sum_rvp    -> Correción a diferencial potencial de volumen , le damos un valor cero para no tener problemas si después la llamamos y no esta definida
!   corr_ener_r2vpp -> Correción a diferencial potencial de voluemn (2o orde), le damos un valor cero para no tener problemas si después la llamamos y no esta definida
!
!   VARIABLES IMPORTANTES (son relevantes, no auxiliares)
!
! np        -> Número de partículas con la que generamos la red. En este caso coinciden np=npmax.
! rx,ry,rz  -> Vectores posiciones de las partículas (rx(i)-> posición en x de la partícula i)
! vx,vy,vz  -> Vectores velocidades de las partículas (vy(i)-> velocidad en y de la partícula i)
! ax,ay,az  -> Vectores aceleracionse de las partículas (az(i)-> aceleracion en z de la partícula i)
! Etot      -> Suma de Ep+Ecin, debe ser igual a Et (si no algo esta mal)
! Epot      -> Energía potencial, se obtiene de la subrutina potlj
! Ecin      -> Energía cinética, debe coincidir al final con Et-fEpot
! dfiv      -> Derivada del potencial respecto el volumen, calculada con la subrutina poltj, una vez esta corregida
! d2fiv     -> Derivada 2a del potencial respecto el volumen, calculada con la subrutina poltj, una vez esta corregida 
! kpasos    -> Entero, Numero de pasos realizados en la interacción (500K en principio)
! dt        -> Real, nos dice cuanto tiempo pasa con cada paso. Nosotros usamos 10^-4, ya que es estable y no produce errores.
! dt12      -> dt/2.
! dt2       -> (dt**2)/2
! 
! ruta      -> Nos permite cambiar la dirección donde está guardado el archivo
! fname     -> Nombre del archivo no formateado (se guarda ENV)   
! gname     -> Nombre del archivo formateado (se guardan velocidades, posiciones y aceleraciones)   
!
!
!   VARIABLES AUXILIARES (no son relevantes)
!
! i         -> Entero, nos ayuda a realizar los distintos lazos
!
!##########################################################################################################################################
                                                                                                                                            
!##########################################################################################################################################
!
! Este es el programa principal del proyecto obligatorio 3 de la asginatura simulación en fisica de materiales por Daniel Vazquez Lago.
! En este programa lo que haremos es avanzar en la simulación mediante el algoritmo velocity verlet descrito en la memoria. Básicamente
! este programa lee una configuración inicial (puede ser la crea red fcc, o cualquier otra), la hace evolucionar en el tiempo, y escri-
! be al final la configuración final. A diferencia del anterior, que escribia datos para saber si estabamos en el equilibrio, en este 
! suponemos que estamos en el equilibrio, de tal manera que medimos las medias de los datos de interes para calcular las propiedades
! termodinámicas del sistema que sean de interés, como puedne ser cv y cp. 
!
! Lo que haremos será una simulación de 5M de pasos, separadas en 10 de 500K pasos. Para eso usaremos el .bat (véase memoria). 
!
!##########################################################################################################################################

      implicit none

      ! Definimos las variables

      real(kind=doblep) :: Etot,Ecin,Epot,dfiv,d2fiv,Ecin_inv
    
      integer(kind=entero) :: kpasos,i,np,numero
      real(kind=doblep) :: rx(Npmax),ry(Npmax),rz(Npmax)
      real(kind=doblep)  :: ax(Npmax),ay(Npmax),az(Npmax)
      real(kind=doblep) :: vx(Npmax),vy(Npmax),vz(Npmax)
      real(kind=doblep) :: rxx(500000/100,Npmax),ryy(500000/100,Npmax),rzz(500000/100,Npmax)
      real(kind=doblep) :: vxx(500000/100,Npmax),vyy(500000/100,Npmax),vzz(500000/100,Npmax)
      
      integer(kind=entero) :: j 
      real(kind=doblep) :: Ec_media,Ecinv_media,dfiv_media,d2fiv_media,dfivEcinInv_media,dfiv2EcinInv_media,Et_media,Ep_media
      real(kind=doblep) :: f,factor,T,P,CV,alphaE,gammaB,ks_inv,factor2
    
      character(LEN=25) :: gname,fname
      character(LEN=50) :: gname1,gname2,gname3,gname4
      character(LEN=15) :: ruta
      character(LEN=26) :: ruta2
      character(LEN=2)  :: Char_val
      
      ! Leemos a teclado la interacción que corresponde (cada interacción 500K pasos, 10 interacciones total)
      ! Recoradmos que aunque se pida a teclado la enviamos con un archivo de lotes (.bat)
      
      !write(*,*) 'Pedimos dato a teclado:'
      read(*,8001)j,numero

      ! Damos valores a los pasa timepo, aunque tambien se vayan a leer (esto lo hacemos para que no haya errores)

      dt=0.0001d00
      dt12=dt/2.d00
      dt2=dt*dt/2.d00

!     Damos valores a los valores medios, iguales a cero en un principio
      
      Et_media=0.d00
      Ep_media=0.d00
      Ec_media=0.d00
      Ecinv_media=0.d00
      dfiv_media=0.d00
      d2fiv_media=0.d00
      dfivEcinInv_media=0.d00
      dfiv2EcinInv_media=0.d00   
      
      f=0.d00 ! grados de libertad
      factor=0.d00
    
      T=0.d00
      P=0.d00
      CV=0.d00
      alphaE=0.d00
      gammaB=0.d00
      ks_inv=0.d00

      
      ! Definimos los nombres de los archivos y la ruta.
      WRITE(char_val, '(i2.2)') j

      fname='Datos_basicos.dat'      
      ruta='../../../Datos/' 
      ruta2='../../../Datos/Optativo2/' 
      gname1='Datos_Valores_medios_energias.dat' 
      gname2='Datos_valores_medios.dat'
      gname3='Datos_Posiciones_DM_'//Char_val//'.dat'
      gname4='Datos_Velocidades_DM_'//Char_val//'.dat'

      write(*,*)gname3,gname4

      ! Leemos la carpeta donde están los datos más interesantes

      open (10,file=ruta//fname, STATUS='OLD', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol, dens
      read (10,9003) Etot,Ecin,Epot
      read (10,9005) Dt,kpasos
      read (10,8000) ruta
      read (10,9000) fname 
      read (10,9000) gname
      close(10)

      ! inicializamos los archivos de datos, ademas damos valores interesantes para calcular posteriores medias    

      if (j.eq.1) then      
         open(50,file=ruta//gname1,status='old')
         write(50,9500)vol,numero
         close(50)
         open(60,file=ruta//gname2,status='old')
         write(60,9500)vol,numero
         close(60)
      endif  
    

      ! Número de pasos (5K si viene de fcc, 500K si no) -> Debería leerse bien en kpasos, pero por si acaso lo volvemos a definir.

      kpasos=500000
      
      ! Leemos la configuración inicial (posiciones, velocidades, aceleraciones) de las 500 partículas

      open (20,file=ruta//gname,form="unformatted", STATUS='OLD', ACTION='READ')  
      read (20) rx,ry,rz,vx,vy,vz,ax,ay,az
      close(20)

      

      ! Comenzamos el lazo. En cada paso avanzamos 0.0001 en el tiempo. Hacemos un número kpasos  de pasos
      
      do i=1,kpasos
            ! Llamamos a la subrutina verlet, recibiendo una configuración de entrada, devolviendo la del insatnte posterior
            call SUB_VERLET(np,rx,ry,rz,vx,vy,vz,ax,ay,az,epot,dfiv,d2fiv)         
            Ecin=(Dot_Product(vx,vx)+Dot_Product(vy,vy)+Dot_Product(vz,vz))
            Ecin_inv=1/Ecin        
    
            Et_media=Et_media+Ecin+Epot*2.d00
            Ep_media=Ep_media+Epot
            Ec_media=Ec_media+Ecin
            Ecinv_media=Ecinv_media+Ecin_inv
            dfiv_media=dfiv_media+dfiv
            d2fiv_media=d2fiv_media+d2fiv
            dfivEcinInv_media=dfivEcinInv_media+dfiv*Ecin_inv
            dfiv2EcinInv_media=dfiv2EcinInv_media+dfiv*dfiv*Ecin_inv
            if (modulo(i,100).eq.0) then
                rxx(i/100,:)=rx
                ryy(i/100,:)=ry
                rzz(i/100,:)=rz
                vxx(i/100,:)=vx
                vyy(i/100,:)=vy
                vzz(i/100,:)=vz
            endif
            if (modulo(i,100000).eq.0) then
                write(*,*)'Llevamos ', i,' pasos. Numero de interaccion: ',j,' La enerita total media',Et_media/2.d00/dble(i+1)
            endif
      enddo

      ! Calculamos los valores meidos de las energias potenciales, totales y cineticas, asi como otros valores de interes para calcular las propiedades macroscopicas

      Et_media=(Et_media)/(2.d00*dble(kpasos))
      Ep_media=(Ep_media)/(dble(kpasos))
      Ec_media=(Ec_media)/(2.d00*dble(kpasos))
      Ecinv_media=2.d00*Ecinv_media/((dble(kpasos)))
      dfiv_media=dfiv_media/(dble(kpasos))
      d2fiv_media=d2fiv_media/(dble(kpasos))
      dfivEcinInv_media=2.d00*dfivEcinInv_media/(dble(kpasos))
      dfiv2EcinInv_media=2.d00*dfiv2EcinInv_media/(dble(kpasos))

      
      
      open(50,file=ruta//gname1,position='APPEND')
      write(50,9007) 'Interaccion 500K pasos Número:',j
      write(50,9006) 'Ec_tot=',Et_media
      write(50,9006) 'Ec_pot=',Ep_media
      write(50,9006) 'Ec_media=',Ec_media
      write(50,9006) 'Ecinv_media=',Ecinv_media
      write(50,9006) 'dfiv_media=',dfiv_media
      write(50,9006) 'd2fiv_media=',d2fiv_media
      write(50,9006) 'dfivEcinInv_media=',dfivEcinInv_media
      write(50,9006) 'd2fivEcinInv_media=',dfiv2EcinInv_media
      write(50,9000) '##############################'
      close(50)

      f=3.d00*dble(np)-3.d00 ! grados de libertad
      factor=2.d00/f-1.d00
    
      T=2.d00*Ec_media/f
      P=np*T/vol-dfiv_media
      CV=1.d00/(1+factor*Ec_media*Ecinv_media)
      alphaE=1/(Vol*(-factor*Ec_media*dfivEcinInv_media-dfiv_media))
      gammaB=Npmax/CV+vol*(f/2.d00-1)*(dfiv_media*Ecinv_media-dfivEcinInv_media)

      factor2=vol*(dfiv2EcinInv_media-2.d00*dfiv_media*dfivEcinInv_media+Ecinv_media*dfiv_media*dfiv_media)
      ks_inv=(Np*T/vol)*(1.d00+2.d00*gammaB-Np/CV)+Vol*d2fiv_media+(f/2.d00-1)*factor2

      open(60,file=ruta//gname2,position='APPEND')
      
      write(60,9007) 'Interaccion 500K pasos Número:',j
      write(60,9006) 'T=',T
      write(60,9006) 'P=',P
      write(60,9006) 'CV=',CV
      write(60,9006) 'alphaE=',alphaE
      write(60,9006) 'gamma=',gammaB
      write(60,9006) '1/ks=',ks_inv
      write(60,9000) '##############################'
      close(60)

      
!     Ahora abrimos los archivos para escribir en los mismos que se leyó la nueva configuración. Escribe por encima de los anteriores, 
!     de tal manera que los primeros son irrecuperables.
      
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

      open (21,file=ruta2//gname3,form='unformatted', ACTION='WRITE')  
      write(21)rxx,ryy,rzz
      close(21)
      open (22,file=ruta2//gname4,form='unformatted',ACTION='WRITE')  
      write(22)vxx,vyy,vzz
      close(22)

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
 
        

end program