! #####################################################################################################
!   DEFINIMOS LAS VARIABLES
!
!       N -> número de partículas, que como debe verificar N=4M**3 -> N=4,32,108,256,500,864
!       M -> dado un N, se define como M=(N/4)**(1/3)       
!       rho -> densidad 
!       V -> volumen de la caja
!       L -> lado de la caja
!       a -> mitad del lado de la caja, usado para colocar las partículas correctamente en la caja (fcc)
!
! #####################################################################################################
!
!   PRIMERA PARTE DEL PROGRAMA
!
!   En la primera parte asignamos a cada partícula una posición en los vectores rx,ry,rz
!
! #####################################################################################################
!
!   SEGUNDA PARTE DEL PROGRAMA
!
!   En la segunda parte del programa calculamos la energía potencial total del sistema
!
! #####################################################################################################


PROGRAM Progm_01_Colocacion_inicial

! IMPORTAMOS LOS MODULOS      

      use Mod_01_Def_prec
      !module variables_comunes ! creo que es para que asuma las variables globales -> investigar

! HACEMOS IMPLICITAS LAS VARIABLES
      
      implicit none
      
! DEFINIMOS LAS VARIABLES 

      integer :: x,y,z,N,K,cuenta
      real(kind=doblep) :: rho,V,L,a
      real, allocatable :: rx(:),ry(:),rz(:)
      
! ASIGNAMOS VALORES A LAS VARIABLES


      K=5
      N=4*K*K*K   
      rho = 0.5
      L=10
      a=L/2
      V=L*L*L

      cuenta = 0  
      allocate(rx(N)); allocate(ry(N)); allocate(rz(N)) 
      

! #####################################################################################################
! PARTE 1: ASIGNAMOS POSICIONES INICIALES A LAS PARTICULAS 

      DO x=0,K-1
          DO y=0,K-1
              DO z=0,K-1
                
                  rx(cuenta)=x*L
                  ry(cuenta)=y*L
                  rz(cuenta)=z*L
                  
                  rx(cuenta+1)=a+x*L
                  ry(cuenta+1)=a+y*L
                  rz(cuenta+1)=z*L
                  
                  rx(cuenta+2)=a+x*L
                  ry(cuenta+2)=y*L
                  rz(cuenta+2)=a+z*L

                  rx(cuenta+3)=x*L
                  ry(cuenta+3)=a+y*L
                  rz(cuenta+3)=a+z*L
                  
                 ! cuenta = cuenta + 4

                  PRINT*,cuenta
              ENDDO
          ENDDO
      ENDDO            


! #####################################################################################################
! PARTE 1.5: APLICAR RANDOMIZACION A LAS POSICIONES

      

! #####################################################################################################
! PARTE 2: CALCULAMOS LAS ENERGÍAS PONTENCIALES






! #####################################################################################################
! PARTE 3: CALCULAMOS LAS VELOCIDADES



! #####################################################################################################
! PARTE 4: CALCULAMOS LAS ENERGÍAS


! #####################################################################################################
! PARTE 5: GUARDAMOS EN LOS ARCHIVOS

      Pause 

ENDPROGRAM Progm_01_Colocacion_inicial
