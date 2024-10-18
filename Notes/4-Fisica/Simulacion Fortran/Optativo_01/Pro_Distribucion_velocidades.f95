program Pro_Distribucion_velocidades

      implicit none

      
      integer, parameter::entero=SELECTED_INT_KIND(9)
      integer, parameter::doblep=SELECTED_REAL_KIND(15,307)
      
      real(kind=doblep) :: vx(500),vy(500),vz(500)
      real(kind=doblep) :: vxx(500*5001),vyy(500*5001),vzz(500*5001)
      real,allocatable :: valores_mitad(:),histx(:),histy(:),histz(:)
      real(kind=doblep) :: minimo,maximo,distancia,v,intervalo,kintervalos
      integer (kind=entero) :: i,j,kpasos,kpasos2,kintervalos_int,kintervalos23,kintervalos12
      character(LEN=25) :: vname1,vname2,vname3
      character(LEN=9) :: ruta
      
      vname1='Datos_vx.dat'    
      vname2='Datos_vy.dat'    
      vname3='Datos_vz.dat'  
      ruta='../Datos/'       
      
      kintervalos=sqrt(5001.d00*500.d00)
      kintervalos_int=int(kintervalos)
      allocate(valores_mitad(kintervalos_int),histx(kintervalos_int),histy(kintervalos_int),histz(kintervalos_int))
      
      kpasos=5001
      kpasos2=500
      
      open (41,file=ruta//vname1,form="unformatted")
      open (42,file=ruta//vname2,form="unformatted")
      open (43,file=ruta//vname3,form="unformatted")
      
      vxx=0.d00
      vyy=0.d00      
      vzz=0.d00
    
!     Leyemos todas las velocidades en vxx,vyy,vzz
      
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



      minimo=min(minval(vxx),minval(vyy),minval(vzz))
      maximo=max(maxval(vxx),maxval(vyy),maxval(vzz))

      write(*,*)'min=',minimo
      write(*,*)'max=',maximo
  
      write(*,*)'Absoluto mas grande entre ambos',max(abs(minimo),abs(maximo))
      write(*,*)'intervalos=',kintervalos
       
      distancia=maximo*2.d00
      intervalo=distancia/kintervalos
      kintervalos12=kintervalos_int/3
      kintervalos23=kintervalos12*2

      histx=0.d00
      histy=0.d00      
      histz=0.d00
      
!     Creamos el array valor medio:

      valores_mitad=0.d00
      do i=1,kintervalos
            valores_mitad(i)=-distancia/2.d00+dble(intervalo)/2.d00+dble(i)*dble(intervalo)
      enddo

      write(*,*)'########################################'
          
!     Rellenamos los histogramas vx

      do i=1,500*5001
        v=vxx(i)   
        do j=1,kintervalos_int
             if (v<=-distancia/2.d00+intervalo*j) then
                histx(j)=histx(j)+1.d00
                exit
             endif   
        enddo     
      enddo
      
      open(12,file=ruta//'Histogramas_vx.dat')
      do i=1,kintervalos    
          write(12,9004) valores_mitad(i),histx(i)
      enddo
      close(12)


!     Rellenamos los histogramas vy

      do i=1,500*5001
        v=vyy(i)   
        do j=1,kintervalos_int
             if (v<=-distancia/2.d00+intervalo*j) then
                histy(j)=histy(j)+1.d00
                exit
             endif   
        enddo     
      enddo
      
      open(13,file=ruta//'Histogramas_vy.dat')
      do i=1,kintervalos    
          write(13,9004) valores_mitad(i),histy(i)
      enddo
      close(13)

!     rellenamos el histograma vz

      do i=1,500*5001
        v=vzz(i)   
        do j=1,kintervalos_int
             if (v<=-distancia/2.d00+intervalo*j) then
                histz(j)=histz(j)+1.d00
                exit
             endif   
        enddo     
      enddo
      
      open(14,file=ruta//'Histogramas_vz.dat')
      do i=1,kintervalos    
          write(14,9004) valores_mitad(i),histz(i)
      enddo
      close(14)


      
      
 9004 format(1pe19.12,2x,e19.12)
 
 
      pause
end program