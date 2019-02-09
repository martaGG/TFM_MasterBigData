      
       SUBROUTINE BHMIE(X,REFREL,NANG,S1,S2,QSCA,QEXT)

C***********************************************************************
C Subroutine BHMIE is the Bohren-Huffman Mie scattering subroutine
C    to calculate scattering and absorption by a homogenous isotropic
C    sphere.
C Given:
C    X = 2*pi*a/lambda
C    REFREL = (complex refr. index of sphere)/(real index of medium)
C    NANG = number of angles between 0 and 90 degrees
C           (will calculate 2*NANG-1 directions from 0 to 180 deg.)
C           if called with NANG<2, will set NANG=2 and will compute
C           scattering for theta=0,90,180.
C Returns:
C    S1(1 - 2*NANG-1) = -i*f_22 (incid. E perp. to scatt. plane,
C                                scatt. E perp. to scatt. plane)
C    S2(1 - 2*NANG-1) = -i*f_11 (incid. E parr. to scatt. plane,
C                                scatt. E parr. to scatt. plane)
C*********************************************************************** 

C***********************************************************************
C                             DECLARATION
c***********************************************************************

C Declare parametres:
C Note: important that MXNANG be consistent with dimension of S1 and S2
C       in calling routine!
       
       INCLUDE 'parameters.for'

       INTEGER MXNANG,NMXX
       PARAMETER(MXNANG=NANGMAX,NMXX=150000)
C Arguments:
       INTEGER NANG
       REAL X,QSCA
       COMPLEX REFREL
       COMPLEX S1(2*MXNANG-1),S2(2*MXNANG-1)
C Local variables:
       INTEGER J,JJ,N,NSTOP,NMX,NN
       REAL CHI,CHI0,CHI1,DANG,DX,EN,FN,P,PII,PSI,PSI0,PSI1,
     &      THETA,XSTOP,YMOD
       REAL AMU(MXNANG),PI(MXNANG),PI0(MXNANG),PI1(MXNANG),
     &      TAU(MXNANG)
       COMPLEX AN,AN1,BN,BN1,DREFRL,XI,XI1,Y
       COMPLEX D(NMXX)

C********************************************************************
C                          Safety checks
C********************************************************************

      IF(NANG.GT.MXNANG)STOP'***Error: NANG > MXNANG in bhmie'
      IF(NANG.LT.2)NANG=2

C********************************************************************
C                           Obtain pi:
C********************************************************************
     
      PII=4.*ATAN(1.E0)

C********************************************************************
      
      DX=X
      DREFRL=REFREL
      Y=X*DREFRL
      YMOD=ABS(Y)

C********************************************************************
C          Series expansion terminated after NSTOP terms
C********************************************************************

      XSTOP=X+4.*X**0.3333+2.
      NMX=MAX(XSTOP,YMOD)+15
C BTD experiment 91/1/15: add one more term to series and compare results
C test: compute 7001 wavelengths between .0001 and 1000 micron
C for a=1.0micron SiC grain.  When NMX increased by 1, only a single
C computed number changed (out of 4*7001) and it only changed by 1/8387
C conclusion: we are indeed retaining enough terms in series!
      NSTOP=XSTOP

      IF(NMX.GT.NMXX)THEN
          WRITE(0,*)'Error: NMX > NMXX=',NMXX,' for |m|x=',YMOD
          STOP
      ENDIF
C Require NANG.GE.1 in order to calculate scattering intensities
      DANG=0.
      IF(NANG.GT.1)DANG=.5*PII/REAL(NANG-1)
      DO 1000 J=1,NANG
          THETA=REAL(J-1)*DANG
          AMU(J)=COS(THETA)
 1000 CONTINUE

C*******************************************************************
C Inicializamos valores
C*******************************************************************

      DO 1100 J=1,NANG
          PI0(J)=0.
          PI1(J)=1.
 1100 CONTINUE
      NN=2*NANG-1
      DO 1200 J=1,NN
          S1(J)=(0.,0.)
          S2(J)=(0.,0.)
 1200 CONTINUE
C
C*** Logarithmic derivative D(J) calculated by downward recurrence
C    beginning with initial value (0.,0.) at J=NMX
C
      D(NMX)=(0.,0.)
      NN=NMX-1
      DO 4000 N=1,NN
          EN=NMX-N+1
          D(NMX-N)=(EN/Y)-(1./(D(NMX-N+1)+EN/Y))
 4000 CONTINUE

C*******************************************************************
C Riccati-Bessel functions with real argument X
C    calculated by upward recurrence
C*******************************************************************

      PSI0=COS(DX)
      PSI1=SIN(DX)
      CHI0=-SIN(DX)
      CHI1=COS(DX)
      XI1=DCMPLX(PSI1,-CHI1)
      QSCA=0.E0
      P=-1.
      DO 3000 N=1,NSTOP
          EN=N
          FN=(2.E0*EN+1.)/(EN*(EN+1.))
C for given N, PSI  = psi_n        CHI  = chi_n
C              PSI1 = psi_{n-1}    CHI1 = chi_{n-1}
C              PSI0 = psi_{n-2}    CHI0 = chi_{n-2}
C Calculate psi_n and chi_n
          PSI=(2.E0*EN-1.)*PSI1/DX-PSI0
          CHI=(2.E0*EN-1.)*CHI1/DX-CHI0
          XI=DCMPLX(PSI,-CHI)

C Store previous values of AN and BN for use
C    in computation of g=<cos(theta)>
          IF(N.GT.1)THEN
              AN1=AN
              BN1=BN
          ENDIF

C Compute AN and BN:
          AN=(D(N)/DREFRL+EN/DX)*PSI-PSI1
          AN=AN/((D(N)/DREFRL+EN/DX)*XI-XI1)
          BN=(DREFRL*D(N)+EN/DX)*PSI-PSI1
          BN=BN/((DREFRL*D(N)+EN/DX)*XI-XI1)

C*** Augment sums for Qsca

          QSCA=QSCA+(2.*EN+1.)*(ABS(AN)**2+ABS(BN)**2)

C*** Now calculate scattering intensity pattern
C    First do angles from 0 to 90
          DO 2500 J=1,NANG
              JJ=2*NANG-J
              PI(J)=PI1(J)
              TAU(J)=EN*AMU(J)*PI(J)-(EN+1.)*PI0(J)
              S1(J)=S1(J)+FN*(AN*PI(J)+BN*TAU(J))
              S2(J)=S2(J)+FN*(AN*TAU(J)+BN*PI(J))
 2500     CONTINUE
C
C*** Now do angles greater than 90 using PI and TAU from
C    angles less than 90.
C    P=1 for N=1,3,...; P=-1 for N=2,4,...
          P=-P
          DO 2600 J=1,NANG-1
              JJ=2*NANG-J
              S1(JJ)=S1(JJ)+FN*P*(AN*PI(J)-BN*TAU(J))
              S2(JJ)=S2(JJ)+FN*P*(BN*PI(J)-AN*TAU(J))
 2600     CONTINUE
          PSI0=PSI1
          PSI1=PSI
          CHI0=CHI1
          CHI1=CHI
          XI1=DCMPLX(PSI1,-CHI1)
C
C*** Compute pi_n for next value of n
C    For each angle J, compute pi_n+1
C    from PI = pi_n , PI0 = pi_n-1
          DO 2800 J=1,NANG
              PI1(J)=((2.*EN+1.)*AMU(J)*PI(J)-(EN+1.)*PI0(J))/EN
              PI0(J)=PI(J)
 2800     CONTINUE
 3000 CONTINUE

C    Have summed sufficient terms.
C    Now compute QSCA,QEXT,QBACK,and GSCA
c      GSCA=2.*GSCA/QSCA
      QSCA=(2./(DX*DX))*QSCA
      QEXT=(4./(DX*DX))*REAL(S1(1))
c      QBACK=(ABS(S1(2*NANG-1))/DX)**2/PII
     
      RETURN
      END



















