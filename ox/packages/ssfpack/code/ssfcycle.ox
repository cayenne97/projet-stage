#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mPhi, mOmega, mSigma;
    GetSsfStsm
    (<CMP_IRREG,1.0, 0, 0, 0; CMP_TREND,0.4, 3, 0, 0;
      CMP_BWCYC,0.6, 0.9, 0.3, 2>, &mPhi, &mOmega, &mSigma);
	format("%8.3f");
    print("Phi =",mPhi, "Omega =",mOmega, "Sigma =",mSigma);
}
