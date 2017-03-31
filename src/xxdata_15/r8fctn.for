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
      FUNCTION R8FCTN( STR , IABT )
      IMPLICIT NONE
C-----------------------------------------------------------------------
C
C  **************** FORTRAN77 REAL*8 FUNCTION: R8FCTN ******************
C
C  PURPOSE : TO CONVERT A FLOATING POINT NUMBER STORED IN A STRING
C            INTO A REAL*8 VARIABLE.
C
C  CALLING PROGRAM: GENERAL USE
C
C  FUNCTION:
C
C          (R*8)   R8FCTN  = FUNCTION NAME
C          (C*(*)) STR     = STRING CONTAINING SINGLE FLOATING POINT NO.
C          (I*4)   IABT    = RETURN CODE:
C                               0 => NO ERROR
C                               2 => ERROR (A VALUE 'R8FCTN=0.0' WILL BE
C                                           RETURNED).
C                               9 => OVERFLOW ERROR (EXPONENT  > IUOFLW)
C                                    (A VALUE 'R8FCTN=0.0' RETURNED)
C                              10 => UNDERFLOW ERROR (EXPONENT <-IUOFLW)
C                                    (A VALUE 'R8FCTN=0.0' RETURNED)
C
C          (I*4)   IUOFLW   = PARAMETER = MODULUS OF MAXIMUM ALLOWED
C                                         EXPONENT = 60
C
C          (C*1)   CH0      = PARAMETER = '0'
C          (C*1)   CH9      = PARAMETER = '9'
C          (C*1)   BLANK    = PARAMETER = ' '
C          (C*1)   CPLUS    = PARAMETER = '+'
C          (C*1)   CMINUS   = PARAMETER = '-'
C          (C*1)   CPNT     = PARAMETER = '.'
C          (C*1)   CHE      = PARAMETER = 'E'
C          (C*1)   CHD      = PARAMETER = 'D'
C          (C*1)   CLE      = PARAMETER = 'e'
C          (C*1)   CLD      = PARAMETER = 'd'
C
C          (I*4)   ILEN     = LENGTH OF 'STR' STRING IN BYTES
C          (I*4)   M1       = STARTING BYTE IN 'STR' OF NUMBER
C                             INCLUDING SIGN
C          (I*4)   M2       = LAST BYTE IN 'STR' OF NUMBER
C          (I*4)   IE       = STARTING BYTE OF EXPONENT IN  'STR'
C                             IGNORING ANY SIGN PRESENT.
C          (I*4)   MS       = 0 => MANTISSA HAS NO SIGN
C                             1 => MANTISSA HAS A SIGN
C          (I*4)   IS       = 0 => EXPONENT HAS NO SIGN
C                             1 => EXPONENT HAS A SIGN
C          (I*4)   IPOW     = EXPONENT
C          (I*4)   ICH0     = ICHAR('0')
C          (I*4)   ICH9     = ICHAR('9')
C          (I*4)   ISTR     = ICHAR(CURRENT BYTE POSITION IN 'STR')
C          (I*4)   I        = GENERAL USE
C
C          (L*4)   LMANT    = .TRUE.  => MANTISSA BEING ANALYSED
C                             .FALSE. => EXPONENT BEING ANALYSED
C          (L*4)   LPOINT   = .TRUE.  => DECIMAL POINT FOUND IN MANTISSA
C                             .FALSE. => NO DECIMAL POINT FOUND IN MANT.
C          (L*4)   LFOUND   = .TRUE.  => ALL OF THE INPUT NUMBER BYTES
C                                        HAVE BEEN ASSESSED.
C                             .FALSE. => INPUT NUMBER BYTES STILL BEING
C                                        ASSESSED.
C
C NOTE:     AN ERROR WILL OCCUR (IABT=2) IF THERE IS MORE THAN ONE
C           NUMBER OCCURING IN THE STRING 'STR()'
C
C
C AUTHOR:   PAUL E. BRIDEN (TESSELLA SUPPORT SERVICES PLC)
C           K1/0/81
C           JET EXT. 4569
C
C DATE:     26/10/90
C
C VERSION  : 1.2                          
C DATE     : 20-12-2001
C MODIFIED : Martin O'Mullane
C               - Removed mainframe listing information beyond column 72.
C
C VERSION  : 1.3                          
C DATE     : 03-12-2003
C MODIFIED : Hugh Summers
C               - Allowed lower case 'e' or 'd' in the real number spec.
C
C VERSION  : 1.4
C DATE     : 10-04-2007
C MODIFIED : Allan Whiteford
C               - Modified documentation as part of automated
C		  subroutine documentation preparation.
C
C-----------------------------------------------------------------------
C
C-----------------------------------------------------------------------
      INTEGER    IUOFLW
C-----------------------------------------------------------------------
      CHARACTER  CH0*1   , CH9*1   , BLANK*1   , CPLUS*1   , CMINUS*1 ,
     &           CPNT*1  , CHE*1   , CHD*1     , CLE*1     , CLD*1
C-----------------------------------------------------------------------
      PARAMETER( IUOFLW=60 )
      PARAMETER( CH0 ='0', CH9='9', BLANK=' ', CPLUS='+', CMINUS='-' ,
     &           CPNT='.', CHE='E', CHD='D'  , CLE='e', CLD='d'  )
C-----------------------------------------------------------------------
      CHARACTER  STR*(*)
C-----------------------------------------------------------------------
      INTEGER    IABT
      INTEGER    M1      , M2      , MS        , IS        , IE       ,
     &           ICH0    , ICH9    , ISTR      , ILEN      , IPOW     ,
     &           I
C-----------------------------------------------------------------------
      LOGICAL    LMANT   , LPOINT  , LFOUND
C-----------------------------------------------------------------------
      REAL*8     R8FCTN
C-----------------------------------------------------------------------
C
C-----------------------------------------------------------------------
C INITIALIZE VALUES
C-----------------------------------------------------------------------
C
      R8FCTN=0.0
      IABT=0
      M1=0
      MS=0
      IS=0
      IE=0
      LMANT=.TRUE.
      LPOINT=.FALSE.
      LFOUND=.FALSE.
      ICH0=ICHAR(CH0)
      ICH9=ICHAR(CH9)
      ILEN=LEN(STR)
C
C-----------------------------------------------------------------------
C FIND STARTING BYTE OF NUMBER
C-----------------------------------------------------------------------
C
         DO 1 I=1,ILEN
               IF ( STR(I:I).NE.BLANK ) THEN
                  M1=I
                  GOTO 2
               ENDIF
    1    CONTINUE
C
C-----------------------------------------------------------------------
C IDENTIFY IF MANTISSA HAS A SIGN
C-----------------------------------------------------------------------
C
    2 IF ( M1.EQ.0 ) RETURN
      IF   ( ( STR(M1:M1).EQ.CPLUS  )
     &                  .OR.
     &       ( STR(M1:M1).EQ.CMINUS ) ) MS=1
C
C***********************************************************************
C IDENTIFY IF MANTISSA AND EXPONENT (IF PRESENT) ARE OF VALID FORM
C***********************************************************************
C
         DO 3 I=M1+MS,ILEN
               IF (LFOUND) THEN
C
C-----------------------------------------------------------------------
C INPUT NO. COMPLETELY DEFINED: IDENTIFY IF EXTRA NON-BLANK BYTES EXIST
C-----------------------------------------------------------------------
C
                  IF ( STR(I:I).NE.BLANK ) IABT=2
C-----------------------------------------------------------------------
               ELSEIF (STR(I:I).EQ.BLANK) THEN
C
C IF NOTHING AFTER EXPONENT 'E' OR 'D' SYMBOL RETURN ERROR CODE
C
                     IF ( I.EQ.IE ) THEN
                        IABT=2
                     ELSE
                        LFOUND=.TRUE.
                     ENDIF
C-----------------------------------------------------------------------
               ELSEIF (I.GE.IE) THEN
                  ISTR=ICHAR(STR(I:I))
                     IF (LMANT) THEN
C
C-----------------------------------------------------------------------
C MANTISSA
C-----------------------------------------------------------------------
C
                        IF ((STR(I:I).EQ.CHE).OR.(STR(I:I).EQ.CHD).OR.
     &                      (STR(I:I).EQ.CLE).OR.(STR(I:I).EQ.CLD)) THEN
                           MS=I-M1-MS
                           IF (LPOINT) MS=MS-1
                           IF (MS.LE.0) IABT=2
                           IE=I+1
                           IF   ( ( STR(IE:IE).EQ.CPLUS  )
     &                                       .OR.
     &                            ( STR(IE:IE).EQ.CMINUS ) ) IS=1
                           IE=IE+IS
                           LMANT=.FALSE.
                        ELSEIF (LPOINT) THEN
                           IF ((ISTR.LT.ICH0).OR.(ISTR.GT.ICH9)) IABT=2
                        ELSEIF ( STR(I:I).EQ.CPNT ) THEN
                           LPOINT=.TRUE.
                        ELSE
                           IF ((ISTR.LT.ICH0).OR.(ISTR.GT.ICH9)) IABT=2
                        ENDIF
                     ELSE
C
C-----------------------------------------------------------------------
C EXPONENT
C-----------------------------------------------------------------------
C
                        IF ( (ISTR.LT.ICH0).OR.(ISTR.GT.ICH9) ) IABT=2
                     ENDIF
               ENDIF
C
C-----------------------------------------------------------------------
C RETURN ERROR CODE IF ERROR FOUND
C-----------------------------------------------------------------------
C
            IF (IABT.NE.0) RETURN
    3    CONTINUE
C***********************************************************************
C
C-----------------------------------------------------------------------
C IDENTIFY IF EXPONENT IS PRESENT AND IS IN THE VALID RANGE
C-----------------------------------------------------------------------
C
      M2=I-1
         IF (IE.GT.0) THEN
               IF (M2.GE.IE) THEN
                  IE=IE-IS
                  READ(STR(IE:M2),*) IPOW
                     IF     ( IPOW .GT.  IUOFLW ) THEN
                        IABT=9
                     ELSEIF ( IPOW .LT. -IUOFLW ) THEN
                        IABT=10
                     ENDIF
               ELSE
                  IABT=2
               ENDIF
         ENDIF
C
C-----------------------------------------------------------------------
C RETURN ERROR CODE IF ERROR FOUND
C-----------------------------------------------------------------------
C
      IF (IABT.NE.0) RETURN
C
C-----------------------------------------------------------------------
C USE INTERNAL READ TO OBTAIN THE FLOATING POINT NUMBER
C-----------------------------------------------------------------------
C
      READ(STR(M1:M2),*) R8FCTN
C-----------------------------------------------------------------------
      RETURN
      END
