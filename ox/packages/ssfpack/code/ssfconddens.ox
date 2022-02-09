#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mYt = rann(1,9); // data
    decl mPhi, mOmega, mSigma; // ssf
    GetSsfStsm(
        <CMP_IRREG, 1.0, 0; CMP_LEVEL, 0.0, 0;
         CMP_SLOPE, 0.1, 0>, &mPhi, &mOmega, &mSigma);
    // smoothing
    decl mp, mest, mcond;
    mp=SsfMomentEst(ST_SMO, &mest, mYt, mPhi, mOmega, mSigma);
    println("mest", mest');
    mcond=SsfCondDens(ST_SMO, mYt, mPhi, mOmega, mSigma);
    println("mcond", mcond');   
}
	
