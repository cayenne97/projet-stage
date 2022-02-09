#include <oxstd.h>
#include <oxdraw.h>
#include <oxfloat.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mdelta, mphi, momega, msigma, myt, mstsmo, mpred, cm, dlik, dvar;

    myt = loadmat("Nile.mat")';
	myt[][1890-1871:1900-1871] = M_NAN; // 1890..1900 missing
	myt[][1950-1871:1960-1871] = M_NAN; // 1850..1960 missing
	
	GetSsfSpline(0.004, <>, &mphi, &momega, &msigma); // Ssf
	SsfLik(&dlik, &dvar, myt, mphi, momega);	// need dVar
	cm = columns(mphi);							// dim state
	momega *= dvar;								// scale Omega
	SsfMomentEst(ST_PRED, &mpred, myt, mphi, momega);
	SsfMomentEst(ST_SMO, &mstsmo, myt, mphi, momega);

	println(mstsmo');

	DrawTMatrix(0, myt, {"Nile"}, 1871, 1, 1);
	DrawTMatrix(0, mpred[cm][2:], {"Pred +/- 2SE"}, 1873, 1, 1, 0, 3);
	DrawZ(sqrt(mpred[2*cm+1][2:]), "", ZMODE_BAND, 2.0, 14);
	DrawTMatrix(1, myt, {"Nile"}, 1871, 1, 1);
	DrawTMatrix(1, mstsmo[cm][], {"Smooth +/- 2SE"}, 1871, 1, 1, 0, 3);
	DrawZ(sqrt(mstsmo[2*cm+1][]), "", ZMODE_BAND, 2.0, 14);
	ShowDrawWindow();
}
