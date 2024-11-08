program Pro_NVT_Montecarlo

! ##################################################################
!
! Calculo de NVT Usando Montecarlo -> Partimos de la configuración de equilibrio del obligatorio 3, pero la escribimos
! en otro archivo, ya que primero tenemos que equilibrar la NVT con 500K pasos, para luego hacer la simulacion. 
!
! ##################################################################

      use Mod_01_Def_prec
      use Mod_03_Interface

      implicit none 

! ########################## VARIABLES USADAS ########################################
! 
! Variables importantes:
!      - Posiciones: rx,ry,rz (arrays dimensión 500)
!      - Temperatura: T (parametro)
!      - Volumen: V (parametro)
!      - Densidad: rho (parametro) 
!      - Lado de la caja: pl, pli (inverso) 
!      - Radio de corte/Radio de corte cuadrado: rc,rc2
!      - Nummero de partículas: np
!      - Numero de particulas maximo que estudiamos: npmax (np=npmax en nuestro caso)
!      - Energia: E(Epot) y Enew(Epot)
!      - Energia del estado inicial y energía del estado final: Ei,Ef (reales doble precisión)
!      - Probabilidad de que pueda pasar: P=min(1,exp(E/T))
!      - Energia potencial: varphi 
!      - Derivada de la energia potencial respecto al volumen: varphiV
!      - Segunda derivada de la energia potencial respecto al volumen: varphiVV
!      - Productoes de las anteriores: varphi2 (1a*1a),varphi2V (1a*2a),varphiV2 (2a*2a)
!      - Valores medios de interés: P,Cv,gammaB,kt_inv-> el calculo de los demas (CP,alphas...) se hace a partir de las medias de los anteriores
!      - Numero de pasos: kpasos (500*500000) (entero) 
!      - Array que nos permite almacenar los valores de la energía cada x pasos: Etot
!
! Variables no importantes, auxiliares:
!      - Variables para leer los datos inciales: vx,vy,vz,ax,ay,az,Ecin,Epot
!
! ##################################################################

! Creamos las variables importantes:

      real(kind=doblep),allocatable::rx(:),ry(:),rz(:)
      real(kind=doblep):: rxnew,ryrew,rznew
      real(kind=doblep),parameter:: T,V,rho
      real(kind=doblep) :: pl,pli,rc,rc2
      real(kind=doblep) :: E,Ei,Ef,P
      real(kind=doblep),allocatable :: Etot(:)
      real(kind=doblep) :: varphi,varphiV,varphiVV,varphi2,varphi2V,varphiV2
      real(kind=doblep) :: P,Cv,gammaB,kt_inv

      integer(kind=entero)::kpasos,np,npmax
      
      character(len=10) :: ruta1,ruta2
      character(len=50) :: fname,gname,gname1,gname2

! Creamos las variables auxiliares:

        
      real(kind=doblep),allocatable::vx(:),vy(:),vz(:),ax(:),ay(:),az(:) ! Si no es la primera esta linea es comentario, irrelevante
      real(kind=doblep)::tasa_cambio
      integer(kind=entero) :: i,j,k,numero,idem1,idem2,idem3

! Le damos valores/inicializamos a algunas variables  

      fname='Datos_basicos_NVT_Montecarlo.dat'    
      gname='Datos_particulas_NVT_Montecarlo.dat'     
      ruta='../../../Datos/' 
      ruta2='../../../Datos/Optativo3/' 

! Ahora tenemos que leer los valores iniciales para montecarlo. Va a cambiar el archivo respecto DM, ya qeu ahora T es el parametro
! Entonces creamos un nuevo archivo de cero si es la primera vez (no cuesta mucho), que servirá para el resto de la simulacion.
! ¿Que va a pasar/leer este archivo? -> V,rc,rc2,pl,pli,T,varphi,E,np,kpasos,fname,gname,ruta,ruta2

      open (10,file=ruta//fname, STATUS='OLD', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol, dens
      read (10,9003) T,E,Epot
      read (10,9005) kpasos
      read (10,8000) ruta
      read (10,8001) ruta2
      read (10,9000) fname 
      read (10,9000) gname
      close(10)

      Npmax=np
        
      ALLOCATE(rx(Npmax),ry(Npmax),rz(Npmax))
      ALLOCATE(vx(Npmax),vy(Npmax),vz(Npmax),ax(Npmax),ay(Npmax),az(Npmax))
      ALLOCATE(dcm(n_tau),corv(n_tau),tau(n_tau))


! Ahora leemos las posiciones de las partículas (si es la primera vez tendremos que leer las velocidades y aceleraciones, pero
! una vez este equilibrada la NVT ya no hará falta, y solo leeremos/pasaremos las posiciones):

      open (20,file=ruta//gname,form="unformatted", STATUS='OLD', ACTION='READ')  
      read (20) rx,ry,rz,vx,vy,vz,ax,ay,az
      close(20)


! Ahora vamos a leer a teclado el numero de inteaccion que es y cuantas hacemos (j,numero)


! Inicializamos algunas variables

      Eold=Epot

      varphi=0.d00
      varphiV=0.d00
      varphiVV=0.d00
      varphi2=0.d00
      varphi2V=0.d00
      varphiV2=0.d00
    
      Tasa_cambio=rc/50.d00


      
      
! La cantidad de pasos es del total de 500*500K (500 por cada uno de DM). Inicializamos el lazo:
                                   
      do i=1,kpasos*500

        part=nint(Fun_random(idem1)*499.d00+1.d00)
        
        !Calculamos Eaux por primera vez, para el resto ya se guardan
        if (i.eq.1)
            SUB_POTLJ_NVT_MONTECARLO(npmax,part,rx,ry,rz,rxnew,rynew,rznew,Eaux,dfivaux,d2fivaux,pl,pli,rc,rc2) 
        endif    
        rxnew=rx(part)+(2.d00*Fun_random(idem1+1)-1.d00)*Tasa_cambio
        rynew=rx(part)+(2.d00*Fun_random(idem1+5)-1.d00)*Tasa_cambio
        rznew=rz(part)+(2.d00*Fun_random(idem1+10)-1.d00)*Tasa_cambio
        
        subroutine SUB_POTLJ_NVT_MONTECARLO(npmax,part,rx,ry,rz,rxnew,rynew,rznew,Eaux_new,dfivaux_new,d2fivaux_new,pl,pli,rc,rc2) 
        
        Enew=Epot+Eaux_new-Eaux    
        
        P=min(1.d00,exp(-(Enew-Epot)/T))
        
        if (P>Fun_random(idem2)) then
            rx(part)=rxnew
            ry(part)=rynew
            rz(part)=rznew
            Epot=Enew
            dfiv=dfiv_new+dfivaux_new-dfivaux
            d2fiv=d2fiv_new+d2fivaux_new-d2fivaux        
        endif  
        
        varphi=varphi+Epot
        varphiV=varphiV+dfiv
        varphiVV=varphiVV+d2fiv
        varphi2=varphi2+Epot*Epot
        varphi2V=varphi2V+Epot*dfiv
        varphiV2=varphiV2+dfiv*dfiv
        
        if (modulo(i,100*500).eq.0) then
            Etot(i)=Epot+3.d00*(np-1.d00)*T/2.d00       
            if (modulo(i,10000*500).eq.0) then
              write(*,*) 'i',i,'Energia',Epot
        endif
      enddo  
      


! Calculamos los valores medios

      varphi=varphi/(500.d00*dble(kpasos))
      varphiV=varphiV/(500.d00*dble(kpasos))
      varphiVV=varphiVV/(500.d00*dble(kpasos))
      varphi2=varphi2V/(500.d00*dble(kpasos))
      varphi2V=varphi2V/(500.d00*dble(kpasos))
      varphiV2=varphi/V2(500.d00*dble(kpasos))

      
        

! Ahora escribimos los nuevos valores de los datos y las posiciones

      open (10,file=ruta//fname, STATUS='OLD', ACTION='WRITE')  
      write (10,9001) np,pl,pli,rc,rc2
      write (10,9002) vol, dens
      write (10,9003) T,E,varphi
      write (10,9005) kpasos
      write (10,8000) ruta
      write (10,8001) ruta2
      write (10,9000) fname 
      write (10,9000) gname
      close(10)

! Escribimos a un .dat los valores medios (si j=1 escribimos por encima, si j.neq.1 escribimos en formato append)

      open (20,file=ruta//gname,form="unformatted", STATUS='OLD', ACTION='WRITE')  
      read (20) rx,ry,rz
      close(20)

! Formatos de escritura para los archivos .dat

end program