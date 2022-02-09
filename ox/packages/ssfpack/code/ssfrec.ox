#include <oxstd.h>
#include <oxdraw.h>
#include <oxfloat.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mPhi = <1,1;0,1;1,0>;
    decl mOmega = diag(<0,0.1,1>);
    decl mSigma = <0,0;0,0;1,.5>;       // Note that Q is zero

    decl mr = sqrt(mOmega) * rann(3, 21);
    decl md = SsfRecursion(mr, mPhi, mOmega, mSigma);
    decl mYt = md[2][1:] ~ M_NAN;       // 20 observations

    print("Generated data (t=10)",
        "%c", {"mu[t+1]","beta[t+1]","y[t]"}, md[][10]');
    DrawTMatrix(0, mYt | md[:1][],
        {"y[t]", "mu[t]","beta[t]"}, 1, 1, 1);
    ShowDrawWindow();
}