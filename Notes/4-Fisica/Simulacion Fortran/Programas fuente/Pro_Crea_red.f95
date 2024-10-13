PROGRAM Pro_Crea_red

      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface
      
      
      implicit none

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
!
!   VARIABLES IMPORTANTES (son relevantes)
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
! 
! ruta      -> Nos permite cambiar la dirección donde está guardado el archivo
! fname     -> Nombre del archivo no formateado (se guarda ENV)   
! gname     -> Nombre del archivo formateado (se guardan velocidades, posiciones y aceleraciones)   
!
!   VARIABLES AUXILIARES (no son relevantes)
!
! x,y,z     -> Variables que nos permiten hace la interacción para colocar las partículas en rx,ry,rz 
! pa,pma    -> Lado de una celda convencional pa->L/numk; pma->pm/2
! porcentaje-> Factor que nos permite dar una sacudida. Nosotros tomamos un 10% (factor=0.1d00)
! Fun_random-> Generador de variables aleatorias para la sacudida de la posición y la velocidad (es una función dada, metes un entero y te saca un real de [0,1)
! cuenta    -> Valor entero que nos permite definir las posiciones de cada partícula
! idum      -> Valor entero que nos permite generar un valor aleatorio para las velocidades
!
!##########################################################################################################################################

!##########################################################################################################################################
!
! Este es el programa principal, y basicamente genera las posiciones de la red, calcula la energía potencial para las posiciones de 
!   cada partícula (usando unas subrutina), luego las velocidades (corrigiendolas para tener momento total cero y la energía cinética
!   adecuada) y escribe los dos .dat.
!
!##########################################################################################################################################



! Definimos las variables:

      integer::cuenta,Idum
      integer(kind=entero)::x,y,z
      real(kind=doblep) :: pa,pma,porcentaje,Fun_Random
      real(kind=doblep) :: rx(Npmax),ry(Npmax),rz(Npmax)

      integer::i,j
      integer(kind=entero)::np
      real(kind=doblep) :: Etot,Epot,dfiv,d2fiv
      real(kind=doblep)  :: ax(Npmax),ay(Npmax),az(Npmax)

      real(kind=doblep) :: vx(Npmax),vy(Npmax),vz(Npmax)
      real(kind=doblep) :: Ecin,px,py,pz,pt,pt1
      

      character(LEN=25) :: gname,fname
      character(LEN=15) :: ruta

! Damos valor a algunas de las variables

      Etot=Et                           ! Le damos un valor por si acaso
      dens=0.5d00                       ! Es un valor dado del ejercicio, constante en toda la dinámica molecular
      np=npmax                          ! Como ya hemos dicho, coinciden.
      pl=(Npmax/dens)**(1/3.d00)        
      pli=1/pl
      vol=pl*pl*pl
      rc=pl/2.d00
      rc2=rc*rc
      
    

                    
!##########################################################################################################################################
! PARTE 1: ASIGNAMOS POSICIONES INICIALES A LAS PART�CULAS

      pa=pl/dble(numk) 
      pma=pa/2.d00 
      porcentaje=0.1d00
      cuenta=1  
      
      do x=0,numk-1
          do y=0,numk-1
              do z=0,numk-1           
                  rx(cuenta)=x*pa+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  ry(cuenta)=y*pa+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  rz(cuenta)=z*pa+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  cuenta=cuenta+1
                  rx(cuenta)=x*pa+pma+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  ry(cuenta)=y*pa+pma+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  rz(cuenta)=z*pa+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  cuenta=cuenta+1
                  rx(cuenta)=x*pa+pma+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  ry(cuenta)=y*pa+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  rz(cuenta)=z*pa+pma+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  cuenta=cuenta+1
                  rx(cuenta)=x*pa+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  ry(cuenta)=y*pa+pma+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  rz(cuenta)=z*pa+pma+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*pma
                  cuenta=cuenta+1
              enddo
          enddo
      enddo

!##########################################################################################################################################

! PARTE 2: CALCULAMOS LAS ENERGÍAS POTENCIALES Y LAS FUERZAS

      ! Le damos unos valores de entrada (posiciones y np, tenemos que meter np, ya que npmax es el número que vamos a tener en cuenta, no el número de partículas para las que está hecha la simulación)
      ! Nos devuelve los valores ax,ay,az,epot,dfiv,d2fiv

      CALL SUB_POTLJ(np,rx,ry,rz,ax,ay,az,epot,dfiv,d2fiv) 
    

!##########################################################################################################################################
! PARTE 3: CALCULAMOS LAS ENERGICAS CINETICAS Y VELOCIDADES

      ! Para generar las velocidades tenemos que usar en random, luego corregir para que VT=0 y para que la Ecin=E-Epot
        
      Idum=898 ! Por poner un número aleatorio diferente al de las posiciones idum>500 (así no hay correlación ninguna)
      
      DO i=1,Npmax
          vx(i)=(2.d00*Fun_random(Idum+i)-1.d00)
          vy(i)=(2.d00*Fun_random(Idum+1+i)-1.d00)
          vz(i)=(2.d00*Fun_random(Idum+2+i)-1.d00)
      ENDDO

      px=sum(vx)/Npmax
      py=sum(vy)/Npmax
      pz=sum(vz)/Npmax

      DO i=1,Npmax
          vx(i)=vx(i)-px
          vy(i)=vy(i)-py
          vz(i)=vz(i)-pz
      ENDDO

      write(*,*) 'Verificamos que la suma de las velocidades aprox 10**(-14)'
      write(*,*) 'sum(vx)=',sum(vx)
      write(*,*) 'sum(vy)=',sum(vy)
      write(*,*) 'sum(vz)=',sum(vz)
      
      px=sum(vx)/Npmax
      py=sum(vy)/Npmax
      pz=sum(vz)/Npmax

      DO i=1,Npmax
          vx(i)=vx(i)-px
          vy(i)=vy(i)-py
          vz(i)=vz(i)-pz
      ENDDO

      
      Ecin=Et-Epot
      
      px=Dot_Product(vx,vx)
      py=Dot_Product(vy,vy)
      pz=Dot_Product(vz,vz) !funciona exactamente igual con sum(vz*vz)
      pt=sqrt(px+py+pz)
      
      pt1=1/pt
          
      Ecin=sqrt(2.d00*Ecin)

      vx=vx*Ecin*pt1
      vy=vy*Ecin*pt1
      vz=vz*Ecin*pt1
      
      
      px=Dot_Product(vx,vx)
      py=Dot_Product(vy,vy)
      pz=Dot_Product(vz,vz)

      Ecin=(px+py+pz)/2      
      write(*,*) 'Verificamos que el valor Ecin+Epot es igual a Et (575 en nuestro caso)'
      write(*,*) 'Etot=',Et,'  Etot_real=',Ecin+Epot, 'Epot',Epot
      

!##########################################################################################################################################
! PARTE 4: GUARDAMOS LOS DATOS EN EL .DAT

      fname='Datos_basicos.dat'      
      gname='Datos_particulas.dat'      
      ruta='../../../Datos/' ! Nos permite guardar el archivo en una carpeta llamada datos 3 posiciones encima de la carpeta donde esta el .exe
      
 8000 format(a15)
 9000 format(a25)
 9001 format(i4,2x,1pe19.12,3(2x,e19.12)) ! -> el 19.12 es perfecto para los decimales, mientras que el 1pe ya sabemos que es por la potenciación. Lo ultimo 3(3x,e19.12) quiere decir que 3 veces con el mismo formato 
 9002 format(1pe19.12,2x,e19.12)
 9003 format(1pe19.12,2x,e19.12,2x,e19.12)
        


      open  (10,file=ruta//fname, status='OLD')  
      write (10,9001) np,pl,pli,rc,rc2
      write (10,9002) vol, dens
      write (10,9003) ecin+epot,Ecin,Epot
      write (10,8000) ruta
      write (10,9000) fname 
      write (10,9000) gname
      close (10)
      
      open (20,file=ruta//gname,form='unformatted')
      write(20) rx,ry,rz,vx,vy,vz,ax,ay,az
      close(20)

      pause 
end program