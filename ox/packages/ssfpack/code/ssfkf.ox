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
    print("mKF\' (t=10)","%c",{"v","K(1,1)","K(2,1)","F^-1"},
           mKF[][9]');

    DrawTMatrix(0, mKF[0][], {"v"},1,1,1);
    DrawTMatrix(1, mKF[1:][], {"K(1,1)","K(2,1)","F^-1"},1,1,1);
    ShowDrawWindow();
}