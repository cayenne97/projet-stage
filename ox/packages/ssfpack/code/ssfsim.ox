#include <oxstd.h>
#include <oxdraw.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl mPhi = <1,1;0,1;1,0>;
    decl mOmega = diag(<0,0.1,5>);
    decl mSigma = diag(<-1,-1>) | 0;

    decl mu = sqrt(mOmega) * rann(3, 21);
    decl md = SsfRecursion(mu, mPhi, mOmega, <0,0;0,0;1,.5>);
    decl mYt = md[2][1:];
    decl mKF = KalmanFil(mYt, mPhi, mOmega, mSigma);

    decl ct = columns(mYt); // 20 observations
    decl mGamma = diag(<0,1,0>);
    decl mWgt = SimSmoWgt(mGamma, mKF, mPhi, mOmega, mSigma);
    print("Simulation smoother weights (t=10)", mWgt[][9]');

    // draw 1
    md = SimSmoDraw(mGamma, rann(1, ct), mWgt, mKF, mPhi,
        mOmega, mSigma);
    print("Draw 1 for slope disturbances (t=10)", md[][10]');
    md = SsfRecursion(md, mPhi, mOmega);
    print("Draw 1 for state and signal (t=10)", md[][10]');
    // draw 2
    decl md2 = SimSmoDraw(mGamma, rann(1, ct), mWgt, mKF, mPhi,
        mOmega, mSigma); md2 = SsfRecursion(md2, mPhi, mOmega);
    // draw 3
    decl md3 = SimSmoDraw(mGamma, rann(1, ct), mWgt, mKF, mPhi,
        mOmega, mSigma); md3 = SsfRecursion(md3, mPhi, mOmega);
    DrawTMatrix(0, md[2][1:] | md2[2][1:] | md3[2][1:] | mYt,
        {"y1[t]","y2[t]","y3[t]", "y"}, 1, 1, 1);
    ShowDrawWindow();
}
