#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mtau, mdelta, mphi, momega, msigma, mj_phi, mj_omega, mx;

	mtau = <2,3,5,9,12,17,20,23,25>;	// tau_0 ... tau_n
    mdelta = diff0(mtau', 1)[1:][]';	// delta_1 ... delta_n
//	GetSsfSpline(0.2, mdelta, &mphi, &momega, &msigma, &mj_phi, &mj_omega, &mx);
	// cubic spline model with q = 0.2
	GetSsfSpline(0.2, <>, &mphi, &momega);
	
    // print state space
    print("Phi", mphi);
	print("Time-varying index for Phi", "%5.0g", mj_phi);
    print("Omega", momega);
	print("Time-varying index for Omega", "%5.0g", mj_omega);
    print("Transposed data matrix", mx');
}
