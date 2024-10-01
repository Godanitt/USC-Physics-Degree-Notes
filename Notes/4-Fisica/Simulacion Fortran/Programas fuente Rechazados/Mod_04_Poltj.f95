!##########################################################################################################################################
!
!
!
!
!      
!##########################################################################################################################################

module Mod_04_Poltj

      implicit none

      contains

      Subroutine SUB_POLTJ (np,rx,ry,rz,ax,ay,az,epot,dfiv,d2fiv) 

            use Mod_01_Def_prec
            use Mod_02_Variables_comunes
            use Mod_03_Random

            implicit none
          
            integer (kind=entero), intent(in) :: np
            real(kind=doblep), dimension(:), intent(in):: rx,ry,rz
            real(kind=doblep),intent(out) :: Epot,dfiv,d2fiv
            real(kind=doblep),dimension(:), intent(out) ::  ax,ay,az
      
            integer(kind=entero)::i,j
            real(kind=doblep) :: dis2,a2,a6,a12,aux1,fmod,rvpp_sum,rvpp2_sum,xnp,factor
            real(kind=doblep) :: rrx,rry,rrz,rijx,rijy,rijz
      

            Epot=0.d00
            fmod=0.d00
            rvpp_sum=0.d00 ! -> Llama a esto sumatorio rvpp_sum
            rvpp2_sum=0.d00 ! -> Llama a esto sumatorio  rvpp2_sum

            ax=0.d00
            ay=0.d00
            az=0.d00
            
            xnp=dble(Npmax)
            
            factor =pi*xnp*xnp/(vol*rc**3)                     !          rc = radio corte, vol =volumen, xnp = doble (npmax)
            corr_ener=8.d00*factor*(1.d00/(3.00*rc**6)-1.d00)/3.d00
            corr_sum_rvp=16.d00*factor*(-2.d00/(3.d00*rc**6)+1.d00)
            corr_sum_r2vpp=16.d00*factor*(26.d00/(3.d00*rc**6)-7.d00)

            DO i=1,np-1
            rrx=rx(i)
            rry=ry(i)
            rrz=rz(i) 
          
            DO j=i+1,np

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
                  rvpp_sum=rvpp_sum+aux1 ! Esto debería llamrse sumatorio, no son las derivadas, que quede claro!!
                  
                  rvpp2_sum=rvpp2_sum+26.d00*a12-7.d00*a6 ! Esto debería llamrse sumatorio, no son las derivadas
                    
                  ax(i)=ax(i)+fmod*rijx
                  ay(i)=ay(i)+fmod*rijy
                  az(i)=az(i)+fmod*rijz                  
                  ax(j)=ax(j)-fmod*rijx
                  ay(j)=ay(j)-fmod*rijy
                  az(j)=az(j)-fmod*rijz               
              end if
            ENDDO
            ENDDO        
      
            Epot=4*Epot+corr_ener
            rvpp_sum=rvpp_sum+corr_sum_rvp
            rvpp2_sum=rvpp2_sum+corr_sum_r2vpp
        
            print*,'Epot=',Epot
      
            ax=24.d00*ax
            ay=24.d00*ay
            az=24.d00*az

            d2fiv=(rvpp2_sum-2.d00*rvpp_sum)/(9.d00*vol*vol)

            dfiv=rvpp_sum/(3.d00*vol) ! loa términos de la derecha hay que llamarles como los sumatorios 

      

      end subroutine

end module 