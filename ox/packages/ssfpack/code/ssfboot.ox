#include <oxstd.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
	decl i, my, ct, mphi, momega, msigma, vquant;
    decl y_i, mn_y, sd_y, dlik, dvar, msco, cboot, vboot;

    my = loadmat("Nile.mat")';		// load data, transpose
    GetSsfStsm(<CMP_LEVEL, 0.0, 0, 0;
                CMP_IRREG, 0.0, 0, 0>, &mphi, &momega, &msigma);
	ct = columns(my);
	momega[1][1] = varr(my);
	mn_y = double(meanr(my));  sd_y = sqrt(momega[1][1]);

	cboot = 1000;					// no of bootstraps
	vboot = zeros(1, cboot);		// for storing bootstrap output

	SsfLikSco(&dlik, &msco, my, mphi, momega, msigma);
	vboot[0][0] = msco[0][0];		// first is actual test value

	for (i = 1; i < cboot; i++)		// bootstrap loop
	{
		y_i = mn_y + (sd_y * standardize(rann(ct, 1))');
        SsfLikSco(&dlik, &msco, y_i, mphi, momega, msigma);
		vboot[0][i] = msco[0][0];
	}
	vquant = quantiler(vboot, <0.9, 0.95, 0.99>);
	
	print("Test for fixed level (Nile data) = ", vboot[0][0]);
	print("%r", {"Bootstrap critical values:"}, "%c", {"90%", "95%", "99%"}, vquant);
}

