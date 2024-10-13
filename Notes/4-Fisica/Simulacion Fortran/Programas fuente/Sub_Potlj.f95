
subroutine SUB_POTLJ(np,rx,ry,rz,ax,ay,az,epot,dfiv,d2fiv) 

            use Mod_02_Variables_comunes
            
            implicit none

            
!##########################################################################################################################################      
!   VARIABLES definias en el modulo VARIABLES_COMUNES
!
!   npmax   -> Número de partículas que vamos a tener en cuenta para la simulacion (coincide con n, el número de particulas de la simulacion)
!   numk    -> Entero que nos permite calcular el numero N para crear una fcc perfecta, tal que Npmax=4*k*k*k
!   pi      -> Número pi
!   pl      -> Lado de la caja, pl=vol**(1/3)
!   pli     -> Lado inverso de la caja pli=1/pl
!   vol     -> Volumen
!   rc      -> Radio de corte, rc=pl/2.d00
!   rc2     -> Radio de corte al cuadrado rc2=rc*rc
!   dt      -> Paso del tiempo
!   dt12    -> Paso del tiempo mitad dt12=dt/2
!   dt2     -> Paso del tiempo cuadrado mitad dt2=dt*dt/2
!   Et      -> Energía total, dato del ejercicio, por eso está definida aquí  
!   corr_ener       -> Correción a la energía, le damos un valor cero para no tener problemas si después la llamamos y no esta definida
!   corr_sum_rvp    -> Correción a diferencial potencial de volumen , le damos un valor cero para no tener problemas si después la llamamos y no esta definida
!   corr_ener_r2vpp -> Correción a diferencial potencial de voluemn (2o orde), le damos un valor cero para no tener problemas si después la llamamos y no esta definida
!
!
!   VARIABLES IMPORTANTES (entrada o salida)
!
! np        -> Número de partículas con la que generamos la red. En este caso coinciden np=npmax.
! rx,ry,rz  -> Vectores posiciones de las partículas (rx(i)-> posición en x de la partícula i)
! vx,vy,vz  -> Vectores velocidades de las partículas (vy(i)-> velocidad en y de la partícula i)
! ax,ay,az  -> Vectores aceleracionse de las partículas (az(i)-> aceleracion en z de la partícula i)
! Etot      -> Suma de Ep+Ecin, debe ser igual a Et (si no algo esta mal)
! Epot      -> Energía potencial, se obtiene de la subrutina potlj
! Ecin      -> Energía cinética, debe coincidir al final con Et-fEpot
! dfiv      -> Derivada del potencial respecto el volumen, calculada con la subrutina poltj, una vez esta corregida
! d2fiv     -> Derivada 2a del potencial respecto el volumen, calculada con la subrutina poltj, una vez esta corregida 
!
!   VARIABLES AUXILIARES (NI entrada NI salida)
!
! i,j       -> Nos ayudan a calcular la energia potencial para cada par de posiciones (i de 1 a 499, j de i+1 a 500)
! dis2      -> Distancia entre dos posicioens i,j. Si dis2>rc2 no se calculara la fuerza ni el potencial entre ambas
! a2,a6,a12 -> Si dis2<rc2, tenemos que a2=1/dis2,a6=a2**3,a12=a6*a6
! fmod      -> Fuerza en modulo, para calcular la fuerza total real en una dirección hay que multiplicarlo por rijx (en x) (analogo para y,z)
! rvpp_sum  -> Valor de la derivada del potencial respecto a r, nos sirve para luego calcluar dfiv (tras corregirlo con corr_sum_rvpp)
! rvppp2_sum-> Valor de la 2a derivada del potencial respecto a r, nos sirve para luego calcluar dfiv2 (tras corregirlo con corr_sum_r2vpp)
! xnp       -> Doble de Npmax, nos sirve para calcular el factor de correción. Dado que el número de partículas que son tenidas en cuenta para la DM es npmax, tenemos que usar npmax y no n
! factor    -> Factor que nos permice agilizar el calculo de dfiv, d2fiv (factor igual en ambas)
! rrx,rry,rrz -> Posición de la partícula i para el lazo
! rijx,rijy,rijz -> Distancia entre la partícula i y j (rrx-rx(j)) en el eje x (para y,z, analogo)
!
!##########################################################################################################################################      

! Este es una subrutina, a la cual le llegan las posiciones de las partículas y el número de partículas que hay en la red y calcula
!   la energía potencial (y las derivadas respecto el volumen) del sistema y las fuerzas que se ejercen entre ellas.
            
            integer (kind=entero), intent(in) :: np
            real(kind=doblep), dimension(:), intent(in):: rx,ry,rz
            real(kind=doblep),intent(out) :: Epot,dfiv,d2fiv
            real(kind=doblep),dimension(:) ::  ax,ay,az
      
            integer(kind=entero)::i,j
            real(kind=doblep) :: dis2,a2,a6,a12,aux1,fmod,rvpp_sum,rvpp2_sum,xnp,factor
            real(kind=doblep) :: rrx,rry,rrz,rijx,rijy,rijz
      
                 
            Epot=0.d00
            fmod=0.d00
            rvpp_sum=0.d00 
            rvpp2_sum=0.d00 

            ax=0.d00
            ay=0.d00
            az=0.d00
            
            xnp=dble(Npmax)
            
            factor =pi*xnp*xnp/(vol*rc**3)        ! rc = radio corte, vol =volumen, xnp = doble (npmax)
            corr_ener=8.d00*factor*(1.d00/(3.00*rc**6)-1.d00)/3.d00
            corr_sum_rvp=16.d00*factor*(-2.d00/(3.d00*rc**6)+1.d00)
            corr_sum_r2vpp=16.d00*factor*(26.d00/(3.d00*rc**6)-7.d00)

            DO i=1,np-1
  
            rrx=rx(i) ! Definimos la posición de la partícula i aquí para agilizar el lazo j=i+1,np; 
            rry=ry(i) !    ya que de otra forma tendríamos con cada interaccion de j definir rx(i),ry(i),rz(i)
            rrz=rz(i) 
          
             DO j=i+1,np

              rijx=rrx-rx(j)
              rijy=rry-ry(j)
              rijz=rrz-rz(j)

              rijx=rijx-pl*dnint(rijx*pli) !Aquí estamos aplicando las condiciones de contorno periodicas, ya que si rijx>L/2
              rijy=rijy-pl*dnint(rijy*pli) !   tendremos que será tenido en cuenta la posición de la partícula análoga mas cercana
              rijz=rijz-pl*dnint(rijz*pli) !   en esa dirección. Esta es la manera correcta de implementar las condicioens de contorno.

              dis2=rijx*rijx+rijy*rijy+rijz*rijz
            
              if (dis2<rc2) then
                  a2=1.d00/dis2
                  a6=a2*a2*a2
                  a12=a6*a6
                  
                  Epot=Epot+a12-a6
                  !print*,'i=',i,'.','j=',j,'.',Epot
                  
                  aux1=-2.d00*a12+a6
                  
                  fmod=-aux1*a2
                  rvpp_sum=rvpp_sum+aux1 
                  
                  rvpp2_sum=rvpp2_sum+26.d00*a12-7.d00*a6 
                    
                  ax(i)=ax(i)+fmod*rijx
                  ay(i)=ay(i)+fmod*rijy
                  az(i)=az(i)+fmod*rijz                  
                  ax(j)=ax(j)-fmod*rijx
                  ay(j)=ay(j)-fmod*rijy
                  az(j)=az(j)-fmod*rijz               
              end if
             ENDDO
            ENDDO        

            ! Corregimos los valores para no crear un error sistematico
            
            Epot=4*Epot+corr_ener
            rvpp_sum=rvpp_sum+corr_sum_rvp
            rvpp2_sum=rvpp2_sum+corr_sum_r2vpp
        
            ! Corregimos las aceleraciones para que tengan el valor correcto
            
            ax=24.d00*ax
            ay=24.d00*ay
            az=24.d00*az

            ! Calculamos las derivadas con los valores corregidos

            d2fiv=(rvpp2_sum-2.d00*rvpp_sum)/(9.d00*vol*vol)

            dfiv=rvpp_sum/(3.d00*vol) 

end subroutine SUB_POTLJ 
