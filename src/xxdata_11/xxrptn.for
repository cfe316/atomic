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
      subroutine  xxrptn( iunit  , ndstack, 
     &                    ndptnl , ndptn  , ndptnc ,
     &                    nptnl  , nptn   , nptnc  ,
     &                    iptnla , iptna  , iptnca ,
     &                    lresol , lptn   ,
     &                    cstrg  , 
     &                    ncptn_stack     , cptn_stack       
     &                  )
       implicit none
c-----------------------------------------------------------------------
c
c  ****************** fortran77 subroutine: xxprtn *********************
c
c  Purpose:  To read and analyse a partition block in a datafile header
c
c  Calling program: adas416
c
c  Notes:  (1) Partition levels, partitions and partition components are 
c              labelled starting at 0 (but see (2)).
c          (2) Partition level 0 labels the resolved root partition level
c              partition level 1 labels the unresolved root partition
c              level.
c          (3) For an unresolved (standard) file, the partitions are each 
c              ionisation stage from the neutral to the bare nucleus and
c              they are labelled by the ion charge.  Each partition has 
c              just the one component.
c          (4) Distinguish the indexing (starting at 1) from the label
c              (starting at 0) .
c
c  Subroutine:
c
c  input : (i*4)  iunit     = unit to which input file is allocated
c  input : (i*4)  ndstack   = maximum no. of text lines in partition block 
c
c  input : (i*4)  ndptnl    = maximum level of partitions
c  input : (i*4)  ndptn     = maximum no. of partitions in one level
c  input : (i*4)  ndptnc    = maximum no. of components in a partition
c  input : (l*4)  lresol    = .true.  => resolved root partition
c                           = .false. => standard root partition
c
c  output: (i*4)  nptnl     = number of partition levels in block 
c  output: (i*4)  nptn()    = number of partitions in partition level
c                             1st dim: partition level 
c  output: (i*4)  nptnc(,)  = number of components in partition
c                             1st dim: partition level 
c                             2nd dim: member partition in partition level 
c  output: (i*4)  iptnla()  = partition level label (0=resolved root,1=
c                                                      unresolved root)
c                             1st dim: partition level index 
c  output: (i*4)  iptna(,)  = partition member label (labelling starts at 0)
c                             1st dim: partition level index 
c                             2nd dim: member partition index in partition 
c                             level 
c  output: (i*4)  iptnca(,,)= component label (labelling starts at 0)
c                             1st dim: partition level index 
c                             2nd dim: member partition index in partition 
c                             level
c                             3rd dim: component index of member partition 
c  output: (l*4)  lptn      = .true.  => partition block present
c                           = .false. => partition block not present
c  output: (c*80) cstrg     = string marking end of partition block
c  output: (i*4)  ncptn_stack= number of text lines in partition block
c  output: (c*80) cptn_stack()=text lines of partition block       
c                              1st dim: text line pointer 
c
c
c Routines:
c  	   Routine    Source	Brief description
c  	   -------------------------------------------------------------
c  	   I4UNIT     ADAS	Fetch unit number for output of messages
c  	   XXSLEN     ADAS	Find non-blank characters in string
c  	   XXWORD     ADAS	Extract position of number in buffer
c
c Author:  H. P. Summers, university of strathclyde
c          JA7.08
c          tel. 0141-548-4196
c
c Date:    25/08/05
c
c Version: 1.1  			Date: 25/08/2005
c Modified: Hugh Summers
c  		- First edition.
c
c Version: 1.2  			Date: 28/02/2008
c Modified: Adam Foster
c  		- Increased length of strg to 1024
c
c Version: 1.3  			Date: 28/02/2008
c Modified: Allan Whiteford
c		- Added comments for Adam's change
c               - Fixed capitalisation of comments section.
c
c-----------------------------------------------------------------------
c-----------------------------------------------------------------------
      integer   idptnl   , idword     
c-----------------------------------------------------------------------
      parameter (idptnl = 4  , idword = 256 )
c-----------------------------------------------------------------------
      integer   iunit     , i4unit 
      integer   ndptnl    , ndptn      , ndptnc    , ndstack
      integer   nptnl
      integer   ifirst    , ilast     
      integer   nchari    , ncharf
      integer   nfirst    , iwords     , nwords
      integer   nfirstc   , iwordsc    , nwordsc
      integer   i         , j          , k         , ic
      integer   ncptn_stack
c-----------------------------------------------------------------------
      character cstrg*80  
      Character strg*1024
c-----------------------------------------------------------------------
      logical   lresol    , lptn 
      logical   lptn_in 
c-----------------------------------------------------------------------
      integer   nptn(ndptnl)          , nptnc(ndptnl,ndptn)
      integer   iptnla(ndptnl)        , iptna(ndptnl,ndptn) 
      integer   iptnca(ndptnl,ndptn,ndptnc)
      integer   ifirsta(idword)       , ilasta(idword)
      integer   ifirstac(idword)      , ilastac(idword)
      integer   ncpta(idptnl)
c-----------------------------------------------------------------------
      character cptna(idptnl)*1024 
      character cptn_stack(ndstack)*80 
c-----------------------------------------------------------------------
c
c-----------------------------------------------------------------------
c  read partition data if present
c-----------------------------------------------------------------------

       if(idptnl.ne.ndptnl) then 
         write(i4unit(-1),1001)'mismatch of internal dimensions'
         write(i4unit(-1),1002)
         stop
       endif
      
       if(idptnl.ne.ndptnl) then 
         write(i4unit(-1),1001)'mismatch of internal dimensions'
         write(i4unit(-1),1002)
         stop
       endif
      
       do i=1,ndptnl
         cptna(i) = ' '
       enddo	
c
       lptn   = .false.
       cstrg  = ' '
       nptnl  = 0
       ncptn_stack = 0
       
   10  read(iunit,'(1a80)') cstrg
   
       if(cstrg(1:3).eq.'//#') then
           nchari = 0
           nptnl = nptnl + 1
	   lptn = .true.
	   lptn_in  = .true.
	   call xxslen(cstrg,ifirst,ilast)
	   
	   ncptn_stack=ncptn_stack+1
	   cptn_stack(ncptn_stack)=' '
           cptn_stack(ncptn_stack)(1:ilast-ifirst+1)=cstrg(ifirst:ilast)
	   
	   ncharf = nchari+ilast-ifirst+1
	   cptna(nptnl)(nchari+1:ncharf) = cstrg(ifirst:ilast)
	   nchari=ncharf
       elseif((cstrg(1:3).eq.'   ').and.lptn_in) then
           call xxslen(cstrg,ifirst,ilast)
	   
	   ncptn_stack=ncptn_stack+1
	   cptn_stack(ncptn_stack)=' '
	   cptn_stack(ncptn_stack)(1:ilast-ifirst+7)=
     &          	   '      '//cstrg(ifirst:ilast)
	   ncharf=nchari+ilast-ifirst+2	
	   cptna(nptnl)(nchari+1: ncharf) = ' '//cstrg(ifirst:ilast)

	   nchari = ncharf
       elseif(cstrg(1:3).eq.'---') then
           lptn_in = .false.
	   go to 15
       else
           write(i4unit(-1),1001)
	   write(i4unit(-1),1002)
	   stop
       endif
       go to 10
   15  continue
   
c
c-----------------------------------------------------------------------
c  preliminary checks
c-----------------------------------------------------------------------
c
       if(lptn) then
           do i = 1,nptnl
	     read(cptna(i)(4:5),'(i2)')iptnla(i)
c             write(i4unit(-1),*)'xxrptn: i,iptnla=',i,iptnla(i)
	   enddo
	   if((iptnla(1).gt.2).and.(nptnl.eq.1).and.(.not.lresol)) then
               write(i4unit(-1),1001) 'partition level',i,' in error'
	       write(i4unit(-1),1002)
	       stop
	   endif
	   do i = 1,nptnl
	     call xxslen(cptna(i),ifirst,ilast)
	     if(cptna(i)(ilast:ilast).ne.'/') then
                 write(i4unit(-1),1001) 'partition level',i,
     &                                  ' not terminated'
	         write(i4unit(-1),1002)
	       stop
	     endif
	   enddo  
	     
	endif   
c
c-----------------------------------------------------------------------
c  analyse partitions
c-----------------------------------------------------------------------
c
       do i=1,nptnl
           nfirst = 1
	   iwords = idword
	   call xxslen(cptna(i),ifirst,ilast)
           call xxword( cptna(i)(ifirst+5:ilast) , '/'    , nfirst ,
     &                   iwords  ,
     &                   ifirsta , ilasta , nwords
     &                 )
           if((nwords-2*int(nwords/2)).ne.0) then
                 write(i4unit(-1),1001) 'partition level',i,
     &                                  ' partition count wrong'
	         write(i4unit(-1),1002)
		 stop
           endif
	   
           nptn(i)=nwords/2
	   ic = 0
c           write(i4unit(-1),*)'xxrptn: i,nwords,nptn(i)=',
c     &                                 i,nwords,nptn(i)
	   do j=1,nptn(i)
	      strg=' '
	      strg=cptna(i)(ifirsta(2*j-1)+5:ilasta(2*j-1)+5)
c              write(i4unit(-1),*)'xxrptn-xxslen:strg=',strg
	      call xxslen(strg,ifirst,ilast)
	      read(strg(ifirst+1:ilast),'(i2)')iptna(i,j)
	      strg = ' '


	      strg=cptna(i)(ifirsta(2*j)+5:ilasta(2*j)+5)
	      
	      iwordsc = idword
	      nfirstc = 1
c              write(i4unit(-1),*)'xxrptn-xxword:strg=',strg
c              write(i4unit(-1),*)'xxrptn-xxword:nfirstc=',nfirstc
              call xxword( strg , ' '    , nfirstc ,
     &                     iwordsc  ,
     &                     ifirstac , ilastac , nwordsc
     &                   )
c              write(i4unit(-1),*)'xxrptn:nwordsc=',nwordsc
              nptnc(i,j)=nwordsc
c              write(i4unit(-1),*)'xxrptn: i,j,nptnc(i,j)=',
c     &                                    i,j,nptnc(i,j)
c              write(i4unit(-1),*)'xxrptn: ifirstac(1),ilastac(1)=',
c     &                                    ifirstac(1),ilastac(1)
c            write(i4unit(-1),*)'xxrptn:',strg(ifirstac(1):ilastac(1))
	      

	      do k=1,nptnc(i,j)

	        read(strg(ifirstac(k):ilastac(k)),*)iptnca(i,j,k)
c------------------------------------------------
c  components should be sequential and contiguous. 
c-------------------------------------------------
		if(iptnca(i,j,k).ne.ic) then
		     write(i4unit(-1),1001) 'partition count',ic,
     &                                  ' out of sequence'
	             write(i4unit(-1),1002)
		     stop
		else
		     ic=ic+1
		endif

	      enddo
           enddo
	   
	   ncpta(i)=ic
c	   write(i4unit(-1),*)'i,ncpta(i)=',i,ncpta(i)
	      
        enddo
c
c-----------------------------------------------------------------------
c  final checks. level i+1 partition components should span 
c  partition i p-values  
c-----------------------------------------------------------------------
c
       if (nptnl.ge.2)then
           do i=2,nptnl
	     if(ncpta(i-1).ne.nptn(i))then
	         write(i4unit(-1),1001) 'partition level',i,
     &                                  ' count incorrect'
	         write(i4unit(-1),1002)
		 stop
             endif
	   enddo
       endif  
   
       return
c
c-----------------------------------------------------------------------
c
 1001 format(1x,32('*'),' xxrptn error ',32('*')//
     &       1x,'fault in input data file: ',a,i3,a)
 1002 format(/1x,29('*'),' program terminated ',29('*'))
 
      end
