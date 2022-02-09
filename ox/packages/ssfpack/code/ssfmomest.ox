#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mYt = rann(1,9); // data
    decl mPhi, mOmega, mSigma; // ssf
    GetSsfStsm(
        <CMP_IRREG, 1.0, 0; CMP_LEVEL, 0.0, 0;
         CMP_SLOPE, 0.1, 0>, &mPhi, &mOmega, &mSigma);
    // prediction or smoothing
    decl mp, mest, isel = ST_PRED; // or ST_SMO, DS_SMO
    mp=SsfMomentEst(isel, &mest, mYt, mPhi, mOmega, mSigma);
    println("mp", mp); println("mest", mest');
}
	
