C-----------------------------------------------------------------
C     UEL for asymptotic homogenization method in the case of general static step
C-----------------------------------------------------------------     
      SUBROUTINE UEL(RHS,AMATRX,SVARS,ENERGY,NDOFEL,NRHS,NSVARS,
     1 PROPS,NPROPS,COORDS,MCRD,NNODE,U,DU,V,A,JTYPE,TIME,DTIME,
     2 KSTEP,KINC,JELEM,PARAMS,NDLOAD,JDLTYP,ADLMAG,PREDEF,
     3 NPREDF,LFLAGS,MLVARX,DDLMAG,MDLOAD,PNEWDT,JPROPS,NJPROP,
     4 PERIOD)
C  
      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
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
      PARAMETER (EIGHTH=0.125D0, QUART=0.25D0, HALF=0.5D0, ZERO=0.D0,
     1 ONE=1.D0, TWO=2.D0)  
      DIMENSION EMATRX(6),TE(6), TM(6)            ! TE Thermal Expansion
      DIMENSION GAUSS(3)                          ! GAUSS point, WEGT
      DIMENSION BN(3,NNODE)                       ! Matrix N 
      DIMENSION BJ(3,3), BL(3,NNODE), BR(3,3)     ! Matrix Jacobian, DNDX and inverse Jacobian
      DIMENSION B(6,NDOFEL), BT(NDOFEL,6)         ! Matrix B and its transport 
      DIMENSION D(6,6), S(6,NDOFEL)               ! Elastic Matrix D and S = D*B
      DIMENSION SSTRAIN(6), SSTRESS(6)            ! Stress and Strain
      INTEGER IGAUSS, JTYPE, KSTEP                ! TO RECORD THE GUASS POINT ORDER AND THE LOADING TYPE
      INTEGER KINC,JELEM     
C-----------------------------------------------------------------        
      DO K1=1,6   
        EMATRX(K1)=ZERO 
        TE(K1)=ZERO
        TM(K1)=ZERO
      ENDDO
C-----------------------------------------------------------------	
C     Elastic Matrix D                             
C-----------------------------------------------------------------   
      DO I=1,6
        DO J=1,6
          D(I,J)=ZERO
        END DO 
      END DO
C                
      IF (JTYPE==3) THEN
        EMOD1=PROPS(1)
        EMOD2=PROPS(2)
        EMOD3=PROPS(2)    
        EG12=PROPS(3)
        EG13=PROPS(3)
        EG23=PROPS(4)
        ENU12=PROPS(5)
        ENU13=PROPS(5)
        VOLUME=PROPS(8)
        ENU23=0.5*EMOD2/EG23-1
        ENU21=ENU12*EMOD2/EMOD1
        ENU31=ENU13*EMOD3/EMOD1
        ENU32=ENU23*EMOD3/EMOD2
C
        TE(1)=PROPS(6)
        TE(2)=PROPS(7)
        TE(3)=PROPS(7)
C
        DELTA=1/(1-ENU12*ENU21-ENU23*ENU32-ENU31*ENU13-2*ENU21
     1        *ENU32*ENU13)
        D(1,1)=EMOD1*(1-ENU23*ENU32)*DELTA
        D(2,2)=EMOD2*(1-ENU13*ENU31)*DELTA
        D(3,3)=EMOD3*(1-ENU12*ENU21)*DELTA
        D(1,2)=EMOD1*(ENU21+ENU31*ENU23)*DELTA
        D(1,3)=EMOD1*(ENU31+ENU21*ENU32)*DELTA
        D(2,3)=EMOD2*(ENU32+ENU12*ENU31)*DELTA
        D(2,1)=D(1,2)
        D(3,1)=D(1,3)
        D(3,2)=D(2,3)
        D(4,4)=EG12
        D(5,5)=EG13
        D(6,6)=EG23 

      ELSEIF  (JTYPE==5)  THEN
          
        VOLUME=PROPS(28)
        
        TE(1)=PROPS(22)
        TE(2)=PROPS(23)
        TE(3)=PROPS(24)
	  TE(4)=PROPS(25)
        TE(5)=PROPS(26)
        TE(6)=PROPS(27)

        D(1,1)=PROPS(1)
	  D(1,2)=PROPS(2)
	  D(2,1)=PROPS(2)
        D(2,2)=PROPS(3)
	  D(1,3)=PROPS(4)
	  D(3,1)=PROPS(4)
        D(2,3)=PROPS(5)
	  D(3,2)=PROPS(5)
        D(3,3)=PROPS(6)
	  D(1,4)=PROPS(7)
	  D(4,1)=PROPS(7)
	  D(2,4)=PROPS(8)
	  D(4,2)=PROPS(8)
	  D(3,4)=PROPS(9)
	  D(4,3)=PROPS(9)
	  D(4,4)=PROPS(10)
	  D(1,5)=PROPS(11)
	  D(5,1)=PROPS(11)
	  D(2,5)=PROPS(12)
	  D(5,2)=PROPS(12)
	  D(3,5)=PROPS(13)
	  D(5,3)=PROPS(13)
	  D(4,5)=PROPS(14)
	  D(5,4)=PROPS(14)
	  D(5,5)=PROPS(15)
	  D(1,6)=PROPS(16)
	  D(6,1)=PROPS(16)
	  D(2,6)=PROPS(17)
	  D(6,2)=PROPS(17)
	  D(3,6)=PROPS(18)
	  D(6,3)=PROPS(18)
	  D(4,6)=PROPS(19)
	  D(6,4)=PROPS(19)
	  D(5,6)=PROPS(20)
	  D(6,5)=PROPS(20)
        D(6,6)=PROPS(21)
      ELSE
        EMOD=PROPS(1)
        EMU=PROPS(2)
        TE(1)=PROPS(3)
        TE(2)=PROPS(3)
        TE(3)=PROPS(3)
        VOLUME=PROPS(4)
        
        EG=EMOD/(1.0+EMU)
        EP=1.0-2.0*EMU
        D(1,1)=EG*(1.0-EMU)/EP
        D(2,2)=D(1,1)
        D(3,3)=D(1,1)
        D(1,2)=EMU*EG/EP
        D(1,3)=D(1,2)
        D(2,1)=D(1,2)
        D(2,3)=D(1,2)
        D(3,1)=D(1,2)
        D(3,2)=D(1,2)
        D(4,4)=EG/2.0
        D(5,5)=D(4,4)
        D(6,6)=D(4,4)   
      ENDIF
C-----------------------------------------------------------------
C     INITAIL RHS, AMATRX, GAUSS point
C-----------------------------------------------------------------
      DO K1=1,NDOFEL
        DO KRHS=1,NRHS
          RHS(K1,KRHS)=ZERO   
        ENDDO
        DO K2=1,NDOFEL
          AMATRX(K2,K1)=ZERO
        ENDDO
      ENDDO
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
        DO I=1,3
          DO J=1,NNODE
            BN(I,J)=ZERO
          ENDDO
        ENDDO
C     
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
C     IVOL = Velement*GUASSWEIGHT                             
C-----------------------------------------------------------------         
        GVOL=BH*WEGT
        EVOL=BH*ONE
C-----------------------------------------------------------------	
C     Matrix DNDX-BL                              
C----------------------------------------------------------------- 
        DO I=1,3
          DO K=1,NNODE
            BL(I,K)=ZERO
          ENDDO
        ENDDO
        DO I=1,3
          DO J=1,4
            DO K=1,3
              BL(I,J)=BL(I,J)+BR(I,K)*BN(K,J)
            ENDDO
          ENDDO
        ENDDO      
C-----------------------------------------------------------------	
C     Matrix B                       
C-----------------------------------------------------------------        
        DO I=1,6
          DO K=1,NDOFEL
            B(I,K)=ZERO
          ENDDO
        ENDDO
        DO K=1,4
          B(1,K*3-2)=BL(1,K)
          B(2,K*3-1)=BL(2,K)
          B(3,K*3)=BL(3,K)
          B(4,K*3-2)=BL(2,K)
          B(4,K*3-1)=BL(1,K)
          B(5,K*3-2)=BL(3,K)
          B(5,K*3)=BL(1,K)
          B(6,K*3-1)=BL(3,K)
          B(6,K*3)=BL(2,K)
        ENDDO
C
        DO K1=1, NDOFEL
          DO K2=1, 6
            BT(K1,K2)=B(K2,K1)
          ENDDO
        ENDDO
C-----------------------------------------------------------------	
C     Elastic Matrix S = D*B                            
C----------------------------------------------------------------- 
        DO I=1,6
          DO K=1,NDOFEL
            S(I,K)=ZERO
          ENDDO
        ENDDO
        DO I=1,6
          DO K=1,NDOFEL
            DO J=1,6
              S(I,K)=S(I,K)+D(I,J)*B(J,K)
            ENDDO
          ENDDO
        ENDDO           	
C-----------------------------------------------------------------	
C     Stress and Strain                            
C----------------------------------------------------------------- 	
        DO I=1,6
          SSTRAIN(I)=ZERO
          SSTRESS(I)=ZERO
        ENDDO
        DO I=1,6
          DO J=1,NDOFEL
            SSTRAIN(I)=SSTRAIN(I)+B(I,J)*U(J)
          ENDDO
        ENDDO
        DO I=1,6
          DO J=1,6
            SSTRESS(I)=SSTRESS(I)+D(I,J)*SSTRAIN(J)
          ENDDO
        ENDDO
        DO I=1,6
          SVARS(I)=SSTRAIN(I)
          SVARS(I+6)=SSTRESS(I)
        ENDDO   
        SVARS(13)=EVOL
        SVARS(14)=GVOL
C-----------------------------------------------------------------	
C     RHS and Amatrix     ! +BT(K1,K2)*D(K2,IColumn)*WEGT*BH                    
C-----------------------------------------------------------------
        DO K1=1,6
          DO K2=1,6
            TM(K1)=TM(K1)+D(K1,K2)*TE(K2)
          ENDDO
        ENDDO
C    
        DO K1=1,NDOFEL
          DO K2=1,6
            RHS(K1,1)=RHS(K1,1)-BT(K1,K2)*SSTRESS(K2)*WEGT*BH
     1       +BT(K1,K2)*TM(K2)*WEGT*BH    
          ENDDO
C          
          DO K2=1,NDOFEL
            DO KK=1,6
              AMATRX(K1,K2)=AMATRX(K1,K2)+BT(K1,KK)*S(KK,K2)*WEGT*BH
            ENDDO
          ENDDO
        ENDDO
C      
        DO K1=1,6
          DO K2=1,6
            EMATRX(K1)=EMATRX(K1)+D(K1,K2)*(TE(K2)-SSTRAIN(K2))
     1                 *WEGT*BH/VOLUME
          ENDDO	
        ENDDO
C      
        WRITE(6,*) JELEM, EMATRX(1:6)
C
      ENDDO  
C 

C-----------------------------------------------------------------	
C     Output data into a file                 
C-----------------------------------------------------------------         
!        OPEN(10, FILE='C:\Temp\ElasMatrx.txt', status='old',action='write',
!     1        position="append")  
!        WRITE(10,*) JELEM, EMATRX(1:6) 
!        CLOSE(10) 
C-----------------------------------------------------------------                                                               
      RETURN
      END

