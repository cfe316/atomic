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
CX ULTRIX PORT - SCCS info: Module @(#)$Header: /work/dummy/xxdata_11/i4fctn.for,v 1.4 2007/04/11 13:02:01 allan Exp $ Date $Date: 2007/04/11 13:02:01 $
CX
      FUNCTION I4FCTN( STR , IABT )
      IMPLICIT NONE
C-----------------------------------------------------------------------
C
C  *************** FORTRAN77 INTEGER*4 FUNCTION: I4FCTN ****************
C
C  PURPOSE:  TO CONVERT AN INTEGER NUMBER STORED IN A STRING
C            INTO A INTEGER*4 VARIABLE
C
C  CALLING PROGRAM: GENERAL USE
C
C  FUNCTION:
C
C          (I*4)   I4FCTN  = FUNCTION NAME
C          (C*(*)) STR     = STRING CONTAINING SINGLE FLOATING POINT NO.
C          (I*4)   IABT    = RETURN CODE:
C                               0 => NO ERROR
C                               1 => ERROR (A VALUE 'I4FCTN=0' WILL BE
C                                           RETURNED).
C
C          (C*1)   CH0      = PARAMETER = '0'
C          (C*1)   CH9      = PARAMETER = '9'
C          (C*1)   BLANK    = PARAMETER = ' '
C          (C*1)   CPLUS    = PARAMETER = '+'
C          (C*1)   CMINUS   = PARAMETER = '-'
C
C          (I*4)   ILEN     = LENGTH OF 'STR' STRING IN BYTES
C          (I*4)   ILAST    = POSITION OF LAST BYTE OF IDENTIFIED NUMBER
C          (I*4)   I1       = STARTING BYTE IN 'STR' OF NUMBER
C                             INCLUDING SIGN IF PRESENT
C          (I*4)   IS       = 0 => NUMBER HAS NO SIGN
C                             1 => NUMBER HAS A SIGN
C          (I*4)   ICH0     = ICHAR('0')
C          (I*4)   ICH9     = ICHAR('9')
C          (I*4)   ISTR     = ICHAR(CURRENT BYTE POSITION IN 'STR')
C          (I*4)   I        = GENERAL USE
C
C          (L*4)   LFOUND   = .TRUE.  => ALL OF THE INPUT NUMBER BYTES
C                                        HAVE BEEN ASSESSED.
C                             .FALSE. => INPUT NUMBER BYTES STILL BEING
C                                        ASSESSED.
C          (L*4)   LSTART   = .TRUE.  => THE FIRST DIGIT HAS BEEN FOUND
C                             .FALSE. => THE FIRST DIGIT HAS NOT YET
C                                        BEEN REACHED.
C
C          (C*5)   CFORM5   = FORMAT FOR INTERNAL READING OF INTEGER
C
C
C NOTE:     AN ERROR WILL OCCUR (IABT=1) IF THERE IS MORE THAN ONE
C           NUMBER OCCURING IN THE STRING 'STR()'
C
C
C AUTHOR:   PAUL E. BRIDEN (TESSELLA SUPPORT SERVICES PLC)
C           K1/0/37
C           JET EXT. 2520
C
C DATE:     11/07/90
C
C UPDATE:   11/02/92 - PE BRIDEN: BLANKS NOW ALLOWED BETWEEN SIGN AND
C                                 FIRST DIGIT. LSTART VARIABLE ADDED.
C                                 VARIABLE I2 REMOVED.
C                                 + SOME MINOR RECODING - (IF STRING
C                                 ENTERED IS BLANK IABT IS NOW SET TO 1)
C
C UPDATE:   16/08/93 - PE BRIDEN: CORRECTED BUG TO ALLOW BLANKS BETWEEN
C                                 SIGN AND FIRST DIGIT (SEE ABOVE).
C                                 1) ILAST VARIABLE ADDED.
C                                 2) FORMATTED READ USED INSTEAD OF *
C                                    WHEN CONVERTING IDENTIFIED INTEGER
C                                    USING THE INTERNAL READ. (THIS
C                                    RESTRICTS IDENTIFIED NUMBER TO BE
C                                    < 100 BYTES IN LENGTH!)
C                                 3) EXCLUDE TRAILING BLANKS IN THE
C                                    INTERNAL READING OF THE INTEGER
C                                    I.E. STR(I1:ILAST) INSTEAD OF
C                                         STR(I1:ILEN)
C
C UPDATE:   07/03/95 - PE BRIDEN: INSTEAD OF USING FORMAT SPECIFIER I99
C                                 WHEN INTERNALLY READING THE INTEGER
C                                 CREATE THE APPROPRIATE SPECIFIER
C                                 WITHIN CFORM5 AND USE THIS.
C
C VERSION  : 1.3                          
C DATE     : 20-12-2001
C MODIFIED : Martin O'Mullane
C               - Removed mainframe listing information beyond column 72.
C
C VERSION  : 1.3                          
C DATE     : 10-04-2007
C MODIFIED : Allan Whiteford
C               - Modified documentation as part of automated
C		  subroutine documentation preparation.
C
C-----------------------------------------------------------------------
C
C-----------------------------------------------------------------------
      CHARACTER  CH0*1   , CH9*1   , BLANK*1   , CPLUS*1   , CMINUS*1
C-----------------------------------------------------------------------
      PARAMETER( CH0='0', CH9='9', BLANK=' ', CPLUS='+', CMINUS='-' )
C-----------------------------------------------------------------------
      CHARACTER  STR*(*)
C-----------------------------------------------------------------------
      INTEGER    I4FCTN  , IABT
      INTEGER    I1      , IS      , ILEN      , ILAST     ,
     &           ICH0    , ICH9    , ISTR      , I
C-----------------------------------------------------------------------
      LOGICAL    LSTART  , LFOUND
C-----------------------------------------------------------------------
      CHARACTER  CFORM5*5
C-----------------------------------------------------------------------
      DATA       CFORM5 / '(I??)' /
C-----------------------------------------------------------------------
      SAVE       CFORM5
C-----------------------------------------------------------------------
C
C-----------------------------------------------------------------------
C INITIALIZE VALUES
C-----------------------------------------------------------------------
C
      I4FCTN = 0
      IABT   = 0
      I1     = 0
      IS     = 0
      LSTART = .FALSE.
      LFOUND = .FALSE.
      ICH0   = ICHAR(CH0)
      ICH9   = ICHAR(CH9)
      ILEN   = LEN(STR)
      ILAST  = ILEN
C
C-----------------------------------------------------------------------
C FIND STARTING BYTE OF NUMBER
C-----------------------------------------------------------------------
C
         DO 1 I=1,ILEN
               IF ( STR(I:I).NE.BLANK ) THEN
                  I1 = I
                  GOTO 2
               ENDIF
    1    CONTINUE
C
C-----------------------------------------------------------------------
C IDENTIFY IF NUMBER HAS A SIGN
C-----------------------------------------------------------------------
C
    2    IF (I1.EQ.0) THEN
            IABT = 1
            RETURN
         ENDIF
C
      IF   ( ( STR(I1:I1).EQ.CPLUS  )
     &                  .OR.
     &       ( STR(I1:I1).EQ.CMINUS ) ) IS=1
C
C-----------------------------------------------------------------------
C IDENTIFY IF NUMBER IS OF A VALID FORM
C-----------------------------------------------------------------------
C
         DO 3 I=I1+IS,ILEN

               IF (LFOUND) THEN
C
C-----------------------------------------------------------------------
C INPUT NO. COMPLETELY DEFINED: IDENTIFY IF EXTRA NON-BLANK BYTES EXIST
C-----------------------------------------------------------------------
C
                  IF (STR(I:I).NE.BLANK) IABT=1
C-----------------------------------------------------------------------
               ELSEIF (STR(I:I).EQ.BLANK) THEN
                  LFOUND = LSTART
C-----------------------------------------------------------------------
               ELSE
                  LSTART = .TRUE.
                  ILAST  = I
                  ISTR   = ICHAR(STR(I:I))
                  IF ( (ISTR.LT.ICH0) .OR. (ISTR.GT.ICH9) ) IABT=1
               ENDIF
C
C-----------------------------------------------------------------------
C RETURN ERROR CODE IF ERROR FOUND
C-----------------------------------------------------------------------
C
            IF (IABT.NE.0) RETURN
    3    CONTINUE
C
C-----------------------------------------------------------------------
C IDENTIFY IF VALID NUMBER FOUND (RECODED: PEB 11/02/92)
C                                (RECODED: PEB 07/03/95 - ADDED CFORM5)
C YES => USE INTERNAL READ TO OBTAIN THE INTEGER NUMBER
C NO  => RETURN ERROR CODE IF ERROR FOUND
C-----------------------------------------------------------------------
C
         IF (LSTART) THEN
            I      = 1 + ILAST - I1
            I      = MIN0(I,99)
            WRITE(CFORM5(3:4),'(I2.2)') I
            READ(STR(I1:ILAST),CFORM5) I4FCTN
         ELSE
            IABT=1
         ENDIF
C
C-----------------------------------------------------------------------
C
      RETURN
      END
