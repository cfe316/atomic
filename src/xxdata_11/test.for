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
C          Test the XXDATA_11 routine and also provide a brief
C          example of its use.
C
C  Explanaton:
C          This program is distributed as part of the ADAS
C          subroutine library either via direct CVS to ADAS Project
C          members or via download by OPEN-ADAS users. It reads a
C          file called "test.dat" (distributed along with this
C          program) and prints out some of the contents. The
C          program is intended to serve as an example of using the
C          XXDATA_11 subroutine as well as testing it. A short
C          shell script called "test.sh" is used to compile and
C          test the code.
C
C  Variables:
C          All variables are documented by XXDATA_11. See either the
C          Fortran source or the PDF documentation for the routine.
C          Variables not passed into XXDATA_11 are trivial in nature.
C
C  Routines:
C          Routine    Source    Brief description
C          -------------------------------------------------------------
C          XXDATA_11  ADAS      Read complete data from an ADF11 file
C
C  Author : Allan Whiteford
C
C  Date   : 11/01/08
C       
C-----------------------------------------------------------------------      

C-----------------------------------------------------------------------
C     Parameters required by XXDATA_11
C     --------------------------------        
      INTEGER     ISDIMD      , IZDIMD     , ITDIMD      , IDDIMD 
      INTEGER     NDPTNL      , NDPTN      , NDPTNC      , NDCNCT
      PARAMETER ( ISDIMD = 200, IZDIMD = 92, ITDIMD = 50 , IDDIMD = 40)
      PARAMETER ( NDPTN  = 128, NDPTNL = 4 , NDPTNC = 256, NDCNCT = 100)
C-----------------------------------------------------------------------

C-----------------------------------------------------------------------
C     Input variables (i.e. non-parameter) required by XXDATA_11
C     ----------------------------------------------------------
      INTEGER   IUNIT     , ICLASS
C-----------------------------------------------------------------------

C-----------------------------------------------------------------------
C     Output variables required by XXDATA_11
C     --------------------------------------
      INTEGER   IZ0       , IS1MIN    , IS1MAX
      INTEGER   IBLMX     , ISMAX     , ITMAX     , IDMAX
      INTEGER   NPTNL     , NCNCT
      REAL*8    DNR_AMS
      INTEGER   NPTN(NDPTNL)          , NPTNC(NDPTNL,NDPTN)
      INTEGER   IPTNLA(NDPTNL)        , IPTNA(NDPTNL,NDPTN) 
      INTEGER   IPTNCA(NDPTNL,NDPTN,NDPTNC)
      INTEGER   ICNCTV(NDCNCT)
      INTEGER   ISPPR(ISDIMD)   , ISPBR(ISDIMD)   , ISSTGR(ISDIMD)
      REAL*8    DDENS(IDDIMD)         , DTEV(ITDIMD)
      REAL*8    DRCOF(ISDIMD,ITDIMD,IDDIMD)
      LOGICAL   LRES    , LSTAN     , LPTN 
      CHARACTER DNR_ELE*12
C-----------------------------------------------------------------------

C-----------------------------------------------------------------------
C     Variables only used by this test program
C     ----------------------------------------
      CHARACTER DSNIN*120
      INTEGER   I         , J         , K 
C-----------------------------------------------------------------------
 
C-----------------------------------------------------------------------
C     Open input file for reading and set the (optional) expected class
C     to 1 (i.e. ACD)
C     ---------------
      IUNIT = 10
      DSNIN = '../scd96_c.dat'
      OPEN(UNIT=IUNIT , FILE = DSNIN , STATUS = 'OLD')
      ICLASS = 1
C-----------------------------------------------------------------------
           
C-----------------------------------------------------------------------
C     Pass unit number and dimension parameters to XXDATA_11 and
C     get back contents of file.
      CALL XXDATA_11( IUNIT  , ICLASS , 
     &                ISDIMD , IDDIMD , ITDIMD , 
     &                NDPTNL , NDPTN  , NDPTNC , NDCNCT ,
     &                IZ0    , IS1MIN , IS1MAX ,
     &                NPTNL  , NPTN   , NPTNC  ,   
     &                IPTNLA , IPTNA  , IPTNCA , 
     &                NCNCT  , ICNCTV ,
     &                IBLMX  , ISMAX  , DNR_ELE, DNR_AMS, 
     &                ISPPR  , ISPBR  , ISSTGR ,
     &                IDMAX  , ITMAX  ,  
     &                DDENS  , DTEV   , DRCOF  ,
     &                LRES   , LSTAN  , LPTN  
     &               )
C-----------------------------------------------------------------------
   
C-----------------------------------------------------------------------
C     Print out some of the contents to screen
C     ----------------------------------------      

      PRINT *,'XXDATA_11 Test Program'      
      PRINT *,'----------------------'
      PRINT *,' '
      PRINT *,'The following is some information about the'
      PRINT *,'input file: '//DSNIN
      PRINT *,' '
      PRINT 1001,IZ0,IS1MIN,IS1MAX,
     &                       LRES,LSTAN,LPTN,
     &                       NPTNL
     
      PRINT 1002
      DO I=1,NPTNL
        PRINT 1003,I,IPTNLA(I),NPTN(I)
         DO J=1,NPTN(I)
           PRINT '(30X,I3,4X,I2,8X,I2,8X,10I3)',J,IPTNA(I,J),NPTNC(I,J),
     &                        (IPTNCA(I,J,K),K=1,NPTNC(I,J))
         ENDDO  
      ENDDO
      
      PRINT 1006,NCNCT
      PRINT 1007,(ICNCTV(I),I=1,NCNCT)
      
      PRINT 1008,IBLMX,ISMAX
      PRINT 1009,(ISPPR(I),I=1,IBLMX)
      PRINT 1010,(ISPBR(I),I=1,IBLMX)
      PRINT 1011,(ISSTGR(I),I=1,IBLMX)

      PRINT 1012,IDMAX,ITMAX
      PRINT 1013,DDENS(1),DDENS(IDMAX)
      PRINT 1014,DTEV(1),DTEV(ITMAX)
      IF(ICLASS.LE.10) THEN
          PRINT 1015,DRCOF(1,1,1),
     &                          DRCOF(IBLMX,1,1),
     &                          DRCOF(1,ITMAX,1),
     &                          DRCOF(1,1,IDMAX),
     &                          DRCOF(IBLMX,ITMAX,IDMAX)
      ELSE 
          PRINT 1016,DRCOF(1,1,1),
     &                          DRCOF(IBLMX,1,1),
     &                          DRCOF(1,ITMAX,1),
     &                          DRCOF(1,1,IDMAX),
     &                          DRCOF(IBLMX,ITMAX,IDMAX)
      ENDIF 
         
 1001 FORMAT(7X,'IZ0    = ',I3,7X,'IS1MIN = ',I3,7X,'IS1MAX = ',I3/
     &       7X,'LRES   = ',L3,7X,'LSTAN  = ',L3,7X,'LPTN   = ',L3/
     &       7X,'NPTNL  = ',I3)
 1002 FORMAT('  Partition information:'/
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
 1008 FORMAT(7X,'IBLMX  = ',I3,7X,'ISMAX  = ',I3)
 1009 FORMAT(22X,'(ISPPR(I),I=1,IBLMX)'/(22X,20I3))
 1010 FORMAT(22X,'(ISPBR(I),I=1,IBLMX)'/(22X,20I3))
 1011 FORMAT(22X,'(ISSTGR(I),I=1,IBLMX)'/(22X,20I3))
 1012 FORMAT(7X,'IDMAX  = ',I3,7X,'ITMAX  = ',I3)
 1013 FORMAT(7X,'DDENS(1) = ',F10.5,3X,'DDENS(IDMAX) = ',F10.5)
 1014 FORMAT(7X,'DTEV(1)  = ',F10.5,3X,'DTEV(ITMAX)  = ',F10.5)
 1015 FORMAT(7X,'DRCOF(1,1,1)              = ',F10.5/
     &       7X,'DRCOF(IBLMX,1,1)          = ',F10.5/
     &       7X,'DRCOF(1,ITMAX,1)          = ',F10.5/
     &       7X,'DRCOF(1,1,IDMAX)          = ',F10.5/
     &       7X,'DRCOF(IBLMX,ITMAX,IDMAX)  = ',F10.5/)
 1016 FORMAT(7X,'DRCOF(1,1,1)              = ',1PD10.3/
     &       7X,'DRCOF(IBLMX,1,1)          = ',1PD10.3/
     &       7X,'DRCOF(1,ITMAX,1)          = ',1PD10.3/
     &       7X,'DRCOF(1,1,IDMAX)          = ',1PD10.3/
     &       7X,'DRCOF(IBLMX,ITMAX,IDMAX)  = ',1PD10.3/)
C-------------------------------------------------------------------
      END      
