     
      SUBROUTINE CALLBH(REFRE,REFIM,RAD,WAVEL,NANG,ANG,
     &  S11,S12,S33,S34,QSCA,QEXT)
C ***************************************************************
C CALMIE CALCULA EL PARAMETRO DE TAMAÑO, EL INDICE DE REFRACCION
C RELATIVO Y LUEGO HACE UNA LLAMADA A LA SUBRRUTINA MIEPHAS Y A 
C PARTIR DE LOS DATOS QUE TIENE Y DE LA MATRIZ DE FASES, CALCULA
C LA MATRIZ DE SCATTERING.SOLO NOS QUEDAMOS CON LA FUNCIÓN DE FASE
C ***************************************************************
C REFRE=PARTE REAL DEL INDICE DE REFRACCION
C REFIM=PARTE IMAGINARIA
C RAD=RADIO DE LA ESFERA
C WAVEL=LONGITUD DE ONDA
C NANG ES EL NUMERO DE ANGULOS ENTRE 0 Y 90 INCLUYENDO 0 Y 90
C ANG ES EL VECTOR DE ANGULOS
C SUPONEMOS QUE LA ESFERA TIENE REFRE=1.33, REFIM=0.0 (MODIFICAR ABAJO)
C Y QUE EL MEDIO TIENE REFMED = 1.0
C **************************************************************

      INCLUDE 'parameters.for'

      INTEGER NAN,NANG
      COMPLEX REFREL,S1(2*NANGMAX-1),S2(2*NANGMAX-1)
      REAL PI,REFRE,REFIM,REFMED,WAVEL,X,QSCA,QEXT
      REAL ANG(NANGMAX),S11(NANGMAX),S12(NANGMAX),S33(NANGMAX),
     &     S34(NANGMAX)

      PI=4.E0*ATAN(1.E0)

      IF (NANG.GT.NANGMAX) STOP 'Increase NANGMAX'
C ***************************************************************
C REFMED = (REAL) REFRACTIVE INDEX OF SURROUNDING MEDIUM        
C ***************************************************************
      REFMED = 1.E0
C ***************************************************************
C REFRACTIVE INDEX OF SPHERE = REFRE + i*REFIM 
C ***************************************************************

      REFREL = CMPLX(REFRE,REFIM)/REFMED	

C ***************************************************************
C NAN ES EL NUMERO DE ANGULOS ENTRE 0 Y 180
C ***************************************************************
      NAN=2*NANG-1

      X=2.E0*PI*RAD*REFMED/WAVEL
      DANG = (PI/2.E0)/FLOAT(NANG-1)                 
      CALL BHMIE (X,REFREL,NANG,S1,S2,QSCA,QEXT)
      DO 355 J=1,NAN
	S11(J)=0.5*(CABS(S2(J))**2+CABS(S1(J))**2)
	S12(J)=0.5*(CABS(S2(J))**2-CABS(S1(J))**2)
        S33(J)=REAL(S1(J)*CONJG(S2(J)))
        S34(J)=AIMAG(S2(J)*CONJG(S1(J)))
	ANG(J)=DANG*FLOAT(J-1)*(180.0/PI)
355   CONTINUE
      RETURN 
      END



