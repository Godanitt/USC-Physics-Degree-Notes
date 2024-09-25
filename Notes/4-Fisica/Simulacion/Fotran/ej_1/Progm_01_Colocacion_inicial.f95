
! #####################################################################################################
!   DEFINIMOS LAS VARIABLES
!
!       Np -> número de partículas, que como debe verificar Np=4M**3 -> Np=4,32,108,256,500,864
!       M -> dado un Np, se define como M=(Np/4)**(1/3)       
!       Npmax -> número de partículas que vamos a usar, que como debe verificar Npmax=4M**3 -> Npmax=4,32,108,256,500,864
!       rho -> densidad 
!       Vol -> volumen de la caja
!       L -> lado de la caja
!       a -> mitad del lado de la caja, usado para colocar las partículas correctamente en la caja (fcc)
!       epot -> energía potencial del sistema
!       Potencial -> Matrix Np x Np que contiene las energías potenciales qeu se ejercen entre las partículas
!       Fuerza -> Matrix Np x Np que contiene las fuerzas que se ejercen las partículas entre ellas - Esta en modulo - F_{kj} Fuerza que ejerce la partícula j sobre k
!       r2 -> distancia entre dos puntos al cuadrado
!       Epot -> Energía potencial global

!       r21 -> distancia entre dos puntos al cuadrado inversa

!
! #####################################################################################################
!
!   PRIMERA PARTE DEL PROGRAMA
!
!   En la primera parte asignamos a cada partícula una posición en los vectores rx,ry,rz
!
!
!   SEGUNDA PARTE DEL PROGRAMA
!
!   En la segunda parte del programa calculamos la energía potencial total del sistema y las fuerzas.

!   TERCERA PARTE DEL PRGRAMA
!
!   Calcular las energías cinéticas, esto es, las velocidades.
!
! #####################################################################################################


PROGRAM Progm_01_Colocacion_inicial
! IMPORTAMOS LOS MODULOS      

      use Mod_01_Def_prec
      use Mod_02_Variables_comunes ! creo que es para que asuma las variables globales -> investigar

! HACEMOS IMPLICITAS LAS VARIABLES
      
      implicit none
      
! DEFINIMOS LAS VARIABLES 

      integer :: i,j,x,y,z,K,cuenta
      real(kind=doblep) :: b,a,r2,r21,Epot
      real (kind=doblep) :: rx(500),ry(500),rz(500)
      real(kind=doblep) :: Fuerza(Np,Np), Potencial(Np,Np)
      
! ASIGNAMOS VALORES A LAS VARIABLES

      Npmax=500
      rho = 0.5
      L=10
      Vol=L*L*L
      rc=L/2

      

! #####################################################################################################
! PARTE 1: ASIGNAMOS POSICIONES INICIALES A LAS PARTICULAS 

      K=5
      b=L/K
      a=b/2
      cuenta = 0  

      DO x=0,K-1
          DO y=0,K-1
              DO z=0,K-1
                                
                  rx(cuenta)=x*b
                  ry(cuenta)=y*b
                  rz(cuenta)=z*b
                                
                  rx(cuenta+1)=a+x*b
                  ry(cuenta+1)=a+y*b
                  rz(cuenta+1)=z*b
                                    
                  rx(cuenta+2)=a+x*b
                  ry(cuenta+2)=y*b
                  rz(cuenta+2)=a+z*b
                                        
                  rx(cuenta+3)=x*b
                  ry(cuenta+3)=a+y*b
                  rz(cuenta+3)=a+z*b
                                    
                  cuenta = cuenta + 4
                                        
                  PRINT*,cuenta
              ENDDO
          ENDDO
      ENDDO            
         

! #####################################################################################################
! PARTE 1.5: APLICAR RANDOMIZACION A LAS POSICIONES

! #####################################################################################################
! PARTE 2: CALCULAMOS LAS ENERGÍA
      r2=0
      r21=0

      Epot=0
      DO i=0,Np-2
          DO j=i+1,Np-1
              r2 = (rx(i)-rx(j))*(rx(i)-rx(j))+(ry(i)-ry(j))*(ry(i)-ry(j))+(rz(i)-rz(j))*(rz(i)-rz(j))
              if (r2<rc) then 
                  print*,'i=',i,'.','j=',j,'.',r2
                  r21=1/r2
                  Epot=Epot+r21**6-r21*r21*r21     
              end if              
          ENDDO
      ENDDO        
      print*,4*Epot
      Potencial=4*Potencial
      Fuerza=24*Fuerza 


! #####################################################################################################
! PARTE 3: CALCULAMOS LAS VELOCIDADES



! #####################################################################################################
! PARTE 4: CALCULAMOS LAS ENERGÍAS



! #####################################################################################################
! PARTE 5: GUARDAMOS EN LOS ARCHIVOS




      Pause 

ENDPROGRAM Progm_01_Colocacion_inicial


! Aquí podemos hacer una subrutina para calcular las energías poteciales

