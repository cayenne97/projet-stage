#include <oxstd.h>
#include <oxdraw.h>
#include <oxfloat.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
	decl ct, ck, myt, mx;
	decl mphi, momega, msigma, mj_phi;
	decl dlik, dvar;
	decl mst, vse, mols;
	decl mif, mkf, mks, mstab;

	myt = loadmat("spirit.in7")';		 // load spirits data
	ct = columns(myt);					 // no of observations
	mx = 1 | range(1, ct, 1) | myt[1:][];// X'=1|t|price|inc
	ck = rows(mx);						 // no of regressors
	myt = myt[0][];						 // Y'

	GetSsfReg(mx, &mphi, &momega, &msigma, &mj_phi);
	// calculate likelihood and error variance
	SsfLikConc(&dlik, &dvar, myt, mphi, momega, msigma,
		<>, mj_phi, <>, <>, mx);
	// regression
	momega *= dvar;
	mst = SsfMomentEst(ST_PRED, 0, myt, mphi, momega, msigma,
		<>, mj_phi, <>, <>, mx);
	vse  = sqrt(diagonal(mst[0:ck-1][]));
	mols = mst[ck][] | vse | fabs(mst[ck][] ./ vse);

	print("Regression results");
	println("%r", {"const", "trend", "price", "income"},
		"%c", {"coef", "s.e.", "t-value"}, mols');
	println("Modified profile log-likelihood ", dlik,
	" log-likelihood ",-ct/2 * log(dvar * (ct-ck)/ct) -ct/2*(log(M_2PI)+1),
	"\nvariance ", dvar, " RSS ", dvar * (ct-ck));
}	
