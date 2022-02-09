static decl s_mY, s_cT;                 // data (1 x T) and T
static decl s_vAR, s_vMA;               // AR and MA pars
static decl s_dSigma, s_dVar;           // std.err. and scale

SetAirlineParameters(const vP)
{
	// map to airline model: y[t] = (1+aL)(1+bL^12)e[t]
	s_vAR = <>;
	s_vMA = vP[0] ~ zeros(1,10) ~ vP[1] ~ vP[0] * vP[1];
	if (!fconc) s_dSigma = exp(vP[2]);
}
ArmaLogLik(const vY, const pdLik, const pdVar)
{
                           // get ARMA model in ssf
    decl mphi, momega, msigma, s = fconc ? 1 : s_dSigma;
	GetSsfArma(s_vAR, s_vMA, s, &mphi, &momega, &msigma);
    decl ret_val = fconc ? // compute (conc) loglikelihood 
		SsfLikConc(pdLik, pdVar, vY, mphi, momega, msigma) : 
		SsfLik(pdLik, pdVar, vY, mphi, momega, msigma);
	if (fconc) s_dSigma = sqrt(pdVar[0]);
    return ret_val;        // 1 indicates success, 0 failure
}
Likelihood(const vP, const pdLik, const pvSco, const pmHes)
{                          // args dictated by MaxBFGS()
    SetAirlineParameters(vP);// map vP to airline model
	decl ret_val = ArmaLogLik(s_mY, pdLik, &s_dVar);// loglik
    pdLik[0] /= s_cT;      // loglik scaled by sample size
	return ret_val;        // 1 indicates success, 0 failure
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
