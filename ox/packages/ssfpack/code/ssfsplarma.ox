#include <oxstd.h>
#include <oxdraw.h>
#import <maximize>

#include <packages/ssfpack/ssfpack.h>
#import <packages/ssfpack/ssfcombine>

static decl s_mY, s_cT;
static decl s_vAR, s_vMA, s_q, s_dSigma;

SetSplArmaParameters(const vP)
{
	s_vAR = vP[0];						// AR(1) model
	s_vMA = <>;
	s_q = exp(2. * vP[1]);
}
SplArmaLogLikc(const vY, const pdLik, const pdVar)
{
    decl mphi, momega, msigma, mphiB, momegaB, msigmaB, ret_val;

	GetSsfSpline(s_q, <>, &mphi, &momega, &msigma);
	GetSsfArma(s_vAR, s_vMA, 1, &mphiB, &momegaB, &msigmaB);

	mphi   = SsfCombine(mphi, mphiB, 0);// combining models
	momega = SsfCombineSym(momega, 2, momegaB, 0);
	msigma = SsfCombine(msigma, msigmaB, 0);
	
    ret_val = SsfLikConc(pdLik, pdVar, vY, mphi, momega, msigma);
	s_dSigma = sqrt(pdVar[0]);			// get sigma from SsfLikConc
    return ret_val;     				// 1 indicates success, 0 failure
}
Likelihood(const vP, const pdLik, const pvSco, const pmHes)
{                       				// arguments dictated by MaxBFGS()
    decl dvar, ret_val;

	SetSplArmaParameters(vP);			// map vP to AR(1) model
	ret_val = SplArmaLogLikc(s_mY, pdLik, &dvar);
    pdLik[0] /= s_cT;					// log-likelihood scaled by sample size
	return ret_val;						// 1 indicates success, 0 failure
}
SplArmaStderr(const vP)
{
    decl covar, invcov, var = s_vAR, vma = s_vMA, dsig = s_dSigma, dq = s_q, result;

    result = Num2Derivative(Likelihood, vP, &covar);
	s_vAR = var, s_vMA = vma, s_dSigma = dsig, s_q = dq; 	// reset after Num2Der

    if (!result)
    {	print("Covar() failed in numerical second derivatives\n");
        return zeros(vP);
    }
    invcov = invertgen(-covar, 30);
    return sqrt(diagonal(invcov) / s_cT)';
}
DrawComponents()
{
    decl cst, mphi, momega, msigma, mphiB, momegaB, msigmaB, ret_val;

	GetSsfSpline(s_q, <>, &mphi, &momega, &msigma);
	GetSsfArma(s_vAR, s_vMA, 1, &mphiB, &momegaB, &msigmaB);

	// combining models
	mphi =     SsfCombine(mphi, mphiB, 0);
	momega =   SsfCombineSym(momega, 2, momegaB, 0);
	msigma =   SsfCombine(msigma, msigmaB, 0);

	//smoothed state vector
	cst = columns(mphi);
	decl md = SsfCondDens(ST_SMO, s_mY, mphi, momega, msigma);

	DrawTMatrix(0, s_mY | md[0][], {"Nile", "trend"}, 1870, 1, 1, 0, 2);
	DrawTMatrix(1, md[2][], {"arma error"}, 1870, 1, 1, 0, 2);
	DrawTMatrix(2, s_mY | md[cst][], {"Nile", "signal"}, 1870, 1, 1, 0, 2);
	DrawTMatrix(3, s_mY - md[cst][], {"irregular"}, 1870, 1, 1, 0, 2);
	ShowDrawWindow();
}

main()
{
	decl vp, ir, dlik;

	s_mY = loadmat("Nile.mat")';
	s_cT = columns(s_mY);				// no of observations
	
	vp = <0.8;-3>;						// set starting values

    MaxControl(-1, 5, 1);
	MaxControlEps(1e-7, 1e-4);			// tighter convergence criteria
    ir = MaxBFGS(Likelihood, &vp, &dlik, 0, TRUE);
    
    println("\n", MaxConvergenceMsg(ir),
          " using numerical derivatives",
          "\nLog-likelihood = ", "%.8g", dlik * s_cT,
		  "; variance = ", s_dSigma, " (= dVar); n=", s_cT);
	print("parameters [transformed] with (standard errors):",
		"%cf", {"%12.5g", "%12.5g", "  (%7.5f)"}, (vp[0] | exp(vp[1])) ~ vp ~ SplArmaStderr(vp));
		
	DrawComponents();
}
