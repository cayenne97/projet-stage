#include <oxstd.h>
#include <oxdraw.h>
#include <oxfloat.h>
#import <maximize>
#include <packages/ssfpack/ssfpack.h>

static decl s_mY, s_cT;
static decl s_vAR, s_vMA, s_dSigma, s_dVar;

SetAirlineParameters(const vP)
{
	// airline model: y[t] = (1+aL)(1+bL^12)e[t]
	s_vAR = <>;
	s_vMA = vP[0] ~ zeros(1,10) ~ vP[1] ~ vP[0] * vP[1];
	s_dSigma = exp(vP[2]);
}
ArmaLogLik(const vY, const pdLik, const pdVar)
{
    decl mphi, momega, msigma, ret_val;

	GetSsfArma(s_vAR, s_vMA, s_dSigma, &mphi, &momega, &msigma);
	
    ret_val = SsfLik(pdLik, pdVar, vY, mphi, momega, msigma);

    return ret_val;     		// 1 indicates success, 0 failure
}
ArmaForc(const vY, const cForc)
{
    decl mphi, momega, msigma, mstate, mfor, m;

	GetSsfArma(s_vAR, s_vMA, s_dSigma, &mphi, &momega, &msigma);
	m = columns(mphi);
	mstate = SsfMomentEst(ST_PRED, 0, vY, mphi, momega, msigma);
	SsfMomentEst(ST_PRED, &mfor, constant(M_NAN,1,cForc), mphi, momega, mstate);
	return (vY ~ mfor[m][]) | (zeros(vY) ~ sqrt(mfor[2 * m + 1][]));
}
Likelihood(const vP, const pdLik, const pvSco, const pmHes)
{                       		// arguments dictated by MaxBFGS()
    decl ret_val;

	SetAirlineParameters(vP);	// map vP to airline model
	ret_val = ArmaLogLik(s_mY, pdLik, &s_dVar);
    pdLik[0] /= s_cT;			// log-likelihood scaled by sample size

	return ret_val;				// 1 indicates success, 0 failure
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
Cum1Cum12(const mD12Y, const mDy, const mY)
{
	decl cy = columns(mD12Y), m = unit(cy, cy), z = zeros(cy, cy);
	decl cum12 = cumulate(mDy[0:11][] | mD12Y, z,z,z,z,z,z,z,z,z,z,z,m);
	return cumulate(mY[0][] | cum12, m);
}

main()
{
    decl vp, ir, dlik, dvar, my, mdy;

    // load Nile data and transpose
    my = log(loadmat("Airline.mat"));	// log(airline)
	mdy = diff0(my, 1)[1:][];			// Dlog(airline)
    s_mY = diff0(mdy, 12)[12:][]';	  	// D12D(log(airline))
	s_cT = columns(s_mY);

	vp = <0.5;0.5;0>;
    // scale initial parameter estimates for better starting values
	SetAirlineParameters(vp);	// map vP to airline model
	ArmaLogLik(s_mY, &dlik, &dvar);
    vp[sizerc(vp)-1] = 0.5 * log(dvar);

    MaxControl(-1, 5, 1);
    ir = MaxBFGS(Likelihood, &vp, &dlik, 0, TRUE);
    
    println("\n", MaxConvergenceMsg(ir),
          " using numerical derivatives",
          "\nLog-likelihood = ", "%12.8g", dlik * s_cT,
		  "; variance = ", exp(2 * vp[sizerc(vp)-1]),
		  "; n = ", s_cT, "; dVar = ", s_dVar);
	print("parameters with standard errors:",
		"%cf", {"%12.5g", "  (%7.5f)"}, vp ~ ArmaStderr(vp));

	decl mforc = ArmaForc(s_mY, 24)';			// forecasts of D1D12
	mforc = Cum1Cum12(mforc[][0], mdy, my)';	// translate to levels
	
	DrawTMatrix(0, mforc[][ : rows(my) - 1], {"actual"}, 1949, 1, 12, 0, 2);
	DrawTMatrix(0, mforc[][rows(my) : ],  {"forecasts"}, 1961, 1, 12, 0, 3);
	ShowDrawWindow();
}
