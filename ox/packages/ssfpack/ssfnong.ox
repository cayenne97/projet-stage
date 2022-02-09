#include <oxfloat.h>

enum // indexes for non-Gaussian densities
{
	D_NORMAL, D_POISSON, D_SV, D_SVM, D_SVT, D_SVT2, D_EXP, D_T,
	D_TOTAL
};

SsfNonG_Expansion(const iD, const vY, const vTheta, ...)
{
	decl mret, vhat, args = va_arglist();
	
	if (iD == D_NORMAL)
		mret = vY | 1.0;
	else if (iD == D_POISSON)
	{
		vhat = exp(-vTheta);
		mret = (vTheta==<>) ? log(vY) | 1 : vTheta + (vhat .* vY) - 1.0 | vhat;
	}
	else if (iD == D_SV)
	{
		decl vy2 = vY .* vY, dsigma2 = args[0];
		vhat = 2.0 * dsigma2 * exp(vTheta) ./ vy2;
		mret = (vTheta==<>) ? log(vy2)-log(dsigma2) | 1 : vTheta + 1.0 - (0.5 * vhat) | vhat;

	}
	else if (iD == D_SVM)
	{
		decl vy2 = vY .* vY, dsigma2 = args[0], dbeta2 = sqr(args[1]);
		decl vx  = exp(vTheta);
		decl vx2 = vx .* vx;
		decl vdp = vy2 + dbeta2 * vx2, vdm = vy2 - dbeta2 * vx2;
		vhat = (2.0 * dsigma2 * vx) ./ vdp;
		mret = (vTheta==<>) ? log(vy2)-log(dsigma2 - dbeta2) | 1 : vTheta + ((vdm - dsigma2 * vx) ./ vdp) | vhat;
	}
	else if (iD == D_EXP)
	{
		vhat = exp(vTheta) ./ vY;
		mret = (vTheta==<>) ? log(vY) | 1 : vTheta + 1.0 - vhat | vhat;
	}
	else if (iD == D_T)
	{
		decl dvar = args[0], df = args[1];
		mret = (vTheta==<>) ? vY | dvar : vY | ((dvar * (df - 2.0)) + (vTheta .* vTheta)) / (df + 1.0);
	}
	else if (iD == D_SVT )	//vTheta = Disturbance, Sandmann and Koopman
	{
		decl vy2 = vY .* vY, dsigma2 = args[0], df = args[1];
		decl vtel = 2 * vTheta;
		decl vnoem = ( exp(vTheta) * (df+1) ./ (df + exp(vTheta)) )-1;
		mret = (vTheta==<>) ? log(vy2)-log(dsigma2) | 1 : log(vy2)-log(dsigma2) | vtel ./vnoem;
	}
	else if (iD == D_SVT2)	//vTheta = Signal, Durbin and Koopman
	{
		decl vy2 = vY .* vY, dsigma2 = args[0], df = args[1];
		decl vhulp = dsigma2 * (df-2) * exp(vTheta) ./ vy2;
		decl vhulp2 = vhulp + 1;
		mret = (vTheta==<>) ? log(vy2)-log(dsigma2) | 1 :
		vTheta - (1/(df+1)) * vhulp2 .* vhulp2 ./ vhulp + vhulp2 ./ vhulp | (2/(df+1)) * vhulp2 .* vhulp2 ./ vhulp;
	}
	return mret; // y-hat | v-hat
}

SsfNonG_LogDensity(const iD, const mY, const vTheta, ...)
{
	decl dret, args = va_arglist();
	if (iD == D_NORMAL)
	{
		decl dvar = args[0];
		dret = -0.5 * sumr(log(dvar) + (vTheta .* vTheta ./ dvar));
	}
	else if (iD == D_POISSON)
		dret = vTheta * mY' - sumr(exp(vTheta));
	else if (iD == D_SVM)
	{
		decl dsigma2 = args[0];
		dret = -0.5 *
		(columns(mY) * log(dsigma2) + sumr(vTheta) + sumr(mY .* mY .* exp(-vTheta)) / dsigma2);
	}
	else if (iD == D_SV)
	{
		decl dsigma2 = args[0];
		dret = -0.5 *
		(columns(mY) * log(dsigma2) + sumr(vTheta) + sumr(mY .* mY .* exp(-vTheta)) / dsigma2);
	}
	else if (iD == D_EXP)
		dret = -sumr(vTheta + mY .* exp(-vTheta));
	else if (iD == D_T)
	{
		decl dvar = args[0], df = args[1];
		decl dk = (df - 2) * dvar;
		dret = columns(mY) * (loggamma((df + 1) / 2) - loggamma(df / 2) - 0.5 * log(dk))
			- 0.5 * (df + 1) * sumr(log(1 + ((vTheta .* vTheta) / dk)));
	}
	else if (iD == D_SVT)		//Sandmann and Koopman, vTheta = disturbance of mean equation
	{
		decl dsigma2 = args[0], df = args[1];
		dret = -0.5 *
		(columns(mY) * (log(M_PI) - log(M_2PI) - 2*loggamma((df + 1) / 2) + 2*loggamma(df / 2) + log(df-2))-
		sumr(vTheta) + (df + 1) * sumr( log(1 + exp(vTheta) / (df-2)) )) ;
	}
	else if (iD == D_SVT2)		  //Durbin and Koopman, vTheta = log volatility
	{
		decl dsigma2 = args[0], df = args[1];
		decl eps2 = mY .* mY .* exp(-vTheta);
		dret = -0.5 *
		(columns(mY) * (log(M_PI) - log(M_2PI) + log(dsigma2) - 2*loggamma((df + 1) / 2) + 2*loggamma(df / 2) + log(df-2))+
		sumr(vTheta) + (df + 1) * sumr( log(1 + eps2 / ((df-2)*dsigma2)) )) ;
	}
	return dret;
}

SsfNonG_Antithetic(const nrAnti, const vDraw, const vHat, const dChi2)
{
	decl i, d, n = columns(vHat), err = vDraw, mret;

	for (mret = err, i=1; i<nrAnti; i++)
	{
		if (i==2)
		{
			d = sqrt(quanchi(1 - probchi(dChi2, n), n) / dChi2);
			err = vHat - d * (err - vHat);
		}
		else err = (2.0 * vHat) - err; 
		mret = mret | err;
	}
	return mret;
}

