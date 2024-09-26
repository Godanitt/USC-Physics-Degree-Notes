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

      implicit none

      integer::x,y,z,k,cuenta
      real(kind=doblep) :: b,a
      real(kind=doblep) :: rx(Npmax),ry(Npmax),rz(Npmax)

      integer::i,j
      real(kind=doblep) :: Epot,dfiv,d2fiv
      real(kind=doblep) :: dis2,a2,a6,a12,aux1,fmod
      real(kind=doblep) :: rrx,rry,rrz,rijx,rijy,rijz
      real(kind=doblep)  :: Fx(Npmax),Fy(Npmax),Fz(Npmax)

      real(kind=doblep) :: vx(Npmax),vy(Npmax),vz(Npmax)
      real(kind=doblep) :: Ecin
      
!      real(kind=doblep) :: Fuerza(Npmax,Npmax),Potencial(Npmax,Npmax)

      dens=0.5
      pl=10.d00
      pli=1/pl
      vol=pl*pl*pl
      rc=pl/2
      rc2=rc*rc
    


!##########################################################################################################################################
! PARTE 1: ASIGNAMOS POSICIONES INICIALES A LAS PARTÍCULAS

      b=pl/numk
      a=b/2.d00
      cuenta=1  

      do x=0,numk-1
          do y=0,numk-1
              do z=0,numk-1                      

                  rx(cuenta)=x*b
                  ry(cuenta)=y*b
                  rz(cuenta)=z*b               

                  rx(cuenta+1)=x*b+a
                  ry(cuenta+1)=y*b+a
                  rz(cuenta+1)=z*b                

                  rx(cuenta+2)=x*b+a
                  ry(cuenta+2)=y*b
                  rz(cuenta+2)=z*b+a              

                  rx(cuenta+3)=x*b
                  ry(cuenta+3)=y*b+a
                  rz(cuenta+3)=z*b+a
                
                  print*,cuenta
                  cuenta=cuenta+4
              enddo
          enddo
      enddo


! hay que hacer aqui la aleatorización 


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
                  print*,'i=',i,'.','j=',j,'.',Epot
                  
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



!##########################################################################################################################################
! PARTE 3: CALCULAMOS LAS ENERGICAS CINETICAS Y VELOCIDADES

        ! Para generar las velocidades tenemos que usar en random, luego corregir para que VT=0 y para que la Ecin=E-Epot

      DO i=1,Npmax
         ! vx(i)=Fun_Random(5)
         ! vy(i)=Fun_Random(7)
         ! vz(i)=Fun_Random(16)
      ENDDO



      
        


        




!##########################################################################################################################################
! PARTE 4: GUARDAMOS LOS DATOS EN EL .DAT




      pause

end program