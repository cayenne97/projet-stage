#include <oxstd.h>
#include <oxdraw.h>
#import <maximize>
#include <packages/ssfpack/ssfpack.h>

static decl s_mYt, s_mPhi, s_mOmega, s_mSigma, s_dVar;
static decl s_mSsf;

Likelihood(const vP, const pdLik, const pvSco, const pmHes)
{	// arguments dictated by MaxBFGS()
    decl dvar, msco, ct = columns(s_mYt);
	s_mSsf[0:1][1] = exp(vP);	// update ssf definition
	GetSsfStsm(s_mSsf, &s_mPhi, &s_mOmega, &s_mSigma);
    if (pvSco) {				// yes: score requested
		SsfLikSco(pdLik, &s_dVar, &msco,
			s_mYt, s_mPhi, s_mOmega, s_mSigma);
        pvSco[0] = (diagonal(s_mOmega) .* diagonal(msco))'/ct;
    } else						// no: num score required
        SsfLik(pdLik, &s_dVar,
			s_mYt, s_mPhi, s_mOmega, s_mSigma);
    pdLik[0] /= ct;				// log-likelihood scaled by n
    return 1;					// 1 = success, 0 failure
}

main()
{
    decl vp, ir, dlik, dvar;

    // load Nile data and transpose
    s_mYt = loadmat("Nile.mat")';
    // set state space definition matrix
	s_mSsf = <CMP_LEVEL, 0.5, 0, 0;
			  CMP_IRREG, 1.0, 0, 0>;
    // scale initial estimates for better starting values
    vp = log(<0.5;1>);			// starting values log(sigma)
	Likelihood(vp, &dlik, 0, 0);// evaluate lik at start val
    vp += 0.5 * log(s_dVar);	// scale starting values
    // max lik estimation with analytical scores
    MaxControl(10, 5, 1);
    ir = MaxBFGS(Likelihood, &vp, &dlik, 0, FALSE);

	print("\n", MaxConvergenceMsg(ir),
          " using analytical derivatives",
          "\nLog-likelihood = ", dlik * columns(s_mYt),
		  "; dVar = ", s_dVar, "; parameters:", vp');
    print("Omega", s_mOmega);

	// the s_mSsf correspond to estimated model
	decl md, ms, mks, mstate;
	mstate =
	SsfMomentEst(ST_SMO,&mks,s_mYt,s_mPhi,s_mOmega,s_mSigma);
	SsfMomentEst(DS_SMO,&md, s_mYt,s_mPhi,s_mOmega,s_mSigma);
	ms = md[0:1][] ./ sqrt(md[2:3][]); // auxiliary resiudals

	DrawTMatrix(0, s_mYt, {"Nile"}, 1871, 1, 1);
	DrawTMatrix(0, mks[1][], {"Smooth +/- 2SE"}, 1871, 1, 1, 0, 3);
	DrawZ(sqrt(mks[3][]), "", ZMODE_BAND, 2.0, 14);
	DrawTMatrix(1, ms,
		{"Structural break t-test", "Outlier t-test"}, 1871, 1, 1);
	ShowDrawWindow();
}
