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
      subroutine xxcase(input,output,type)

      IMPLICIT NONE

C-----------------------------------------------------------------------
C
C  ****************** FORTRAN77 SUBROUTINE: XXCASE *********************
C
C  PURPOSE: Change a string of arbitrary size into all upper case
C           or all lower case
C
C  CALLING PROGRAM: GENERAL USE.
C
C  INPUT    : (C*(*)) INPUT = Input String
C  INPUT    : (C*2)   TYPE = Type of case to convert to:
C                       'UC' -> Convert to Upper Case
C                       'LC' -> Convert to Lower Case
C                       Anything else -> No conversion
C
C  OUTPUT   : (C*(*)) OUTPUT = Output string in selected case
C
C  ROUTINES : NONE
C
C  AUTHOR   : Allan Whiteford,
C             University of Strathclyde
C
C  VERSION  : 1.1                          
C  DATE     : 05/09/2001
C  MODIFIED : Allan Whiteford
C             First version.
C
C  VERSION  : 1.2                          
C  DATE     : 05/05/2005
C  MODIFIED : Martin O'Mullane
C             The routine converted length-1 rather than the whole
C             input string.
C
C-----------------------------------------------------------------------
       integer i
       integer size
C----------------------------------------------------------------------
       character*(*) input
       character*(*) output
       character*2 type
C----------------------------------------------------------------------

       size=len(input)

       write(output(1:size),'(A)') input(1:size)
       i=1

       if (type.eq.'UC' .or. type.eq.'uc') then
10        if    ( ichar(input(i:i)) .ge. ichar('a')
     &    .and.   ichar(input(i:i)) .le. ichar('z')
     &          ) output(i:i)=char(ichar(input(i:i))+ichar('A')
     &                                              -ichar('a'))

          i=i+1
          if (i .le. size) goto 10
       endif

       if (type.eq.'LC' .or. type.eq.'lc') then
20        if    ( ichar(input(i:i)) .ge. ichar('A')
     &    .and.   ichar(input(i:i)) .le. ichar('Z')
     &          ) output(i:i)=char(ichar(input(i:i))+ichar('a')
     &                                              -ichar('A'))

          i=i+1
          if (i .le. size) goto 20
       endif

       end
