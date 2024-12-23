program Propiedades_dinamicas

      implicit none
      
      integer, parameter::entero=SELECTED_INT_KIND(9)
      integer, parameter::doblep=SELECTED_REAL_KIND(15,307)

      integer(kind=entero) :: Npmax,kpasos,i,i1,i2,np,j
      real (kind=doblep) :: pl,pli,vol,dens,rc,rc2,dt,Etot,Ecin,Epot
      
      real(kind=doblep),ALLOCATABLE  :: rxx(:,:),ryy(:,:),rzz(:,:)
      real(kind=doblep),ALLOCATABLE  :: vxx(:,:),vyy(:,:),vzz(:,:)
      real(kind=doblep),ALLOCATABLE :: dcm(:),corv(:),tau(:)
      real(kind=doblep)::dx2,dy2,dz2


      character(LEN=25) :: gname,fname
      character(LEN=50) :: gname1,gname2,gname3,gname4,gname5,gname6
      character(LEN=9) :: ruta
      character(LEN=19) :: ruta2
      character(LEN=2)  :: Char_val
      
      integer(kind=entero) :: n_tau,salto,numero

      ! Lee el valor que le da el archivo de lotes (.bat)

      read(*,8001)j,numero

      ! Decimos el archivo que va a leer
      
      WRITE(char_val, '(i2.2)') j

      ! Creamos el nombre de los archivos

      ruta='../Datos/' 
      ruta2='../Datos/Optativo2/' 
      fname='Datos_basicos.dat'   
      gname3='Datos_Posiciones_DM_'//Char_val//'.dat'
      gname4='Datos_Velocidades_DM_'//Char_val//'.dat'
      gname5='Datos_Desplazamiento2_DM_'//Char_val//'.dat'
      gname6='Datos_CorrVel_DM_'//Char_val//'.dat'
           
      ! Lo usamos para leer el nuero de particulas, volumen, numero de pasos
       
      write(*,*)ruta//fname
      open (10,file=ruta//fname, STATUS='old', ACTION='READ')  
      read (10,9001) np,pl,pli,rc,rc2
      read (10,9002) vol, dens
      read (10,9003) Etot,Ecin,Epot
      read (10,9005) Dt,kpasos
      read (10,8000) ruta
      read (10,9000) fname 
      read (10,9000) gname
      close(10)
 
      ! Definimos variables de interes        

      npmax=np
      n_tau=300
      salto=10

      ! LE damos dimension a los arrays

      kpasos=kpasos/100
        
      ALLOCATE(rxx(kpasos,Npmax),ryy(kpasos,Npmax),rzz(kpasos,Npmax))
      ALLOCATE(vxx(kpasos,Npmax),vyy(kpasos,Npmax),vzz(kpasos,Npmax))
      ALLOCATE(dcm(n_tau),corv(n_tau),tau(n_tau))

      ! Leemos los valores iniciales
      
      write(*,*)ruta2//gname3
      open (21,file=ruta2//gname3,form="unformatted",STATUS='old',ACTION='READ')   
      read(21)rxx,ryy,rzz
      close(21)
      open (22,file=ruta2//gname4,form="unformatted",STATUS='old',ACTION='READ')    
      read(22)vxx,vyy,vzz
      close(22)

      ! Inicializamos los valores
      
      tau=0.d00
      corv=0.d00
      dcm=0.d00

      write(*,*)tau(300)

      do i1=1,n_tau
        tau(i1)=Dt*dble(i1)*100.d00
      enddo  
                

      do i1=1,kpasos-n_tau,salto
        do i2=i1,i1+n_tau-1
            do i=1,np
                dx2=(rxx(i1,i)-rxx(i2,i))*(rxx(i1,i)-rxx(i2,i))
                dy2=(ryy(i1,i)-ryy(i2,i))*(ryy(i1,i)-ryy(i2,i))
                dz2=(rzz(i1,i)-rzz(i2,i))*(rzz(i1,i)-rzz(i2,i))

                dcm(i2+1-i1)=dcm(i2+1-i1)+dx2+dy2+dz2
                corv(i2+1-i1)=corv(i2+1-i1)+(vxx(i2,i)*vxx(i1,i))+(vyy(i2,i)*vyy(i1,i))+(vzz(i2,i)*vzz(i1,i))      
            enddo
        enddo    
      enddo  

      dcm=dcm/dble((kpasos-n_tau)*np/salto)
      corv=corv/dble((kpasos-n_tau)*np/salto)
      
      open (23,file=ruta2//gname5,STATUS='old', ACTION='WRITE') 
      open (24,file=ruta2//gname6,STATUS='old', ACTION='WRITE')    
      do i=1,n_tau
         write(23,9800)tau(i),dcm(i)
         write(24,9800)tau(i),corv(i)
      enddo   
      close(23)
      close(24)

      
      
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