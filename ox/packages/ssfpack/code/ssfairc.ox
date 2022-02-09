#include <oxstd.h>
#import <maximize>
#include <packages/ssfpack/ssfpack.h>

static decl s_mY, s_cT;
static decl s_vAR, s_vMA, s_dSigma;

SetAirlineParameters(const vP)
{
	// map to airline model: y[t] = (1+aL)(1+bL^12)e[t]
	s_vAR = <>;
	s_vMA = vP[0] ~ zeros(1,10) ~ vP[1] ~ vP[0] * vP[1];
}
ArmaLogLikc(const vY, const pdLik, const pdVar)
{
    decl mphi, momega, msigma, ret_val;
										// use 1 in GetSsfArma
	GetSsfArma(s_vAR, s_vMA, 1, &mphi, &momega, &msigma);
    ret_val = SsfLikConc(pdLik, pdVar, vY, mphi, momega, msigma);
	s_dSigma = sqrt(pdVar[0]);			// get sigma from SsfLikConc
    return ret_val;     				// 1 indicates success, 0 failure
}
Likelihood(const vP, const pdLik, const pvSco, const pmHes)
{                       				// arguments dictated by MaxBFGS()
    decl dvar, ret_val;

	SetAirlineParameters(vP);			// map vP to airline model
	ret_val = ArmaLogLikc(s_mY, pdLik, &dvar);
    pdLik[0] /= s_cT;					// log-likelihood scaled by sample size
	return ret_val;						// 1 indicates success, 0 failure
}
ArmaStderr(const vP)
{
    decl covar, invcov, var = s_vAR, vma = s_vMA, dsig = s_dSigma, result;

    result = Num2Derivative(Likelihood, vP, &covar);
	s_vAR = var, s_vMA = vma, s_dSigma = dsig; 	// reset after Num2Der

    if (!result)
    {	print("Covar() failed in numerical second derivatives\n");
        return zeros(vP);
    }
    invcov = invertgen(-covar, 30);
    return sqrt(diagonal(invcov) / s_cT)';
}

main()
{
    decl vp, ir, dlik, dvar, my, mdy;

    // load Nile data and transpose
    my = log(loadmat("Airline.mat"));	// log(airline)
	mdy = diff0(my, 1)[1:][];			// Dlog(airline)
    s_mY = diff0(mdy, 12)[12:][]';	  	// D12D(log(airline)) transposed!!
	s_cT = columns(s_mY);				// no of observations

	vp = <0.5;0.5>;						// set starting values

    MaxControl(-1, 5, 1);
	MaxControlEps(1e-7, 1e-5);			// tighter convergence criteria
    ir = MaxBFGS(Likelihood, &vp, &dlik, 0, TRUE);
    
    println("\n", MaxConvergenceMsg(ir),
          " using numerical derivatives",
          "\nLog-likelihood = ", "%.8g", dlik * s_cT,
		  "; variance = ", sqr(s_dSigma), " (= dVar); n=", s_cT);
	print("parameters with standard errors:",
		"%cf", {"%12.5g", "  (%7.5f)"}, vp ~ ArmaStderr(vp));
}