#include "SSF.oxh"
//#import  "./FinancialTS/ACtest"
//#import  "./FinancialTS/JBtest"


SSF::SSF()
{
}

//SSF::OlsCAPM()
//{
//	decl vP, mCovar, vResid, dSigmaSqr, vStdError,
//		 cK, vTStatistic, vPValue, dRSquared,
//		 dAdjRSquared, dDWStatistic;
//
//	cK = columns(s_mX);								//Number of regressors
//	olsc(s_vY, s_mX, &vP, &mCovar);
//	vResid = s_vY - s_mX * vP;
//    dSigmaSqr = vResid'vResid / (s_cT - cK);
//    mCovar *= dSigmaSqr;
//	vStdError = <>;
//	for(decl i=0;i<columns(s_mX);i++)
//	{
//		vStdError = vStdError | sqrt(mCovar[i][i]);
//	}
//	vTStatistic = vP./vStdError;
//	vPValue = tailt(vTStatistic, s_cT)*2;			//Two sided t-test
//	dRSquared = 1 - sumsqrc(vResid)/sumsqrc(s_vY-meanc(s_vY));
//	dAdjRSquared = 1 - (s_cT-1)/(s_cT-cK) * (1-dRSquared);
//	dDWStatistic = sumsqrc(diff0(vResid,1)[1:]) / sumsqrc(vResid);
//
//	println("---- Summary OLS estimation of CAPM model ----");
//	print("%13g","Coefficients:","%c",{"Value","Std. Error","t-value", "P value"},
//		  "%r",{"Intercept"}|a_names_X,vP ~ vStdError ~ vTStatistic ~ vPValue);
//	print("%13g","Regression Diagnostics:", "%r",{"R-Squared","Adjusted R-Squared",
//		  "Durbin-Watson Stat"},dRSquared | dAdjRSquared | dDWStatistic);
//	print("%13g","Residual  Diagonostics:","%c",{"Statistic","P-Value"},
//		  "%r",{"Jarque-Bera","Ljung-Box(25)"}, JBtest(vResid) | ACtest(vResid, 25));
//	print("%13g","%r",{"Residual standard error:"},sqrt(varc(vResid)));	
//}

SSF::Likelihood(const vP, const pdLik, const pvSco, const pmHes)
{													// arguments dictated by MaxBFGS()
	decl ret_val;

	GetSsfReg(s_mX',&s_mPhi, &s_mOmega, &s_mSigma,  // Get state space model
	&s_mJPhi);
	switch (s_sModel)
    {												// Update Omega
		case 0:
            s_mOmega[2][2] = exp(vP);				
            break;
        case 1:
            s_mOmega = setdiagonal(s_mOmega,exp(vP));
            break;
        default:
            println("Such model not programmed");
            break;
    }
	ret_val = SsfLik(pdLik, &s_dVar, s_vY',s_mPhi,	// Get loglike
	s_mOmega, s_mSigma, <>, s_mJPhi, <>, <>, s_mX');
	pdLik[0] /= s_cT;								// log-likelihood scaled by n
	return ret_val;									// 1 = success, 0 failure
}

SSF::Get_Info_Criteria_SSF(const LogL, const n, const q)
{
	decl aic,sch,shi,hq	; 
 //	decl LogL=m_dLogLik,n=m_cT,q=sizer(m_vPar);
	aic = (-2*LogL)/n + 2 * q/n; 
	sch	= (-2*LogL)/n + q * log(n)/n; 
	shi = (-2*LogL)/n + log((n+2*q)/n); 
	hq = (-2*LogL)/n + (2*q*log(log(n)))/n; 
    return aic~sch~shi~hq;  
}

SSF::MaxLik(const print_output, const IC)
{
	decl vp, ir, dlik;
	switch (s_sModel)
    {												// starting value
		case 0:
            vp = <0.1>;												
            break;
        case 1:
            vp = zeros(sizec(s_mX),1)|0;							    
//            vp = <0;0;0>;							    
            break;
        default:
            println("Such model not programmed");
            break;
    }
	Likelihood(vp, &dlik, 0, 0);					// evaluate lik at start val
    vp += 0.5 * log(s_dVar);						// scale starting values
	//MaxControl(10, 5, 1);
	ir = MaxBFGS(Likelihood,&vp,&dlik, 0 , 1); 		// max lik estimation with analytical scores
	if (print_output)
	{
		print("---- Maximum likelihood estimation of state space model ",s_sModel," ----");
		print("\n", MaxConvergenceMsg(ir),				// printing results state space estimation
	          " using analytical derivatives",
	          "\nLog-likelihood = ", dlik * s_cT,
			  "; n = ", s_cT);

		decl AIC= (-2*dlik*s_cT)/s_cT + 2 * sizec(vp)/s_cT; 
 		println("; AIC: ", double(AIC));	  
		decl name_sigma_eps=new array[sizerc(a_names_X)];
		for (decl i=0;i<sizerc(a_names_X);++i)
			name_sigma_eps[sizerc(a_names_X)-i-1]=sprint("Sigma ",a_names_X[i]);	
	
		print("%13g","%r",{"Sigma e"}~name_sigma_eps~{"Sigma eta"}, "%c", {"Estimates","Squares"} ,
			  reverser(sqrt(exp(vp))')'~reverser((exp(vp))')');
	}
	IC[0]=Get_Info_Criteria_SSF(dlik*s_cT, s_cT, sizec(vp));

	s_dVar = exp(vp);
	return vp;
}

SSF::MaxLik_eval(const para)
{
	decl ir, dlik;
	decl vp=para;
	Likelihood(vp, &dlik, 0, 0);					// evaluate lik at start val
//	decl name_sigma_eps=new array[sizerc(a_names_X)];
//	for (decl i=0;i<sizerc(a_names_X);++i)
//		name_sigma_eps[sizerc(a_names_X)-i-1]=sprint("Sigma ",a_names_X[i]);	
//
//	print("%13g","%r",{"Sigma e"}~name_sigma_eps~{"Sigma eta"}, "%c", {"Estimates"} ,
//		  reverser(sqrt(exp(vp))')');
	s_dVar = exp(vp);
//	return vp;
}

SSF::GetSeries()
{
	decl mD=Smoothing();
	return s_vY~(s_vY-sumr(s_mX.*mD[:sizer(mD)-2][]'));
}

SSF::Smoothing()
{
	decl mSmo, mks, mD;
	GetSsfReg(s_mX',&s_mPhi, &s_mOmega, &s_mSigma,	// Get estimated state space model
	&s_mJPhi);
	switch (s_sModel)
    {												// starting value
		case 0:
            s_mOmega[2][2] = s_dVar;				// Estimated Omega
			mSmo = SsfMomentEst(ST_SMO, &mks, s_vY',// Perform smoothing
					s_mPhi, s_mOmega, s_mSigma, <>,
					s_mJPhi,	<>, <>, s_mX');		//Obtain estimate and standard errors					
			print("%13g","Coefficients:","%c",{"Value",	
		  		  "Std. Err."},"%r",{"Intercept"}~a_names_X,
		  		  mks[0:sizerc(a_names_X)][10]~sqrt(mks[sizerc(a_names_X)+2:sizerc(a_names_X)*2+2][10])); //Use 10th row to avoid impact of starting value												
			break;
        case 1:
            s_mOmega = diag(s_dVar);				// Values for sigma_eta, sigma_eps and sigma_e
			mD = SsfCondDens(ST_SMO, s_vY',s_mPhi,	// Perform smoothing
			 	s_mOmega, s_mSigma, <>, s_mJPhi, <>,
			 	<>, s_mX');
//			DrawTMatrix(0,s_vY',1,1,1,1,0,2);		// Draw results
//			DrawText(0, "excess rtn", 0, 0, -1, -1, TEXT_YLABEL); 
//			DrawTitle(0,"(a) Monthly simple excess return");
//			DrawTMatrix(1,mD[3][],1,1,1,1,0,2);			
//			DrawText(1, "rtn", 0, 0, -1, -1, TEXT_YLABEL); 
//			DrawTitle(1,"(b) Expected return");
//			DrawTMatrix(2,mD[0][],1,1,1,1,0,2);			
//			DrawText(2, "Value", 0, 0, -1, -1, TEXT_YLABEL); 
//			DrawTitle(2,"(c) Alpha(t) estimate");
//			DrawTMatrix(3,mD[1][],1,1,1,1,0,2);			
//			DrawText(3, "Value", 0, 0, -1, -1, TEXT_YLABEL); 
//			DrawTitle(3,"(d) Beta 1(t) estimate");
//			DrawTMatrix(4,mD[2][],1,1,1,1,0,2);			
//			DrawText(4, "Value", 0, 0, -1, -1, TEXT_YLABEL); 
//			DrawTitle(4,"(d) Beta 2(t) estimate");
//			DrawTMatrix(5,mD[3][],1,1,1,1,0,2);			
//			DrawText(5, "Value", 0, 0, -1, -1, TEXT_YLABEL); 
//			DrawTitle(5,"(d) Beta 3(t) estimate");
//			SetDrawWindow("SSF");
//			ShowDrawWindow();
			return mD;
            break;
        default:
            println("Such model not programmed");
            break;
    }	
}
