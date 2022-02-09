#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mPhi, mOmega, mSigma;
	format("%5.1f");
    GetSsfArma
    (<0.6,0.2>, <-0.2>, sqrt(0.9), &mPhi, &mOmega, &mSigma);
    print("Phi =",mPhi, "Omega =",mOmega, "Sigma =",mSigma);
}
