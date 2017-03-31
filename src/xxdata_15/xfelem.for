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
CX UNIX PORT - SCCS Info : Module @(#)$Header: /work/dummy/xxdata_15/xfelem.for,v 1.2 2004/07/06 15:30:02 whitefor Exp $ Date $Date: 2004/07/06 15:30:02 $
CX
      FUNCTION XFELEM ( IZ0 )
      IMPLICIT NONE
C-----------------------------------------------------------------------
C
C ************* FORTRAN77 CHARACTER*12 FUNCTION: XFELEM ****************
C
C PURPOSE: TO RETURN THE NAME OF THE ELEMENT WITH NUCLEAR CHARGE IZ0
C          (CHARACTER*12 FUNCTION VERSION OF 'XXELEM')
C
C CALLING PROGRAM: GENERAL USE
C
C FUNCTION:
C
C          (C*12) XFELEM  = FUNCTION NAME -
C                           NAME OF ELEMENT WITH NUCLEAR CHARGE 'IZ0'
C          (I*4)  IZ0     = ELEMENT NUCLEAR CHARGE
C
C          (C*12) NAMES() = NAMES OF FIRST 50 ELEMENTS.
C                           ARRAY DIMENSION => NUCLEAR CHARGE
C
C NOTES:    IF NUCLEAR CHARGE IS OUT OF RANGE, I.E.NOT BETWEEN 1 & 50,
C           THEN THE CHARACTER STRING 'XFELEM' IS RETURNED BLANK.
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
C VERSION: 1.2
C UPDATE:   17/09/99  HUGH SUMMERS - INCREASED ELEMENT NUMBER TO 92
C
C-----------------------------------------------------------------------
C-----------------------------------------------------------------------
      INTEGER      IZ0
C-----------------------------------------------------------------------
      CHARACTER*12 XFELEM , NAMES(92)
C-----------------------------------------------------------------------
      DATA NAMES/'HYDROGEN    ','HELIUM      ','LITHIUM     ',
     &           'BERYLLIUM   ','BORON       ','CARBON      ',
     &           'NITROGEN    ','OXYGEN      ','FLUORINE    ',
     &           'NEON        ','SODIUM      ','MAGNESIUM   ',
     &           'ALUMINIUM   ','SILICON     ','PHOSPHORUS  ',
     &           'SULPHUR     ','CHLORINE    ','ARGON       ',
     &           'POTASSIUM   ','CALCIUM     ','SCANDIUM    ',
     &           'TITANIUM    ','VANADIUM    ','CHROMIUM    ',
     &           'MANGANESE   ','IRON        ','COBALT      ',
     &           'NICKEL      ','COPPER      ','ZINC        ',
     &           'GALLIUM     ','GERMANIUM   ','ARSENIC     ',
     &           'SELENIUM    ','BROMINE     ','KRYPTON     ',
     &           'RUBIDIUM    ','STRONTIUM   ','YTTRIUM     ',
     &           'ZIRCONIUM   ','NIOBIUM     ','MOLYBDENUM  ',
     &           'TECHNETIUM  ','RUTHENIUM   ','RHODIUM     ',
     &           'PALLADIUM   ','SILVER      ','CADMIUM     ',
     &           'INDIUM      ','TIN         ','ANTIMONY    ',
     &           'TELLURIUM   ','IODINE      ','XENON       ',
     &           'CESIUM      ','BARIUM      ','LANTHANUM   ',
     &           'CERIUM      ','PRAESODYMIUM','NEODYMIUM   ',
     &           'PROMETHIUM  ','SAMARIUM    ','EUROPIUM    ',
     &           'GADOLINIUM  ','TERBIUM     ','DYSPROSIUM  ',
     &           'HOLMIUM     ','ERBIUM      ','THULIUM     ',
     &           'YTTERBIUM   ','LUTETIUM    ','HAFNIUM     ',
     &           'TANTALUM    ','TUNGSTEN    ','RHENIUM     ',
     &           'OSMIUM      ','IRIDIUM     ','PLATINUM    ',
     &           'GOLD        ','MERCURY     ','THALLIUM    ',
     &           'LEAD        ','BISMUTH     ','POLONIUM    ',
     &           'ASTATINE    ','RADON       ','FRANCIUM    ',
     &           'RADIUM      ','ACTINIUM    ','THORIUM     ',
     &           'PROTACTINIUM','URANIUM     '/
C-----------------------------------------------------------------------
         IF ( (IZ0.GT.92).OR.(IZ0.LT.0) ) THEN
            XFELEM = ' '
         ELSE
            XFELEM = NAMES(IZ0)
         ENDIF
C-----------------------------------------------------------------------
      RETURN
      END
