#include <oxstd.h>
#include <oxdraw.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mPhi = <1,1;0,1;1,0>, mOmega = diag(<.5,.1,1>);
    decl mSigma = diag(<-1,-1>) | 0;
    decl mu = sqrt(mOmega) * rann(3, 21);
    decl mr = SsfRecursion(mu, mPhi, mOmega, <0,0;0,0;1,.5>);
    decl mYt = mr[2][1:];
    decl ct = columns(mYt);

    decl mGamma = diag(<1,1,0>);
    decl mKF = KalmanFil(mYt, mPhi, mOmega, mSigma);
    decl mWgt = SimSmoWgt(mGamma, mKF, mPhi, mOmega, mSigma);
    
    // monte carlo study
    decl i, imc = 10000, md, mdcum, mdcum2;
    mdcum = mdcum2 = zeros(rows(mPhi), ct);
    for (i=0; i<imc; i++)
    {
		md = SsfCondDens(DS_SIM, mYt, mPhi, mOmega, mSigma);
        mdcum  += md; mdcum2 += sqr(md);
    }
    mdcum  ./= imc; mdcum2 ./= imc; // Mean, Mean squared
    mdcum2 -= sqr(mdcum); // Variance
    mdcum2 = diagonal(mOmega)' - mdcum2; // Cond Var

    decl mmom;
    SsfMomentEst(DS_SMO, &mmom, mYt, mPhi, mOmega, mSigma);
//    println("Exact moments:", (mmom[:1][]|mmom[3:4][])');
//    println("Monte Carlo moms:", (mdcum[:1][]|mdcum2[:1][])');
	println("Exact moments:");
	println("      --------mean--------     --mean square error--",
		mmom[:1][]' ~ mmom[3:4][]');
	println("Monte Carlo moments:");
	println("      --------mean--------     --mean square error--",
		mdcum[:1][]' ~ mdcum2[:1][]');
}
