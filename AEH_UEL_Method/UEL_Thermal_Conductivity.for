C-----------------------------------------------------------------
C     UEL for asymptotic homogenization method in the case of general static step
C-----------------------------------------------------------------     
      SUBROUTINE UEL(RHS,AMATRX,SVARS,ENERGY,NDOFEL,NRHS,NSVARS,
     1 PROPS,NPROPS,COORDS,MCRD,NNODE,U,DU,V,A,JTYPE,TIME,DTIME,
     2 KSTEP,KINC,JELEM,PARAMS,NDLOAD,JDLTYP,ADLMAG,PREDEF,
     3 NPREDF,LFLAGS,MLVARX,DDLMAG,MDLOAD,PNEWDT,JPROPS,NJPROP,
     4 PERIOD)
C  
      INCLUDE 'aba_param.inc'
C
      DIMENSION RHS(MLVARX,*),AMATRX(NDOFEL,NDOFEL),
     1 SVARS(*),ENERGY(7),PROPS(*),COORDS(MCRD,NNODE),
     2 U(NDOFEL),DU(MLVARX,*),V(NDOFEL),A(NDOFEL),TIME(2),
     3 PARAMS(*),JDLTYP(MDLOAD,*),ADLMAG(MDLOAD,*),
     4 DDLMAG(MDLOAD,*),PREDEF(2,NPREDF,NNODE),LFLAGS(4),
     5 JPROPS(*)
C
C-----------------------------------------------------------------
C     DEFINE  PARAMETERS AND M     
C-----------------------------------------------------------------   
      PARAMETER (EIGHTH=0.125D0, QUART=0.25D0, HALF=0.5D0, 
     1 ZERO=0.D0, ONE=1.D0, TWO=2.D0)  
      DIMENSION EMATRX(3),TMATRX(3)    
      DIMENSION GAUSS(3)                          ! GAUSS point, WEGT
      DIMENSION BN(3,NNODE)                       ! Matrix N 
      DIMENSION BJ(3,3), BL(3,NNODE), BR(3,3)     ! Matrix Jacobian, DNDX and inverse Jacobian
      DIMENSION B(3,NDOFEL), BT(NDOFEL,3)         ! Matrix B and its transport 
      DIMENSION D(3,3), S(3,NDOFEL)               ! Elastic Matrix D and S = D*B
      DIMENSION SSTRAIN(3), SSTRESS(3)            ! Stress and Strain
      INTEGER   IGAUSS, JTYPE, ISTEP, KSTEP       ! TO RECORD THE GUASS POINT ORDER AND THE LOADING TYPE
      INTEGER   KINC, JELEM     
C-----------------------------------------------------------------	
C     Loading case 1                             
C-----------------------------------------------------------------  
      ISTEP=1.D0
C-----------------------------------------------------------------	
C     Elastic Matrix D                             
C-----------------------------------------------------------------   
      IF (LFLAGS(1).EQ.31) THEN
C
      DO K1=1,3   
        EMATRX(K1)=ZERO 
        TMATRX(K1)=ZERO 
      ENDDO
C
      DO I=1,3
        DO J=1,3
          D(I,J)=ZERO
        END DO 
      END DO
C     
      IF (JTYPE==5) THEN 
	  D(1,1)=PROPS(1)
	  D(1,2)=PROPS(2)
	  D(2,2)=PROPS(3)
	  D(1,3)=PROPS(4)
	  D(2,3)=PROPS(5)
	  D(3,3)=PROPS(6)
	  D(2,1)=D(1,2)
	  D(3,1)=D(1,3)
	  D(3,2)=D(2,3)
      ELSE  
	  D(1,1)=PROPS(1)
	  D(2,2)=PROPS(2)
	  D(3,3)=PROPS(3)
      END IF
C-----------------------------------------------------------------
C     INITAIL RHS, AMATRX
C-----------------------------------------------------------------
      DO K1=1,NDOFEL
        DO KRHS=1,NRHS
          RHS(K1,KRHS)=ZERO   
        ENDDO
        DO K2=1,NDOFEL
          AMATRX(K1,K2)=ZERO
        ENDDO
      ENDDO
C-----------------------------------------------------------------
C     INITAIL GAUSS point
C-----------------------------------------------------------------
      GAUSS(1)=QUART
      GAUSS(2)=QUART
      GAUSS(3)=QUART
      WEGT=1.0D0/6
C        
      IGAUSS=ZERO 
      DO Kintk=1,1
        X=GAUSS(1)       
        Y=GAUSS(2)        
        Z=GAUSS(3)  
        IGAUSS=IGAUSS+1          
C-----------------------------------------------------------------	
C     Matrix B in the local coordiante system                                
C-----------------------------------------------------------------          
        BN(1,1)=ONE 
        BN(1,2)=ZERO
        BN(1,3)=-ONE
        BN(1,4)=ZERO
C
        BN(2,1)=ZERO
        BN(2,2)=ONE
        BN(2,3)=-ONE
        BN(2,4)=ZERO
C
        BN(3,1)=ZERO
        BN(3,2)=ZERO
        BN(3,3)=-ONE
        BN(3,4)=ONE    
C-----------------------------------------------------------------	
C     Matrix Jacobian                              
C-----------------------------------------------------------------                 
        DO I=1,3
          DO K=1,3
            BJ(I,K)=ZERO
          ENDDO
        ENDDO
C
        DO J=1,4
          BJ(1,1)=BJ(1,1)+BN(1,J)*COORDS(1,J)
          BJ(1,2)=BJ(1,2)+BN(1,J)*COORDS(2,J)
          BJ(1,3)=BJ(1,3)+BN(1,J)*COORDS(3,J)
          BJ(2,1)=BJ(2,1)+BN(2,J)*COORDS(1,J)
          BJ(2,2)=BJ(2,2)+BN(2,J)*COORDS(2,J)
          BJ(2,3)=BJ(2,3)+BN(2,J)*COORDS(3,J)
          BJ(3,1)=BJ(3,1)+BN(3,J)*COORDS(1,J)
          BJ(3,2)=BJ(3,2)+BN(3,J)*COORDS(2,J)
          BJ(3,3)=BJ(3,3)+BN(3,J)*COORDS(3,J)
        ENDDO	
C-----------------------------------------------------------------	
C     Matrix Inverse Jacobian BR                         
C-----------------------------------------------------------------  	
        DO I=1,3
          DO K=1,3
            BR(I,K)=ZERO
          ENDDO
        ENDDO
C      
        BH=BJ(1,1)*BJ(2,2)*BJ(3,3)+BJ(1,2)*BJ(2,3)*BJ(3,1)+
     1   BJ(1,3)*BJ(3,2)*BJ(2,1)-BJ(1,1)*BJ(3,2)*BJ(2,3)-
     2   BJ(1,2)*BJ(2,1)*BJ(3,3)-BJ(1,3)*BJ(2,2)*BJ(3,1)    ! 雅克比行列式值
C     
        BR(1,1)= (BJ(2,2)*BJ(3,3)-BJ(2,3)*BJ(3,2))/BH
        BR(1,2)=-(BJ(1,2)*BJ(3,3)-BJ(1,3)*BJ(3,2))/BH
        BR(1,3)= (BJ(1,2)*BJ(2,3)-BJ(1,3)*BJ(2,2))/BH
        BR(2,1)=-(BJ(2,1)*BJ(3,3)-BJ(2,3)*BJ(3,1))/BH
        BR(2,2)= (BJ(1,1)*BJ(3,3)-BJ(1,3)*BJ(3,1))/BH
        BR(2,3)=-(BJ(1,1)*BJ(2,3)-BJ(1,3)*BJ(2,1))/BH
        BR(3,1)= (BJ(2,1)*BJ(3,2)-BJ(2,2)*BJ(3,1))/BH
        BR(3,2)=-(BJ(1,1)*BJ(3,2)-BJ(1,2)*BJ(3,1))/BH
        BR(3,3)= (BJ(1,1)*BJ(2,2)-BJ(1,2)*BJ(2,1))/BH   
C-----------------------------------------------------------------	
C     GVOL = Velement*GUASSWEIGHT                             
C-----------------------------------------------------------------         
        GVOL=BH*WEGT
        EVOL=BH*ONE
C-----------------------------------------------------------------	
C     Matrix B                              
C----------------------------------------------------------------- 
        DO I=1,3
          DO K=1,NNODE
            B(I,K)=ZERO
          ENDDO
        ENDDO
C
        DO I=1,3
          DO J=1,NNODE
            DO K=1,3
              B(I,J)=B(I,J)+BR(I,K)*BN(K,J)
            ENDDO
          ENDDO
        ENDDO      
C
        DO K1=1,NDOFEL
          DO K2=1,3
            BT(K1,K2)=B(K2,K1)
          ENDDO
        ENDDO
C-----------------------------------------------------------------	
C     Elastic Matrix S = D*B                            
C----------------------------------------------------------------- 
        DO I=1,3
          DO K=1,NDOFEL
            S(I,K)=ZERO
          ENDDO
        ENDDO
      
        DO I=1,3
          DO K=1,NDOFEL
            DO J=1,3
              S(I,K)=S(I,K)+D(I,J)*B(J,K)
            ENDDO
          ENDDO
        ENDDO           	
C-----------------------------------------------------------------	
C     Stress (equivalent heat flux) and Strain (equivalent temperature gradient)                      
C----------------------------------------------------------------- 	
        DO I=1,3
          SSTRAIN(I)=ZERO
          SSTRESS(I)=ZERO
        ENDDO
C      
        DO I=1,3
          DO J=1,NDOFEL
            SSTRAIN(I)=SSTRAIN(I)+B(I,J)*U(J)
          ENDDO
        ENDDO
C      
        DO I=1,3
          DO J=1,3
            SSTRESS(I)=SSTRESS(I)+D(I,J)*SSTRAIN(J)
          ENDDO
        ENDDO
C      
        DO I=1,3
          SVARS(I)=SSTRAIN(I)
          SVARS(I+3)=SSTRESS(I)
        ENDDO   
        SVARS(7)=EVOL
        SVARS(8)=GVOL
C-----------------------------------------------------------------	
C     RHS and Amatrix     ! +BT(K1,K2)*D(K2,IColumn)*WEGT*BH                    
C-----------------------------------------------------------------
        DO K1=1,NDOFEL
          DO K2=1,3
            RHS(K1,1)=RHS(K1,1)-BT(K1,K2)*SSTRESS(K2)*WEGT*BH
     1       +BT(K1,K2)*D(K2,KSTEP)*WEGT*BH  
          ENDDO
C          
          DO K2=1,NDOFEL
            DO KK=1,3
              AMATRX(K1,K2)=AMATRX(K1,K2)+BT(K1,KK)*S(KK,K2)*WEGT*BH
            ENDDO
          ENDDO
        ENDDO
C-----------------------------------------------------------------	
C     Output equivalent thermal conductivity of gauss point
C-----------------------------------------------------------------        
        DO K1=1,3   
          DO K2=1,3
            TMATRX(K1)=TMATRX(K1)+D(K1,K2)*SSTRAIN(K2)
          ENDDO
        ENDDO
C
        DO K1=1,3   
          EMATRX(K1)=(D(K1,KSTEP)-TMATRX(K1))*WEGT*BH
        ENDDO
C      
        SVARS(9:11)=EMATRX
C      
        WRITE(6,*) JELEM, EMATRX(1:3) 
C      
      ENDDO	

C
      ENDIF
      
C-----------------------------------------------------------------	
C     Output data into a file                 
C-----------------------------------------------------------------         
C        OPEN(10, FILE='C:\Temp\ElasMatrx.txt', status='old',action='write',
C     1        position="append")  
C        WRITE(10,*) JELEM, EMATRX(1:6) 
C        CLOSE(10) 
C-----------------------------------------------------------------                                                               
      RETURN
      END

