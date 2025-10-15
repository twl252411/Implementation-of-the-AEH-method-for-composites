Code by Zheng Yuan
C======================================================================
      SUBROUTINE UEXPAN(EXPAN,DEXPANDT,TEMP,TIME,DTIME,PREDEF,DPRED,
     1     STATEV,CMNAME,NSTATV,NOEL)
C======================================================================
C	  The UEXPAN subroutine for defining the thermal expansion
C
C	  The major variables passed in:
C		TEMP(1) - Current temperature
C		TEMP(2) - Temperature increment
C
C	  The major variables to be defined:
C		EXPAN - Increments of thermal strain
C
      INCLUDE 'ABA_PARAM.INC'
C
      CHARACTER*80 CMNAME
      DIMENSION EXPAN(*),DEXPANDT(*),TEMP(2),TIME(2),PREDEF(*),
     1     DPRED(*),STATEV(NSTATV)
C
C	  Local variables (thermal expansion coefficients)
	  DIMENSION ALPHA(6)
C
C	  Initialized
	  ALPHA = 0.D0
C	
C	  TEMP(2)=(0.1 - 0.6), six modes for preprocessing
	  IF (ABS(TEMP(2)-1.D0) < 1E-3) THEN
		ALPHA(1) = 1.D0/TEMP(2)
      END IF
	  IF (ABS(TEMP(2)-2.D0) < 1E-3) THEN
		ALPHA(2) = 1.D0/TEMP(2)
      END IF
	  IF (ABS(TEMP(2)-3.D0) < 1E-3) THEN
		ALPHA(3) = 1.D0/TEMP(2)
      END IF
	  IF (ABS(TEMP(2)-4.D0) < 1E-3) THEN
		ALPHA(4) = 1.D0/TEMP(2)
      END IF
	  IF (ABS(TEMP(2)-5.D0) < 1E-3) THEN
		ALPHA(5) = 1.D0/TEMP(2)
      END IF
	  IF (ABS(TEMP(2)-6.D0) < 1E-3) THEN
		ALPHA(6) = 1.D0/TEMP(2)
	  END IF
C
C	  Compute increments of thermal strain
	  DO I = 1,6
		EXPAN(I) = ALPHA(I)*TEMP(2)
      END DO
C      WRITE(*,*) EXPAN(1),EXPAN(2),EXPAN(3),EXPAN(4),EXPAN(5),EXPAN(6)
C      WRITE(*,*) "EXPAN"
C
      RETURN
      END