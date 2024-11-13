subroutine SUB_POTLJ_NVT_MONTECARLO(np,part,rx,ry,rz,rxnew,rynew,rznew,Eaux,pl,pli,rc,rc2,vol) 

            use Mod_01_Def_prec
        
            implicit none
            
! Este es una subrutina, la cual calcula la energia potencial cambiando solo una particula
            
            real (kind=doblep), parameter :: pi=3.1415926535898d00
            integer(kind=entero), intent(in) :: np,part
            real(kind=doblep), dimension(:) :: rx,ry,rz
            real(kind=doblep), intent(in) :: rxnew,rynew,rznew
            real(kind=doblep), intent(in) :: vol,pl,pli,rc,rc2
            real(kind=doblep),intent(out) :: Eaux
      
            integer(kind=entero)::i,j
            real(kind=doblep) :: dis2,a2,a6,a12,Esum
            real(kind=doblep) :: rxx,ryy,rzz
            real(kind=doblep) :: rijx,rijy,rijz
      
                 
            Esum=0.d00
            
          !  rxx=rx(part)
          !  ryy=ry(part)
          !  rzz=rz(part)

           ! rx(part)=rx(1)
            !ry(part)=ry(1)
            !rz(part)=rz(1)

     !       rx(1)=rxx
      !      ry(1)=ryy
       !     rz(1)=rzz

    
            Do i=1,np
              if (i.eq.part) cycle
              rijx=rxnew-rx(i)
              rijy=rynew-ry(i)
              rijz=rznew-rz(i)

              rijx=rijx-pl*dnint(rijx*pli) !Aquí estamos aplicando las condiciones de contorno periodicas, ya que si rijx>L/2
              rijy=rijy-pl*dnint(rijy*pli) !   tendremos que será tenido en cuenta la posición de la partícula análoga mas cercana
              rijz=rijz-pl*dnint(rijz*pli) !   en esa dirección. Esta es la manera correcta de implementar las condicioens de contorno.

              dis2=rijx*rijx+rijy*rijy+rijz*rijz
              
            
              if (dis2<rc2) then
                  a2=1.d00/dis2
                  a6=a2*a2*a2
                  a12=a6*a6
                  
                  Esum=Esum+a12-a6
                  !print*,'i=',i,'.','j=',j,'.',Epot
              end if             
            enddo
                
            
            Eaux=4.d00*Esum

end subroutine SUB_POTLJ_NVT_MONTECARLO

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
