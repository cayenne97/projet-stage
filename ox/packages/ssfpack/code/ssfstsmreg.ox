#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mPhi, mOmega, mSigma, mJPhi = <>;
    GetSsfStsm
    (<CMP_IRREG, 1.0, 0, 0, 0; CMP_TREND, 0.4, 2, 0, 0>,
    &mPhi, &mOmega, &mSigma);
    AddSsfReg(rann(3,20), &mPhi, &mOmega, &mSigma, &mJPhi);
	format("%8.3f");
    print("Phi =",mPhi, "Omega =",mOmega, "Sigma =",mSigma);
    print("JPhi = ", mJPhi);
}
