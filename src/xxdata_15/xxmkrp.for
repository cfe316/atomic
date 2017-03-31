C--------------------------------------------------------------------
C The user of the OPEN-ADAS system and data (hereinafter "the User")
C accepts the following terms and conditions: 
C 
C   1. The University of Strathclyde uses all reasonable endeavours
C      to ensure the accuracy of the data provided and any
C      information given, but the University makes no warranty,
C      expressed or implied as to its accuracy, integrity, fitness
C      for purpose and shall not be responsible for the use to
C      which the data is put by the User and/or any consequences
C      arising out of any inaccuracies or omissions.
C 
C   2. Any downloaded OPEN-ADAS file is made available here for the
C      personal use of the User only.  It must not be used for any
C      commercial application, incorporated into any web site or in
C      any form re-distributed without express prior written
C      permission from the ADAS Project. In particular, but not by
C      way of limitation, it must not be:
C 
C        * inserted into a managed database structure
C        * redistributed along with a modelling or analysis code
C        * made available on a public website.
C 
C Permission for OPEN-ADAS data incorporation in non-commercial
C code/system development for scientific advance will not be
C unreasonably withheld, but will be subject to written agreement
C on a case by case basis.
C 
C The User will indemnify the University of Strathclyde and keep
C it fully and effectively indemnified against each and every
C claim made against the University as a result of the User's
C use of the data.  
C--------------------------------------------------------------------
       subroutine xxmkrp( ndstack       , 
     &                    iz0           , iptnl       , 
     &                    ncptn_stack   , cptn_stack   
     &                 )
        implicit none
c-----------------------------------------------------------------------
c								       
c ****************** fortran 77 subroutine: xxmkrp *********************
c
c purpose: To create a root partition and return the partition block.
c
c
c calling program: adas416
c
c subroutine:
c
c input : (i*4)   ndstack     = maximum partition block lines
c input : (i*4)   iz0         = nuclear charge
c input : (i*4)   iptnl       = root partition level (0 or 1)
c
c output: (i*4)  ncptn_stack  = number of lines in the partition block
c output: (c*80) cptn_stack() = character string lines of the partition
c                               block
c
c
c routines:
c	   routine    source	brief description
c	   ----------------------------------------------------------
c	  i4unit     adas      fetch unit number for output of messages
c         xxopen     adas      inquire, open and allocate file to unit
c         xxslen     adas      find non-blank characters in string
c         xxword     adas      extract position of number in buffer
c
c
c author:  h. p. summers, university of strathclyde
c          ja7.08
c          tel. 0141-548-4196
c
c date:    04/10/06
c
c version: 1.1				date: 04/10/2006
c modified: hugh p summers
c		- first edition.
c
c version  : 1.2
c date     : 15-01-2007
c modified : Hugh Summers
c              - corrected metastable count for Ne+0.
c
c------------------------------------------------------------------------
c-----------------------------------------------------------------------
      integer   ia_dim 
      integer   idcnct  , iz0_max_res
c-----------------------------------------------------------------------
      parameter (ia_dim = 80 , idcnct = 100 , iz0_max_res = 10 )
c-----------------------------------------------------------------------
      integer	ndstack       
      integer	iz0	, i	  , k
      integer	i4unit  , iabt   
      integer	nfirst  , iwords  , maxwrd   , istart  , istop
      integer	np	, np_nat  , min_a    , max_a
      integer	i_pos	, icount
      integer	ipt_0	, ipt_1 , ipt_2      , is1min  , is1max
      integer	ncptn_stack
      integer   iptnl   , nptn
c-----------------------------------------------------------------------
      character c80*80         , strg*120      
      character cblanks*6	 
      character p_string*1024
c-----------------------------------------------------------------------
      integer	ifirst(20)     , ilast(20)
      integer	ip0(ia_dim)    , ip1(ia_dim)
      integer   ncncta(iz0_max_res)   , icnctva(iz0_max_res,idcnct)
c-----------------------------------------------------------------------
      character cptn_stack(ndstack)*80 
c-----------------------------------------------------------------------
      data	cblanks/'      '/ 
c-----------------------------------------------------------------------
      data  ncncta(1),(icnctva(1,i),i=1,2)   / 2,1,1/  
      data  ncncta(2),(icnctva(2,i),i=1,3)   / 3,2,1,1/  
      data  ncncta(3),(icnctva(3,i),i=1,4)   / 4,1,2,1,1/  
      data  ncncta(4),(icnctva(4,i),i=1,5)   / 5,2,1,2,1,1/  
      data  ncncta(5),(icnctva(5,i),i=1,6)   / 6,2,2,1,2,1,1/  
      data  ncncta(6),(icnctva(6,i),i=1,7)   / 7,4,2,2,1,2,1,1/  
      data  ncncta(7),(icnctva(7,i),i=1,8)   / 8,3,4,2,2,1,2,1,1/
      data  ncncta(8),(icnctva(8,i),i=1,9)   / 9,4,3,4,2,2,1,2,1,1/
      data  ncncta(9),(icnctva(9,i),i=1,10)  /10,2,4,3,4,2,2,1,2,1,1/
      data  ncncta(10),(icnctva(10,i),i=1,11)/11,2,2,4,3,4,2,2,1,2,1,1/
c-----------------------------------------------------------------------
c-----------------------------------------------------------------------
c-----------------------------------------------------------------------
      if(iptnl.eq.1) then	   
c----------------------------------------------
c  create root unresolved partition #01 string
c----------------------------------------------
           p_string=' '
           i_pos = 1
           write(p_string(i_pos:i_pos+5),'(1a6)')'//#01/'
	   i_pos=i_pos+6
	   nptn=iz0+1
	   do i=1,nptn
	     p_string(i_pos:i_pos+7)='p00/ 00/'
	     if(i.le.10) then
                 write(p_string(i_pos+2:i_pos+2),'(i1)')i-1
                 write(p_string(i_pos+6:i_pos+6),'(i1)')i-1
	     else	 
                 write(p_string(i_pos+1:i_pos+2),'(i2)')i-1
                 write(p_string(i_pos+5:i_pos+6),'(i2)')i-1
	     endif
	     i_pos=i_pos+8
	   enddo
      elseif((iptnl.eq.0).and.iz0.le.iz0_max_res) then
      
           nptn=0
           do i=1,ncncta(iz0)
             nptn=nptn+icnctva(iz0,i)
           enddo	
           p_string=' '
           i_pos = 1
           write(p_string(i_pos:i_pos+5),'(1a6)')'//#00/'
	   i_pos=i_pos+6
	   do i=1,nptn
	     p_string(i_pos:i_pos+7)='p00/ 00/'
	     if(i.le.10) then
                 write(p_string(i_pos+2:i_pos+2),'(i1)')i-1
                 write(p_string(i_pos+6:i_pos+6),'(i1)')i-1
	     else	 
                 write(p_string(i_pos+1:i_pos+2),'(i2)')i-1
                 write(p_string(i_pos+5:i_pos+6),'(i2)')i-1
	     endif
	     i_pos=i_pos+8
	   enddo
      
      else
          write(i4unit(-1),1001)iz0,iz0_max_res
	  write(i4unit(-1),1002)
	  stop
      endif	  
c-----------------------------------
c  print root partition string tidly
c-----------------------------------

	  call xxslen(p_string,istart,istop)

	  ncptn_stack = 0
	   
	   icount=0
	   ipt_0 = 1
	   ipt_1 = 0
	   do i=1,nptn
	     ipt_2=index(p_string(ipt_1+2:800),'p')+ipt_1+1
	     if((ipt_2-ipt_0+1).gt.80) then
	         if(icount.eq.0) then
		     c80=' '
		     write(c80(1:ipt_1-ipt_0+1),'(a)')
     &                                  p_string(ipt_0:ipt_1) 
                     ncptn_stack = ncptn_stack+1
		     cptn_stack(ncptn_stack)=c80
		 else    
		     c80=' '
		     write(c80(1:ipt_1-ipt_0+7),'(a)')
     &                                  cblanks//p_string(ipt_0:ipt_1) 
                     ncptn_stack = ncptn_stack+1
		     cptn_stack(ncptn_stack)=c80
		 endif
		 icount=1
	         ipt_0=ipt_1+1
		 ipt_1=ipt_2-1
	     else
	         ipt_1=ipt_2-1
             endif
	     
	   enddo
           
	   if((ipt_1.gt.ipt_0).and.((istop-ipt_0+1).ge.80)) then   		 
	         if(icount.eq.0) then
		     write(c80(1:ipt_1-ipt_0+1),'(a)')
     &                                  p_string(ipt_0:ipt_1) 
                     ncptn_stack = ncptn_stack+1
		     cptn_stack(ncptn_stack)=c80
		 else    
		     c80=' '
		     write(c80(1:ipt_1-ipt_0+7),'(a)')
     &                                  cblanks//p_string(ipt_0:ipt_1) 
                     ncptn_stack = ncptn_stack+1
		     cptn_stack(ncptn_stack)=c80
		 endif
		 c80=' '
		 write(c80(1:istop-ipt_1+6),'(a)')
     &                              cblanks//p_string(ipt_1+1:istop) 
                 ncptn_stack = ncptn_stack+1
		 cptn_stack(ncptn_stack)=c80
           else
	         if(icount.eq.0) then
		     c80=' '
		     write(c80(1:istop-ipt_0+1),'(a)')
     &                                  p_string(ipt_0:istop) 
                     ncptn_stack = ncptn_stack+1
		     cptn_stack(ncptn_stack)=c80
		 else    
		     c80=' '
		     write(c80(1:istop-ipt_0+7),'(a)')
     &                                  cblanks//p_string(ipt_0:istop) 
                     ncptn_stack = ncptn_stack+1
		     cptn_stack(ncptn_stack)=c80
		 endif
           endif
	      	 
	  return 

c-----------------------------------------------------------------------
 1001 format(1x,32('*'),' xxmkrp error ',32('*')//
     &       1x,'Cannot form #00 partition for z0= ',i2,' > ',i2)
 1002 format(/1x,29('*'),' program terminated ',29('*'))
c-----------------------------------------------------------------------
       end		
	
