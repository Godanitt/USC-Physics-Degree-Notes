program Distribucion_rardial

      implicit none
      
      integer, parameter::entero=SELECTED_INT_KIND(9)
      integer, parameter::doblep=SELECTED_REAL_KIND(15,307)

      integer(kind=entero) :: Npmax,kpasos,i,j,k,np,ksum,numero
      real (kind=doblep) :: pl,pli,vol,dens,rc,rc2,dt,Etot,Ecin,Epot
      real (kind=doblep), parameter :: pi=3.1415926535898d00
      real (kind=doblep) :: dis2,dis,deltar
      
      real(kind=doblep),ALLOCATABLE  :: rxx(:,:),ryy(:,:),rzz(:,:)
      real (kind=doblep) :: rijx,rijy,rijz,rrx,rry,rrz
      real(kind=doblep) :: r(1000),gr(1000),gr_ideal(1000)


      character(LEN=25) :: gname,fname
      character(LEN=50) :: gname1,gname2,gname3,gname5
      character(LEN=9) :: ruta
      character(LEN=19) :: ruta2
      character(LEN=2)  :: Char_val
      

      ! Lee el valor que le da el archivo de lotes (.bat)

      read(*,8001)j,numero

      ! Decimos el archivo que va a leer
      
      WRITE(char_val, '(i2.2)') j

      ! Creamos el nombre de los archivos

      ruta='../Datos/' 
      ruta2='../Datos/Optativo2/' 
      fname='Datos_basicos.dat'   
      gname3='Datos_Posiciones_DM_'//Char_val//'.dat'
      gname5='Datos_gr_DM_'//Char_val//'.dat'
           
      ! Lo usamos para leer el nuero de particulas, volumen, numero de pasos
        
      write(*,*)ruta//fname
      open (10,file=ruta//fname, STATUS='OLD', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol, dens
      read (10,9003) Etot,Ecin,Epot
      read (10,9005) Dt,kpasos
      read (10,8000) ruta
      read (10,9000) fname 
      read (10,9000) gname
      close(10)
      ! Definimos la dimension de los arrays

      Npmax=Np

      ALLOCATE(rxx(kpasos/100,Npmax),ryy(kpasos/100,Npmax),rzz(kpasos/100,Npmax))

      ! Le damos valores a los arrays

      write(*,*)ruta2//gname3
      open (21,file=ruta2//gname3,form="unformatted",STATUS='old',ACTION='READ')   
      read(21)rxx,ryy,rzz
      close(21)

      ! Creamos los valores a los valores de r a los que va asociado gr(r)

      deltar=rc/1000.d00
      do i=1,1000
        r(i)=deltar/2.d00+deltar*(i-1)
      enddo  
      

      ! Inicializamos


      gr=0.d00
   
      

      ! Tenemos que el radio de corte rc marca cual es el valor maximo para la distribucion radial, asi que:

      do k=1,kpasos/100
        do i=1,np-1 
            rrx=rxx(k,i) 
            rry=ryy(k,i) 
            rrz=rzz(k,i) 
          
            DO j=i+1,np

              rijx=rrx-rxx(k,j) 
              rijy=rry-ryy(k,j) 
              rijz=rrz-rzz(k,j) 

              rijx=rijx-pl*dnint(rijx*pli) !Aquí estamos aplicando las condiciones de contorno periodicas, ya que si rijx>L/2
              rijy=rijy-pl*dnint(rijy*pli) !   tendremos que será tenido en cuenta la posición de la partícula análoga mas cercana
              rijz=rijz-pl*dnint(rijz*pli) !   en esa dirección. Esta es la manera correcta de implementar las condicinens de contorno. 

              dis2=rijx*rijx+rijy*rijy+rijz*rijz
            
              if (dis2<rc2) then
                dis=sqrt(dis2)
                ksum=int(dis/deltar)
                gr(ksum+1)=gr(ksum+1)+2.d00

              endif
            enddo
        enddo      
      enddo
      ! Normalizamos

      gr=gr/(dble(np)*dble(kpasos/100))

      ! Calculamos el valor del g(r) para el gas ideal

    <Z  do i=1,1000
        if(i.eq.1) then
          gr_ideal(i)=(4.d00*pi/3.d00)*dens*((r(i)+deltar/2.d00)**3)
        else  
          gr_ideal(i)=(4.d00*pi/3.d00)*dens*((r(i)+deltar/2.d00)**3-(r(i-1)+deltar/2.d00)**3)
        endif
      enddo  

      ! Calculo final:

      gr=gr/gr_ideal
  

      ! Escribimos


      
      open (23,file=ruta2//gname5,STATUS='old', ACTION='WRITE')   
      do i=1,1000
         write(23,9800)r(i),gr(i)
      enddo   
      close(23)

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
 9800 format(1pe19.12,2x,1e19.12)
 
end program