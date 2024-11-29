
subroutine SUB_GEAR5(np,rx,ry,rz,vx,vy,vz,ax,ay,az,bx,by,bz,cx,cy,cz,dx,dy,dz,s,vs,as,epot,dfiv,d2fiv,Q,f) 

            use Mod_01_Def_prec
            use Mod_02_Variables_comunes
            use Mod_03_Interface

            
            implicit none
         
            integer (kind=entero), intent(in) :: np
            real (kind=doblep), intent(in) :: Q,f
            real(kind=doblep),intent(out) :: Epot,dfiv,d2fiv
            real(kind=doblep)  :: s,vs,as
            real (kind=doblep), parameter :: a0=3.d00/16.d00,a1=251.d00/360.d00,a2=1.d00,a3=11.d00/18.d00,a4=1/6.d00,a5=1/60.d00
            real(kind=doblep),dimension(np)::rx,ry,rz,vx,vy,vz,ax,ay,az,bx,by,bz,cx,cy,cz,dx,dy,dz
            real(kind=doblep),dimension(np)::dax,day,daz ! d=delta; Error en las  aceleraciones 
            real(kind=doblep),dimension(np)::axc,ayc,azc ! Aceleraciones corregidas

            !dt12=dt/2.d00

            ! Calculamos en t+dt
                   
            rx=rx+vx*dt+ax*dt*dt/2.d00+bx*dt*dt*dt/6.d00+cx*dt*dt*dt*dt/24.d00+dx*dt*dt*dt*dt*dt/120.d00
            ry=ry+vy*dt+ay*dt*dt/2.d00+by*dt*dt*dt/6.d00+cy*dt*dt*dt*dt/24.d00+dy*dt*dt*dt*dt*dt/120.d00
            rz=rz+vz*dt+az*dt*dt/2.d00+bz*dt*dt*dt/6.d00+cz*dt*dt*dt*dt/24.d00+dz*dt*dt*dt*dt*dt/120.d00

            vx=vx+ax*dt+bx*dt*dt/2.d00+cx*dt*dt*dt/6.d00+dx*dt*dt*dt*dt/24.d00
            vy=vy+ay*dt+by*dt*dt/2.d00+cy*dt*dt*dt/6.d00+dy*dt*dt*dt*dt/24.d00
            vz=vz+az*dt+bz*dt*dt/2.d00+cz*dt*dt*dt/6.d00+dz*dt*dt*dt*dt/24.d00

            ax=ax+bx*dt+cx*dt*dt/2.d00+dx*dt*dt*dt/6.d00
            ay=ay+by*dt+cy*dt*dt/2.d00+dy*dt*dt*dt/6.d00
            az=az+bz*dt+cz*dt*dt/2.d00+dz*dt*dt*dt/6.d00
            
            bx=bx+cx*dt+dx*dt*dt/2.d00
            by=by+cy*dt+dy*dt*dt/2.d00
            bz=bz+cz*dt+dz*dt*dt/2.d00

            cx=cx+dx*dt
            cy=cy+dy*dt
            cz=cz+dz*dt

            ! Llamamos a la subrutina ponteical para calcular el valor corregido


            call SUB_POTLJ(np,rx,ry,rz,axc,ayc,azc,epot,dfiv,d2fiv)  

            ! Calculamos s,vs,as en t+dt (aplicamos verlet en esta)
            
            ! Calculamos el error     

            axc=axc/(s*s)-2.d00*vs*vx/s
            ayc=ayc/(s*s)-2.d00*vs*vy/s
            azc=azc/(s*s)-2.d-00*vs*vz/s
            
            
            dax=(axc-ax)
            day=(ayc-ay)
            daz=(azc-az)

            ! Calculamos el valor corregido

            rx=rx+a0*dt12*dt*dax
            ry=ry+a0*dt12*dt*day
            rz=rz+a0*dt12*dt*daz

            vx=vx+a1*dt12*dax
            vy=vy+a1*dt12*day
            vz=vz+a1*dt12*daz

            ax=ax+a2*dax
            ay=ay+a2*day
            az=az+a2*daz

            bx=bx+a3*dti*dax*3
            by=by+a3*dti*day*3
            bz=bz+a3*dti*daz*3

            cx=cx+a4*dti*dti*dax*12
            cy=cy+a4*dti*dti*day*12
            cz=cz+a4*dti*dti*daz*12

            dx=dx+a5*dti*dti*dti*dax*60
            dy=dy+a5*dti*dti*dti*day*60
            dz=dz+a5*dti*dti*dti*daz*60

            s=s+vs*dt+as*dt12*dt

            vs=vs+as*dt12

            as=(s*(Dot_Product(vx,vx)+Dot_Product(vy,vy)+Dot_Product(vz,vz))-f*T/s)/Q
            
            vs=vs+as*dt12
            

            call SUB_POTLJ(np,rx,ry,rz,axc,ayc,azc,epot,dfiv,d2fiv)  
end subroutine
    
            