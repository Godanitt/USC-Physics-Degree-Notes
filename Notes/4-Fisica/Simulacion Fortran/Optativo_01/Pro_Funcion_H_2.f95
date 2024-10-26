program Pro_Funcion_H

      implicit none
!##############################################################
!
! En este programa vamos a calcular la función H de Boltzman como se ha descrito en la memoria. Para esto usamos las siguientes variables:
!
! np       -> real, numero de particulas
! t   -> real, nos permite saber en que valor de tiempo se le asocia a cada Hx,Hy,Hz al escribirlos
!
! vx,vy,vz -> Nos permiten ir leyendo las velocidades en cada interacción, para completar las 5001. 
! vxx,vyy,vzz -> Nos permiten apilar las velocidades vx,vy,vz, teniendo un array completo con (2.5M) datos cada una. 
! valores_mitad -> Array. Cada uno de los valores de este array contiene el valor medio de un bin.
! minimo -> De todas las velocidades (7.5M valores) la velocidad mas pequeña
! maximo -> De todas las velocidades (7.5M valores) la velocidad mas grande
! v -> Variable auxiliar, se asocia a un valor concreto de vxx,vyy o vzz
! i,j -> Enteros, nos ayudan a realizar los lazos
! kpasos -> Numero de interacciones guardadas por el Pro_equilibración, nos permiten leer los valores de vx,vy,vz
! kpasos2 -> Numero de valores de las velocidades vx, vy, vz
! kintervalos -> Número de bins del histograma
! kintervalos_int -> Entero de kintervalos
! intervalo -> Ancho de cada bin
! 
! ruta -> Nos permite leer/escribir en la carpeta donde se encuentran almacenados los datos
! vname1,vname2,vname3 -> Nombre de los archivos donde tenemos almacenadas las velocidades de vx,vy,vz
! 
! Hx,Hy,Hz -> Valores de la H de boltzman para cada uno de los ejes
!
! histx,histy,histz -> Vector asociado a valores_mitat (misma dimensión) que nos dice el número de velocidades asociado a cada uno de los valores mitad
!                       A diferencia del anterior, son valores auxiliares que se resetena cada 500 pasos (500 pasos es un intervalo temporal)
!##############################################################
      
      integer, parameter::entero=SELECTED_INT_KIND(9)
      integer, parameter::doblep=SELECTED_REAL_KIND(15,307)
      
      real(kind=doblep) :: np,t
      real(kind=doblep) :: vx(500),vy(500),vz(500)
      real(kind=doblep) :: vxx(500*5001),vyy(500*5001),vzz(500*5001)
      real,allocatable :: valores_mitad(:),Hx(:),Hy(:),Hz(:),histx(:),histy(:),histz(:)
      real(kind=doblep) :: minimo,maximo,distancia,v,intervalo,kintervalos
      integer (kind=entero) :: i,j,kpasos,kpasos2,kintervalos_int
      character(LEN=25) :: vname1,vname2,vname3,vname4
      character(LEN=9) :: ruta
      
      np=500.d0        

      vname1='Datos_vx_2.dat'    
      vname2='Datos_vy_2.dat'    
      vname3='Datos_vz_2.dat'  
      ruta='../Datos/'       
      
      kintervalos=sqrt(500.d00)*10
      kintervalos_int=int(kintervalos)
      allocate(valores_mitad(kintervalos_int),histx(kintervalos_int),histy(kintervalos_int),histz(kintervalos_int))
      
      kpasos=5001
      kpasos2=500
      allocate(Hx(kpasos),Hy(kpasos),Hz(kpasos))
      
      open (41,file=ruta//vname1,form="unformatted")
      open (42,file=ruta//vname2,form="unformatted")
      open (43,file=ruta//vname3,form="unformatted")
      
      vxx=0.d00
      vyy=0.d00      
      vzz=0.d00
    
! Leyemos todas las velocidades en vxx,vyy,vzz
      
      do i=0,kpasos-1
        read(41)vx
        read(42)vy
        read(43)vz
        do j=1,kpasos2
            vxx(i*500+j)=vx(j)
            vyy(i*500+j)=vy(j)
            vzz(i*500+j)=vz(j)     
        enddo       
      enddo
      close(41)
      close(42)
      close(43)

! Creamos valores auxiliares

      minimo=min(minval(vxx),minval(vyy),minval(vzz))
      maximo=max(maxval(vxx),maxval(vyy),maxval(vzz))

      write(*,*)'min=',minimo
      write(*,*)'max=',maximo
  
      write(*,*)'Absoluto mas grande entre ambos',max(abs(minimo),abs(maximo))
      write(*,*)'intervalos=',kintervalos
       
      distancia=maximo*2.d00
      intervalo=distancia/kintervalos
      write(*,*)'Intervalo (distancia)=',intervalo

      Hx=0.d00
      Hy=0.d00      
      Hz=0.d00
      
! Creamos el array valor medio:

      valores_mitad=0.d00
      do i=1,kintervalos
            valores_mitad(i)=-distancia/2.d00+dble(intervalo)/2.d00+dble(i)*dble(intervalo)
      enddo

      write(*,*)'########################################'
          
      histx=0.d00
      histy=0.d00      
      histz=0.d00

! Rellenamos el histograma vx y calculamos Hx

      do i=1,500*5001
        v=vxx(i)   
        do j=1,kintervalos_int
             if (v<=-distancia/2.d00+intervalo*j) then
                histx(j)=histx(j)+1.d00
                exit
             endif   
        enddo     
        if (modulo(i,500).eq.0) then 
           do j=1,kintervalos_int
             if (histx(j).ne.0.d00) then
                 Hx(int(i/500))=Hx(int(i/500))+intervalo*(log(histx(j)/np))*histx(j)/np
             endif    
           enddo     
           histx=0.d00
        endif  
      enddo
      write(*,*)'########################################'

! Rellenamos el histograma vy y calculamos Hy

      do i=1,500*5001
        v=vyy(i)   
        do j=1,kintervalos_int
             if (v<=-distancia/2.d00+intervalo*j) then
                histy(j)=histy(j)+1.d00
                exit
             endif   
        enddo     
        if (modulo(i,500).eq.0) then 
           do j=1,kintervalos_int
             if (histy(j).ne.0.d00) then
                 Hy(int(i/500))=Hy(int(i/500))+intervalo*(log(histy(j)/np))*histy(j)/np
             endif    
           enddo     
           histy=0.d00
        endif  
      enddo
      write(*,*)'########################################'

      
! Rellenamos el histograma vz y calculamos Hz

      do i=1,500*5001
        v=vzz(i)   
        do j=1,kintervalos_int
             if (v<=-distancia/2.d00+intervalo*j) then
                histz(j)=histz(j)+1.d00
                exit
             endif   
        enddo     
        if (modulo(i,500).eq.0) then 
           do j=1,kintervalos_int
             if (histz(j).ne.0.d00) then
                 Hz(int(i/500))=Hz(int(i/500))+intervalo*(log(histz(j)/np))*histz(j)/np
             endif    
           enddo     
           histz=0.d00
        endif  
      enddo
      write(*,*)'########################################'
    
      t=0.d00
      open(44,file=ruta//"Funcion_H_2.dat")      
        do i=1,kpasos    
            write(44,9004)t,Hx(i),Hy(i),Hz(i)
            t=t+0.0001d00*100.d00
        enddo
      close(44)


 9004 format(1pe19.12,2x,e19.12,2x,e19.12,2x,e19.12)
 
 
      pause
end program