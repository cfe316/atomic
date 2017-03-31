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
       subroutine xxdata_15( iunit  , dsname ,
     &                       nstore , ntdim  , nddim  ,
     &                       ndptnl , ndptn  , ndptnc , ndcnct ,
     &                       ndstack, ndcmt ,
     &                       iz0    , is     , is1    , esym   ,
     &                       nptnl  , nptn   , nptnc  ,
     &                       iptnla , iptna  , iptnca ,
     &                       ncnct  , icnctv ,
     &                       ncptn_stack     , cptn_stack      ,
     &                       lres   , lptn   , lcmt   , lsup   ,
     &                       nbsel  , isela  ,
     &                       cwavel , cfile  , ctype  , cindm  ,
     &                       wavel  , ispbr  , isppr  , isstgr , iszr  ,
     &                       ita    , ida    ,
     &                       teta   , teda   ,
     &                       pec    , pec_max,
     &                       ncmt_stack      , cmt_stack
     &                     )
       implicit none
c-----------------------------------------------------------------------
c
c  ***************** fortran77 subroutine: xxdata_15 *******************
c
c  purpose:  To fetch  data  from  an input photon emissivity file
c            for a given emitting element superstage .
c
c  data:    Up to 'nstore' sets (data-blocks) of data may be  read from
c           the file - each block forming a complete set of photon
c           emissivity coefft. values for given temp/density grid.
c           Each data-block  is  analysed independently of any  other
c           datablock.
c
c           the units used in the data file are taken as follows:
c
c           temperatures : ev
c           densities    : cm-3
c           pec          : phot. cm3 s-1
c
c  subroutine:
c
c  input : (i*4)  iunit    = unit to which input file is allocated.
c          (i*4)  dsname   = name of opened data set on iunit
c
c          (i*4)  nstore   = maximum number  of  input data-blocks  that
c                            can be stored.
c          (i*4)  ntdim    = max number of electron temperatures allowed
c          (i*4)  nddim    = max number of electron densities    allowed
c          (i*4)  ndptnl   = maximum level of partitions
c          (i*4)  ndptn    = maximum no. of partitions in one level
c          (i*4)  ndptnc   = maximum no. of components in a partition
c          (i*4)  ndcnct   = maximum number of elements in connection
c          (i*4)  ndstack  = maximum number of partition text lines
c          (i*4)  ndcmt    = maximum number of comment text lines
c                             vector
c output:  (i*4)  iz0      = read - emitting ion - nuclear charge
c          (i*4)  is       = read - emitting ion - charge
c                            (generalised to superstage label)
c          (i*4)  is1      = read - emitting ion - charge + 1
c                            (generalised to superstage index= is + 1)
c          (c*2)  esym     = read - emitting ion - element symbol
c
c          (i*4)  nptnl    = number of partition levels in block
c          (i*4)  nptn()   = number of partitions in partition level
c                            1st dim: partition level
c          (i*4)  nptnc(,) = number of components in partition
c                            1st dim: partition level
c                            2nd dim: member partition in partition level
c          (i*4)  iptnla() = partition level label (0=resolved root,1=
c                                                     unresolved root)
c                            1st dim: partition level index
c          (i*4)  iptna(,) = partition member label (labelling starts at 0)
c                            1st dim: partition level index
c                            2nd dim: member partition index in partition
c                            level
c          (i*4)  iptnca(,,)= component label (labelling starts at 0)
c                            1st dim: partition level index
c                            2nd dim: member partition index in partition
c                            level
c                            3rd dim: component index of member partition
c          (i*4)  ncnct     = number of elements in connection vector
c          (i*4)  icnctv()  = connection vector of number of partitions
c                             of each superstage in resolved case
c                             including the bare nucleus
c                             1st dim: connection vector index
c          (i*4)  ncptn_stack = number of text lines in partition block
c          (c*80) cptn_stack()= text lines in partition block
c                               1st dim: text line index (1->ncptn_stack)
c
c          (l*4)  lres      = .true.  => partial file
c                           = .false. => not partial file
c          (l*4)  lptn      = .true.  => partition block present
c                           = .false. => partition block not present
c          (l*4)  lcmt      = .true.  => comment text block present
c                           = .false. => comment text block not present
c          (l*4)  lsup      = .true.  => ss use of filmem field
c                           = .false. => old use of filmem field
c
c          (i*4)  nbsel     = number of data-blocks accepted & read in.
c          (i*4)  isela()   = read - data-set data-block entry indices
c                            dimension: data-block index
c
c          (c*10) cwavel() = wavelength string (angstroms)
c                            1st dim: data-block index
c          (c*8)  cfile()  = specific ion file source string in older
c                            forms.  Field not present in superstage
c                            version, but reused for added information
c                            1st dim: data-block index
c          (c*8)  ctype()  = data type string
c                            1st dim: data-block index
c          (c*2)  cindm()  = metastable index string
c                            1st dim: data-block index
c
c          (r*8)  wavel()   = wavelength (angstroms)
c                             dimension: data-block index
c          (i*4)  isppr()   = parent index for each line block
c                             1st dim: index of block in adf15 file
c          (i*4)  ispbr()   = base index for each line block
c                             1st dim: index of block in adf15 file
c          (i*4)  isstgr()  = s1 for each resolved data block
c                             1st dim: index of block in adf15 file
c          (i*4)  iszr()    = ion charge relating to each line
c                             1st dim: index of block in adf15 file
c
c          (i*4)  ita()     = number of electron temperatures
c                             dimension: data-block index
c          (i*4)  ida()     = read - number of electron densities
c                             1st dim: data-block index
c
c          (r*8)  teta(,)   =  electron temperatures (units: ev)
c                             1st dim: electron temperature index
c                             2nd dim: data-block index
c          (r*8)  teda(,)   = electron densities (units: cm-3)
c                             1st dim: electron density index
c                             2nd dim: data-block index
c
c          (r*8)  pec(,,)   = photon emissivity coeffts
c                             1st dim: electron temperature index
c                             2nd dim: electron density index
c                             3rd dim: data-block index
c          (r*8)  pec_max() = photon emissivity coefft. maximum
c                             as a function of Te at first Ne value
c                             1st dim: data-block index
c          (i*4)  ncmt_stack = number of text lines in comment block
c          (c*80) cmt_stack()= text lines in comment block
c                               1st dim: text line index (1->ncmt_stack)
c
c routine: (i*4)  i4eiz0   = function - (see routines section below)
c          (i*4)  i4fctn   = function - (see routines section below)
c          (i*4)  i4unit   = function - (see routines section below)
c          (i*4)  iblk     = array index: data-block index
c          (i*4)  itt      = array index: electron temperature index
c          (i*4)  itd      = array index: electron density     index
c          (i*4)  ntnum    = number of electron temperatures for current
c                            data-block
c          (i*4)  ndnum    = number of electron densities    for current
c                            data-block
c          (i*4)  iabt     = return code from 'i4fctn'
c          (i*4)  ipos1    = general use string index variable
c          (i*4)  ipos2    = general use string index variable
c
c          (l*4)  lbend    = identifies whether the last of the  input
c                            data sub-blocks has been located.
c                            (.true. => end of sub-blocks reached)
c
c          (c*1)  cslash   = '/' - delimiter for 'xxhkey'
c          (c*2)  c2       = general use two byte character string
c          (c*5)  ionnam   = emitting ion read from dataset
c          (c*6)  ckey1    = 'filmem' - input block header key
c          (c*4)  ckey2    = 'type  ' - input block header key
c          (c*4)  ckey3    = 'indm  ' - input block header key
c          (c*4)  ckey4    = 'isel  ' - input block header key
c          (c*80) c80      = general use 80 byte  character  string  for
c                            the input of data-set records.
c
c routines:
c          routine    source    brief description
c          ------------------------------------------------------------
c          i4eiz0     adas      returns z0 for given element symbol
c          i4fctn     adas      convert character string to integer
c          i4unit     adas      fetch unit number for output of messages
c          r8fctn     adas      convert string to real number
c          xxmkrp     adas      make up root partition text lines
c          xxcase     adas      convert a string to upper or lower case
c          xxhkey     adas      obtain key/response strings from text
c          xxrptn     adas      analyse an adf11 file partition block
c          xxword     adas      extract position of number in buffer
c          xxslen     adas      find string less front and tail blanks
c
c author:  H. P. Summers
c          k1/1/57
c          jet ext. 4941
c
c date:    11/10/91
c
c update:  05/12/91 - PE Briden: ionnam now allowed to occupy either
c                                4 or 5 spaces in the header.
c
c update:  23/04/93 - PE Briden - adas91: added i4unit function to write
c                                         statements for screen messages
c
c update:  24/05/93 - PE Briden - adas91: changed i4unit(0)-> i4unit(-1)
c
c update:  27/2/95  - L. Jalota - idl_adas : increased size dsname for
c                                            use under unix systems
c
c unix-idl port:
c
c version: 1.2                          date: 23-1-96
c modified: Tim Hammond (tessella support services plc)
c               - corrected format statements for dsname length
c
c-----------------------------------------------------------------------
c
c
c notes: copied from e3data.for. this is v1.1 of xxdata_15.
c
c
c version  : 1.1
c date     : 12-04-2005
c modified : Martin o'Mullane
c              - first version
c
c version  : 1.2
c date     : 25-04-2005
c modified : Martin o'Mullane
c              - increase c3 to character*3 to permit more than
c                100 entries in adf15 file.
c
c version  : 1.3
c date     : 15-05-2006
c modified : Hugh Summers
c              - extended to operation with superstages and partitions.
c
c version  : 1.4                         
c date     : 03-01-2007
c modified : Hugh Summers
c               - remove redundant variables.
c
c-----------------------------------------------------------------------
      integer    idword    , idcnct  , iz0_max_res
c-----------------------------------------------------------------------
      parameter ( idword = 256 , idcnct = 100 )
      parameter ( iz0_max_res = 10 )
c-----------------------------------------------------------------------
      integer    i4eiz0    , i4fctn   , i4unit
      integer    iunit     , nstore   ,
     &           ntdim     , nddim    ,
     &           iz0       , is       ,
     &           is1       , nbsel
      integer    iblk      ,
     &           itt       , itd      ,
     &           ntnum     , ndnum    ,
     &           ipos1     , ipos2    , iabt
      integer    ndptnl    , ndptn    , ndptnc        , ndcnct
      integer    ndstack   , ndcmt
      integer    nptnl     , ncnct    , ncptn_stack   , ncmt_stack  ,
     &           iptnl
      integer    nfirst    , iwords   , nwords
      integer    i         , j        , ifirst        , ilast
      integer    max_indm  , indm
c-----------------------------------------------------------------------
      real*8     pmax      , r8fctn
c-----------------------------------------------------------------------
      logical    lbend
      logical    lptn      , lresol   , lres    , lsup
      logical    lcmt      , lptn_temp
c-----------------------------------------------------------------------
      character  dsname*80             , esym*2
      character  cslash*1              , colon*1
      character  c2*2                  , c3*3                ,
     &           ckey1*6               , ckey2*4             ,
     &           ckey3*4               , ckey4*4             ,
     &           ckey5*2               , ckey6*2             ,
     &           ckey7*2               , ckey8*2             ,
     &           ckey9*2               , ckey10*4            ,
     &           ckey11*4              ,
     &           ionnam*5              , c80*80              , cstrg*80
      character  cblnk8*8
c-----------------------------------------------------------------------
      integer    isela(nstore)         ,
     &           ita(nstore)           , ida(nstore)
      integer    nptn(ndptnl)          , nptnc(ndptnl,ndptn)
      integer    iptnla(ndptnl)        , iptna(ndptnl,ndptn)
      integer    iptnca(ndptnl,ndptn,ndptnc)
      integer    icnctv(ndcnct)
      integer    ifirsta(idword)       , ilasta(idword)
      integer    isstgr(nstore)        , iszr(nstore)
      integer    ispbr(nstore)         , isppr(nstore)
      integer    ncncta(iz0_max_res)   , icnctva(iz0_max_res,idcnct)
c-----------------------------------------------------------------------
      character  cindm(nstore)*2       , cfile(nstore)*8      ,
     &           ctype(nstore)*8       , cwavel(nstore)*10
      character  cptn_stack(ndstack)*80,cmt_stack(ndcmt)*80
c-----------------------------------------------------------------------
      real*8     teta(ntdim,nstore)    , teda(nddim,nstore)
      real*8     wavel(nstore)         , pec(ntdim,nddim,nstore)
      real*8     pec_max(nstore)
c-----------------------------------------------------------------------
      save       cslash                ,
     &           ckey1                 , ckey2                ,
     &           ckey3                 , ckey4
c-----------------------------------------------------------------------
      data       cslash / '/' /        , colon  / ':' /
      data       cblnk8 /'        '/
      data       ckey1  / 'filmem' /   , ckey2  / 'type'   /  ,
     &           ckey3  / 'indm'   /   , ckey4  / 'isel'   /  ,
     &           ckey5  /  'pl'    /   , ckey6  /  'ss'    /  ,
     &           ckey7  /  'pb'   /    , ckey8  /  'pp'    /  ,
     &           ckey9  /  'sz'   /    , ckey10 / 'ispb'   /  ,
     &           ckey11 / 'ispp'   /

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
      lbend = .false.
c-----------------------------------------------------------------------


c-----------------------------------------------------------------------
c read in number of data-blocks present in input file.
c-----------------------------------------------------------------------

      read(iunit,1000) c80
      read(c80, *) nbsel

      if(index(c80(1:15),'+').gt.0) then
          lptn_temp=.false.
      elseif(index(c80(1:15),':').gt.0) then
          lptn_temp=.true.
      else
          write(i4unit(-1),2003)'Incorrect element/ion field: ',
     &                          c80(11:15)
          write(i4unit(-1),2004)
          stop
      endif

      ipos1 = index(c80,'/') + 1
      ipos2 = ipos1          + 4
      read(c80(ipos1:ipos2),1001) ionnam

      if (( ionnam(2:2).eq.'+').or.( ionnam(2:2).eq.':') ) then
         esym  = ionnam(1:1) // ' '
      else
         esym  = ionnam(1:2)
      endif

      iz0   = i4eiz0( esym )
      iabt = 0
      is    = i4fctn( ionnam(4:5) , iabt )
      if (iabt.ne.0) is = i4fctn( ionnam(3:4) , iabt )


      is1   = is + 1

      if (nbsel.gt.nstore) then
         write(i4unit(-1),2000) dsname , nstore , nbsel , nstore
         nbsel = nstore
      endif

c-----------------------------------------------------------------------
c input connection vector and partition block if appropriate
c-----------------------------------------------------------------------
      lres=.false.
      ncptn_stack = 0

      if(lptn_temp) then
          ncnct = 0
          read(iunit,'(1a80)') c80
          if(c80(2:10).eq.'---------')then
               read(iunit,'(1a80)')c80
               if(c80(1:2).eq.'//') then
                   lres = .false.
                   backspace(iunit)
                   go to 20
               endif

               lres=.true.
               backspace(iunit)
   10          c80=' '
               read(iunit,'(1a80)')c80
               if(c80(2:10).eq.'---------')go to 20
               nfirst = 1
               iwords = idword
               call xxword( c80 , ' '    , nfirst ,
     &                      iwords  ,
     &                      ifirsta , ilasta , nwords
     &                    )
               do j=1,nwords
                 ncnct = ncnct + 1
                 read(c80(ifirsta(j):ilasta(j)),*)icnctv(ncnct)
               enddo

               go to 10
           else
               write(i4unit(-1),2005)'No connection/partition ',
     &                               'block  present'
               write(i4unit(-1),2006)
               backspace(iunit)
               lptn = .false.
               go to 30
           endif

   20      lresol = .false.
           if(lptn_temp) then
               call  xxrptn( iunit  , ndstack,
     &                       ndptnl , ndptn  , ndptnc ,
     &                       nptnl  , nptn   , nptnc  ,
     &                       iptnla , iptna  , iptnca ,
     &                       lresol , lptn   ,
     &                       c80    ,
     &                       ncptn_stack         , cptn_stack
     &                     )
               lptn=.true.
               iptnl=0
               do j=1,nptnl
                 iptnl=max(iptnl,iptnla(j))
               enddo
           endif

       endif

c-----------------------------------------------------------------------
c input data for each of the data-blocks.  Evaluate largest indm to see
c if confirms unresolved.
c-----------------------------------------------------------------------
   30  max_indm = 0

       do iblk=1,nbsel

c-----------------------------------------------------------------------
c input title, wavelength and other information (check block exists)
c-----------------------------------------------------------------------

         if (.not.lbend) then

            read(iunit,1000)cstrg
            call xxcase(cstrg,c80,'lc')

            if ( c80(1:1).ne.'c') then

               ipos1 =  index(c80,'a') + 1
               ipos2 =  index(c80,'/') - 1

               if (ipos1.eq.1) then
                  ipos1        = 11
                  cwavel(iblk) = c80(1:10)
               elseif (ipos1.gt.10) then
                  cwavel(iblk) = c80(1:10)
               else
                  cwavel(iblk) = c80(1:ipos1-1)
               endif

               call xxslen(cwavel(iblk),ifirst,ilast)
               if((cwavel(iblk)(ilast:ilast).eq.'a').or.
     &             (cwavel(iblk)(ilast:ilast).eq.'A'))then
                    wavel(iblk)=r8fctn(cwavel(iblk)(ifirst:ilast-1),
     &                          iabt)
               else
                   wavel(iblk)=r8fctn(cwavel(iblk)(ifirst:ilast),iabt)
               endif


               read(c80(ipos1:ipos2),*) ida(iblk) , ita(iblk)

               call xxhkey( c80 , ckey2 , cslash , ctype(iblk)  )
               lsup = .false.
               call xxhkey( c80 , ckey1 , cslash , cfile(iblk)  )
               if(cfile(iblk).eq.cblnk8) then
                   ipos1=ipos2+2
                   ipos2=index(c80(ipos1:80),'/')+ipos1-2

                   call xxhkey(c80(ipos1:ipos2),ckey5,colon,c2)
                   iabt  = 0
                   i    = i4fctn( c2 , iabt )
                   if(i.ne.iptnl) then
                      write(i4unit(-1),2003)'partition level mismatch:',
     &                                      'isel = ',iblk
                      write(i4unit(-1),2004)
                      stop
                   endif

                   call xxhkey(c80(ipos1:ipos2),ckey6,colon,c2)
                   iabt  = 0
                   i    = i4fctn( c2 , iabt )
                   if(i.ne.is) then
                      write(i4unit(-1),2003)'superstage mismatch:',
     &                                      'isel = ',iblk
                      write(i4unit(-1),2004)
                      stop
                   else
                      isstgr(iblk)=i+1
                   endif

                   call xxhkey(c80(ipos1:ipos2),ckey9,colon,c2)
                   iabt  = 0
                   i    = i4fctn( c2 , iabt )
                   if(iabt.gt.0) then
                      write(i4unit(-1),2003)'ionis. stage error:',
     &                                      'isel = ',iblk
                      write(i4unit(-1),2004)
                      stop
                   else
                      iszr(iblk)=i
                   endif

                   if(ctype(iblk).eq.'excit')then
                       call xxhkey(c80(ipos1:ipos2),ckey7,colon,c2)
                       iabt  = 0
                       i    = i4fctn( c2 , iabt )
                       if(iabt.gt.0) then
                          write(i4unit(-1),2003)'pb error:',
     &                                      'isel = ',iblk
                          write(i4unit(-1),2004)
                          stop
                       else
                          ispbr(iblk)=i
                          isppr(iblk)=0
                       endif
                   else
                       call xxhkey(c80(ipos1:ipos2),ckey8,colon,c2)
                       iabt  = 0
                       i    = i4fctn( c2 , iabt )
                       if(iabt.gt.0) then
                          write(i4unit(-1),2003)'pp error:',
     &                                      'isel = ',iblk
                          write(i4unit(-1),2004)
                          stop
                       else
                          ispbr(iblk)=0
                          isppr(iblk)=i
                       endif
                   endif

                   lsup = .true.

               endif

               if(.not.lptn_temp)then
                   call xxhkey( c80 , ckey3 , cslash , cindm(iblk)  )
                   iabt=0
                   indm=i4fctn(cindm(iblk),iabt)
                   if(iabt.gt.0) then
                       max_indm=max(max_indm,1)
                   else
                       max_indm=max(max_indm,indm)
                   endif
                   if(ctype(iblk).eq.'excit') then
                       ispbr(iblk)=indm
                       isppr(iblk)=0
                   elseif(ctype(iblk).eq.'recom') then
                       ispbr(iblk)=0
                       isppr(iblk)=indm
                   else
                       ispbr(iblk)=0
                       isppr(iblk)=0
                   endif
                   isstgr(iblk)=is+1
                   iszr(iblk)=is
               elseif(lptn_temp.and.(ctype(iblk).eq.'excit')) then
                   call xxhkey( c80 , ckey10 , cslash , cindm(iblk)  )
               elseif(lptn_temp.and.(ctype(iblk).eq.'recom')) then
                   call xxhkey( c80 , ckey11 , cslash , cindm(iblk)  )
               elseif(lptn_temp.and.(ctype(iblk).eq.'chexc')) then
                   call xxhkey( c80 , ckey11 , cslash , cindm(iblk)  )
               endif
               call xxhkey( c80 , ckey4 , cslash , c3           )
               isela(iblk) = i4fctn( c3 , iabt )

               ndnum = ida(iblk)
               ntnum = ita(iblk)

               if (ntnum.gt.ntdim) then
                  write(i4unit(-1),2001) dsname , iblk  ,
     &                                  'temperatures'  ,
     &                                  ntdim   , ntnum
                  stop
               endif

               if (ndnum.gt.nddim) then
                  write(i4unit(-1),2001) dsname , iblk   ,
     &                                  'densities'      ,
     &                                  nddim   , ndnum
                  stop
               endif

c-----------------------------------------------------------------------
c input temperature, density and photon emissivities for block
c-----------------------------------------------------------------------

               read(iunit,1002) ( teda(itd,iblk) , itd=1,ndnum )
               read(iunit,1002) ( teta(itt,iblk) , itt=1,ntnum )

               do itd=1,ndnum
                  read(iunit,1002) (pec(itt,itd,iblk),
     &                              itt=1,ntnum        )
               enddo

               pmax=0.0d0
               do itt=1,ntnum
                 if(pec(itt,1,iblk).gt.pmax)then
                     pmax=dmax1(pmax,pec(itt,1,iblk))
                 endif
               enddo
                     pec_max(iblk)=pmax

            else

               write(i4unit(-1),2002) dsname  , nbsel    ,
     &                               iblk - 1 , iblk - 1
               lbend = .true.
               nbsel = iblk - 1

            endif

         endif

       enddo

c-----------------------------------------------------------------------
c acquire the comments section as text lines if it exists
c-----------------------------------------------------------------------

       ncmt_stack = 0
       lcmt = .false.

   40  read(iunit,'(1a80)',end=50)cstrg
       call xxcase(cstrg,c80,'lc')
       if ((.not.lcmt).and.(c80(1:10).eq.'c---------').and.
     &     (index(c80,'sccs info').eq.0))then
           lcmt = .true.
           go to 40
       elseif(lcmt.and.(index(c80,'sccs info').eq.0))then
           ncmt_stack=ncmt_stack+1
           cmt_stack(ncmt_stack)=c80
           go to 40
       elseif(index(c80,'sccs info').gt.0)then
           ncmt_stack=ncmt_stack-1
       endif
   50  continue


c-----------------------------------------------------------------------
c     make up connection vectors and root partitions if appropriate
c     in the resolved case with 0 root partition level, the sum over
c     the connection vector gives the number of partitions
c-----------------------------------------------------------------------

      if ((.not.lres).and.(max_indm.eq.1)) then
          ncnct = iz0+1
          do i=1,ncnct
             icnctv(i)=1
          enddo
      elseif ((.not.lres).and.(max_indm.gt.1)) then
          if(iz0.le.iz0_max_res) then
              ncnct=ncncta(iz0)
              do i=1,ncnct
                icnctv(i)=icnctva(iz0,i)
              enddo
          else
              write(i4unit(-1),2003)'Connection vector required',
     &                    'in datasets since iz0 > ',iz0_max_res
              write(i4unit(-1),2004)
              stop
          endif

      endif

      if ((.not.lptn_temp).and.(max_indm.eq.1)) then
          nptnl   = 1
          iptnla(nptnl) = 1
          nptn(1) =  iz0+1
          do i=1,nptn(1)
            iptna(nptnl,i) = i-1
            nptnc(nptnl,i) = 1
            iptnca(1,iptna(nptnl,i)+1,nptnc(nptnl,i))=i-1
          enddo

          call xxmkrp( ndstack       ,
     &                 iz0           , iptnla(nptnl) ,
     &                 ncptn_stack   , cptn_stack
     &                )

       elseif ((.not.lptn_temp).and.(max_indm.gt.1)) then
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

          call xxmkrp( ndstack       ,
     &                 iz0           , iptnla(nptnl) ,
     &                 ncptn_stack   , cptn_stack
     &                )

      endif

      lptn=lptn_temp



c-----------------------------------------------------------------------
 1000 format(1a80)
 1001 format(a5)
 1002 format(8d9.2)

 2000 format(/1x,31('*'),' xxdata_15 message ',31('*')/
     &        2x,'input phot. emiss. data set name: ',a80/
     &        2x,'number of wavelength data-blocks',
     &           ' in input data set too great.'/
     &        2x,'the maximum number allowed     = ',i3/
     &        2x,'the number present in data set = ',i3/
     &        2x,'therefore only the first ',i2,' have been accepted'/
     &        1x,31('*'),' end of message ',31('*'))
 2001 format(/1x,32('*'),' xxdata_15 error ',32('*')/
     &        2x,'input phot. emiss. data set name: ',a80/
     &        2x,'data-block index: ',i3//
     &        2x,'the number of input electron ',a,' too large'/
     &        2x,'the maximum number allowed       = ',i3/
     &        2x,'the number present in data-block = ',i3/
     &        1x,29('*'),' program terminated ',29('*'))
 2002 format(/1x,31('*'),' xxdata_15 message ',31('*')/
     &        2x,'input ions./photon data set name: ',a80/
     &        2x,'inconsistency in the number of wavelengths',
     &           ' expected and read.'/
     &        2x,'the number expected = ',i3/
     &        2x,'the number read in  = ',i3/
     &        2x,'therefore only ',i3,' have been accepted'/
     &        1x,31('*'),' end of message ',31('*'))
 2003 format(1x,30('*'),' xxdata_15 error   ',30('*')//
     &       2x,a,a,i3,a,i3 )
 2004 format(/1x,30('*'),' program terminates ',29('*'))
 2005 format(1x,30('*'),' xxdata_15 warning ',30('*')//
     &       2x,a,a,i3,a,i3 )
 2006 format(/1x,30('*'),' program continues ',30('*'))
c-----------------------------------------------------------------------

      return
      end
