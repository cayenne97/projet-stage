#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mphi, momega, msigma, mj_phi;

	// regression model in state space
	GetSsfReg(zeros(3,20), &mphi, &momega, &msigma, &mj_phi);
	
    // print state space
    print("Phi", mphi);
	print("Time-varying index for Phi", "%5.0g", mj_phi);
    print("Omega", momega);
    print("Sigma", msigma);
}
