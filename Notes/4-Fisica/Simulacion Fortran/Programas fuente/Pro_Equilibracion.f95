program Pro_Equilibracion

      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface

!################################################ VARIABLES  ##########################################################################################
!
!   VARIABLES definias en el modulo VARIABLES_COMUNES
!
!   npmax   -> N�mero de part�culas que vamos a tener en cuenta para la simulacion (coincide con n, el n�mero de particulas de la simulacion)
!   numk    -> Entero que nos permite calcular el numero N para crear una fcc perfecta, tal que Npmax=4*k*k*k
!   pi      -> N�mero pi
!   pl      -> Lado de la caja, pl=vol**(1/3)
!   pli     -> Lado inverso de la caja pli=1/pl
!   vol     -> Volumen
!   rc      -> Radio de corte, rc=pl/2.d00
!   rc2     -> Radio de corte al cuadrado rc2=rc*rc
!   dt      -> Paso del tiempo
!   dt12    -> Paso del tiempo mitad dt12=dt/2
!   dt2     -> Paso del tiempo cuadrado mitad dt2=dt*dt/2
!   Et      -> Energ�a total, dato del ejercicio, por eso est� definida aqu�  
!   corr_ener       -> Correci�n a la energ�a, le damos un valor cero para no tener problemas si despu�s la llamamos y no esta definida
!   corr_sum_rvp    -> Correci�n a diferencial potencial de volumen , le damos un valor cero para no tener problemas si despu�s la llamamos y no esta definida
!   corr_ener_r2vpp -> Correci�n a diferencial potencial de voluemn (2o orde), le damos un valor cero para no tener problemas si despu�s la llamamos y no esta definida
!
!   VARIABLES IMPORTANTES (son relevantes)
!
! np        -> N�mero de part�culas con la que generamos la red. En este caso coinciden np=npmax.
! rx,ry,rz  -> Vectores posiciones de las part�culas (rx(i)-> posici�n en x de la part�cula i)
! vx,vy,vz  -> Vectores velocidades de las part�culas (vy(i)-> velocidad en y de la part�cula i)
! ax,ay,az  -> Vectores aceleracionse de las part�culas (az(i)-> aceleracion en z de la part�cula i)
! Etot      -> Suma de Ep+Ecin, debe ser igual a Et (si no algo esta mal)
! Epot      -> Energ�a potencial, se obtiene de la subrutina potlj
! Ecin      -> Energ�a cin�tica, debe coincidir al final con Et-fEpot
! dfiv      -> Derivada del potencial respecto el volumen, calculada con la subrutina poltj, una vez esta corregida
! d2fiv     -> Derivada 2a del potencial respecto el volumen, calculada con la subrutina poltj, una vez esta corregida 
! kpasos    -> Entero, Numero de pasos realizados en la interacci�n (500K en principio)
! dt        -> Real, nos dice cuanto tiempo pasa con cada paso. Nosotros usamos 10^-4, ya que es estable y no produce errores.
! dt12      -> dt/2.
! dt2       -> (dt**2)/2
! 
! ruta      -> Nos permite cambiar la direcci�n donde est� guardado el archivo
! fname     -> Nombre del archivo no formateado (se guarda ENV)   
! gname     -> Nombre del archivo formateado (se guardan velocidades, posiciones y aceleraciones)   
!
! gname1    -> Nombre del fichero en el que guardamos las energ�as a lo largo de la interacci�n. 
! vname1    -> Nombre del fichero en el que guardamos las velocidades eje x a lo largo de la interacci�n. 
! vname2    -> Nombre del fichero en el que guardamos las velocidades eje y a lo largo de la interacci�n. 
! vname3    -> Nombre del fichero en el que guardamos las velocidades eje z a lo largo de la interacci�n. 
!
!   VARIABLES AUXILIARES (no son relevantes)
!
! i         -> Entero, nos ayuda a realizar los distintos lazos
!
!##########################################################################################################################################
                                                                                                                                            
!##########################################################################################################################################
!
! Este es el programa principal del proyecto obligatorio 2 de la asginatura simulaci�n en fisica de materiales por Daniel Vazquez Lago.
! En este programa lo que haremos es avanzar en la simulaci�n mediante el algoritmo velocity verlet descrito en la memoria. B�sicamente
! este programa lee una configuraci�n inicial (puede ser la crea red fcc, o cualquier otra), la hace evolucionar en el tiempo, y escri-
! be al final la configuraci�n final. Como vamos a ver los pasos son bastante intuitivos, y no es muy dif�cil seguirlo.
!
!##########################################################################################################################################

      implicit none

      ! Definimos las variables

      real(kind=doblep) :: Etot,Ecin,Epot,dfiv,d2fiv
      integer(kind=entero) :: kpasos,i,np
      real(kind=doblep) :: rx(Npmax),ry(Npmax),rz(Npmax)
      real(kind=doblep)  :: ax(Npmax),ay(Npmax),az(Npmax)
      real(kind=doblep) :: vx(Npmax),vy(Npmax),vz(Npmax)
    
      character(LEN=25) :: gname,fname,vname1,vname2,vname3
      character(LEN=50) :: gname1
      character(LEN=15) :: ruta

      ! Damos valores a los pasa timepo, aunque tambien se van a leer (esto lo hacemos para que no haya errores)

      dt=0.0001d00
      dt12=dt/2.d00
      dt2=dt*dt/2.d00
      

      ! Leemos la carpeta donde est�n los datos m�s interesantes

      fname='Datos_basicos.dat'  
      ruta='../../../Datos/' 
      open (10,file=ruta//fname, STATUS='OLD', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol, dens
      read (10,9003) Etot,Ecin,Epot
      read (10,9005) Dt,kpasos
      read (10,8000) ruta
      read (10,9000) fname 
      read (10,9000) gname
      close(10)
    
      ! Definimos los nombres de los archivos y la ruta. En funci�n de i se eligir� un tipo de equilibraci�n u otra.
      ! En cada una se define de manera difernete el n�mero de pasos y el nombre de los archivos para ver la equilibraci�n.
      ! i=1 -> Venimos de una configuraci�n fcc. 5K pasos es suficiente, ya qeu luego aplicamos el programa cambia energ�a
      ! i=2 -> Primera equilibraci�n tras cambiar la energ�a. 500K pasos.
      ! i=3 -> Segunda equilibraci�n tras la primera. 500K pasos

      i=3    
      if (i.eq.1) then
        kpasos=5000
        gname1='Datos_energia_equilibracion-5K-1.dat'
        vname1='Datos_vx_1.dat'    
        vname2='Datos_vy_1.dat'    
        vname3='Datos_vz_1.dat'    
        ruta='../../../Datos/'  
      elseif (i.eq.2) then
        kpasos=500000    
        gname1='Datos_energia_equilibracion-500K-1.dat'
        vname1='Datos_vx_1.dat'    
        vname2='Datos_vy_1.dat'    
        vname3='Datos_vz_1.dat'    
        ruta='../../../Datos/'  
      elseif (i.eq.3) then
        kpasos=500000 
        gname1='Datos_energia_equilibracion-500K-2.dat'
        vname1='Datos_vx_2.dat'    
        vname2='Datos_vy_2.dat'    
        vname3='Datos_vz_2.dat'    
      endif
      
      ! Leemos la configuraci�n inicial (posiciones, velocidades, aceleraciones) de las 500 part�culas

      open (20,file=ruta//gname,form="unformatted", STATUS='OLD', ACTION='READ')  
      read (20) rx,ry,rz,vx,vy,vz,ax,ay,az
      close(20)

      ! Abrimos los archivos que vamos a usar para guardar datos para estudiar en el optativo 1 si se llega al equilibrio.
      
      open (31,file=ruta//gname1,STATUS='UNKNOWN')
      open (41,file=ruta//vname1,form="unformatted")
      open (42,file=ruta//vname2,form="unformatted")
      open (43,file=ruta//vname3,form="unformatted")

      ! Comenzamos el lazo. En cada paso avanzamos 0.0001 en el tiempo. Hacemos un n�mero kpasos  de pasos
      
      do i=0,kpasos
            ! Llamamos a la subrutina verlet, recibiendo una configuraci�n de entrada, devolviendo la del insatnte posterior
            call SUB_VERLET(np,rx,ry,rz,vx,vy,vz,ax,ay,az,epot,dfiv,d2fiv)         
            Ecin=(Dot_Product(vx,vx)+Dot_Product(vy,vy)+Dot_Product(vz,vz))/2
            
            ! Leemos los archivos. Se hace cada 100 pasos para que haya avanzado suficiente y sea significativo el cambio.
            if (modulo(i,100).eq.0) then
                 write(31,9004) Ecin+Epot,Ecin,Epot
                 write(41)vx 
                 write(42)vy
                 write(43)vz
                 ! Punto check cada 10K pasos, para ver como avanza la simulaci�n, cuanto le queda.
                 if (modulo(i,10000).eq.0) then
                   write(*,*)i
                 endif  
            endif       
      enddo
      ! Cerramos los archivos
      close(31)
      close(41)
      close(42)
      close(43)
      
!     Ahora abrimos los archivos para escribir en los mismos que se ley� la nueva configuraci�n. Escribe por encima de los anteriores, 
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

!      Formatos usado para leer/escribir a lo largo de la simulaci�n

 8000 format(a15)
 9000 format(a25)
 9001 format(i4,2x,1pe19.12,3(2x,e19.12)) ! -> el 19.12 es perfecto para los decimales, mientras que el 1pe ya sabemos que es por la potenciaci�n. Lo ultimo 3(3x,e19.12) quiere decir que 3 veces con el mismo formato 
 9002 format(1pe19.12,2x,e19.12)
 9003 format(1pe19.12,2x,e19.12,2x,e19.12)
 9004 format(1pe19.12,2x,e19.12,2x,e19.12)
 9005 format(1pe19.12,2x,i6)
 
      pause 
      
        

end program