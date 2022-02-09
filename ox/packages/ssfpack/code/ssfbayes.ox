#include <oxstd.h>
#include <oxdraw.h>
#include <oxprob.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
	decl k, i, j, crep = 2000, cinit = 200, myt, mphi, momega, msigma;
	decl s_eta, s_xi, c_eta, c_xi, md, mpsi;

    myt = loadmat("Nile.mat")';
    GetSsfStsm(<CMP_LEVEL, 1.0;
                CMP_IRREG, 1.0>, &mphi, &momega, &msigma);

	s_eta = 5000; s_xi = 50000;
	c_eta = c_xi = 2.5 + (0.5 * columns(myt));

	for (i = 0, mpsi = zeros(2, crep); i < crep; ++i)
	{
		md = SsfCondDens(DS_SIM, myt, mphi, momega, msigma);
		md = md * md';
		mpsi[0][i] = 1.0 / rangamma(1,1, c_eta, (s_eta + md[0][0])/2);
		mpsi[1][i] = 1.0 / rangamma(1,1, c_xi, (s_xi + md[1][1])/2);
		momega = diag(mpsi[][i]);
	}
	mpsi = mpsi[][cinit:];				// drop first cinit draws
	print("%r", {"var_eta", "var_xi"}, "%c", {"mean", "st.dev."}, "%15.3f",
		meanr(mpsi)~sqrt(varr(mpsi)));
		
	DrawTMatrix(0, mpsi[0][], "drawn var_eta",1, 1, 1);
	DrawTMatrix(1, mpsi[1][], "drawn var_xi", 1, 1, 1);
	DrawCorrelogram(2, mpsi[0][], "ACF var_eta", 100);
	DrawCorrelogram(3, mpsi[1][], "ACF var_xi", 100);
	DrawDensity(4, mpsi[0][], "Density var_eta", TRUE, TRUE, FALSE);
	DrawDensity(5, mpsi[1][], "Density var_xi", TRUE, TRUE, FALSE);
	ShowDrawWindow();
}
