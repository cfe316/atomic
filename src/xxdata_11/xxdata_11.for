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
      subroutine  xxdata_11( iunit  , iclass , 
     &                       isdimd , iddimd , itdimd , 
     &                       ndptnl , ndptn  , ndptnc , ndcnct ,
     &                       iz0    , is1min , is1max , 
     &                       nptnl  , nptn   , nptnc  ,   
     &                       iptnla , iptna  , iptnca , 
     &                       ncnct  , icnctv ,
     &                       iblmx  , ismax  , dnr_ele, dnr_ams, 
     &                       isppr  , ispbr  , isstgr ,
     &                       idmax  , itmax  , 
     &                       ddens  , dtev   , drcof  ,
     &                       lres   , lstan  , lptn  
     &                     )
       implicit none
c-----------------------------------------------------------------------
c
c  ****************** fortran77 subroutine: xxdata_11 ******************
c
c  purpose: to read a complete  adf11 file, check its class and 
c           determine its standard, resolved and partition organisation.
c
c  calling program: various
c
c  notes:    (1) A `standard' adf11 file contains gcr data between one  
c                whole ionisation stage and another whole ionisation 
c                stage.  
c                A `resolved' (or partial) adf11 file contains gcr data
c                between a set of metastables of one ionisation stage
c                and a set of metastables of another ionisation stage.
c                A resolved file is distinguished from a standard file
c                by the presence of a `connection vector' in the adf11
c                data file header lines.
c                The connection vector specifies the number of meta-
c                stables in each ionisation stage which are coupled 
c                together by gcr data.
c            (2) A `partitioned' adf11 file contains gcr data between 
c                clumps of ionisation stages or metastables or comb-
c                inations of the two called `partitions'.  
c                A `partition level' is a specification of the 
c                partitions which span all the ionisation stages (and
c                metastables) of an element.  Successive partition 
c                levels give a heirarchy corresponding to larger 
c                partitions and greater clumping. 
c                A `superstage' is a set of partitions which are close-
c                coupled.
c                There are thus equivalences :
c                        ionisation stage   -   superstage
c                        metastable         -   partition
c                        ion charge         -   superstage index
c                A partitioned adf11 file may be standard (with each 
c                superstage comprising only one partition) or resolved.
c                A partitioned file is distinguished by the presence of 
c                `partition specification block' in the adf11 data  
c                file header lines.
c            (3) When  a partition specification block is present, it 
c                should be ordered from the highest partition level  
c                index to lowest partition level index.  Thus the first 
c                partition in the partition block has the least number 
c                of partitions and the last has the greatest number.
c            (4) Twelev classes of adf11 data file may be read by the
c                subroutine as follow:
c
c            	 class index	type	  GCR data content
c            	 -----------	----	  ----------------
c            	     1  	acd	  recombination coeffts
c            	     2  	scd	  ionisation coeffts
c            	     3  	ccd	  CX recombination coeffts
c            	     4  	prb	  recomb/brems power coeffts
c            	     5  	prc	  CX power coeffts
c            	     6  	qcd	  base meta. coupl. coeffts 
c            	     7  	xcd	  parent meta. coupl. coeffts
c            	     8  	plt	  low level line power coeffts
c            	     9  	pls	  represent. line power coefft
c            	    10  	zcd	  effective charge
c            	    11  	ycd	  effective squared charge
c            	    12  	ecd	  effective ionisation potential
c
c            (5) A resolved adf11 file, with a connection vector, has a set
c                of names and pointers at precise positions in the data file
c                which are recognised.
c                The names are different for partitioned and unpartitioned
c                data files as follow:
c
c                       file      unpartitioned         partitioned 
c                       class        names                 names  
c                       
c                       (all)         z1                   s1
c
c                       	 (indices 1 and 2)     (indices 1 and 2)
c                   	----	   ----     ----         ----	  ----
c                   	acd        iprt     igrd         ispp	  ispb
c                   	scd        iprt     igrd         ispp	  ispb
c                   	ccd        iprt     igrd         ispp	  ispb
c                   	prb        iprt                  ispp	      
c                   	prc        iprt                  ispp	      
c                   	qcd        igrd     jgrd         ispb	  jspb
c                   	xcd        iprt     jprt         ispp	  jspp
c                   	plt        igrd 	         ispb
c                   	pls        igrd 	         ispb
c                   	zcd        igrd 	         ispb
c                   	ycd        igrd 	         ispb
c                   	ecd        igrd 	         ispb
c
c             (6) In partitioned nomenclature: s=superstage; p=partition;
c                 b=base (current superstage), p=parent (next up super-
c                 stage), c=child (next down superstage). Thus arrays
c                 `iprtr' and `igrd' in old notation are now substituted
c                 by `isppr' and `ispbr' respectively internally and in
c                 external naming. 
c
c
c  subroutine:
c
c  input : (i*4)  iunit     = unit to which input file is allocated
c  input : (i*4)  iclass    = class of data (1 - 12 ):
c                               1-acd, 2-scd, 3-ccd, 4-prb, 5-prc
c                               6-qcd, 7-xcd, 8-plt, 9-pls,10-zcd
c                              11-ycd,12-ecd
c
c  input : (i*4)  isdimd    = maximum number of (sstage, parent, base)
c                             blocks in isonuclear master files
c  input : (i*4)  iddimd    = maximum number of dens values in
c                             isonuclear master files
c  input : (i*4)  itdimd    = maximum number of temp values in
c                             isonuclear master files
c  input : (i*4)  ndptnl    = maximum level of partitions
c  input : (i*4)  ndptn     = maximum no. of partitions in one level
c  input : (i*4)  ndptnc    = maximum no. of components in a partition
c  input : (i*4)  ndcnct    = maximum number of elements in connection
c                             vector  
c
c  output: (i*4)  iz0       = nuclear charge
c  output: (i*4)  is1min    = minimum ion charge + 1 
c                             (generalised to connection vector index)
c  output: (i*4)  is1max    = maximum ion charge + 1 
c                             (note excludes the bare nucleus)
c                             (generalised to connection vector index 
c                              and excludes last one which always remains
c                              the bare nucleus)
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
c  output: (i*4)  ncnct     = number of elements in connection vector 
c  output: (i*4)  icnctv()  = connection vector of number of partitions 
c                             of each superstage in resolved case
c                             including the bare nucleus
c                             1st dim: connection vector index
c
c  output: (i*4)  iblmx     = number of (sstage, parent, base)
c                             blocks in isonuclear master file
c  output: (i*4)  ismax     = number of charge states
c                             in isonuclear master file
c                             (generalises to number of elements in
c                              connection vector)
c  output: (c*12) dnr_ele   = CX donor element name for iclass = 3 or 5
c                             (blank if unset)
c  output: (r*8)  dnr_ams   = CX donor element mass for iclass = 3 or 5
c                             (0.0d0 if unset)
c  output: (i*4)  isppr()   = 1st (parent) index for each partition block 
c                             1st dim: index of (sstage, parent, base)
c                                      block in isonuclear master file
c  output: (i*4)  ispbr()   = 2nd (base) index for each partition block 
c                             1st dim: index of (sstage, parent, base)
c                                      block in isonuclear master file
c  output: (i*4)  isstgr()  = s1 for each resolved data block
c                             (generalises to connection vector index)
c                             1st dim: index of (sstage, parent, base)
c                                      block in isonuclear master file
c
c  output: (i*4)  idmax     = number of dens values in
c                             isonuclear master files
c  output: (i*4)  itmax     = number of temp values in
c                             isonuclear master files
c  output: (r*8)  ddens()   = log10(electron density(cm-3)) from adf11 
c  output: (r*8)  dtev()    = log10(electron temperature (eV) from adf11
c  output: (r*8)  drcof(,,) = if(iclass <=9):
c                                log10(coll.-rad. coefft.) from 
c                                isonuclear master file
c                             if(iclass >=10):
c                                coll.-rad. coefft. from 
c                                isonuclear master file
c                             1st dim: index of (sstage, parent, base)
c                                      block in isonuclear master file
c                             2nd dim: electron temperature index
c                             3rd dim: electron density index 
c
c  output: (l*4)  lres      = .true.  => partial file
c                           = .false. => not partial file
c  output: (l*4)  lstan     = .true.  => standard file
c                           = .false. => not standard file
c  output: (l*4)  lptn      = .true.  => partition block present
c                           = .false. => partition block not present
c
c  routines:
c          routine    source    brief description
c          -------------------------------------------------------------
c          i4unit     adas      fetch unit number for output of messages
c          i4fctn     adas      convert string to integer form
c          xfelem     adas      return element name given nuclear charge 
c          xxword     adas      extract position of number in buffer
c          xxslen     adas      find string less front and tail blanks
c          xxcase     adas      convert a string to upper or lower case 
c          xxrptn     adas      analyse an adf11 file partition block 
c
c author:  h. p. summers, university of strathclyde
c          ja7.08
c          tel. 0141-548-4196
c
c date:    04/10/06
c
c version: 1.1				date: 04/10/2006
c modified: hugh summers
c		- first edition.
c
c version: 1.2				date: 21/01/2007
c modified: Allan Whiteford
c		- Commented out warning about lack of iclass,
c                 all of the present ADAS files do not contain
c                 this information
c                 (first commit to CVS)
c
c version: 1.3				date: 08/03/2007
c modified: Hugh Summers
c		- adjustments for revised ecd formats.
c                 charge exchange donor/donor mass checks and
c                 dnr_ele, dnr_ams added to parameter return.
c
c-----------------------------------------------------------------------
      integer   nddash    , idword      , ndstack  , ndonors
c-----------------------------------------------------------------------
      character csrch1*4   , csrch2*4     , csrch3*4     
      character csrch4*4   , csrch5*4        
      character cdash*8    , cpart*3 
c-----------------------------------------------------------------------
      parameter ( nddash = 6  , idword = 256 , ndstack = 40 )
      parameter ( csrch1 = 'iprt' , csrch2 = 'igrd'  ,csrch3 = '---/')
      parameter ( csrch4 = 'ispp' , csrch5 = 'ispb') 
      parameter ( cdash = '--------' , cpart = '//#' )
      parameter ( ndonors = 4 )
c-----------------------------------------------------------------------
      integer   iunit     , i4unit   , i4fctn
      integer   iz0       , is1min   , is1max
      integer   iddimd    , itdimd   , isdimd     
      integer   ndptnl    , ndptn    , ndptnc   , ndcnct    
      integer   iblmx     , ismax    , itmax    , idmax
      integer   ischk    
      integer   iclass    , iclass_file
      integer   i         , ic       , it         , id      
      integer   icptn     , iabt     , iabt1      , iabt2    ,
     &          j         , ndash_line
      integer   nptnl     , ncnct    , ncptn_stack        
      integer   nfirst    , iwords   , nwords   , ifirst     , ilast
c-----------------------------------------------------------------------
      real*8    dnr_ams   , dmass
c-----------------------------------------------------------------------
      character cstrg*80  , cstrgl*80, cterm*80   ,  chindi*4
      character xfelem*12 , str12*12 , dnr_ele*12
c-----------------------------------------------------------------------
      logical   lres      , lstan     , lptn      , lresol     
      logical   lptn_old  , lwarn     , ldonor    , ldmass       
c-----------------------------------------------------------------------
      integer   idash_linea(nddash)
      integer   nptn(ndptnl)          , nptnc(ndptnl,ndptn)
      integer   iptnla(ndptnl)        , iptna(ndptnl,ndptn) 
      integer   iptnca(ndptnl,ndptn,ndptnc)
      integer   icnctv(ndcnct)
      integer   isstgr(isdimd)
      integer   ifirsta(idword)       , ilasta(idword)
      integer   ispbr(isdimd)         , isppr(isdimd)
c-----------------------------------------------------------------------
      real*8    ddens(iddimd)         , dtev(itdimd)
      real*8    drcof(isdimd,itdimd,iddimd)
c-----------------------------------------------------------------------
      character cclass(12)*4          , cpatrn(12)*4
      character cptrn1(12)*4          , cptrn2(12)*4
      character cptn_stack(ndstack)*80
      character cdonors(ndonors)*12 
c-----------------------------------------------------------------------
      data      cterm /'------------------------------------------------
     &--------------------------------'/
      data      cclass/'/ACD','/SCD','/CCD','/PRB','/PRC',
     &                 '/QCD','/XCD','/PLT','/PLS','/ZCD',
     &                 '/YCD','/ECD'/
      data      cptrn1/'iprt','iprt','iprt','iprt','iprt',
     &                 'igrd','iprt','igrd','igrd','igrd',
     &                 'igrd','igrd'/
      data      cptrn2/'ispp','ispp','ispp','ispp','ispp',
     &                 'ispb','ispp','ispb','ispb','ispb',
     &                 'ispb','ispb'/
      data      cdonors/'HYDROGEN    ','DEUTERIUM   ','TRITIUM     ',
     &                  'HELIUM      '/  
c-----------------------------------------------------------------------
c
c-----------------------------------------------------------------------
c  search for 'prnt' and count number of dash delimiters
c-----------------------------------------------------------------------

       ic = 0
       icptn = 0
       ndash_line = 0
       
       lstan  = .false.
       lres = .false.
       lptn   = .false.
       nptnl  = 0
       
   10  read(iunit,'(1a80)') cstrg
       ic = ic + 1
       
   
       call xxcase(cstrg,cstrgl,'lc')
       
       if((index(cstrgl,csrch1).le.0) .and.
     &    (index(cstrgl,csrch2).le.0) .and.
     &    (index(cstrgl,csrch4).le.0) .and.
     &    (index(cstrgl,csrch5).le.0) .and.
     &    (index(cstrgl,csrch3).le.0)) then
     
            if(index(cstrgl,cdash).gt.0) then
	        ndash_line = ndash_line+1
		idash_linea(ndash_line)=ic
            endif
            if((cstrgl(1:3).eq.cpart).and.(.not.lptn)) then
	        lptn = .true.
		icptn = ic
	    endif
	    go to 10
       else
            if((iclass.eq.1).or.(iclass.eq.3).or.
     &         (iclass.eq.4).or.(iclass.eq.5).or.
     &         (iclass.eq.6).or.(iclass.eq.7)) then
                if(ndash_line.eq.1) then
		    lstan = .true.
		elseif ((ndash_line.eq.2).and.lptn)then
		    lstan = .true.
		elseif ((ndash_line.eq.2).and.(.not.lptn))then
		    lres = .true.
		elseif ((ndash_line.eq.3).and.lptn)then
		    lres = .true.
		elseif ((ndash_line.eq.3).and.(.not.lptn))then
		    write(i4unit(-1),2002)'header lines faulty'
		    write(i4unit(-1),2003)
		    stop
		elseif (ndash_line.gt.3) then
		    write(i4unit(-1),2002)'header lines faulty'
		    write(i4unit(-1),2003)
		    stop
		endif
            elseif((iclass.eq.2).or.(iclass.eq.8).or.
     &             (iclass.eq.9).or.(iclass.eq.10).or.
     &             (iclass.eq.11).or.(iclass.eq.12)) then
                if(ndash_line.eq.1) then
		    lstan = .true.
		elseif ((ndash_line.eq.2).and.lptn)then
		    lstan = .true.
		elseif ((ndash_line.eq.2).and.(.not.lptn))then
		    lres = .true.
		elseif ((ndash_line.eq.3).and.lptn)then
		    lres = .true.
		elseif ((ndash_line.eq.3).and.(.not.lptn))then
		    write(i4unit(-1),2002)'header lines faulty'
		    write(i4unit(-1),2003)
		    stop
		elseif (ndash_line.gt.3) then
		    write(i4unit(-1),2002)'header lines faulty'
		    write(i4unit(-1),2003)
		    stop
		endif
	    endif
       endif
c-----------------------------------------------------------------------
c  assign look-up names according to partitioning & set warning logical
c-----------------------------------------------------------------------

       do i=1,12
         if(lptn) then
             cpatrn(i)=cptrn2(i)
	 else
	     cpatrn(i)=cptrn1(i)
	 endif
       enddo
       
       lwarn = .false.
       	         
c-----------------------------------------------------------------------
c  rewind, separate and analyse header sections according to type
c-----------------------------------------------------------------------

       rewind(iunit)
       
       ic =0
       
c-----------------------------------------------------------------------
c  first line 
c-----------------------------------------------------------------------
       read(iunit,'(a80)')cstrg
       call xxcase(cstrg,cstrgl,'uc')
       ic=ic+1
       
       iabt = 0
       iz0 = i4fctn(cstrg(1:5),iabt)
       if(iabt.gt.0) then
            write(i4unit(-1),2002)'faulty nuclear charge'
            write(i4unit(-1),2003)
            stop
       endif
       str12=xfelem(iz0)
       call xxslen(str12,ifirst,ilast)
       if(index(cstrgl,str12(ifirst:ilast)).le.0) then
              write(i4unit(-1),2000)'inconsistent element name '//
     &                               'for iz0= ',iz0
              write(i4unit(-1),2001)
       endif
       
       iabt = 0
       idmax = i4fctn(cstrg(6:10),iabt)
       if(iabt.gt.0.or.idmax.le.0.or.idmax.gt.iddimd) then
              write(i4unit(-1),2002)'invalid number of densities',
     &                               idmax,' = 0 or > ',iddimd
              write(i4unit(-1),2003)
            stop
       endif
       iabt = 0
       itmax = i4fctn(cstrg(11:15),iabt)
       if(iabt.gt.0.or.itmax.le.0.or.itmax.gt.itdimd) then
            write(i4unit(-1),2002)'invalid number of ','temperatures',
     &                               itmax,' = 0 or > ',itdimd
            write(i4unit(-1),2003)
            stop
       endif
       iabt1 = 0
       is1min = i4fctn(cstrg(16:20),iabt1)
       iabt2 = 0
       is1max = i4fctn(cstrg(21:25),iabt2)
       iabt = iabt1 + iabt2
       
       iclass_file = 0
       do i=1,12
         if(index(cstrgl,cclass(i)).gt.0) then
	    iclass_file=i
	 endif   
       enddo
       if(iclass_file.le.0) then
            write(i4unit(-1),2000)'no class name given in file' 
            write(i4unit(-1),2001)
       elseif(iclass_file.ne.iclass) then	    
            write(i4unit(-1),2004)'file class name ',
     &                             cclass(iclass_file), 
     &                            ' does not match iclass = ',iclass	    
            write(i4unit(-1),2003)
	    stop
       endif

c-----------------------------------------------------------------------
c  check if CX donor is explicitly named in dataset top line 
c-----------------------------------------------------------------------
       ldonor  = .false.
       ldmass  = .false.
       dnr_ele = ' '
       dnr_ams = 0.0d0
       if((iclass_file.eq.3).or.(iclass_file.eq.5)) then
           do i=1,ndonors
	     call xxslen(cdonors(i),ifirst,ilast)
	     if(index(cstrgl,':'//cdonors(i)(ifirst:ilast)).gt.0) then
	         ldonor=.true.
		 dnr_ele=cdonors(i)
	     endif
	   enddo
       endif       
       
c-----------------------------------------------------------------------
c  read connection vector if partial file
c-----------------------------------------------------------------------

       if(lres) then
           do i=2,idash_linea(1)
	     read(iunit,'(1a80)')cstrg
	   enddo
	   
	   ncnct = 0
	   
	   do i=idash_linea(1)+1,idash_linea(2)-1
	     cstrg=' '
	     read(iunit,'(1a80)')cstrg
             nfirst = 1
	     iwords = idword
             call xxword( cstrg , ' '    , nfirst ,
     &                    iwords  ,
     &                    ifirsta , ilasta , nwords
     &                  )
             do j=1,nwords
	       ncnct = ncnct + 1
	       read(cstrg(ifirsta(j):ilasta(j)),*)icnctv(ncnct)
	     enddo
	   enddo
	   
       else
       
           ncnct = 0	   
	   
       endif
       
       rewind(iunit)
      		
c-----------------------------------------------------------------------
c  read partition data if present
c-----------------------------------------------------------------------
c
       lptn_old = lptn
       if(lptn_old) then 
          do i=1,icptn-1
            read(iunit,'(1a80)')cstrg
          enddo
		
           lresol = .false.
	   call  xxrptn( iunit  , ndstack, 
     &                   ndptnl , ndptn  , ndptnc ,
     &                   nptnl  , nptn   , nptnc  ,
     &                   iptnla , iptna  , iptnca ,
     &                   lresol , lptn   ,
     &                   cstrg  ,
     &                   ncptn_stack     ,cptn_stack       
     &                 )

       endif
       
c------- now check is1min and is1max 

       if(.not.lptn) then
       
           if((iabt.gt.0).or.(is1min.gt.is1max).or.(is1min.lt.1)
     &         .or.(is1max.gt.iz0)) then
               write(i4unit(-1),2002)'incorrect ion or partition limits'
               write(i4unit(-1),2003)
               stop
           endif
	   
       elseif(lstan.and.lptn) then

           if((iabt.gt.0).or.(is1min.gt.is1max).or.(is1min.ne.1)
     &         .or.(is1max.ne.nptn(1)-1)) then
               write(i4unit(-1),2002)'incorrect ion or partition limits'
               write(i4unit(-1),2003)
               stop
           endif

       elseif(lres.and.lptn) then

           if((iabt.gt.0).or.(is1min.gt.is1max).or.(is1min.ne.1)
     &         .or.(is1max.ne.ncnct-1)) then
               write(i4unit(-1),2002)'incorrect ion or partition limits'
               write(i4unit(-1),2003)
               stop
           endif
       
       endif

c-----------------------------------------------------------------------
c  read temperatures and densities 
c-----------------------------------------------------------------------

       rewind(iunit)
       
       do i=1,idash_linea(ndash_line)
          read(iunit,'(1a80)')cstrg
       enddo

       read(iunit,1000) ( ddens(i) , i = 1 , idmax )
       read(iunit,1000) ( dtev(i)  , i = 1 , itmax )
       
c------------------------------------------
c  read parent and base metastable indices
c------------------------------------------

       chindi = cpatrn(iclass)

       iblmx  = 0
   20  read(iunit,'(a80)',end=30)cstrg
       call xxcase(cstrg,cstrgl,'lc')
       if(cstrgl(2:80).ne.cterm(2:80).and.cstrgl(2:2).ne.' ') then
c           if(lptn) then
           if(lres) then
               if( cstrgl(24:27) .eq. chindi) then
                  iblmx = iblmx  + 1
		  if((iclass.eq.4).or.(iclass.eq.5).or.
     &               (iclass.eq.8).or.(iclass.eq.9).or.
     &               (iclass.eq.10).or.(iclass.eq.11))then
                      read(cstrgl,1003)isppr(iblmx),
     &                                 isstgr(iblmx)
                      ispbr(iblmx)=0
                  else 
                      read(cstrgl,1002) isppr(iblmx), ispbr(iblmx), 
     &                                 isstgr(iblmx)
                  endif 
               elseif(( cstrgl(24:27). eq. cptrn1(iclass)).or.
     &                ( cstrgl(24:27). eq. cptrn2(iclass))) then
                  iblmx = iblmx  + 1
		  if((iclass.eq.4).or.(iclass.eq.5).or.
     &               (iclass.eq.8).or.(iclass.eq.9).or.
     &               (iclass.eq.10).or.(iclass.eq.11))then
                      read(cstrgl,1003)isppr(iblmx),
     &                                 isstgr(iblmx)
                      ispbr(iblmx)=0
                  else 
                     read(cstrgl,1002) isppr(iblmx), ispbr(iblmx), 
     &                                 isstgr(iblmx)
                  endif 
                  if(.not.lwarn) then 
                      write(i4unit(-1),2006)'incorrect pointer code',  
     &                                  ' for class: actual = ',
     &                                    cstrgl(24:27), 
     &                                 ', expected = ',chindi
                      write(i4unit(-1),2001)
		      lwarn = .true.
		  endif    
               else
                  write(i4unit(-1),2005)'incorrect pointer code for', 
     &                                  ' class: actual = ',
     &                                    cstrgl(24:27), 
     &                                 ', expected = ',chindi
                  write(i4unit(-1),2003)
		  stop
              endif
           else
              iblmx = iblmx + 1
              read(cstrgl,1001) isstgr(iblmx)
	      isppr(iblmx) = 1
              if((iclass.eq.4).or.(iclass.eq.5).or.
     &           (iclass.eq.8).or.(iclass.eq.9).or.
     &           (iclass.eq.10).or.(iclass.eq.11))then
                  ispbr(iblmx) = 0
	      else    
	          ispbr(iblmx) = 1
	      endif
           endif
c----------------------------------------------
c  get the donor mass for classes ccd and prc
c----------------------------------------------
	   
           dmass   = 0.0d0
           if((iclass.eq.3).or.(iclass.eq.5))then
	      if((cstrgl(46:47). eq. 'mh').or.
     &           (cstrgl(46:47). eq. 'md')) then	
                      read(cstrgl(49:52),'(f4.2)')dmass
	      endif
	      if((dmass.gt.0.0d0).and.(dnr_ams.eq.0.0d0))then
	          dnr_ams=dmass
		  ldmass = .true.
	      elseif((dmass.gt.0.d0).and.(dmass.eq.dnr_ams))then
	          continue	  	      
	      else
	          ldmass  = .false.
		  dnr_ams = 0.0d0
	      endif
	   endif   	  
	         	                                       
c--------------------------
c  read  final gcr values
c--------------------------
        
           do 25 it = 1 , itmax
	     if(iclass.le.9) then
                 read(iunit,1000) ( drcof(iblmx,it,id) , id = 1 , idmax)
	     else
                 read(iunit,1004) ( drcof(iblmx,it,id) , id = 1 , idmax)
	     endif
   25      continue
           go to 20
       endif
c
   30  close(iunit)

c-----------------------------------------------------------------------
c  issue warnings if donor element and/or donor mass is ambiguous
c-----------------------------------------------------------------------
       if(((iclass.eq.3).or.(iclass.eq.5)).and.(.not.ldonor)) then
           write(i4unit(-1),2000)'unspecified CX donor element'
	   write(i4unit(-1),2001)
       endif	   
       if(((iclass.eq.3).or.(iclass.eq.5)).and.(.not.ldmass)) then   
           write(i4unit(-1),2000)'unspecified CX donor mass'
	   write(i4unit(-1),2001)
       endif   
c
c-----------------------------------------------------------------------
c      verify s1 set in master file consistent with is1min and is1max
c      except for xcd and qcd cases
c-----------------------------------------------------------------------
c
       if(iclass.eq.6.or.iclass.eq.7) then
           ismax = is1max-is1min+1
       else
           if(iclass.eq.12) then
	       ischk=is1min-1
	   else
	       ischk = is1min
	   endif
	       
           do i=1,iblmx
             if(isstgr(i).ne.ischk) then
                 ischk = ischk+1
             endif
          enddo
	  
          if(((iclass.ne.10).and.(iclass.ne.11).and.(iclass.ne.12))
     &        .and.(ischk.eq.is1max)) then
               ismax = is1max-is1min+1
          elseif(((iclass.eq.10).or.(iclass.eq.11)).and.
     &        (ischk.eq.is1max+1)) then
               ismax = is1max-is1min+2
          elseif((iclass.eq.12).and.
     &        (ischk.eq.is1max)) then
               ismax = is1max-is1min+1
               ismax = is1max-is1min+2
          else
                write(i4unit(-1),2002)'inconsistent s1 set in file'
                write(i4unit(-1),2003)
                stop
           endif
       endif
c
c-----------------------------------------------------------------------
c     make up connection vectors and root partitions if appropriate
c     in the resolved case with 0 root partition level, the sum over
c     the connection vector gives the number of partitions 
c-----------------------------------------------------------------------
c
      if ((.not.lres).and.(.not.lptn)) then
          ncnct = iz0+1
	  do i=1,ncnct
	     icnctv(i)=1
	  enddo
      elseif ((.not.lres).and.lptn) then
          ncnct = is1max+1
	  do i=1,ncnct
	     icnctv(i)=1
	  enddo
      endif
       
      if ((.not.lres).and.(.not.lptn)) then
          nptnl   = 1 
          iptnla(nptnl) = 1
	  nptn(1) =  iz0+1 
          do i=1,nptn(1)
	    iptna(nptnl,i) = i-1
	    nptnc(nptnl,i) = 1
	    iptnca(1,iptna(nptnl,i)+1,nptnc(nptnl,i))=i-1
	  enddo
      elseif (lres.and.(.not.lptn)) then
      
          nptnl   = 1 
          iptnla(nptnl) = 0
	  nptn(1)=1
	  do i=1,ncnct
	    nptn(1)=nptn(1)+icnctv(i)
	  enddo  
          do i=1,nptn(1)
	    iptna(nptnl,i) = i-1
	    nptnc(nptnl,i) = 1
	    iptnca(1,iptna(nptnl,i)+1,nptnc(nptnl,i))=i-1
	  enddo
      endif  
c 
c-----------------------------------------------------------------------
c
 1000 format(8f10.5)
 1001 format(57x,i2)
 1002 format(28x,i2,9x,i2,16x,i2)
 1003 format(28x,i2,9x,2x,16x,i2)
 1004 format(1p8d10.3)
c 
 2000 format(1x,30('*'),' xxdata_11 warning ',30('*')//
     &       2x,a,a,i3,a,i3 )
 2001 format(/1x,30('*'),' program continues ',30('*'))
 2002 format(1x,30('*'),'  xxdata_11 error  ',30('*')//
     &       2x,a,a,i3,a,i3 )
 2003 format(/1x,30('*'),' program terminated ',29('*'))
 2004 format(1x,30('*'),'  xxdata_11 error  ',30('*')//
     &       2x,a,a,a,i3)
 2005 format(1x,30('*'),'  xxdata_11 error  ',30('*')//
     &       2x,a,a,a4,a,a4 )
 2006 format(1x,30('*'),' xxdata_11 warning ',30('*')//
     &       2x,a,a,a4,a,a4 )
c
c-----------------------------------------------------------------------
c
      return
      end
