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
CX UNIX PORT - SCCS Info : Module @(#)$Header: /work/dummy/xxdata_15/xxslen.for,v 1.1 2004/07/06 15:39:12 whitefor Exp $ Date $Date: 2004/07/06 15:39:12 $
CX      
      SUBROUTINE XXSLEN( CSTRNG , IFIRST , ILAST )
      IMPLICIT NONE
C-----------------------------------------------------------------------
C
C  ****************** FORTRAN77 SUBROUTINE: XXSLEN *********************
C
C  PURPOSE: TO IDENTIFY THE FIRST AND LAST NON-BLANK CHARACTER IN A
C           STRING. (IF INPUT STRING IS BLANK IFIRST=ILAST=0)
C
C  CALLING PROGRAM: GENERAL USE
C
C  SUBROUTINE:
C
C  INPUT : (C*(*)) CSTRNG   = INPUT STRING FOR INTERROGATION
C
C  OUTPUT: (I*4)   IFIRST   = BYTE POSITION OF FIRST NON-BLANK CHARACTER
C                             IN INPUT STRING.
C  OUTPUT: (I*4)   ILAST    = BYTE POSITION OF LAST  NON-BLANK CHARACTER
C                             IN INPUT STRING.
C
C          (I*4)   I        = GENERAL USE
C          (I*4)   ILEN     = LENGTH OF 'CSTRNG' STRING IN BYTES
C
C ROUTINES: NONE
C
C NOTE:
C
C
C AUTHOR:  PAUL E. BRIDEN (TESSELLA SUPPORT SERVICES PLC)
C          K1/0/37
C          JET EXT. 6023
C
C DATE  :  06/07/93
C
C-----------------------------------------------------------------------
C-----------------------------------------------------------------------
C
C-----------------------------------------------------------------------
      INTEGER     IFIRST     , ILAST    , ILEN    , I
C-----------------------------------------------------------------------
      CHARACTER   CSTRNG*(*)
C-----------------------------------------------------------------------
C-----------------------------------------------------------------------
C
C-----------------------------------------------------------------------
C
      ILEN   = LEN(CSTRNG)
C-----------------------------------------------------------------------
      IFIRST = 0
      ILAST  = 0
C-----------------------------------------------------------------------
C
         DO 1 I=1,ILEN
C
            IF (CSTRNG(I:I).NE.' ') THEN
               IF (IFIRST.EQ.0) IFIRST = I
               ILAST = I
            ENDIF
C
    1    CONTINUE
C
C-----------------------------------------------------------------------
C
       RETURN
       END
