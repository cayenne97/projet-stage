#include <oxstd.h>
#include <oxdraw.h>
#include <packages/ssfpack/ssfpack.h>

main()
{
	SsfAbout();
	decl iVersion = SsfVersion();
	println("iVersion = ", iVersion);

	decl mvareps = <1,0.8;0.8,1>, mvareta = 0.1 * ones(2,2);
	decl mphi   = unit(2) | unit(2);
	decl momega = diagcat(mvareta , mvareps);

	decl dlik, dvar;
	print("first likelihood call"); SsfWarning(TRUE);
	SsfLikEx(&dlik, &dvar, rann(2,10), mphi, momega);
	println("second likelihood call"); SsfWarning(FALSE);
	SsfLikEx(&dlik, &dvar, rann(2,10), mphi, momega);
}
