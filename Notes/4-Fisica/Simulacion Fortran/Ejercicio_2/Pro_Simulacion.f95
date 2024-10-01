program Pro_Simulacion

      use Mod_01_Def_prec
      use Mod_02_Variables_comunes
      use Mod_03_Interface

      real(kind=doblep) :: E,Ecin,Epot  
      integer(kind=entero) :: iter,i
    
      character(LEN=25) :: gname,fname

 9000 format(a25)
 9001 format(i4,1pe19.12,3(e19.12))  
 9002 format(1pe19.12,e19.12)
 9003 format(1pe19.12,e19.12,e19.12)

 
      iter=1 ! por ahora 1
      


      Do i=0, iter

        open  (10, STATUS='OLD', ACTION='READ')  
        read (10,9001) np,pl,pli,rc,rc2
        read (10,9002) vol, dens
        read (10,9003) E,Ecin,Epot
        read (10,9000) fname 
        read (10,9000) gname
        close (10)
      
        open (20,form='unformatted')
        read (20) rx,ry,rz,vx,vy,vz,ax,ay,az
        close(20)

      enddo
      
        

end program