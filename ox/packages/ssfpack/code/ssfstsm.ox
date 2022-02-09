#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mPhi, mOmega, mSigma;
    GetSsfStsm
    (<CMP_IRREG,    1.0, 0, 0, 0; CMP_LEVEL, 0.5, 0, 0, 0;
    CMP_SEAS_DUMMY, 0.2, 3, 0, 0; CMP_SLOPE, 0.1, 0, 0, 0>,
    &mPhi, &mOmega, &mSigma);
    print("Phi =",mPhi, "Omega =",mOmega, "Sigma =",mSigma);
}
