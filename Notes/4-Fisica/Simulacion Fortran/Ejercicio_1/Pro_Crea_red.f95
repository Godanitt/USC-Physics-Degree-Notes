!##########################################################################################################################################
!
!
!
!
!
!
!
!
!
!
!
!##########################################################################################################################################


PROGRAM Pro_01_Crea_red

      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Random
      
      implicit none

     ! real(kind=doblep) :: Fun_Random
      integer(kind=entero) :: Idum
      
      integer::x,y,z,k,cuenta      
      real(kind=doblep) :: b,a,porcentaje
      real(kind=doblep) :: rx(Npmax),ry(Npmax),rz(Npmax)

      integer::i,j
      real(kind=doblep) :: Epot,dfiv,d2fiv
      real(kind=doblep) :: dis2,a2,a6,a12,aux1,fmod
      real(kind=doblep) :: rrx,rry,rrz,rijx,rijy,rijz
      real(kind=doblep)  :: Fx(Npmax),Fy(Npmax),Fz(Npmax)
      real(kind=doblep)  :: ax(Npmax),ay(Npmax),az(Npmax)

      real(kind=doblep) :: vx(Npmax),vy(Npmax),vz(Npmax)
      real(kind=doblep) :: Ecin,px,py,pz,pt,pt1

      character(LEN=25) :: gname,fname

      
      
!      real(kind=doblep) :: Fuerza(Npmax,Npmax),Potencial(Npmax,Npmax)


      dens=0.5
      pl=10.d00
      pli=1/pl
      vol=pl*pl*pl
      rc=pl/2
      rc2=rc*rc
    

                    
!##########################################################################################################################################
! PARTE 1: ASIGNAMOS POSICIONES INICIALES A LAS PART�CULAS

      b=pl/numk
      a=b/2.d00
      porcentaje=0.1d00
      cuenta=1  
      do x=0,numk-1
          do y=0,numk-1
              do z=0,numk-1           
                  rx(cuenta)=x*b+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  ry(cuenta)=y*b+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  rz(cuenta)=z*b+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  cuenta=cuenta+1
                  rx(cuenta)=x*b+a+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  ry(cuenta)=y*b+a+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  rz(cuenta)=z*b+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  cuenta=cuenta+1
                  rx(cuenta)=x*b+a+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  ry(cuenta)=y*b+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  rz(cuenta)=z*b+a+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  cuenta=cuenta+1
                  rx(cuenta)=x*b+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  ry(cuenta)=y*b+a+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  rz(cuenta)=z*b+a+(2.d00*Fun_random(cuenta)-1.d00)*porcentaje*a
                  cuenta=cuenta+1
              enddo
          enddo
      enddo


! hay que hacer aqui la aleatorizaci�n 


!##########################################################################################################################################
! PARTE 2: CALCULAMOS LAS ENERGÍAS POTENCIALES Y LAS FUERZAS

      Epot=0.d00
      fmod=0.d00
      dfiv=0.d00
      d2fiv=0.d00

      Fx=0.d00
      Fy=0.d00
      Fz=0.d00

      DO i=1,Npmax-1
          rrx=rx(i)
          rry=ry(i)
          rrz=rz(i) 
          
          DO j=i+1,Npmax

              rijx=rrx-rx(j)
              rijy=rry-ry(j)
              rijz=rrz-rz(j)

              rijx=rijx-pl*dnint(rijx*pli) !No se que es esto, no se que es dnint
              rijy=rijy-pl*dnint(rijy*pli)
              rijz=rijz-pl*dnint(rijz*pli)

              dis2=rijx*rijx+rijy*rijy+rijz*rijz
            
              if (dis2<rc2) then
                  a2=1.d00/dis2
                  a6=a2*a2*a2
                  a12=a6*a6
                  
                  Epot=Epot+a12-a6
                  !print*,'i=',i,'.','j=',j,'.',Epot
                  
                  aux1=-2.d00*a12+a6
                  fmod=aux1*a2
                  dfiv=dfiv+aux1
                  d2fiv=d2fiv+26.d00*a12-7.d00*a6
                    
                  Fx(i)=Fx(i)+fmod*rijx
                  Fy(i)=Fy(i)+fmod*rijy
                  Fz(i)=Fz(i)+fmod*rijz                  
                  Fx(j)=Fx(j)-fmod*rijx
                  Fy(j)=Fy(j)-fmod*rijy
                  Fz(j)=Fz(j)-fmod*rijz               
              end if
          ENDDO
      ENDDO        
      
      Epot=4*Epot+corr_ener
      dfiv=dfiv+corr_sum_rvp
      d2fiv=d2fiv+corr_sum_r2vpp
        
      print*,'Epot=',Epot
      
      Fx=24.d00*Fx
      Fy=24.d00*Fy
      Fz=24.d00*Fz
        
      ax=Fx
      ay=Fy
      az=Fz  


!##########################################################################################################################################
! PARTE 3: CALCULAMOS LAS ENERGICAS CINETICAS Y VELOCIDADES

        ! Para generar las velocidades tenemos que usar en random, luego corregir para que VT=0 y para que la Ecin=E-Epot
        
      Idum=5 ! Ya le daremo una variable random
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
      pz=Dot_Product(vz,vz)
      !print*,'sum(px)=',(px)
      !print*,'sum(py)=',(py)
      !print*,'sum(pz)=',(pz)

      pt=sqrt(px+py+pz)
      
      pt1=1/pt
          
      Ecin=sqrt(2.d00*Ecin)
      
      DO i=1,Npmax
          vx(i)=vx(i)*Ecin*pt1
          vy(i)=vy(i)*Ecin*pt1
          vz(i)=vz(i)*Ecin*pt1
      ENDDO    
      
      px=Dot_Product(vx,vx)
      py=Dot_Product(vy,vy)
      pz=Dot_Product(vz,vz)
      !print*,'sum(px)=',(px)
      !print*,'sum(py)=',(py)
      !print*,'sum(pz)=',(pz)

      Ecin=(px+py+pz)/2      
      !print*,'Ecin=',Ecin

      print*,'Etot=',Et,'  Etot_real=',Ecin+Epot
      

!##########################################################################################################################################
! PARTE 4: GUARDAMOS LOS DATOS EN EL .DAT

      fname='Datos_Constantes.txt'      
      gname='Velocidades.txt'      


      open  (10,file=fname)  
      write (10,9001) npmax,pl,pli,rc,rc2
      write (10,9002) vol, dens
      write (10,9003) ecin+epot,Ecin,Epot
      write (10,9000) fname 
      write (10,9000) gname
      close (10)
      
      open (20,file=gname,form='unformatted')
      write(20) rx,ry,rz,vx,vy,vz,ax,ay,az
      close(20)

 9000 format (a25)
 9001 format(i4,2x,1pe19.12,3(2x,e19.12)) !-> el 19.12 es perfecto para los decimales, mientras que el 1pe ya sabemos que es por la potenciaci�n. Lo ultimo 3(3x,e19.12) quiere decir que 3 veces con el mismo formato 
 9002 format(1pe19.12,2x,e19.12)
 9003 format(1pe19.12,2x,e19.12,2x,e19.12)


      pause
end program