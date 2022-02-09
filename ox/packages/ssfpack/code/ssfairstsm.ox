#include <oxstd.h>
#include <oxdraw.h>
#import  <maximize>
#include <packages/ssfpack/ssfpack.h>

static decl s_mY, s_cT;					// data (1 x T) and T
static decl s_mStsm, s_vVarCmp;         // matrix for unobserved components model
static decl s_dSigma, s_dVar;			// residual std.err. and scale factor
static decl s_vPar;                     // parameter vector of model

SetStsmModel(const vP)
{
	// map to sts model with level, slope and trig seasonal
	s_mStsm = <CMP_LEVEL,     1,  0, 0;
		       CMP_SLOPE,     0,  0, 0;
    		   CMP_SEAS_TRIG, 1, 12, 0;	// 12 for monthly data
			   CMP_IRREG,     1,  0, 0>;

	decl vr = exp(2.0 * vP);			// from log(s.d.) to variance
	s_vVarCmp =							// s_vVarCmp is diagonal(Omega)
	 // level  slope  ---------  monthly trigonometric seasonal  --------  irreg
		vr[0] |  0  | ((vr[1] | vr[2] | 0 | vr[3] | vr[4]) ** <1;1>) | 0 | vr[5];
}
LogLikStsm(const vY, const pdLik, const pdVar)
{
    decl mphi, momega, msigma, ret_val;
	GetSsfStsm(s_mStsm, &mphi, &momega, &msigma); // get state space model
	momega = diag(s_vVarCmp);			// create Omega from s_vVarCmp
    ret_val = SsfLik(pdLik, pdVar, vY, mphi, momega, msigma);
    return ret_val;     				// 1 indicates success, 0 failure
}
LogLikScoStsm(const vY, const pdLik, const pvSco)
{
    decl mphi, momega, msigma, msco, ret_val, dvar;
	GetSsfStsm(s_mStsm, &mphi, &momega, &msigma);
	momega = diag(s_vVarCmp);
										// get state space model, loglik and score
    ret_val = SsfLikSco(pdLik, &dvar, &msco, vY, mphi, momega, msigma);
	decl vs = (diagonal(msco)' .*  s_vVarCmp);
	pvSco[0][0][0] = vs[0] /*| vs[1] */;
	pvSco[0][1:4][0] = vs[2] + vs[3] | vs[4] + vs[5] |/* vs[6] + vs[7] |*/
		vs[8] + vs[9] | vs[10] + vs[11]/* | vs[12]*/;
	pvSco[0][5][0] = vs[13];
	
    return ret_val;     				// 1 indicates success, 0 failure
}
InitialPar()
{
	decl cp = 6, vp = constant(-2, cp, 1);
	vp[0] = -1;
	vp[cp-1] = 0;
	SetStsmModel(vp);					// map vP to STSM model
	
	decl dlik, dvar;
	LogLikStsm(s_mY, &dlik, &dvar);

	return vp + 0.5 * log(dvar);
}
Likelihood(const vP, const pdLik, const pvSco, const pmHes)
{                       				// arguments dictated by MaxBFGS()
    decl ret_val;

	SetStsmModel(vP);					// map vP to airline model
	if (isarray(pvSco))
	{	ret_val = LogLikScoStsm(s_mY, pdLik, pvSco);
		pvSco[0][][] /= s_cT;			// scores scaled by sample size
	}
	else
		ret_val = LogLikStsm(s_mY, pdLik, &s_dVar);
    pdLik[0] /= s_cT;					// log-likelihood scaled by sample size
	return ret_val;						// 1 indicates success, 0 failure
}
MaxLik()
{
	decl vp, dlik, ir;

	vp = InitialPar();					// get starting values
	MaxControl(-1, 5, 1);				// get some output from MaxBFGS
    ir = MaxBFGS(Likelihood, &vp, &dlik, 0, FALSE);

    println("\n", MaxConvergenceMsg(ir),
          " using analytical derivatives",
          "\nLog-likelihood = ", "%.8g", dlik * s_cT,
		  "; n = ", s_cT, ";");
	println("variance parameters (* 10,000):",
		"%5.2f", 10000 * s_vVarCmp');
	s_vPar = vp;
}
DrawComponents(const mY)
{
    decl cst, mphi, momega, msigma;

	SetStsmModel(s_vPar);              	// map vP to STSM model
	GetSsfStsm(s_mStsm, &mphi, &momega, &msigma);
	momega = diag(s_vVarCmp);

	//smoothed state vector
	cst = columns(mphi);
	decl md = SsfCondDens(ST_SMO, mY, mphi, momega, msigma);
	decl mw = <0,0> ~ (<1,1,1,1,1> ** <1,0>) ~ <1,0>;

	DrawTMatrix(0, mY | md[0][], {"Nile", "trend"}, 1949, 1, 12, 0, 2);
	DrawTMatrix(1, mw * md, {"seasonal"}, 1949, 1, 12, 0, 2);
	DrawTMatrix(2, mY - md[cst][], {"irregular"}, 1949, 1, 12, 0, 2);
	DrawTMatrix(3, mY - mw * md, {"seasonally adjusted data"}, 1949, 1, 12, 0, 2);
	DrawTMatrix(4, md[2][],  {"trig 1"}, 1949, 1, 12, 0, 2);
	DrawTMatrix(5, md[4][],  {"trig 2"}, 1949, 1, 12, 0, 2);
	DrawTMatrix(6, md[8][],  {"trig 4"}, 1949, 1, 12, 0, 2);
	DrawTMatrix(7, md[10][], {"trig 5"}, 1949, 1, 12, 0, 2);
	ShowDrawWindow();
}

main()
{
	s_mY = log(loadmat("Airline.mat"))';	// load data, transpose
	s_cT = columns(s_mY);				    // no of observations

	MaxLik();
	DrawComponents(s_mY);
}
