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

    decl mYt = md[2][1:];       // 20 observations
    decl mKF = KalmanFil(mYt, mPhi, mOmega);
    decl mKS = KalmanSmo(mKF, mPhi, mOmega);
    print("Basic smoother output: mKS\' (t=10)",
        "%c", {"r(1,1)","r(2,1)","e","N(1,1)","N(2,2)","D"},
        mKS[][10]');
    decl msmodist = mKS[0:2][0] ~ mOmega * mKS[0:2][1:];
    print("Smoothed disturbances (t=10)",
        "%c", {"E[H.eta](1,1)","E[H.eta](2,1)","E[G.eps]"},
        msmodist[][10]');
    decl msmostat = SsfRecursion(msmodist, mPhi, mOmega);
    print("Smoothed states (t=10)", "%c",
        {"muhat[t+1]","betahat[t+1]","y[t]"}, msmostat[][10]');

    DrawTMatrix(0, msmodist[1:2][],
        {"E[H.eta](2,1)[t]","E[G.eps][t]"}, 0, 1, 1);
    DrawTMatrix(1, msmostat[0:1][:columns(mYt)-1] | mYt ,
        {"muhat[t]","betahat[t]","y[t]"}, 0, 1, 1);
    ShowDrawWindow();
}