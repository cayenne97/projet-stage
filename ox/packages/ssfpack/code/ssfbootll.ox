#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
    decl i, mYt, ct, mPhi, mOmega, mSigma, vquant;
    decl y_i, mn_y, sd_y, dlik, dvar, msco, cboot, vboot;

    mYt = loadmat("Nile.mat")';         // load data
    GetSsfStsm(<CMP_LEVEL, 0, 0, 0;     // local level model
                CMP_IRREG, 0, 0, 0>, &mPhi, &mOmega, &mSigma);
    ct = columns(mYt);
    mOmega[1][1] = varr(mYt);
    mn_y = double(meanr(mYt));  sd_y = sqrt(mOmega[1][1]);

    cboot = 10000;              // nr bootstraps
    vboot = zeros(1, cboot);    // storage bootstrap output

    SsfLikSco(&dlik,&dvar,&msco,mYt,mPhi,mOmega,mSigma);
    vboot[0][0] = msco[0][0];   // first is actual test value

    for (i = 1; i < cboot; i++) // bootstrap loop
    {
        y_i = mn_y + (sd_y * standardize(rann(ct, 1))');
        SsfLikSco(&dlik,&dvar,&msco,y_i,mPhi,mOmega,mSigma);
        vboot[0][i] = msco[0][0];
    }
    vquant = quantiler(vboot, <0.9, 0.95, 0.99>);
    print("Test for fixed level (Nile data) = ", vboot[0][0]);
    print("%r", {"Bootstrap critical values:"},
          "%c", {"90%", "95%", "99%"}, vquant);
}

