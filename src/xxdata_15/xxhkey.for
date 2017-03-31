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
      SUBROUTINE XXHKEY( CTEXT  , CKEY , CBREAK , CANS )
      IMPLICIT NONE
C-----------------------------------------------------------------------
C
C  ****************** FORTRAN77 SUBROUTINE: XXHKEY *********************
C
C  PURPOSE: TO EXTRACT FROM A LINE OF TEXT 'CTEXT' A RESPONSE TO A KEY
C           IN THER FORM OF '<CKEY> = <CANS>'.
C
C  CALLING PROGRAM: GENERAL USE
C
C  SUBROUTINE:
C
C  INPUT : (C*(*)) CTEXT   = INPUT TEXT LINE CONTAINING KEY & RESPONSES
C  INPUT : (C*(*)) CKEY    = KEY TEXT
C  INPUT : (C*1  ) CBREAK  = KEY/RESPONSE PAIR SEPERATOR SYMBOL
C
C  OUTPUT: (C*(*)) CANS    = RERSPONSE FOR GIVEN KEY: BLANK IF NOT FOUND
C
C          (I*4)   LENTXT  = LENGTH IN BYTES OF 'CTEXT' STRING
C          (I*4)   LENKEY  = LENGTH IN BYTES OF 'CKEY' STRING
C          (I*4)   LENANS  = LENGTH IN BYTES OF 'CANS' STRING
C          (I*4)   IKEY    = LENGTH IN BYTES OF 'CKEY' IGNORING TRAILING
C                            BLANKS
C          (I*4)   IPOS1   = USED IN IDENTIFYING RELEVANT BYTES IN CTEXT
C          (I*4)   IPOS2   = USED IN IDENTIFYING RELEVANT BYTES IN CTEXT
C          (I*4)   IPOS3   = USED IN IDENTIFYING RELEVANT BYTES IN CTEXT
C          (I*4)   I       = GENERAL USE INDEX
C
C ROUTINES: NONE
C
C NOTES:    THIS ROUTINE EXTRACTS FROM 'CTEXT' A RESPONSE TO A GIVEN KEY
C           IN THER FORM OF '<CKEY> = <CANS>'. E.G. 'FILE = DSN001'
C           WOULD REQUIRE AS INPUT CKEY='FILE' AND WOULD GIVE AS OUTPUT
C           CANS='DSN001'. ALL KEY/RESPONSE PAIRS MUST BE SEPARATED BY
C           THE CHARACTER GIVEN BY 'CBREAK' E.G. A SLASH, AND EACH KEY
C           MUST BE FOLLOWED BY AN EQUALS SIGN. THE NUMBER OF SPACES
C           BETWEEN THE KEY AND THE EQUAL SIGN AND BETWEEN THE RESPONSE
C           AND THE EQUAL SIGN IS NOT IMPORTANT.
C
C           THE BYTE PRECEEDING THE KEY MUST BE A BLANK OR 'CBREAK'
C           CHARACTER UNLESS IT STARTS AT BYTE ONE IN 'CTEXT'.
C
C           IF A KEY DOES NOT EXIST IN 'CTEXT' THEN 'CANS' IS RETURNED
C           BLANK.
C
C           THE KEY IS TAKEN AS 'CKEY' REMOVING ANY TRAILING BLANKS.
C           LEADING BLANKS ARE LEFT IN PLACE AND WILL USED WHEN THE
C           THE SEARCH FOR THE KEY IS MADE:
C
C           I.E.  'DATA   ' AND 'DATA' ARE THE SAME KEY BUT
C                 ' DATA '  AND 'DATA ' ARE DIFFERENT KEYS ALTHOUGH
C                 BOTH WILL GIVE THE SAME RESULTS IF A SPACE EXISTS
C                 BEFORE 'DATA' IN THE INPUT TEXT LINE.
C
C           AN EXAMPLE OF AN INPUT TEXT LINE IS:
C
C           8524.0 A    5 7 /FILMEM = FBBH91BE/   CODE=   V2B DLN1   /
C
C           THIS WOULD GIVE THE FOLLOWING:
C
C           CKEY='FILMEM'  =>  CANS='FBBH91BE'
C           CKEY=' FILMEM' =>  CANS=' '
C           CKEY='CODE'    =>  CANS='V2B DLN1'
C           CKEY=' CODE'   =>  CANS='V2B DLN1'
C           CKEY='OTHER'   =>  CANS=' '
C
C           (IF THE CHARACTER STRING IS SHORTER THAN THE RESPONSE THEN
C            THE RESPONSE IS TRUNCATED ACCORDINGLY.)
C
C           SPACES CAN EXIST IN THE KEY. I.E. CKEY='PLOT A'. BUT CARE
C           SHOULD BE TAKEN WHEN USING PREFIXES ON A COMMON KEY BASE,
C           I.E. 'A PLOT', 'B PLOT'. THIS IS BECAUSE IF A SUBSEQUENT
C           KEY TO BE FOUND IS 'PLOT' THEN  EITHER OF THESE SATISFY
C           THIS CRITERION AS WELL AS 'PLOT' ITSELF.
C
C           AN EXAMPLE OF AN INPUT TEXT LINE IS:
C
C           A FILE=TEST0/B FILE = TEST1/FILE=TEST2/FILE 1=TEST3/FILE 2=/
C
C           THIS WOULD GIVE THE FOLLOWING:
C
C           CKEY='A FILE'  =>  CANS='TEST0'
C           CKEY='B FILE'  =>  CANS='TEST1'
C           CKEY='FILE'    =>  CANS='TEST0' (WRONG RESPONSE PICKED UP)
C           CKEY='FILE 1'  =>  CANS='TEST3'
C           CKEY='FILE 2'  =>  CANS='TEST4'
C
C           IT IS ALSO POSSIBLE TO IMBED RESPONSES
C
C           AN EXAMPLE OF AN INPUT TEXT LINE IS:
C
C           FILE 1 =  Z1 = 23 / FILE = FILE 1 = 6 /
C
C           THIS WOULD GIVE THE FOLLOWING:
C
C           CKEY='FILE 1'  =>  CANS='Z1 = 23'
C           CKEY=' FILE 1' =>  CANS='6'
C           CKEY='Z1'      =>  CANS='23'
C           CKEY='FILE'    =>  CANS='FILE 1 = 6'
C
C AUTHOR:  PAUL E. BRIDEN (TESSELLA SUPPORT SERVICES PLC)
C          K1/0/37
C          JET EXT. 2520
C
C DATE:    26/04/91
C
C VERSION  : 1.2                          
C DATE     : 31-05-2007
C MODIFIED : H P Summers
C              - Increased robustness for single letter keys occurring
C                elsewhere at non-key positions in strings.
C
C-----------------------------------------------------------------------
      INTEGER    LENTXT      , LENKEY      , LENANS      ,
     &           IPOS1       , IPOS2       , IPOS3       ,
     &           IKEY        , I
C-----------------------------------------------------------------------
      CHARACTER  CTEXT*(*)   , CKEY*(*)    , CBREAK*1    , CANS*(*)
C-----------------------------------------------------------------------
C
C-----------------------------------------------------------------------
C
      LENTXT = LEN(CTEXT)
      LENKEY = LEN(CKEY)
      LENANS = LEN(CANS)
C
C-----------------------------------------------------------------------
C FIND THE LENGTH OF THE KEY IGNORING ANY TRAILING BLANKS
C-----------------------------------------------------------------------
C
      IKEY   = 0
C
         DO 1 I = 1,LENKEY
            IF (CKEY(I:I).NE.' ') IKEY = I
    1    CONTINUE
    
c         write(i4unit(-1),*)'xxhkey: ikey=',ikey
    
C
      IF (IKEY.EQ.0) GOTO 999
C
C-----------------------------------------------------------------------
C ESTABLISH IF A VALID KEY CAN BE FOUND IN 'CTEXT'
C-----------------------------------------------------------------------
C
      IPOS1 = 1
  100 IPOS1 = INDEX( CTEXT(IPOS1:LENTXT) , CKEY(1:IKEY) ) + IPOS1 - 1
      IPOS2 = IPOS1 + IKEY
C
	 
         IF (IPOS2.GT.LENTXT) THEN
            GOTO 999
         ELSEIF (IPOS1.EQ.1) THEN
            IPOS1 = IPOS2
         ELSEIF (IPOS1.NE.0) THEN
            IPOS1 = IPOS1 - 1
               IF ( (CTEXT(IPOS1:IPOS1).EQ.' '   )
     &                       .OR.
     &              (CTEXT(IPOS1:IPOS1).EQ.CBREAK) ) THEN
                  IPOS1 = IPOS2
               ELSE
c                  GOTO 999
                  ipos1=ipos2
	    	  if(index(ctext(ipos1:lentxt),ckey(1:ikey)).ne.0)then
	    	      go to 100
	    	  else  				      
	    	      go to 999
	    	  endif
               ENDIF
         ELSE
            GOTO 999
         ENDIF
	 if((ctext(ipos2:ipos2).ne.' ')	  	
     &   	       .and.			  	
     &   	( ctext(ipos2:ipos2).ne.'=')) then	
            ipos1=ipos2
	    if(index(ctext(ipos1:lentxt),ckey(1:ikey)).ne.0)then
	        go to 100
	    else				  	
	        go to 999
	    endif
	 endif    
C
C-----------------------------------------------------------------------
C ESTABLISH IF EQUAL SIGN EXISTS AFTER THE KEY (SEPERATED BY BLANKS).
C-----------------------------------------------------------------------
C
      IPOS2 = INDEX( CTEXT(IPOS1:LENTXT) , '=' )
      IPOS3 = IPOS2 + IPOS1
      
C
         IF (IPOS3.GT.LENTXT) THEN
            GOTO 999
         ELSEIF (IPOS2.EQ.1) THEN
            IPOS2 = IPOS3
         ELSEIF (IPOS2.NE.0) THEN
            IPOS2 = IPOS3 - 2
               IF (CTEXT(IPOS1:IPOS2).EQ.' ') THEN
                  IPOS2 = IPOS3
               ELSE
C
C- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C SEE IF VALID KEY EXISTS FURTHER DOWN THE 'CTEXT' STRING.
C- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
C
                  GOTO 100
               ENDIF
         ELSE
            GOTO 999
         ENDIF
C
C-----------------------------------------------------------------------
C FIND SEPERATOR CHARACTER AND IDENTIFY RESPONSE (IF PRESENT).
C-----------------------------------------------------------------------
C
      IPOS1 = 0
      IPOS3 = INDEX( CTEXT(IPOS2:LENTXT) , CBREAK )
C
     
         IF     (IPOS3.EQ.0) THEN
            IPOS3 = LENTXT
         ELSEIF (IPOS3.EQ.1) THEN
            GOTO 999
         ELSE
            IPOS3 = IPOS3 + IPOS2 - 2
         ENDIF
C
         DO 3 I = IPOS2,IPOS3
            IF ( ( IPOS1.EQ.0 ) .AND. ( CTEXT(I:I).NE.' ' ) ) IPOS1 = I
            if ( ( ipos1.ne.0 ) .and. ( ctext(i:i).eq.' ' ) ) then
	        ipos3 = i
		go to 4
	    endif	
    3    CONTINUE
C
c         IF (IPOS1.EQ.0) THEN
    4    IF (IPOS1.EQ.0) THEN
            GOTO 999
         ELSEIF ( (IPOS3-IPOS1+1).GT.LENANS ) THEN
            IPOS3 = IPOS1 + LENANS - 1
         ENDIF
C
C-----------------------------------------------------------------------
C VALID RESPONSE FOUND - SET UP 'CANS'
C-----------------------------------------------------------------------
C
      CANS = CTEXT(IPOS1:IPOS3)
      RETURN
C
C-----------------------------------------------------------------------
C INVALID OR NO RESPONSE/KEY FOUND - RETURN 'CANS' AS BLANK
C-----------------------------------------------------------------------
C
  999 CANS = ' '
      RETURN
C
C-----------------------------------------------------------------------
C
      END
