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
       PROGRAM TEST
       
       IMPLICIT NONE
C------------------------------------------------------------------------
C  Purpose:
C          Test the XXDATA_15 routine and also provide a brief
C          example of its use.
C
C  Explanaton:
C          This program is distributed as part of the ADAS
C          subroutine library either via direct CVS to ADAS Project
C          members or via download by OPEN-ADAS users. It reads a
C          file called "test.dat" (distributed along with this
C          program) and prints out some of the contents. The
C          program is intended to serve as an example of using the
C          XXDATA_15 subroutine as well as testing it. A short
C          shell script called "test.sh" is used to compile and
C          test the code.
C
C  Variables:
C          All variables are documented by XXDATA_15. See either the
C          Fortran source or the PDF documentation for the routine.
C          Variables not passed into XXDATA_15 are trivial in nature.
C
C  Routines:
C          Routine    Source    Brief description
C          -------------------------------------------------------------
C          XXDATA_15  ADAS      Read complete data from an ADF15 file
C
C  Author : Allan Whiteford
C
C  Date   : 11/01/08
C       
C-----------------------------------------------------------------------

C-----------------------------------------------------------------------
C     Parameters required by XXDATA_15
C     --------------------------------        
      INTEGER     NSTORE       , NDDIM         , NTDIM
      INTEGER     NDPTNL       , NDPTN         , NDPTNC
      INTEGER     NDCNCT       , NDSTACK       , NDCMT
      PARAMETER ( NSTORE = 500 , NDDIM = 50    , NTDIM = 40 )
      PARAMETER ( NDPTNL = 4   , NDPTN  = 128  , NDPTNC = 256 )
      PARAMETER ( NDCNCT = 100 , NDSTACK = 40  , NDCMT  = 2000 )
C-----------------------------------------------------------------------

C-----------------------------------------------------------------------
C     Input variables (i.e. non-parameter) required by XXDATA_15
C     ----------------------------------------------------------
      INTEGER   IUNIT
      CHARACTER*80 DSNAME     
C-----------------------------------------------------------------------		

C-----------------------------------------------------------------------
C     Output variables required by XXDATA_15
C     --------------------------------------
      CHARACTER*8         CFILE(NSTORE)
      CHARACTER*2         CINDM(NSTORE)
      CHARACTER*80        CMT_STACK(NDCMT),         CPTN_STACK(NDSTACK)
      CHARACTER*8         CTYPE(NSTORE)
      CHARACTER*10        CWAVEL(NSTORE)
      CHARACTER*2         ESYM
      INTEGER             ICNCTV(NDCNCT),           IDA(NSTORE)
      INTEGER             IPTNA(NDPTNL,NDPTN)
      INTEGER             IPTNCA(NDPTNL,NDPTN,NDPTNC)
      INTEGER             IPTNLA(NDPTNL),           IS,          IS1
      INTEGER             ISELA(NSTORE),            ISPBR(NSTORE)
      INTEGER             ISPPR(NSTORE),            ISSTGR(NSTORE)
      INTEGER             ISZR(NSTORE),             ITA(NSTORE)
      INTEGER             IZ0,         NBSEL,       NCMT_STACK,  NCNCT
      INTEGER             NPTN(NDPTNL),             NPTNC(NDPTNL,NDPTN)
      INTEGER             NPTNL,       NCPTN_STACK
      LOGICAL             LCMT,        LPTN,        LRES,        LSUP
      REAL*8              PEC(NTDIM,NDDIM,NSTORE),  PEC_MAX(NSTORE)
      REAL*8              TEDA(NDDIM,NSTORE),       TETA(NTDIM,NSTORE)
      REAL*8              WAVEL(NSTORE)
C-----------------------------------------------------------------------

C-----------------------------------------------------------------------
C     Variables only used by this test program
C     ----------------------------------------
      INTEGER   I,J,K
      INTEGER   ISTORE
C----------------------------------------------------------------------

C-----------------------------------------------------------------------
C     Open input file for reading
C     ---------------------------      
      IUNIT = 10
      DSNAME='test.dat'
      OPEN(UNIT = IUNIT , FILE=DSNAME , STATUS = 'OLD')
C-----------------------------------------------------------------------
       
C-----------------------------------------------------------------------
C     Pass unit number and dimension parameters to XXDATA_15 and
C     get back contents of file.
C     --------------------------      

      CALL XXDATA_15( IUNIT  , DSNAME ,
     &                NSTORE , NTDIM  , NDDIM  ,
     &                NDPTNL , NDPTN  , NDPTNC , NDCNCT ,
     &                NDSTACK, NDCMT ,
     &                IZ0    , IS     , IS1    , ESYM   ,
     &                NPTNL  , NPTN   , NPTNC  ,
     &                IPTNLA , IPTNA  , IPTNCA ,
     &                NCNCT  , ICNCTV ,
     &                NCPTN_STACK     , CPTN_STACK      ,
     &                LRES   , LPTN   , LCMT   , LSUP   ,
     &                NBSEL  , ISELA  ,
     &                CWAVEL , CFILE  , CTYPE  , CINDM  ,
     &                WAVEL  , ISPBR  , ISPPR  , ISSTGR , ISZR  ,
     &                ITA    , IDA    ,
     &                TETA   , TEDA   ,
     &                PEC    , PEC_MAX,
     &                NCMT_STACK      , CMT_STACK
     &              )
C-----------------------------------------------------------------------
   
C-----------------------------------------------------------------------
C     Print out some of the contents to screen
C     ---------------------------------------- 

      PRINT *,'XXDATA_15 Test Program'      
      PRINT *,'----------------------'
      PRINT *,' '
      PRINT *,'The following is some information about the'
      PRINT *,'input file: '//DSNAME
      PRINT *,' '       
      PRINT 1001,IZ0,IS,IS1,
     &                       LRES,LPTN,LCMT,LSUP
 
      PRINT 1002,NPTNL
      DO I=1,NPTNL
        PRINT 1003,I,IPTNLA(I),NPTN(I)
        DO J=1,NPTN(I)
           PRINT '(30X,I3,4X,I2,8X,I2,8X,10I3)',
     &  		       J,IPTNA(I,J),NPTNC(I,J),
     &  		      (IPTNCA(I,J,K),K=1,NPTNC(I,J))
        ENDDO
          
      ENDDO
      
      PRINT 1006,NCNCT
      PRINT 1007,(ICNCTV(I),I=1,NCNCT)
      
      PRINT 1008,NBSEL,ISTORE
      
      PRINT 1009,(ISELA(I),I=1,NBSEL,10)
      
C      IF(LPTN) THEN
          PRINT 1010,(ISPBR(I),I=1,NBSEL,10)
          PRINT 1011,(ISPPR(I),I=1,NBSEL,10)
          PRINT 1012,(ISSTGR(I),I=1,NBSEL,10)
          PRINT 1013,(ISZR(I),I=1,NBSEL,10)
C      ELSE	  
          PRINT 1018,('   ',CINDM(I),I=1,NBSEL,10)
C      ENDIF	  
      
      PRINT 1019,CWAVEL(ISTORE)
      PRINT 1014,ITA(ISTORE),IDA(ISTORE)
      PRINT 1015,TETA(1,ISTORE),TETA(ITA(ISTORE),ISTORE)
      PRINT 1016,TEDA(1,ISTORE),TEDA(IDA(ISTORE),ISTORE)
      PRINT 1017,PEC(1,1,1),
     &                      PEC(1,1,ISTORE),
     &                      PEC(ITA(ISTORE),1,1),
     &                      PEC(1,IDA(ISTORE),1),
     &                      PEC(ITA(ISTORE),IDA(ISTORE),ISTORE)


 1001 FORMAT(7X,'IZ0    = ',I3,7X,'IS     = ',I3,7X,'IS1    = ',I3/
     &       7X,'LRES   = ',L3,7X,'LPTN   = ',L3,7X,'LCMT   = ',L3,
     &       7X,'LSUP   = ',L3)
 1002 FORMAT('  Partition information:'/
     &       7X,'NPTNL  = ',I3/
     &       8X,' I IPTNLA(I) NPTN(I)',
     &       2X,' J IPTNA(I,J) NPTNC(I,J)',
     &       2X,'  IPTNCA(I,J,K)')
 1003 FORMAT(8X,I2,I5,I10)
 1004 FORMAT(30X,I2,I5,I11,8X,10I3/56X,10I3/56X,10I3/56X,10I3/56X,10I3) 
C 1004 FORMAT(30X,I2,I5,I11)
 1005 FORMAT(56X,I2,I5)
 1006 FORMAT('  Connection information:'/
     &       7X,'NCNCT  = ',I3,3X,'(ICNCTV(I),I=1,NCNCT)')
 1007 FORMAT(22X,20I3)
 1008 FORMAT('  Transition information:'/
     &       7X,'NBSEL  = ',I3,7X,'ISTORE  = ',I3)
 1009 FORMAT(22X,'(ISELA(I),I=1,NBSEL,10)'/(22X,10I5))
 1010 FORMAT(22X,'(ISPBR(I),I=1,NBSEL,10)'/(22X,10I5))
 1011 FORMAT(22X,'(ISPPR(I),I=1,NBSEL,10)'/(22X,10I5))
 1012 FORMAT(22X,'(ISSTGR(I),I=1,NBSEL,10)'/(22X,10I5))
 1013 FORMAT(22X,'(ISZR(I),I=1,NBSEL,10)'/(22X,10I5))
 1014 FORMAT(7X,'ITA(ISTORE)  = ',I3,7X,'IDA(ISTORE)  = ',I3)
 1015 FORMAT(7X,'TETA(1,ISTORE) = ',1PD10.2,3X,
     &          'TETA(ITA,ISTORE) = ',1PD10.2)
 1016 FORMAT(7X,'TEDA(1,ISTORE) = ',1PD10.2,3X,
     &          'TEDA(IDA,ISTORE) = ',1PD10.2)
 1017 FORMAT(7X,'PEC(1,1,1)              = ',1PD10.2/
     &       7X,'PEC(1,1,ISTORE)         = ',1PD10.2/
     &       7X,'PEC(ITA,1,1)            = ',1PD10.2/
     &       7X,'PEC(1,IDA,1)            = ',1PD10.2/
     &       7X,'PEC(ITA,IDA,ISTORE)     = ',1PD10.2/)
 1018 FORMAT(22X,'(CINDM(I),I=1,NBSEL,10)'/(22X,10A5))
 1019 FORMAT(7X,'CWAVEL(ISTORE)  = ',A10)
C-------------------------------------------------------------------

      END					  	
