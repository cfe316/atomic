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
CX UNIX PORT - SCCS Info : Module @(#)$Header: /work/dummy/xxdata_15/xxword.for,v 1.1 2004/07/06 15:40:43 whitefor Exp $ Date $Date: 2004/07/06 15:40:43 $
CX
      SUBROUTINE XXWORD( CTEXT  , CDELIM , NFIRST ,
     &                   IWORDS ,
     &                   IFIRST , ILAST  , NWORDS
     &                 )
      IMPLICIT NONE
C-----------------------------------------------------------------------
C
C  ****************** FORTRAN77 SUBROUTINE: XXWORD *********************
C
C  PURPOSE: TO EXTRACT THE Nfirst to (Nfirst+IWORDS-1) WORDS FROM AN
C           INPUT STRING. OUTPUTS THE FIRST AND LAST BYTE INDEXES OF
C           EACH WORD AS WELL AS THE TOTAL NUMBER OF WORDS FOUND.
C
C           A WORD = A STRING OF CHARACTERS SEPARATED BY ANY CHARACTER
C                    CONTAINED IN THE INPUT STRING CDELIM.
C
C  CALLING PROGRAM: GENERAL USE
C
C  SUBROUTINE:
C
C  INPUT : (C*(*)) CTEXT   = INPUT TEXT LINE CONTAINING STRING
C  INPUT : (C*(*)) CDELIM  = INPUT STRING CONTAINING DELIMITER CHARS.
C  INPUT : (I*4)   NFIRST  = THE INDEX NO. OF THE FIRST WORD TO EXTRACT.
C
C  I/O   : (I*4)   IWORDS  = INPUT : SIZE OF IFIRST, ILAST(ARRAYS)
C                                    (I.E. NUMBER OF WORDS TO EXTRACT)
C                          = OUTPUT: NUMBER OF REQUESTED WORDS FOUND
C
C  OUTPUT: (I*4)   IFIRST()= INDEX OF FIRST BYTE OF THE Nth WORD
C  OUTPUT: (I*4)   ILAST() = INDEX OF LAST  BYTE OF THE Nth WORD
C  OUTPUT: (I*4)   NWORDS  = THE TOTAL NUMBER OF WORDS FOUND IN CTEXT
C
C          (I*4)   LENTXT  = LENGTH IN BYTES OF 'CTEXT' STRING
C          (I*4)   IDELIM  = 0 => CTEXT CHARACTER IS NOT A DELIMITER
C                          > 0 => CTEXT CHARACTER IS A DELIMITER
C          (I*4)   ITOTAL  = NUMBER OF WORDS FOUND SO FAR
C          (I*4)   IINDEX  = IFIRST()/ILAST() INDEX OF CURRENT WORD
C          (I*4)   NLAST   = THE INDEX NO. OF THE LAST WORD TO EXTRACT
C          (I*4)   I       = GENERAL USE INDEX
C
C          (L*4)   LWORD   = .TRUE.  - PROCESSING AN IDENTIFIED WORD
C                            .FALSE. - PROCESSING SPACE BETWEEN WORDS
C
C ROUTINES: NONE
C
C NOTES:    IF THERE IS NO Nfirst WORD OR NO WORDS ARE FOUND
C           (I.E. INPUT STRING IS BLANK) THEN IWORDS=0
C
C AUTHOR:  PAUL E. BRIDEN (TESSELLA SUPPORT SERVICES PLC)
C          K1/0/37
C          JET EXT. 5023
C
C DATE:    20/05/93
C
C-----------------------------------------------------------------------
      INTEGER    NFIRST          , IWORDS           , NWORDS      ,
     &           LENTXT          , IDELIM           , ITOTAL      ,
     &           IINDEX          , NLAST            , I
C-----------------------------------------------------------------------
      LOGICAL    LWORD
C-----------------------------------------------------------------------
      CHARACTER  CTEXT*(*)       , CDELIM*(*)
C-----------------------------------------------------------------------
      INTEGER    IFIRST(IWORDS)  , ILAST(IWORDS)
C-----------------------------------------------------------------------
C
C-----------------------------------------------------------------------
C
      LENTXT = LEN(CTEXT)
      NLAST  = IWORDS + NFIRST - 1
C
C-----------------------------------------------------------------------
C FIND THE REQUIRED WORDS
C-----------------------------------------------------------------------
C
         DO 1 I = 1,IWORDS
            IFIRST(I) = 0
            ILAST(I)  = 0
    1    CONTINUE
C
      ITOTAL = 0
      LWORD  = .FALSE.
      IINDEX = 0
C
         DO 2 I = 1,LENTXT
 
            IDELIM = INDEX( CDELIM , CTEXT(I:I) )
 
               IF (LWORD) THEN
 
                  IF (IDELIM.GT.0) THEN
                     LWORD  = .FALSE.
                     IF ((ITOTAL.GE.NFIRST).AND.(ITOTAL.LE.NLAST)) THEN
                        ILAST(IINDEX)  = I - 1
                     ENDIF
                  ENDIF
 
               ELSE
 
                  IF (IDELIM.EQ.0) THEN
                     LWORD  = .TRUE.
                     ITOTAL = ITOTAL + 1
                     IF ((ITOTAL.GE.NFIRST).AND.(ITOTAL.LE.NLAST)) THEN
                        IINDEX         = IINDEX + 1
                        IFIRST(IINDEX) = I
                        ILAST(IINDEX)  = LENTXT
                     ENDIF
                  ENDIF
 
               ENDIF
 
    2    CONTINUE
C
      IWORDS = IINDEX
      NWORDS = ITOTAL
C
C-----------------------------------------------------------------------
C
      RETURN
      END
