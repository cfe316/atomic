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
CX UNIX PORT - SCCS Info : Module @(#)$Header: /work/dummy/xxdata_15/i4eiz0.for,v 1.3 2004/07/06 14:06:28 whitefor Exp $ Date $Date: 2004/07/06 14:06:28 $
CX
      FUNCTION I4EIZ0 ( ESYM )
      IMPLICIT NONE
C-----------------------------------------------------------------------
C
C *************** FORTRAN77 INTEGER*4 FUNCTION: I4EIZ0 *****************
C
C PURPOSE: TO RETURN THE NUCLEAR CHARGE FOR THE ELEMENT SYMBOL ESYM
C          (INTEGER*4 FUNCTION VERSION OF 'XXEIZ0')
C
C CALLING PROGRAM: GENERAL USE
C
C FUNCTION:
C
C          (I*4)  I4EIZ0  = FUNCTION NAME -
C                           ELEMENT NUCLEAR CHARGE
C          (C*2)  ESYM    = SYMBOL OF ELEMENT WITH NUCLEAR CHARGE I4EIZ0
C
C          (I*4)  NSYM    = PARAMETER = NUMBER OF SYMBOLS LISTED
C
C          (I*4)  I       = GENERAL ARRAY USE
C
C          (C*2)  SYMBOL()= SYMBOLS OF FIRST 'NSYM' ELEMENTS (NORMAL).
C                           ARRAY DIMENSION => NUCLEAR CHARGE
C          (C*2)  SYMBLC()= SYMBOLS OF FIRST 'NSYM' ELEMENTS (L.C.).
C                           ARRAY DIMENSION => NUCLEAR CHARGE
C          (C*2)  SYMBUC()= SYMBOLS OF FIRST 'NSYM' ELEMENTS (U.C.).
C                           ARRAY DIMENSION => NUCLEAR CHARGE
C
C NOTES:    IF SYMBOL IS NOT RECOGNISED, I.E.NOT IN Z0 RANGE 1 & 'NSYM',
C           THEN THE INTEGER 'I4EIZ0' IS RETURNED AS ZERO.
C
C ROUTINES: NONE
C
C
C AUTHOR:   PAUL E. BRIDEN (TESSELLA SUPPORT SERVICES PLC)
C           K1/0/81
C           JET EXT. 4569
C
C DATE:     13/02/91
C
C UPDATE:
C
C VERSION 1.2:  					DATE: 30/01/98  
C MODIFIED: HP SUMMERS 
C		- ALLOWED SEQUENCE SYMBOL TO BE IN  UPPER, LOWER OR MIXED 
C		  CASE.
C VERSION 1.3:  					DATE: 37/09/99  
C MODIFIED: HP SUMMERS 
C		- EXTENDED ELEMENT RANGE TO URANIUM.
C
C-----------------------------------------------------------------------
C-----------------------------------------------------------------------
      INTEGER    I4EIZ0    , NSYM
C-----------------------------------------------------------------------
      PARAMETER( NSYM = 92 )
C-----------------------------------------------------------------------
      INTEGER    I
C-----------------------------------------------------------------------
      CHARACTER  ESYM*2         , SYMBOL(NSYM)*2  , SYMBLC(NSYM)*2
      CHARACTER  SYMBUC(NSYM)*2  
C-----------------------------------------------------------------------
      DATA SYMBOL/'H ','He','Li','Be','B ','C ','N ','O ','F ','Ne',
     &            'Na','Mg','Al','Si','P ','S ','Cl','Ar','K ','Ca',
     &            'Sc','Ti','V ','Cr','Mn','Fe','Co','Ni','Cu','Zn',
     &            'Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y ','Zr',
     &            'Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn',
     &            'Sb','Te','I ','Xe','Cs','Ba','La','Ce','Pr','Nd',
     &            'Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb',
     &            'Lu','Hf','Ta','W ','Re','Os','Ir','Pt','Au','Hg',
     &            'Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th',
     &            'Pa','U '/
      DATA SYMBLC/'h ','he','li','be','b ','c ','n ','o ','f ','ne',
     &            'na','mg','al','si','p ','s ','cl','ar','k ','ca',
     &            'sc','ti','v ','cr','mn','fe','co','ni','cu','zn',
     &            'ga','ge','as','se','br','kr','rb','sr','y ','zr',
     &            'nb','mo','tc','ru','rh','pd','ag','cd','in','sn',
     &            'sb','te','i ','xe','cs','ba','la','ce','pr','nd',
     &            'pm','sm','eu','gd','tb','dy','ho','er','tm','yb',
     &            'lu','hf','ta','w ','re','os','ir','pt','au','hg',
     &            'tl','pb','bi','po','at','rn','fr','ra','ac','th',
     &            'pa','u '/
      DATA SYMBUC/'H ','HE','LI','BE','B ','C ','N ','O ','F ','NE',
     &            'NA','MG','AL','SI','P ','S ','CL','AR','K ','CA',
     &            'SC','TI','V ','CR','MN','FE','CO','NI','CU','ZN',
     &            'GA','GE','AS','SE','BR','KR','RB','SR','Y ','ZR',
     &            'NB','MO','TC','RU','RH','PD','AG','CD','IN','SN',
     &            'SB','TE','I ','XE','CS','BA','LA','CE','PR','ND',
     &            'PM','SM','EU','GD','TB','DY','HO','ER','TM','YB',
     &            'LU','HF','TA','W ','RE','OS','IR','PT','AU','HG',
     &            'TL','PB','BI','PO','AT','RN','FR','RA','AC','TH',
     &            'PA','U '/
C-----------------------------------------------------------------------
      I4EIZ0 = 0
         DO 1 I=1,NSYM
            IF ( (ESYM.EQ.SYMBOL(I)) .OR. (ESYM.EQ.SYMBLC(I)) .OR.
     &           (ESYM.EQ.SYMBUC(I))) THEN
               I4EIZ0 = I
            ENDIF
    1    CONTINUE
C-----------------------------------------------------------------------
      RETURN
      END
