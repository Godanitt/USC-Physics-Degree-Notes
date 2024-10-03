
!##########################################################################################################################################
!
!
!
!##########################################################################################################################################


PROGRAM Pro_Crea_red

      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface
     ! use Mod_03_Random
     ! use Mod_04_Poltj
      
      
      implicit none

     ! real(kind=doblep) :: Fun_Random

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
      character(LEN=9) :: ruta

     ! integer::i,j
     ! real(kind=doblep) :: dis2,a2,a6,a12,aux1,fmod
     ! real(kind=doblep) :: rrx,rry,rrz,rijx,rijy,rijz

      Etot=575.d00
      dens=0.5d00
      np=Npmax
      pl=10.d00
      pli=1/pl
      vol=pl*pl*pl
      rc=pl/2
      rc2=rc*rc
      
    

                    
!##########################################################################################################################################
! PARTE 1: ASIGNAMOS POSICIONES INICIALES A LAS PART�CULAS

      pa=pl/dble(numk) ! Hay que llamarle pa 
      pma=pa/2.d00 ! Hay que llamarle pma
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


      ! hay que hacer aqui la aleatorización 


!##########################################################################################################################################

! PARTE 2: CALCULAMOS LAS ENERGÍAS POTENCIALES Y LAS FUERZAS

      CALL SUB_POLTJ(np,rx,ry,rz,ax,ay,az,epot,dfiv,d2fiv) 
    


!##########################################################################################################################################
! PARTE 3: CALCULAMOS LAS ENERGICAS CINETICAS Y VELOCIDADES

      ! Para generar las velocidades tenemos que usar en random, luego corregir para que VT=0 y para que la Ecin=E-Epot
        
      Idum=898 ! Ya le daremo una variable random
      DO i=1,Npmax
          vx(i)=(2.d00*Fun_random(Idum)-1.d00)
          vy(i)=(2.d00*Fun_random(Idum)-1.d00)
          vz(i)=(2.d00*Fun_random(Idum)-1.d00)
      ENDDO

      px=sum(vx)/Npmax
      py=sum(vy)/Npmax
      pz=sum(vz)/Npmax

      DO i=1,Npmax
          vx(i)=vx(i)-px
          vy(i)=vy(i)-py
          vz(i)=vz(i)-pz
      ENDDO

      print*,'sum(vx)=',sum(vx)
      print*,'sum(vy)=',sum(vy)
      print*,'sum(vz)=',sum(vz)

      Ecin=Et-Epot
      !print*,'Ecin=',Ecin
      
      px=Dot_Product(vx,vx)
      py=Dot_Product(vy,vy)
      pz=Dot_Product(vz,vz) !funciona exactamente igual con sum(vz*vz)
      !print*,'sum(px)=',(px)
      !print*,'sum(py)=',(py)
      !print*,'sum(pz)=',(pz)

      pt=sqrt(px+py+pz)
      
      pt1=1/pt
          
      Ecin=sqrt(2.d00*Ecin)

      vx=vx*Ecin*pt1
      vy=vy*Ecin*pt1
      vz=vz*Ecin*pt1
      
      
      px=Dot_Product(vx,vx)
      py=Dot_Product(vy,vy)
      pz=Dot_Product(vz,vz)
      !print*,'sum(px)=',(px)
      !print*,'sum(py)=',(py)
      !print*,'sum(pz)=',(pz)

      Ecin=(px+py+pz)/2      
      !print*,'Ecin=',Ecin

      print*,'Etot=',Et,'  Etot_real=',Ecin+Epot, 'Epot',Epot
      

!##########################################################################################################################################
! PARTE 4: GUARDAMOS LOS DATOS EN EL .DAT

      fname='Datos_basicos.dat'      
      gname='Datos_particulas.dat'      
      ruta='../Datos/'

      open  (10,file=ruta//fname)  
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

 8000 format(a9)
 9000 format(a25)
 9001 format(i4,2x,1pe19.12,3(2x,e19.12)) ! -> el 19.12 es perfecto para los decimales, mientras que el 1pe ya sabemos que es por la potenciación. Lo ultimo 3(3x,e19.12) quiere decir que 3 veces con el mismo formato 
 9002 format(1pe19.12,2x,e19.12)
 9003 format(1pe19.12,2x,e19.12,2x,e19.12)
        

end program