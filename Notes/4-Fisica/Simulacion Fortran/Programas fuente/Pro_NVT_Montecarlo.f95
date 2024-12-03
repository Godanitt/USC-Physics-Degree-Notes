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
      real(kind=doblep) :: rxnew,rynew,rznew
      real(kind=doblep) :: T,Tinv,Vol=1000.d00,dens,P,f
      real(kind=doblep) :: pl,pli,rc,rc2
      real(kind=doblep) :: E,Ei,Ef,P,Epot!,Epot2
      real(kind=doblep),allocatable :: Etot(:)
      real(kind=doblep) :: varphi,varphiV,varphiVV,varphi2,varphi2V,varphiV2
      real(kind=doblep) :: Eaux,Eaux_new,dfivaux,dfivaux_new,d2fivaux,d2fivaux_new,enew,d2fiv,dfiv
      real(kind=doblep) :: Presion,Cv,gammaB,kt_inv

      integer(kind=entero)::kpasos,np,npmax
      
      character(len=2) :: char_val
      character(len=25) :: ruta1
      character(len=25) :: ruta2
      character(len=50) :: fname,gname,gname1,gname2,gname3

! Creamos las variables auxiliares:

        
      real(kind=doblep),allocatable::vx(:),vy(:),vz(:),ax(:),ay(:),az(:) ! Si no es la primera esta linea es comentario, irrelevante
      real(kind=doblep)::tasa_cambio,fun_random
      integer(kind=entero) :: i,j,k,numero,idem1,idem2,idem3,part,numeros



! Leemos variables de entrada
      

      read(*,8001)j,numeros   
      
      WRITE(char_val, '(i2.2)') j

      write(*,*)'##############'


      fname='Datos_basicos_NVT_Montecarlo.dat'    
      gname='Datos_particulas_NVT_Montecarlo.dat'  
      gname1='Energias_NVT_Montecarlo_'//Char_val//'.dat'  
      gname2='Valores_medios_energias_NVT_Montecarlo_'//Char_val//'.dat'
      gname3='Valores_medios_NVT_Montecarlo_'//Char_val//'.dat'          
      ruta1='../../../Datos/Optativo3/' 
      ruta2='../../../Datos/Optativo3/' 

      if (j.eq.1) then      
         open(22,file=ruta2//gname1,status='old', ACTION='WRITE')  
         write(22,9500)vol,numero
         close(22)
         open(23,file=ruta2//gname2,status='old', ACTION='WRITE')  
         write(23,9500)vol,numero
         close(23)
         open (23,file=ruta2//gname3,STATUS='old', ACTION='WRITE')  
         write(23,9500)vol,numero
         close(23)
      endif  
    
! Ahora tenemos que leer los valores iniciales para montecarlo. Va a cambiar el archivo respecto DM, ya qeu ahora T es el parametro
! Entonces creamos un nuevo archivo de cero si es la primera vez (no cuesta mucho), que servirá para el resto de la simulacion.
! ¿Que va a pasar/leer este archivo? -> V,rc,rc2,pl,pli,T,varphi,E,np,kpasos,fname,gname,ruta,ruta2

      open (10,file=ruta1//fname, STATUS='old', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol,dens
      read (10,9003) T,E,Epot
      read (10,9002) dfiv,d2fiv
      read (10,9005) kpasos
      read (10,9000) ruta1
      read (10,9000) ruta2
      read (10,9015) fname 
      read (10,9015) gname
      close(10)
      T=1.416
      Tinv=1/T

      Npmax=np
        
      ALLOCATE(rx(Npmax),ry(Npmax),rz(Npmax))
      ALLOCATE(vx(Npmax),vy(Npmax),vz(Npmax),ax(Npmax),ay(Npmax),az(Npmax))

! Ahora leemos las posiciones de las partículas (si es la primera vez tendremos que leer las velocidades y aceleraciones, pero
! una vez este equilibrada la NVT ya no hará falta, y solo leeremos/pasaremos las posiciones):

      rx=0.d00
      ry=0.d00
      rz=0.d00

      fname='Datos_basicos_NVT_Montecarlo.dat'    
      gname='Datos_particulas_NVT_Montecarlo.dat'  
      gname1='Energias_NVT_Montecarlo_'//Char_val//'.dat'  
      gname2='Valores_medios_energias_NVT_Montecarlo_'//Char_val//'.dat'
      gname3='Valores_medios_NVT_Montecarlo_'//Char_val//'.dat'       
      ruta1='../../../Datos/Optativo3/' 
      ruta2='../../../Datos/Optativo3/' 

      open (20,file=ruta1//gname,form="unformatted", STATUS='old', ACTION='read')  
      read (20) rx,ry,rz!,vx,vy,vz,ax,ay,az
      close(20)

! Ahora vamos a leer a teclado el numero de inteaccion que es y cuantas hacemos (j,numero)


! Inicializamos algunas variables
      Epot=0.d00
      varphi=0.d00
      varphiV=0.d00
      varphiVV=0.d00
      varphi2=0.d00
      varphi2V=0.d00
      varphiV2=0.d00
    
      Tasa_cambio=(pl/5.d00)*0.01d00

      kpasos=1000
      ALLOCATE(Etot(kpasos))
      
      call SUB_POTLJ_2(np,rx,ry,rz,Epot,dfiv,d2fiv,pl,pli,rc,rc2,vol)
      ! La cantidad de pasos es del total de 500*500K (500 por cada uno de DM). Inicializamos el lazo:
      !kpasos=0.01                             
      do i=1,kpasos*500

        part=nint(Fun_random(1)*499.d00+1.d00)
        !write(*,*)'Energia',Epot+3.d00*(np-1.d00)*T/2.d00

        
        !Calculamos Eaux por primera vez, para el resto ya se guardan
        rxnew=rx(part)+(2.d00*Fun_random(1)-1.d00)*Tasa_cambio
        rynew=ry(part)+(2.d00*Fun_random(1)-1.d00)*Tasa_cambio
        rznew=rz(part)+(2.d00*Fun_random(1)-1.d00)*Tasa_cambio
        
      !  call SUB_POTLJ_NVT_MONTECARLO(npmax,part,rx,ry,rz,rx(part),ry(part),rz(part),Eaux,pl,pli,rc,rc2,vol) 
        call SUB_POTLJ_NVT_MONTECARLO(npmax,part,rx,ry,rz,rxnew,rynew,rznew,Eaux,Eaux_new,pl,pli,rc,rc2,vol)
        
        P=min(1.d00,exp(-(Eaux_new-Eaux)*Tinv))
        
        if (P>Fun_random(1)) then     
            rx(part)=rxnew
            ry(part)=rynew
            rz(part)=rznew
        endif  
       ! write(*,*)'Estamos en el',j,'con energia',Epot+3.d00*(np-1.d00)*T/2.d00
        
        if (modulo(i,500).eq.0) then
            call SUB_POTLJ_2(np,rx,ry,rz,Epot,dfiv,d2fiv,pl,pli,rc,rc2,vol)
            Etot(i/500)=Epot
            varphi=varphi+Epot
            varphiV=varphiV+dfiv
            varphiVV=varphiVV+d2fiv
            varphi2=varphi2+Epot*Epot
            varphi2V=varphi2V+Epot*dfiv
            varphiV2=varphiV2+dfiv*dfiv
        endif               
       ! if (modulo(i,50*500).eq.0) then
       !     write(*,*)'Estamos en el',j,'con energia',Etot(i)
       ! endif
               
      enddo  
      write(*,*)'##############'

        
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
      kt_inv=np*T/vol+Vol*varphiVV-(Vol/T)*(varphiV2-varphiV*varphiV)

       
        

! Ahora escribimos los nuevos valores de los datos y las posiciones

      open (10,file=ruta1//fname, STATUS='OLD', ACTION='WRITE')  
      write (10,9001) np,pl,pli,rc,rc2
      write (10,9002) vol,dens
      write (10,9003) T,E,Epot
      write (10,9002) dfiv,d2fiv
      write (10,9005) kpasos
      write (10,9000) ruta1
      write (10,9000) ruta2
      write (10,9015) fname 
      write (10,9015) gname
      close(10)

! Escribimos a un .dat los valores medios !(si j=1 escribimos por encima, si j.neq.1 escribimos en formato append)

      open (20,file=ruta1//gname,form="unformatted", STATUS='OLD', ACTION='WRITE')  
      write (20) rx,ry,rz
      close(20)

! Escribimos los datos fuera del optativo


      open (21,file=ruta2//gname1,STATUS='old', ACTION='WRITE')  
      do i=1,kpasos
          write(21,9600) Etot(i)+3.d00*(dble(np)-1.d00)*T/2.d00
          !write(*,*) Etot(i)+3.d00*(dble(np)-1.d00)*T/2.d00
      enddo
      close(21)

      write(*,*)Etot

      open (22,file=ruta2//gname2,STATUS='append', ACTION='WRITE')  
      write(22,9007) 'Interaccion 500K pasos Número:',j
      write (22,9006) 'varphi=',varphi
      write (22,9006) 'varphiV=',varphiV
      write (22,9006) 'varphiVV=',varphiVV
      write (22,9006) 'varphi2=',varphi2
      write (22,9006) 'varphi2V=',varphi2V
      write (22,9006) 'varphiV2=',varphiV2
      write(22,9000) '##############################'
      close(22)
      open (23,file=ruta2//gname3,STATUS='append', ACTION='WRITE')  
      write(23,9007) 'Interaccion 500K pasos Número:',j
      write (23,9006) 'P=',P
      write (23,9006) 'CV=',CV
      write (23,9006) 'gammaB=',gammaB
      write (23,9006) 'kt_inv=',kt_inv
      write(23,9000) '##############################'
      close(23)




! Formatos de escritura para los archivos .dat

 8000 format(a15)
 8001 format(i4,i4)
 9015 format(a50)
 9000 format(a25)
 9001 format(i4,2x,1pe19.12,3(2x,e19.12)) ! -> el 19.12 es perfecto para los decimales, mientras que el 1pe ya sabemos que es por la potenciación. Lo ultimo 3(3x,e19.12) quiere decir que 3 veces con el mismo formato 
 9002 format(1pe19.12,2x,e19.12)
 9003 format(1pe19.12,2x,e19.12,2x,e19.12)
 9005 format(i6)
 9006 format(a15,2x,1pe19.12)
 9007 format(a35,2x,i4)
 9500 format(1pe19.12,2x,i4)
 9600 format(1pe19.12)

      pause
 
end program