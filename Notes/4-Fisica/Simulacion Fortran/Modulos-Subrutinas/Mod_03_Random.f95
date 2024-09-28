
module Mod_03_Random

use Mod_01_Def_prec

contains

real(kind=doblep) function Fun_Random(idum)

      use Mod_01_Def_prec

      implicit none
        
!
!       mi_random es real*8. idum integer*4
!       devuelve un numero alatorio entre (0,1), si el parametro
!       idum es negativo o es la primera vez que se la llama
!       inicializa el generador en base a idum.
!
      integer (kind=entero) :: idum
      real (kind=doblep), parameter :: mbig=4.d+06,mseed=1618033.d00
      real (kind=doblep), parameter :: mz=0.d00,fac=1.d00/mbig
      integer (kind=entero) :: i,iff,ii,inext,inextp,k
      real (kind=doblep) :: Fun_random,mj,mk,ma(55)
      

      save iff,inext,inextp,ma
      data iff/0/
!
      if (idum<=0.or.iff==0) then
            iff=1
            mj=abs(mseed-abs(idum))
            mj=mod(mj,mbig)
            ma(55)=mj
            mk=1
            do i=1,54
                  ii=mod(21*i,55)
                  ma(ii)=mk
                  mk=mj-mk
                  if (mk.lt.mz) mk=mk+mbig
                  mj=ma(ii)
            end do
            do k=1,4
                  do i=1,55
                        ma(i)=ma(i)-ma(1+mod(i+30,55))
                        if (ma(i).lt.mz) ma(i)=ma(i)+mbig
                  end do
            end do
            inext=0
            inextp=31
            idum=1
      end if
      inext=inext+1
      if (inext==56) inext=1
      inextp=inextp+1
      if (inextp==56) inextp=1
      mj=ma(inext)-ma(inextp)
      if(mj.lt.mz) mj=mj+mbig
      ma(inext)=mj
      Fun_Random=mj*fac
      
  
end function Fun_Random

end module