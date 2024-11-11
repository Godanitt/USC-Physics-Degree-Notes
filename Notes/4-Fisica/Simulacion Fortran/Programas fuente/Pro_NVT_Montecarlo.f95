program Pro_NVT_Montecarlo

! ##################################################################
!
! Calculo de NVT Usando Montecarlo -> Partimos de la configuraci�n de equilibrio del obligatorio 3, pero la escribimos
! en otro archivo, ya que primero tenemos que equilibrar la NVT con 500K pasos, para luego hacer la simulacion. 
!
! ##################################################################

      use Mod_01_Def_prec
      use Mod_03_Interface

      implicit none 

! ########################## VARIABLES USADAS ########################################
! 
! Variables importantes:
!      - Posiciones: rx,ry,rz (arrays dimensi�n 500)
!      - Temperatura: T (parametro)
!      - Volumen: V (parametro)
!      - Densidad: rho (parametro) 
!      - Lado de la caja: pl, pli (inverso) 
!      - Radio de corte/Radio de corte cuadrado: rc,rc2
!      - Nummero de part�culas: np
!      - Numero de particulas maximo que estudiamos: npmax (np=npmax en nuestro caso)
!      - Energia: E(Epot) y Enew(Epot)
!      - Energia del estado inicial y energ�a del estado final: Ei,Ef (reales doble precisi�n)
!      - Probabilidad de que pueda pasar: P=min(1,exp(E/T))
!      - Energia potencial: varphi 
!      - Derivada de la energia potencial respecto al volumen: varphiV
!      - Segunda derivada de la energia potencial respecto al volumen: varphiVV
!      - Productoes de las anteriores: varphi2 (1a*1a),varphi2V (1a*2a),varphiV2 (2a*2a)
!      - Valores medios de inter�s: P,Cv,gammaB,kt_inv-> el calculo de los demas (CP,alphas...) se hace a partir de las medias de los anteriores
!      - Numero de pasos: kpasos (500*500000) (entero) 
!      - Array que nos permite almacenar los valores de la energ�a cada x pasos: Etot
!
! Variables no importantes, auxiliares:
!      - Variables para leer los datos inciales: vx,vy,vz,ax,ay,az,Ecin,Epot
!
! ##################################################################

! Creamos las variables importantes:

      real(kind=doblep),allocatable::rx(:),ry(:),rz(:)
      real(kind=doblep) :: rxnew,rynew,rznew
      real(kind=doblep) :: T,Vol,dens,P
      real(kind=doblep) :: pl,pli,rc,rc2
      real(kind=doblep) :: E,Ei,Ef,P,Epot
      real(kind=doblep),allocatable :: Etot(:)
      real(kind=doblep) :: varphi,varphiV,varphiVV,varphi2,varphi2V,varphiV2
      real(kind=doblep) :: Eaux,Eaux_new,dfivaux,dfivaux_new,d2fivaux,d2fivaux_new,enew,d2fiv,dfiv!,dfiv_new,d2fiv_new
      real(kind=doblep) :: Presion,Cv,gammaB,kt_inv

      integer(kind=entero)::kpasos,np,npmax
      
      character(len=15) :: ruta1
      character(len=25) :: ruta2
      character(len=50) :: fname,gname,gname1,gname2,gname3

! Creamos las variables auxiliares:

        
      real(kind=doblep),allocatable::vx(:),vy(:),vz(:),ax(:),ay(:),az(:) ! Si no es la primera esta linea es comentario, irrelevante
      real(kind=doblep)::tasa_cambio,fun_random
      integer(kind=entero) :: i,j,k,numero,idem1,idem2,idem3,part

! Le damos valores/inicializamos a algunas variables  

      fname='Datos_basicos_NVT_Montecarlo.dat'    
      gname='Datos_particulas_NVT_Montecarlo.dat'  
      gname1='Datos_Energias_NVT_Montecarlo.dat'  
      gname2='Datos_Valores_medios_energias_NVT_Montecarlo.dat'
      gname3='Datos_Valores_medios_NVT_Montecarlo.dat'       
      ruta1='../../../Datos/' 
      ruta2='../../../Datos/Optativo3/' 

! Ahora tenemos que leer los valores iniciales para montecarlo. Va a cambiar el archivo respecto DM, ya qeu ahora T es el parametro
! Entonces creamos un nuevo archivo de cero si es la primera vez (no cuesta mucho), que servir� para el resto de la simulacion.
! �Que va a pasar/leer este archivo? -> V,rc,rc2,pl,pli,T,varphi,E,np,kpasos,fname,gname,ruta,ruta2

      open (10,file=ruta1//fname, STATUS='old', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol,dens
      read (10,9003) T,E,Epot
      read (10,9002) dfiv,d2fiv
      read (10,9005) kpasos
      read (10,8000) ruta1
      read (10,9000) ruta2
      read (10,9015) fname 
      read (10,9015) gname
      close(10)

      Npmax=np
        
      ALLOCATE(rx(Npmax),ry(Npmax),rz(Npmax))
      ALLOCATE(vx(Npmax),vy(Npmax),vz(Npmax),ax(Npmax),ay(Npmax),az(Npmax))

! Ahora leemos las posiciones de las part�culas (si es la primera vez tendremos que leer las velocidades y aceleraciones, pero
! una vez este equilibrada la NVT ya no har� falta, y solo leeremos/pasaremos las posiciones):

      rx=0.d00
      ry=0.d00
      rz=0.d00

      open (20,file=ruta1//gname,form="unformatted", STATUS='old', ACTION='read')  
      read (20) rx,ry,rz!,vx,vy,vz,ax,ay,az
      close(20)

! Ahora vamos a leer a teclado el numero de inteaccion que es y cuantas hacemos (j,numero)


! Inicializamos algunas variables

      varphi=0.d00
      varphiV=0.d00
      varphiVV=0.d00
      varphi2=0.d00
      varphi2V=0.d00
      varphiV2=0.d00
    
      Tasa_cambio=rc/500.d00

      kpasos=500000
      ALLOCATE(Etot(kpasos*500/100))

      
! La cantidad de pasos es del total de 500*500K (500 por cada uno de DM). Inicializamos el lazo:
                                   
      do i=1,kpasos*500
        idem1=i
        idem2=i+1
        idem3=i+2

        part=nint(Fun_random(idem1)*499.d00+1.d00)

        
        !Calculamos Eaux por primera vez, para el resto ya se guardan
        
        if (i.eq.1) then
            call SUB_POTLJ_NVT_MONTECARLO(npmax,part,rx,ry,rz,rx(part),ry(part),rz(part),Eaux,dfivaux,d2fivaux,pl,pli,rc,rc2,vol) 
        endif

        rxnew=rx(part)+(2.d00*Fun_random(idem1+2)-1.d00)*Tasa_cambio
        rynew=ry(part)+(2.d00*Fun_random(idem1+5)-1.d00)*Tasa_cambio
        rznew=rz(part)+(2.d00*Fun_random(idem1+10)-1.d00)*Tasa_cambio
        
        
        call SUB_POTLJ_NVT_MONTECARLO(npmax,part,rx,ry,rz,rxnew,rynew,rznew,Eaux_new,dfivaux_new,d2fivaux_new,pl,pli,rc,rc2,vol)
        
        !write(*,*)Eaux,Eaux_new
        
        Enew=Epot+Eaux_new-Eaux    
        if (Eaux_new-Eaux<-500.d00) then
           Eaux_new=-500.d00+Eaux
        endif           
        P=min(1.d00,exp(-(Eaux_new-Eaux)/T))
        
        if (P>Fun_random(idem2)) then
            rx(part)=rxnew
            ry(part)=rynew
            rz(part)=rznew
            Eaux=Eaux_new
            Epot=Enew
            dfiv=dfiv+dfivaux_new-dfivaux
            d2fiv=d2fiv+d2fivaux_new-d2fivaux        
        endif  
        
        varphi=varphi+Epot
        varphiV=varphiV+dfiv
        varphiVV=varphiVV+d2fiv
        varphi2=varphi2+Epot*Epot
        varphi2V=varphi2V+Epot*dfiv
        varphiV2=varphiV2+dfiv*dfiv
        
        if (modulo(i,100*500).eq.0) then
            Etot(i)=Epot+3.d00*(np-1.d00)*T/2.d00       
            write(*,*) 'Epot',Epot
            if (modulo(i,1000*500).eq.0) then
              write(*,*) 'i',i/500,'Energia',Etot(i),'particula',part,'epot',epot
            endif  
        endif
      enddo  
      


! Calculamos los valores medios

      varphi=varphi/(500.d00*dble(kpasos))
      varphiV=varphiV/(500.d00*dble(kpasos))
      varphiVV=varphiVV/(500.d00*dble(kpasos))
      varphi2=varphi2V/(500.d00*dble(kpasos))
      varphi2V=varphi2V/(500.d00*dble(kpasos))
      varphiV2=varphiV2/(500.d00*dble(kpasos))

      
        

! Ahora escribimos los nuevos valores de los datos y las posiciones

      open (10,file=ruta1//fname, STATUS='OLD', ACTION='WRITE')  
      write (10,9001) np,pl,pli,rc,rc2
      write (10,9002) vol,dens
      write (10,9003) T,E,Epot
      write (10,9002) dfiv,d2fiv
      write (10,9005) kpasos
      write (10,8000) ruta1
      write (10,9000) ruta2
      write (10,9015) fname 
      write (10,9015) gname
      close(10)

! Escribimos a un .dat los valores medios (si j=1 escribimos por encima, si j.neq.1 escribimos en formato append)

      open (20,file=ruta1//gname,form="unformatted", STATUS='OLD', ACTION='WRITE')  
      write (20) 
      close(20)

! Escribimos los datos fuera del optativo


      open (21,file=ruta2//gname1,STATUS='new', ACTION='WRITE')  
      do i=i,kpasos/100
          write(21,9600) Etot(i)
      enddo
      close(21)

      open (22,file=ruta2//gname2,STATUS='new', ACTION='WRITE')  
      write (22,9006) 'varphi=',varphi
      write (22,9006) 'varphiV=',varphiV
      write (22,9006) 'varphiVV=',varphiVV
      write (22,9006) 'varphi2=',varphi2
      write (22,9006) 'varphi2V=',varphi2V
      write (22,9006) 'varphiV2=',varphiV2
      close(22)

    !  open (23,file=ruta2//gname3,STATUS='new', ACTION='WRITE')  
    !  write (23) rx,ry,rz
    !  close(23)


! Formatos de escritura para los archivos .dat

 8000 format(a15)
 8001 format(i4,i4)
 9015 format(a50)
 9000 format(a25)
 9001 format(i4,2x,1pe19.12,3(2x,e19.12)) ! -> el 19.12 es perfecto para los decimales, mientras que el 1pe ya sabemos que es por la potenciaci�n. Lo ultimo 3(3x,e19.12) quiere decir que 3 veces con el mismo formato 
 9002 format(1pe19.12,2x,e19.12)
 9003 format(1pe19.12,2x,e19.12,2x,e19.12)
 9005 format(i6)
 9006 format(a15,2x,1pe19.12)
 9007 format(a35,2x,i4)
 9500 format(1pe19.12,2x,i4)
 9600 format(1pe19.12)

      pause
 
end program